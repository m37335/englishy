"""
Parser for English learning materials.
"""

import csv
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any

from utils.logging import logger


class EnglishLearningParser:
    """Parser for English learning materials."""
    
    def __init__(self):
        self.supported_formats = ['.csv', '.json', '.txt']
    
    def parse_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse a file and return structured data."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if file_path.suffix.lower() == '.csv':
            return self._parse_csv(file_path)
        elif file_path.suffix.lower() == '.json':
            return self._parse_json(file_path)
        elif file_path.suffix.lower() == '.txt':
            return self._parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    def _parse_csv(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse CSV file containing English learning materials."""
        chunks = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row_num, row in enumerate(reader, 1):
                    # Skip empty rows
                    if not any(row.values()):
                        continue
                    
                    chunk = self._process_csv_row(row, row_num)
                    if chunk:
                        chunks.append(chunk)
                        
        except Exception as e:
            logger.error(f"Error parsing CSV file {file_path}: {e}")
            raise
        
        logger.info(f"Parsed {len(chunks)} chunks from {file_path}")
        return chunks
    
    def _process_csv_row(self, row: Dict[str, str], row_num: int) -> Optional[Dict[str, Any]]:
        """Process a single CSV row and create a chunk."""
        # Extract key fields
        question_text = self._build_question_text(row)
        answer = row.get('Answer', '').strip()
        grammar = row.get('GRAMMER', '').strip()
        note = row.get('NOTE', '').strip()
        
        # Skip if no meaningful content
        if not question_text and not answer:
            return None
        
        chunk = {
            'id': f"q_{row_num}",
            'type': 'english_question',
            'content': {
                'question': question_text,
                'answer': answer,
                'grammar': grammar,
                'note': note,
                'metadata': {
                    'prefecture': row.get('prefecture', ''),
                    'year': row.get('year', ''),
                    'question_no': row.get('questionNo', ''),
                    'condition': row.get('condition', ''),
                    'subject': row.get('SUBJECT', ''),
                    'verb': row.get('VERB', ''),
                    'not_using': row.get('NOT USING', '')
                }
            },
            'text_for_search': f"{question_text} {answer} {grammar} {note}".strip()
        }
        
        return chunk
    
    def _build_question_text(self, row: Dict[str, str]) -> str:
        """Build question text from conversation parts."""
        talk_a = row.get('TALK:A', '').strip()
        talk_b = row.get('TALK:B', '').strip()
        talk_c = row.get('TALK:C', '').strip()
        
        parts = []
        if talk_a:
            parts.append(talk_a)
        if talk_b:
            parts.append(talk_b)
        if talk_c:
            parts.append(talk_c)
        
        return ' '.join(parts)
    
    def _parse_json(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse JSON file containing English learning materials."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                return self._process_json_list(data)
            elif isinstance(data, dict):
                return self._process_json_dict(data)
            else:
                raise ValueError(f"Unexpected JSON structure in {file_path}")
                
        except Exception as e:
            logger.error(f"Error parsing JSON file {file_path}: {e}")
            raise
    
    def _process_json_list(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process JSON list data."""
        chunks = []
        
        for i, item in enumerate(data):
            chunk = {
                'id': f"item_{i+1}",
                'type': 'english_material',
                'content': item,
                'text_for_search': self._extract_text_from_json(item)
            }
            chunks.append(chunk)
        
        return chunks
    
    def _process_json_dict(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process JSON dict data."""
        # Convert dict to list format
        return self._process_json_list([data])
    
    def _extract_text_from_json(self, item: Dict[str, Any]) -> str:
        """Extract searchable text from JSON item."""
        if isinstance(item, dict):
            return ' '.join(str(v) for v in item.values() if v)
        elif isinstance(item, str):
            return item
        else:
            return str(item)
    
    def _parse_txt(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse text file containing English learning materials."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            chunks = []
            current_chunk = []
            
            for i, line in enumerate(lines):
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    if current_chunk:
                        chunk = self._create_text_chunk(current_chunk, i)
                        chunks.append(chunk)
                        current_chunk = []
                    continue
                
                current_chunk.append(line)
            
            # Add final chunk
            if current_chunk:
                chunk = self._create_text_chunk(current_chunk, len(lines))
                chunks.append(chunk)
            
            return chunks
            
        except Exception as e:
            logger.error(f"Error parsing text file {file_path}: {e}")
            raise
    
    def _create_text_chunk(self, lines: List[str], chunk_id: int) -> Dict[str, Any]:
        """Create a chunk from text lines."""
        text = ' '.join(lines)
        
        return {
            'id': f"text_{chunk_id}",
            'type': 'english_text',
            'content': {
                'text': text,
                'lines': lines
            },
            'text_for_search': text
        } 