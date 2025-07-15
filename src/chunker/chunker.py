"""
Chunker for English learning content.
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from utils.logging import logger


@dataclass
class Chunk:
    """Represents a chunk of English learning content."""
    id: str
    type: str
    content: Dict[str, Any]
    text: str
    metadata: Dict[str, Any]


class EnglishLearningChunker:
    """Chunker for English learning materials."""
    
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
        
        # Sentence splitting patterns
        self.sentence_patterns = [
            r'[.!?]+',  # English sentence endings
            r'[。！？]+',  # Japanese sentence endings
            r'\n+',  # Line breaks
        ]
    
    def chunk_parsed_data(self, parsed_data: List[Dict[str, Any]]) -> List[Chunk]:
        """Chunk parsed English learning data."""
        chunks = []
        
        for item in parsed_data:
            item_chunks = self._chunk_item(item)
            chunks.extend(item_chunks)
        
        logger.info(f"Created {len(chunks)} chunks from {len(parsed_data)} items")
        return chunks
    
    def _chunk_item(self, item: Dict[str, Any]) -> List[Chunk]:
        """Chunk a single parsed item."""
        item_type = item.get('type', 'unknown')
        
        if item_type == 'english_question':
            return self._chunk_question(item)
        elif item_type == 'english_material':
            return self._chunk_material(item)
        elif item_type == 'english_text':
            return self._chunk_text(item)
        else:
            return self._chunk_generic(item)
    
    def _chunk_question(self, item: Dict[str, Any]) -> List[Chunk]:
        """Chunk an English question item."""
        content = item.get('content', {})
        question = content.get('question', '')
        answer = content.get('answer', '')
        grammar = content.get('grammar', '')
        note = content.get('note', '')
        
        chunks = []
        
        # Create separate chunks for different parts
        if question:
            chunks.append(Chunk(
                id=f"{item['id']}_question",
                type="question_text",
                content={"text": question, "part": "question"},
                text=question,
                metadata=item.get('content', {}).get('metadata', {})
            ))
        
        if answer:
            chunks.append(Chunk(
                id=f"{item['id']}_answer",
                type="answer_text",
                content={"text": answer, "part": "answer"},
                text=answer,
                metadata=item.get('content', {}).get('metadata', {})
            ))
        
        if grammar:
            chunks.append(Chunk(
                id=f"{item['id']}_grammar",
                type="grammar_explanation",
                content={"text": grammar, "part": "grammar"},
                text=grammar,
                metadata=item.get('content', {}).get('metadata', {})
            ))
        
        if note:
            chunks.append(Chunk(
                id=f"{item['id']}_note",
                type="learning_note",
                content={"text": note, "part": "note"},
                text=note,
                metadata=item.get('content', {}).get('metadata', {})
            ))
        
        # If no specific parts, create a combined chunk
        if not chunks:
            combined_text = f"{question} {answer} {grammar} {note}".strip()
            if combined_text:
                chunks.append(Chunk(
                    id=f"{item['id']}_combined",
                    type="combined_content",
                    content={"text": combined_text, "parts": ["question", "answer", "grammar", "note"]},
                    text=combined_text,
                    metadata=item.get('content', {}).get('metadata', {})
                ))
        
        return chunks
    
    def _chunk_material(self, item: Dict[str, Any]) -> List[Chunk]:
        """Chunk a generic English learning material item."""
        content = item.get('content', {})
        text = item.get('text_for_search', '')
        
        if not text:
            return []
        
        # Split by sentences first
        sentences = self._split_sentences(text)
        
        chunks = []
        for i, sentence in enumerate(sentences):
            if sentence.strip():
                chunks.append(Chunk(
                    id=f"{item['id']}_sentence_{i+1}",
                    type="sentence",
                    content={"text": sentence, "sentence_index": i+1},
                    text=sentence,
                    metadata=content
                ))
        
        return chunks
    
    def _chunk_text(self, item: Dict[str, Any]) -> List[Chunk]:
        """Chunk a text item."""
        content = item.get('content', {})
        text = content.get('text', '')
        lines = content.get('lines', [])
        
        if not text:
            return []
        
        # If text is short enough, keep as one chunk
        if len(text) <= self.chunk_size:
            return [Chunk(
                id=f"{item['id']}_full",
                type="text_chunk",
                content={"text": text, "lines": lines},
                text=text,
                metadata={}
            )]
        
        # Split into overlapping chunks
        return self._split_text_with_overlap(text, item['id'])
    
    def _chunk_generic(self, item: Dict[str, Any]) -> List[Chunk]:
        """Chunk a generic item."""
        text = item.get('text_for_search', '')
        
        if not text:
            return []
        
        return [Chunk(
            id=f"{item['id']}_generic",
            type="generic_content",
            content={"text": text},
            text=text,
            metadata=item.get('content', {})
        )]
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Combine all sentence patterns
        pattern = '|'.join(self.sentence_patterns)
        
        # Split text
        sentences = re.split(pattern, text)
        
        # Clean up sentences
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def _split_text_with_overlap(self, text: str, base_id: str) -> List[Chunk]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence ending near the end
                for i in range(end, max(start, end - 100), -1):
                    if text[i] in '.!?。！？':
                        end = i + 1
                        break
            
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunks.append(Chunk(
                    id=f"{base_id}_chunk_{len(chunks)+1}",
                    type="text_chunk",
                    content={"text": chunk_text, "start": start, "end": end},
                    text=chunk_text,
                    metadata={"chunk_index": len(chunks) + 1}
                ))
            
            # Move start position with overlap
            start = end - self.overlap
            if start >= len(text):
                break
        
        return chunks
    
    def merge_small_chunks(self, chunks: List[Chunk], min_size: int = 50) -> List[Chunk]:
        """Merge small chunks with adjacent ones."""
        if not chunks:
            return chunks
        
        merged = []
        current_chunk = chunks[0]
        
        for next_chunk in chunks[1:]:
            # If current chunk is small and same type, merge
            if (len(current_chunk.text) < min_size and 
                current_chunk.type == next_chunk.type):
                
                # Merge chunks
                merged_text = f"{current_chunk.text} {next_chunk.text}"
                merged_id = f"{current_chunk.id}_merged"
                
                current_chunk = Chunk(
                    id=merged_id,
                    type=current_chunk.type,
                    content={"text": merged_text, "merged": True},
                    text=merged_text,
                    metadata=current_chunk.metadata
                )
            else:
                merged.append(current_chunk)
                current_chunk = next_chunk
        
        merged.append(current_chunk)
        return merged 