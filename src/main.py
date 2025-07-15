"""
Main CLI entry point for Englishy.
"""

import typer
from pathlib import Path
from typing import Optional

from parser.parser import EnglishLearningParser
from chunker.chunker import EnglishLearningChunker
from encoder.openai import OpenAIEncoder
from retriever.article_search.faiss import FAISSSearch
from utils.logging import logger

app = typer.Typer()


@app.command()
def parse_data(
    input_file: str = typer.Argument(..., help="Input file to parse"),
    output_file: Optional[str] = typer.Option(None, help="Output file for parsed data")
):
    """Parse English learning data from file."""
    try:
        parser = EnglishLearningParser()
        parsed_data = parser.parse_file(input_file)
        
        logger.info(f"Parsed {len(parsed_data)} items from {input_file}")
        
        if output_file:
            import json
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(parsed_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved parsed data to {output_file}")
        else:
            # Print first few items
            for i, item in enumerate(parsed_data[:3]):
                print(f"\nItem {i+1}:")
                print(f"  ID: {item.get('id')}")
                print(f"  Type: {item.get('type')}")
                print(f"  Text: {item.get('text_for_search', '')[:100]}...")
    
    except Exception as e:
        logger.error(f"Error parsing data: {e}")
        raise typer.Exit(1)


@app.command()
def chunk_data(
    input_file: str = typer.Argument(..., help="Input file with parsed data"),
    output_file: Optional[str] = typer.Option(None, help="Output file for chunked data"),
    chunk_size: int = typer.Option(512, help="Maximum chunk size"),
    overlap: int = typer.Option(50, help="Overlap between chunks")
):
    """Chunk parsed English learning data."""
    try:
        import json
        
        # Load parsed data
        with open(input_file, 'r', encoding='utf-8') as f:
            parsed_data = json.load(f)
        
        # Chunk data
        chunker = EnglishLearningChunker(chunk_size=chunk_size, overlap=overlap)
        chunks = chunker.chunk_parsed_data(parsed_data)
        
        logger.info(f"Created {len(chunks)} chunks from {len(parsed_data)} items")
        
        if output_file:
            # Convert chunks to dict format for JSON serialization
            chunk_dicts = []
            for chunk in chunks:
                chunk_dict = {
                    'id': chunk.id,
                    'type': chunk.type,
                    'content': chunk.content,
                    'text': chunk.text,
                    'metadata': chunk.metadata
                }
                chunk_dicts.append(chunk_dict)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(chunk_dicts, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved chunked data to {output_file}")
        else:
            # Print first few chunks
            for i, chunk in enumerate(chunks[:3]):
                print(f"\nChunk {i+1}:")
                print(f"  ID: {chunk.id}")
                print(f"  Type: {chunk.type}")
                print(f"  Text: {chunk.text[:100]}...")
    
    except Exception as e:
        logger.error(f"Error chunking data: {e}")
        raise typer.Exit(1)


@app.command()
def build_index(
    chunks_file: str = typer.Argument(..., help="File with chunked data"),
    index_path: str = typer.Option("cache/englishy_index", help="Path to save index"),
    encoder_model: str = typer.Option("text-embedding-3-small", help="OpenAI embedding model")
):
    """Build search index from chunked data."""
    try:
        import json
        
        # Load chunked data
        with open(chunks_file, 'r', encoding='utf-8') as f:
            chunk_dicts = json.load(f)
        
        # Initialize encoder
        encoder = OpenAIEncoder(model=encoder_model)
        
        # Encode chunks
        texts = [chunk['text'] for chunk in chunk_dicts]
        embeddings = encoder.encode_texts(texts)
        
        # Build index
        faiss_search = FAISSSearch(index_path=index_path, dimension=len(embeddings[0]))
        faiss_search.build_index(chunk_dicts, embeddings)
        
        logger.info(f"Built index with {len(chunk_dicts)} chunks")
        logger.info(f"Index saved to {index_path}")
    
    except Exception as e:
        logger.error(f"Error building index: {e}")
        raise typer.Exit(1)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    index_path: str = typer.Option("cache/englishy_index", help="Path to index"),
    encoder_model: str = typer.Option("text-embedding-3-small", help="OpenAI embedding model"),
    limit: int = typer.Option(5, help="Number of results to return")
):
    """Search English learning content."""
    try:
        # Load index
        faiss_search = FAISSSearch(index_path=index_path)
        faiss_search.load_index()
        
        # Initialize encoder
        encoder = OpenAIEncoder(model=encoder_model)
        
        # Search
        results = faiss_search.search_by_text(query, encoder, k=limit)
        
        print(f"\nSearch results for: '{query}'")
        print(f"Found {len(results.results)} results\n")
        
        for i, result in enumerate(results.get_top_results(limit), 1):
            print(f"{i}. {result.text[:100]}...")
            print(f"   Score: {result.score:.3f}")
            print(f"   Type: {result.type}")
            print()
    
    except Exception as e:
        logger.error(f"Error searching: {e}")
        raise typer.Exit(1)


@app.command()
def process_pipeline(
    input_file: str = typer.Argument(..., help="Input file to process"),
    output_dir: str = typer.Option("cache", help="Output directory"),
    chunk_size: int = typer.Option(512, help="Maximum chunk size"),
    encoder_model: str = typer.Option("text-embedding-3-small", help="OpenAI embedding model")
):
    """Run the complete processing pipeline."""
    try:
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Step 1: Parse data
        logger.info("Step 1: Parsing data...")
        parser = EnglishLearningParser()
        parsed_data = parser.parse_file(input_file)
        
        parsed_file = output_path / "parsed_data.json"
        import json
        with open(parsed_file, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)
        
        # Step 2: Chunk data
        logger.info("Step 2: Chunking data...")
        chunker = EnglishLearningChunker(chunk_size=chunk_size)
        chunks = chunker.chunk_parsed_data(parsed_data)
        
        chunked_file = output_path / "chunked_data.json"
        chunk_dicts = []
        for chunk in chunks:
            chunk_dict = {
                'id': chunk.id,
                'type': chunk.type,
                'content': chunk.content,
                'text': chunk.text,
                'metadata': chunk.metadata
            }
            chunk_dicts.append(chunk_dict)
        
        with open(chunked_file, 'w', encoding='utf-8') as f:
            json.dump(chunk_dicts, f, ensure_ascii=False, indent=2)
        
        # Step 3: Build index
        logger.info("Step 3: Building index...")
        encoder = OpenAIEncoder(model=encoder_model)
        texts = [chunk['text'] for chunk in chunk_dicts]
        embeddings = encoder.encode_texts(texts)
        
        index_path = str(output_path / "englishy_index")
        faiss_search = FAISSSearch(index_path=index_path, dimension=len(embeddings[0]))
        faiss_search.build_index(chunk_dicts, embeddings)
        
        logger.info(f"Pipeline completed successfully!")
        logger.info(f"Parsed: {len(parsed_data)} items")
        logger.info(f"Chunks: {len(chunks)} chunks")
        logger.info(f"Index: {index_path}")
    
    except Exception as e:
        logger.error(f"Error in pipeline: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app() 