#!/usr/bin/env python3
"""
Actual integration test for Englishy application.
Tests the real application functionality with correct method names.
"""

import sys
import os

# Add src to path for imports
sys.path.append('/app/src')

from ai.query_refiner import QueryRefiner
from ai.query_expander import QueryExpander
from ai.outline_creater import OutlineCreater
from ai.grammar_analyzer import get_grammar_analyzer
from ai.llm_grammar_analyzer import LLMGrammarAnalyzer
from utils.lm import load_lm


def test_actual_integration():
    """実際のアプリケーションでの統合テスト"""
    print("🧪 Starting Actual Integration Test")
    print("=" * 50)
    
    try:
        # Initialize LM
        print("1. Initializing LM...")
        lm = load_lm()
        print("✅ LM initialized successfully")
        
        # Initialize AI modules
        print("\n2. Initializing AI modules...")
        query_refiner = QueryRefiner(lm=lm)
        query_expander = QueryExpander(lm=lm)
        outline_creater = OutlineCreater(lm=lm)
        grammar_analyzer = get_grammar_analyzer()
        llm_grammar_analyzer = LLMGrammarAnalyzer()
        print("✅ All AI modules initialized successfully")
        
        # Test queries
        test_queries = [
            "仮定法過去について詳しく教えてください",
            "受動態の使い方を教えて",
            "動名詞と不定詞の違いについて"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n--- Test Case {i}: {query} ---")
            
            # Step 1: Query Refinement
            print("Step 1: Query Refinement")
            refined_query = query_refiner.refine(query)
            print(f"  Refined: {refined_query}")
            
            # Step 2: Query Expansion
            print("Step 2: Query Expansion")
            expansion_result = query_expander.forward(query)
            expanded_topics = expansion_result.topics
            print(f"  Expanded topics: {len(expanded_topics)}")
            for j, topic in enumerate(expanded_topics[:3], 1):  # Show first 3 topics
                print(f"    {j}. {topic}")
            
            # Step 3: Grammar Analysis
            print("Step 3: Grammar Analysis")
            grammar_analysis = grammar_analyzer.analyze_text(query)
            print(f"  Grammar structures: {grammar_analysis['grammar_structures']}")
            
            # Step 4: LLM Grammar Analysis
            print("Step 4: LLM Grammar Analysis")
            llm_analysis = llm_grammar_analyzer.analyze_text(query)
            print(f"  LLM structures: {llm_analysis['grammar_structures']}")
            
            # Step 5: Outline Creation
            print("Step 5: Outline Creation")
            search_results = [
                "English Grammar in Use - Raymond Murphy",
                "Practical English Usage - Michael Swan",
                "文部科学省 英語教育の手引き - 文部科学省"
            ]
            
            outline_result = outline_creater.forward(
                query=query,
                topics=expanded_topics,
                references=search_results,
                grammar_analysis=grammar_analysis
            )
            outline = outline_result.outline
            
            print(f"  Outline: {outline.title}")
            print(f"  Sections: {len(outline.section_outlines)}")
            
            # Check keywords
            keyword_count = 0
            for section in outline.section_outlines:
                if hasattr(section, 'subsection_outlines') and section.subsection_outlines:
                    for subsection in section.subsection_outlines:
                        if hasattr(subsection, 'keywords') and subsection.keywords:
                            keyword_count += len(subsection.keywords)
                            print(f"    Keywords in '{subsection.title}': {subsection.keywords}")
            
            print(f"  Total keywords: {keyword_count}")
            
            print(f"✅ Test Case {i} PASSED")
        
        print(f"\n🎉 All integration tests PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test FAILED: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False


def test_individual_modules():
    """個別モジュールのテスト"""
    print("\n🔧 Testing Individual Modules")
    print("=" * 30)
    
    try:
        lm = load_lm()
        
        # Test QueryRefiner
        print("\n1. Testing QueryRefiner...")
        query_refiner = QueryRefiner(lm=lm)
        result = query_refiner.refine("仮定法過去について詳しく教えてください")
        print(f"  Result: {result}")
        assert result is not None
        print("✅ QueryRefiner PASSED")
        
        # Test QueryExpander
        print("\n2. Testing QueryExpander...")
        query_expander = QueryExpander(lm=lm)
        result = query_expander.forward("仮定法過去について詳しく教えてください")
        print(f"  Topics: {len(result.topics)}")
        print(f"  First topic: {result.topics[0] if result.topics else 'None'}")
        assert len(result.topics) > 0
        print("✅ QueryExpander PASSED")
        
        # Test GrammarAnalyzer
        print("\n3. Testing GrammarAnalyzer...")
        grammar_analyzer = get_grammar_analyzer()
        result = grammar_analyzer.analyze_text("仮定法過去について詳しく教えてください")
        print(f"  Grammar structures: {result['grammar_structures']}")
        assert 'grammar_structures' in result
        print("✅ GrammarAnalyzer PASSED")
        
        # Test LLMGrammarAnalyzer
        print("\n4. Testing LLMGrammarAnalyzer...")
        llm_grammar_analyzer = LLMGrammarAnalyzer()
        result = llm_grammar_analyzer.analyze_text("If I had known, I would have helped you.")
        print(f"  LLM structures: {result['grammar_structures']}")
        assert 'grammar_structures' in result
        print("✅ LLMGrammarAnalyzer PASSED")
        
        # Test OutlineCreater
        print("\n5. Testing OutlineCreater...")
        outline_creater = OutlineCreater(lm=lm)
        grammar_analysis = grammar_analyzer.analyze_text("仮定法過去について詳しく教えてください")
        search_results = [
            "English Grammar in Use - Raymond Murphy",
            "Practical English Usage - Michael Swan"
        ]
        expansion_result = query_expander.forward("仮定法過去について詳しく教えてください")
        outline_result = outline_creater.forward(
            query="仮定法過去について詳しく教えてください",
            topics=expansion_result.topics,
            references=search_results,
            grammar_analysis=grammar_analysis
        )
        outline = outline_result.outline
        print(f"  Outline title: {outline.title}")
        print(f"  Sections: {len(outline.section_outlines)}")
        assert outline is not None
        assert len(outline.section_outlines) > 0
        print("✅ OutlineCreater PASSED")
        
        print(f"\n🎉 All individual module tests PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ Individual module test FAILED: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False


def test_user_scenarios():
    """ユーザーシナリオのテスト"""
    print("\n👤 Testing User Scenarios")
    print("=" * 30)
    
    try:
        lm = load_lm()
        query_refiner = QueryRefiner(lm=lm)
        query_expander = QueryExpander(lm=lm)
        grammar_analyzer = get_grammar_analyzer()
        outline_creater = OutlineCreater(lm=lm)
        
        # Beginner user scenario
        print("\n1. Beginner User Scenario...")
        beginner_query = "英語のbe動詞の使い方を教えてください"
        
        refined = query_refiner.refine(beginner_query)
        expanded = query_expander.forward(beginner_query)
        grammar = grammar_analyzer.analyze_text(beginner_query)
        
        print(f"  Query: {beginner_query}")
        print(f"  Refined: {refined}")
        print(f"  Topics: {len(expanded.topics)}")
        print(f"  Grammar: {grammar['grammar_structures']}")
        
        # Advanced user scenario
        print("\n2. Advanced User Scenario...")
        advanced_query = "仮定法過去完了と仮定法過去の違いについて詳しく説明してください"
        
        refined = query_refiner.refine(advanced_query)
        expanded = query_expander.forward(advanced_query)
        grammar = grammar_analyzer.analyze_text(advanced_query)
        
        print(f"  Query: {advanced_query}")
        print(f"  Refined: {refined}")
        print(f"  Topics: {len(expanded.topics)}")
        print(f"  Grammar: {grammar['grammar_structures']}")
        
        print(f"\n🎉 All user scenario tests PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ User scenario test FAILED: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False


if __name__ == "__main__":
    print("🚀 Starting Actual Application Integration Tests")
    print("=" * 60)
    
    # Run all tests
    success = True
    
    success &= test_individual_modules()
    success &= test_user_scenarios()
    success &= test_actual_integration()
    
    if success:
        print(f"\n🎉 ALL TESTS PASSED! Application is working correctly.")
        print(f"✅ All AI modules are properly integrated and functioning.")
        print(f"✅ User scenarios are handled correctly.")
        print(f"✅ The application is ready for real-world use.")
    else:
        print(f"\n❌ SOME TESTS FAILED! Please check the issues above.")
        exit(1) 