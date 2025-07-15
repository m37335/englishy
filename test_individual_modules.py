#!/usr/bin/env python3
"""
Individual module testing script for Englishy.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.lm import load_lm
from src.ai.openai_client import OpenAIClient
from src.ai.query_refiner import QueryRefiner
from src.ai.query_expander import QueryExpander
from src.ai.outline_creater import OutlineCreater
from src.ai.report_writer import (
    StreamLeadWriter, StreamSectionWriter, StreamConclusionWriter,
    WriteLeadJapanese, WriteSectionJapanese, WriteConclusionJapanese,
    StreamRelatedTopicsWriter, StreamReferencesWriter, StreamIntegratedSectionWriter
)
from src.ai.mindmap_maker import MindMapMaker
from src.ai.grammar_analyzer import get_grammar_analyzer
from src.ai.english_extractor import get_english_extractor
from src.retriever.web_search.duckduckgo_search import DuckDuckGoSearch
from src.utils.logging import logger


def test_query_refiner():
    """Test the query refiner module"""
    print("\n=== Testing Query Refiner ===")
    
    try:
        from src.ai.query_refiner import QueryRefiner
        
        refiner = QueryRefiner()
        query = "英語の文法について教えて"
        refined = refiner.refine(query)
        print(f"Original query: {query}")
        print(f"Refined query: {refined}")
        
        print("✅ Query refiner test completed")
        
    except Exception as e:
        print(f"❌ Query refiner test failed: {e}")
        import traceback
        traceback.print_exc()


def test_english_extractor():
    """Test English extraction module."""
    print("🔤 Testing English Extractor...")
    
    extractor = get_english_extractor()
    
    test_queries = [
        "動名詞の使い方を教えて",
        "I want to learn about gerunds and infinitives",
        "不定詞と動名詞の違いについて",
        "How to use 'I wish I were better at' in English"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = extractor.process_query(query)
        print(f"Has English: {result['has_english']}")
        if result['has_english']:
            print(f"English texts: {result['english_texts']}")
            print(f"Grammar structures: {result['grammar_structures']}")
        print(f"Search query: {result['search_query']}")


def test_grammar_analyzer():
    """Test grammar analysis module."""
    print("\n🔍 Testing Grammar Analyzer...")
    
    analyzer = get_grammar_analyzer()
    
    test_texts = [
        "I want to learn about gerunds",
        "How to use infinitives in English",
        "The difference between gerunds and infinitives"
    ]
    
    for text in test_texts:
        print(f"\nText: {text}")
        result = analyzer.analyze_text(text)
        print(f"Grammar structures: {result['grammar_structures']}")
        if result.get('key_points'):
            print(f"Key points: {result['key_points']}")
        if result.get('related_topics'):
            print(f"Related topics: {result['related_topics']}")


async def test_ai_modules():
    """Test AI modules with LM."""
    print("\n🤖 Testing AI Modules...")
    
    # Initialize LM
    lm = load_lm()
    
    # Test QueryRefiner
    print("\n--- Testing QueryRefiner ---")
    refiner = QueryRefiner(lm=lm)
    refined = refiner(query="動名詞の使い方")
    print(f"Original: 動名詞の使い方")
    print(f"Refined: {refined.refined_query}")
    
    # Test QueryExpander
    print("\n--- Testing QueryExpander ---")
    expander = QueryExpander(lm=lm)
    expanded = expander(query="動名詞の使い方", web_search_results="")
    print(f"Expanded topics: {expanded.topics}")
    
    # Test OutlineCreater
    print("\n--- Testing OutlineCreater ---")
    outline_creater = OutlineCreater(lm=lm)
    outline_result = outline_creater(
        query="動名詞の使い方",
        topics=["gerunds", "grammar", "teaching"],
        references=[]
    )
    print(f"Outline title: {outline_result.outline.title}")
    print(f"Number of sections: {len(outline_result.outline.section_outlines)}")


async def test_report_writers():
    """Test report writing modules."""
    print("\n📝 Testing Report Writers...")
    
    lm = load_lm()
    
    # Test Japanese Lead Writer
    print("\n--- Testing Japanese Lead Writer ---")
    lead_writer = StreamLeadWriter(lm=lm)
    lead_content = ""
    async for chunk in lead_writer(
        query="動名詞の使い方",
        title="動名詞の活用と英語スキル向上",
        draft="# 動名詞の活用と英語スキル向上\n## 動名詞とは\n### 動名詞の定義と使用法"
    ):
        lead_content += chunk
    print(f"Lead content (first 100 chars): {lead_content[:100]}...")
    
    # Test Japanese Section Writer
    print("\n--- Testing Japanese Section Writer ---")
    section_writer = StreamSectionWriter(lm=lm)
    section_content = ""
    async for chunk in section_writer(
        query="動名詞の使い方",
        references="Title: Gerunds in English\nURL: example.com\nContent: Gerunds are verb forms ending in -ing...",
        section_outline="### 動名詞の定義と使用法"
    ):
        section_content += chunk
    print(f"Section content (first 100 chars): {section_content[:100]}...")
    
    # Test Related Topics Writer
    print("\n--- Testing Related Topics Writer ---")
    related_writer = StreamRelatedTopicsWriter(lm=lm)
    related_content = ""
    async for chunk in related_writer(query="動名詞"):
        related_content += chunk
    print(f"Related topics (first 100 chars): {related_content[:100]}...")


async def test_web_search():
    """Test web search functionality."""
    print("\n🌐 Testing Web Search...")
    
    search = DuckDuckGoSearch()
    
    test_queries = [
        "gerunds in English grammar",
        "teaching infinitives ESL"
    ]
    
    for query in test_queries:
        print(f"\nSearching for: {query}")
        results = search.search(query, k=3)
        print(f"Found {len(results)} results")
        for i, result in enumerate(results[:2], 1):
            print(f"{i}. {result.get('title', 'No title')}")
            print(f"   URL: {result.get('url', 'No URL')}")
            print(f"   Content: {result.get('snippet', 'No content')[:100]}...")


def test_mindmap_maker():
    """Test mind map generation."""
    print("\n🗺️ Testing Mind Map Maker...")
    
    lm = load_lm()
    mindmap_maker = MindMapMaker(lm=lm)
    
    test_report = """
    # 動名詞の活用と英語スキル向上
    
    ## 動名詞とは
    動名詞は動詞の-ing形で、名詞として機能する文法要素です。
    
    ## 動名詞の使い方
    動名詞は主語、目的語、前置詞の目的語として使用できます。
    
    ## 動名詞と不定詞の違い
    動名詞と不定詞は異なる用法と意味を持ちます。
    """
    
    result = mindmap_maker(report=test_report, related_topics="不定詞、分詞、動詞の活用")
    print(f"Mind map content (first 200 chars): {result.mindmap[:200]}...")


async def main():
    """Run all tests."""
    print("🧪 Starting Individual Module Tests for Englishy")
    print("=" * 50)
    
    try:
        # Test basic modules
        test_query_refiner()
        test_english_extractor()
        test_grammar_analyzer()
        
        # Test AI modules
        await test_ai_modules()
        
        # Test report writers
        await test_report_writers()
        
        # Test web search
        await test_web_search()
        
        # Test mind map maker
        test_mindmap_maker()
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main()) 