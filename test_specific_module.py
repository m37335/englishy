#!/usr/bin/env python3
"""
Test specific modules individually.
Usage: python test_specific_module.py [module_name]
"""

import asyncio
import sys
import os
import argparse
import dspy

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.lm import load_lm
from src.ai.english_extractor import get_english_extractor
from src.ai.grammar_analyzer import get_grammar_analyzer
from src.ai.query_refiner import QueryRefiner, GrammarAwareQueryRefiner
from src.ai.query_expander import QueryExpander
from src.ai.outline_creater import OutlineCreater
from src.ai.report_writer import StreamLeadWriter, StreamSectionWriter
from src.ai.mindmap_maker import MindMapMaker
from src.retriever.web_search.duckduckgo_search import DuckDuckGoSearch


async def test_english_extractor():
    """Test English extraction module."""
    print("🔤 Testing English Extractor...")
    
    extractor = get_english_extractor()
    
    test_query = "動名詞の使い方を教えてください。I want to learn about gerunds."
    print(f"Test query: {test_query}")
    
    result = extractor.process_query(test_query)
    print(f"Has English: {result['has_english']}")
    if result['has_english']:
        print(f"English texts: {result['english_texts']}")
        print(f"Grammar structures: {result['grammar_structures']}")
    print(f"Search query: {result['search_query']}")


async def test_grammar_analyzer():
    """Test grammar analysis module."""
    print("🔍 Testing Grammar Analyzer...")
    
    analyzer = get_grammar_analyzer()
    
    test_text = "I want to learn about gerunds and infinitives in English grammar."
    print(f"Test text: {test_text}")
    
    result = analyzer.analyze_text(test_text)
    print(f"Grammar structures: {result['grammar_structures']}")
    if result.get('key_points'):
        print(f"Key points: {result['key_points']}")
    if result.get('related_topics'):
        print(f"Related topics: {result['related_topics']}")


async def test_query_refiner():
    """Test query refinement module."""
    print("🔧 Testing Query Refiner...")
    
    lm = load_lm()
    
    # dspyのグローバル設定
    dspy.settings.configure(lm=lm)
    
    # 従来のQueryRefiner
    print("--- 従来のQueryRefiner ---")
    refiner = QueryRefiner(lm=None)
    test_query = "動名詞の使い方"
    print(f"Original query: {test_query}")
    with dspy.settings.context(lm=lm):
        result = refiner(query=test_query)
    print(f"Refined query: {result}")
    
    # 新しいGrammarAwareQueryRefiner
    print("\n--- 新しいGrammarAwareQueryRefiner ---")
    grammar_aware_refiner = GrammarAwareQueryRefiner(lm=None)
    with dspy.settings.context(lm=lm):
        refinement_result = grammar_aware_refiner(query=test_query)
    print(f"Original query: {test_query}")
    print(f"Refined query: {refinement_result['refined_query']}")
    print(f"Detected grammar: {refinement_result['detected_grammar']}")
    print(f"Related items: {refinement_result['related_items']}")
    print("✅ Query Refiner test completed\n")


async def test_query_expander():
    """Test query expansion module."""
    print("📈 Testing Query Expander...")
    
    lm = load_lm()
    expander = QueryExpander(lm=lm)
    
    test_query = "動名詞の使い方"
    test_results = "Title: Gerunds in English\nContent: Gerunds are verb forms ending in -ing..."
    print(f"Original query: {test_query}")
    
    result = expander(query=test_query, web_search_results=test_results)
    print(f"Expanded topics: {result.topics}")


async def test_outline_creater():
    """Test outline creation module."""
    print("📋 Testing Outline Creater...")
    
    lm = load_lm()
    outline_creater = OutlineCreater(lm=lm)
    
    test_query = "動名詞の使い方"
    test_topics = ["gerunds", "grammar", "teaching"]
    test_references = []
    
    result = outline_creater(
        query=test_query,
        topics=test_topics,
        references=test_references
    )
    
    print(f"Outline title: {result.outline.title}")
    print(f"Number of sections: {len(result.outline.section_outlines)}")
    for i, section in enumerate(result.outline.section_outlines[:3], 1):
        print(f"Section {i}: {section.title}")


async def test_report_writer():
    """Test report writing module."""
    print("📝 Testing Report Writer...")
    
    lm = load_lm()
    lead_writer = StreamLeadWriter(lm=lm)
    
    test_query = "動名詞の使い方"
    test_title = "動名詞の活用と英語スキル向上"
    test_draft = "# 動名詞の活用と英語スキル向上\n## 動名詞とは\n### 動名詞の定義と使用法"
    
    print(f"Test query: {test_query}")
    print(f"Test title: {test_title}")
    
    content = ""
    async for chunk in lead_writer(
        query=test_query,
        title=test_title,
        draft=test_draft
    ):
        content += chunk
    
    print(f"Generated content (first 200 chars): {content[:200]}...")


async def test_mindmap_maker():
    """Test mind map generation module."""
    print("🗺️ Testing Mind Map Maker...")
    
    lm = load_lm()
    mindmap_maker = MindMapMaker(lm=lm)
    
    test_report = """
    # 動名詞の活用と英語スキル向上
    
    ## 動名詞とは
    動名詞は動詞の-ing形で、名詞として機能する文法要素です。
    
    ## 動名詞の使い方
    動名詞は主語、目的語、前置詞の目的語として使用できます。
    """
    
    test_related_topics = "不定詞、分詞、動詞の活用"
    
    result = mindmap_maker(report=test_report, related_topics=test_related_topics)
    print(f"Mind map content (first 300 chars): {result.mindmap[:300]}...")


async def test_web_search():
    """Test web search module."""
    print("🌐 Testing Web Search...")
    
    search = DuckDuckGoSearch()
    
    test_query = "gerunds in English grammar"
    print(f"Search query: {test_query}")
    
    results = search.search(test_query, k=3)
    print(f"Found {len(results)} results")
    
    for i, result in enumerate(results[:2], 1):
        print(f"{i}. {result.get('title', 'No title')}")
        print(f"   URL: {result.get('url', 'No URL')}")
        print(f"   Content: {result.get('snippet', 'No content')[:100]}...")


async def main():
    """Main function to run specific module tests."""
    parser = argparse.ArgumentParser(description='Test specific Englishy modules')
    parser.add_argument('module', choices=[
        'english_extractor', 'grammar_analyzer', 'query_refiner', 
        'query_expander', 'outline_creater', 'report_writer', 
        'mindmap_maker', 'web_search', 'all'
    ], help='Module to test')
    
    args = parser.parse_args()
    
    # dspyのグローバル設定（main関数の最初で必ず呼ぶ）
    lm = load_lm()
    dspy.settings.configure(lm=lm)
    
    print(f"🧪 Testing module: {args.module}")
    print("=" * 50)
    
    try:
        if args.module == 'english_extractor' or args.module == 'all':
            await test_english_extractor()
        
        if args.module == 'grammar_analyzer' or args.module == 'all':
            await test_grammar_analyzer()
        
        if args.module == 'query_refiner' or args.module == 'all':
            await test_query_refiner()
        
        if args.module == 'query_expander' or args.module == 'all':
            await test_query_expander()
        
        if args.module == 'outline_creater' or args.module == 'all':
            await test_outline_creater()
        
        if args.module == 'report_writer' or args.module == 'all':
            await test_report_writer()
        
        if args.module == 'mindmap_maker' or args.module == 'all':
            await test_mindmap_maker()
        
        if args.module == 'web_search' or args.module == 'all':
            await test_web_search()
        
        print("\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main()) 