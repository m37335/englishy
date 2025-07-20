#!/usr/bin/env python3
"""
Simple integration test for all AI modules in the Englishy pipeline.
Tests the complete research pipeline from query input to final report generation.
"""

import sys
import os
import pytest

# Add src to path for imports
sys.path.append('/app/src')

from ai.query_refiner import QueryRefiner
from ai.query_expander import QueryExpander
from ai.outline_creater import OutlineCreater
from ai.grammar_analyzer import get_grammar_analyzer
from ai.llm_grammar_analyzer import LLMGrammarAnalyzer
from utils.lm import load_lm


class TestSimpleIntegration:
    """シンプルな統合テストクラス"""
    
    @pytest.fixture
    def ai_modules(self):
        """全AIモジュールを初期化"""
        try:
            lm = load_lm()
            
            return {
                'query_refiner': QueryRefiner(lm=lm),
                'query_expander': QueryExpander(lm=lm),
                'outline_creater': OutlineCreater(lm=lm),
                'grammar_analyzer': get_grammar_analyzer(),
                'llm_grammar_analyzer': LLMGrammarAnalyzer(lm=lm)
            }
        except Exception as e:
            pytest.skip(f"AI modules initialization failed: {e}")
    
    def test_query_refiner_integration(self, ai_modules):
        """QueryRefinerの統合テスト"""
        print(f"\n🔍 Testing QueryRefiner Integration")
        
        test_queries = [
            "仮定法過去について詳しく教えてください",
            "受動態の使い方を教えて",
            "動名詞と不定詞の違いについて"
        ]
        
        for query in test_queries:
            print(f"\nTesting query: '{query}'")
            
            # Query refinement
            refined_query = ai_modules['query_refiner'].refine_query(query)
            print(f"Refined query: {refined_query}")
            
            # Verify results
            assert refined_query is not None
            assert len(refined_query) > 0
            assert isinstance(refined_query, str)
        
        print(f"\n✅ QueryRefiner integration test PASSED")
    
    def test_query_expander_integration(self, ai_modules):
        """QueryExpanderの統合テスト"""
        print(f"\n📈 Testing QueryExpander Integration")
        
        test_queries = [
            "仮定法過去について詳しく教えてください",
            "受動態の使い方を教えて",
            "動名詞と不定詞の違いについて"
        ]
        
        for query in test_queries:
            print(f"\nTesting query: '{query}'")
            
            # Query expansion
            expanded_topics = ai_modules['query_expander'].expand_query(query)
            print(f"Expanded topics: {expanded_topics}")
            
            # Verify results
            assert expanded_topics is not None
            assert len(expanded_topics) > 0
            assert isinstance(expanded_topics, list)
            assert all(isinstance(topic, str) for topic in expanded_topics)
        
        print(f"\n✅ QueryExpander integration test PASSED")
    
    def test_grammar_analyzer_integration(self, ai_modules):
        """GrammarAnalyzerの統合テスト"""
        print(f"\n📊 Testing GrammarAnalyzer Integration")
        
        test_queries = [
            "仮定法過去について詳しく教えてください",
            "受動態の使い方を教えて",
            "動名詞と不定詞の違いについて",
            "If I had known, I would have helped you.",
            "The book was written by him."
        ]
        
        for query in test_queries:
            print(f"\nTesting query: '{query}'")
            
            # Grammar analysis
            grammar_analysis = ai_modules['grammar_analyzer'].analyze_text(query)
            print(f"Grammar analysis: {grammar_analysis}")
            
            # Verify results
            assert grammar_analysis is not None
            assert isinstance(grammar_analysis, dict)
            assert 'grammar_structures' in grammar_analysis
            assert isinstance(grammar_analysis['grammar_structures'], list)
        
        print(f"\n✅ GrammarAnalyzer integration test PASSED")
    
    def test_llm_grammar_analyzer_integration(self, ai_modules):
        """LLM GrammarAnalyzerの統合テスト"""
        print(f"\n🤖 Testing LLM GrammarAnalyzer Integration")
        
        test_queries = [
            "If I had known, I would have helped you.",
            "The book was written by him.",
            "I enjoy reading books."
        ]
        
        for query in test_queries:
            print(f"\nTesting query: '{query}'")
            
            # LLM-based grammar analysis
            llm_analysis = ai_modules['llm_grammar_analyzer'].analyze_text(query)
            print(f"LLM analysis: {llm_analysis}")
            
            # Verify results
            assert llm_analysis is not None
            assert isinstance(llm_analysis, dict)
            assert 'grammar_structures' in llm_analysis
            assert isinstance(llm_analysis['grammar_structures'], list)
        
        print(f"\n✅ LLM GrammarAnalyzer integration test PASSED")
    
    def test_outline_creater_integration(self, ai_modules):
        """OutlineCreaterの統合テスト"""
        print(f"\n📋 Testing OutlineCreater Integration")
        
        query = "仮定法過去について詳しく教えてください"
        
        # Grammar analysis
        grammar_analysis = ai_modules['grammar_analyzer'].analyze_text(query)
        
        # Search results (simulated)
        search_results = [
            "Teaching Subjunctive Mood in ESL - Cambridge University Press",
            "English Grammar in Use - Raymond Murphy",
            "Practical English Usage - Michael Swan",
            "文部科学省 英語教育の手引き - 文部科学省",
            "仮定法の指導法 - 東京大学教育学部"
        ]
        
        # Outline creation
        outline = ai_modules['outline_creater'].create_outline(
            query=query,
            search_results=search_results,
            grammar_analysis=grammar_analysis
        )
        
        print(f"Outline created: {outline.title if hasattr(outline, 'title') else 'No title'}")
        
        # Verify results
        assert outline is not None
        assert hasattr(outline, 'title')
        assert hasattr(outline, 'section_outlines')
        assert isinstance(outline.section_outlines, list)
        assert len(outline.section_outlines) > 0
        
        # Check for keywords in subsections
        keyword_found = False
        for section in outline.section_outlines:
            if hasattr(section, 'subsection_outlines') and section.subsection_outlines:
                for subsection in section.subsection_outlines:
                    if hasattr(subsection, 'keywords') and subsection.keywords:
                        print(f"Keywords in subsection '{subsection.title}': {subsection.keywords}")
                        keyword_found = True
                        assert isinstance(subsection.keywords, list)
                        assert len(subsection.keywords) > 0
        
        assert keyword_found, "No keywords found in outline"
        
        print(f"\n✅ OutlineCreater integration test PASSED")
    
    def test_complete_pipeline_integration(self, ai_modules):
        """完全パイプラインの統合テスト"""
        print(f"\n🚀 Testing Complete Pipeline Integration")
        
        query = "仮定法過去について詳しく教えてください"
        
        try:
            # Step 1: Query Refinement
            print(f"\nStep 1: Query Refinement")
            refined_query = ai_modules['query_refiner'].refine_query(query)
            print(f"Refined query: {refined_query}")
            assert refined_query is not None
            
            # Step 2: Query Expansion
            print(f"\nStep 2: Query Expansion")
            expanded_topics = ai_modules['query_expander'].expand_query(query)
            print(f"Expanded topics: {expanded_topics}")
            assert expanded_topics is not None
            
            # Step 3: Grammar Analysis
            print(f"\nStep 3: Grammar Analysis")
            grammar_analysis = ai_modules['grammar_analyzer'].analyze_text(query)
            print(f"Grammar analysis: {grammar_analysis}")
            assert grammar_analysis is not None
            
            # Step 4: LLM Grammar Analysis
            print(f"\nStep 4: LLM Grammar Analysis")
            llm_analysis = ai_modules['llm_grammar_analyzer'].analyze_text(query)
            print(f"LLM analysis: {llm_analysis}")
            assert llm_analysis is not None
            
            # Step 5: Web Search (simulated)
            print(f"\nStep 5: Web Search (simulated)")
            search_results = [
                "Teaching Subjunctive Mood in ESL - Cambridge University Press",
                "English Grammar in Use - Raymond Murphy",
                "Practical English Usage - Michael Swan",
                "文部科学省 英語教育の手引き - 文部科学省",
                "仮定法の指導法 - 東京大学教育学部"
            ]
            print(f"Search results: {len(search_results)} items")
            
            # Step 6: Outline Creation
            print(f"\nStep 6: Outline Creation")
            outline = ai_modules['outline_creater'].create_outline(
                query=query,
                search_results=search_results,
                grammar_analysis=grammar_analysis
            )
            print(f"Outline created: {outline.title}")
            assert outline is not None
            
            # Step 7: Verify Keywords Integration
            print(f"\nStep 7: Keywords Integration Verification")
            keyword_count = 0
            for section in outline.section_outlines:
                if hasattr(section, 'subsection_outlines') and section.subsection_outlines:
                    for subsection in section.subsection_outlines:
                        if hasattr(subsection, 'keywords') and subsection.keywords:
                            keyword_count += len(subsection.keywords)
                            print(f"Keywords in '{subsection.title}': {subsection.keywords}")
            
            print(f"Total keywords found: {keyword_count}")
            assert keyword_count > 0, "No keywords found in outline"
            
            print(f"\n✅ Complete pipeline integration test PASSED")
            
        except Exception as e:
            print(f"\n❌ Complete pipeline integration test FAILED: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            pytest.fail(f"Complete pipeline integration test failed: {e}")
    
    def test_multiple_grammar_topics(self, ai_modules):
        """複数の文法項目での統合テスト"""
        print(f"\n📚 Testing Multiple Grammar Topics")
        
        test_cases = [
            {
                "query": "仮定法過去について詳しく教えてください",
                "expected_keywords": ["仮定法", "過去形", "would"]
            },
            {
                "query": "受動態の使い方を教えて",
                "expected_keywords": ["受動態", "be動詞", "過去分詞"]
            },
            {
                "query": "動名詞と不定詞の違いについて",
                "expected_keywords": ["動名詞", "不定詞", "ing形", "to"]
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest case {i}: {test_case['query']}")
            
            # Query refinement
            refined_query = ai_modules['query_refiner'].refine_query(test_case['query'])
            print(f"Refined: {refined_query}")
            
            # Query expansion
            expanded_topics = ai_modules['query_expander'].expand_query(test_case['query'])
            print(f"Expanded: {len(expanded_topics)} topics")
            
            # Grammar analysis
            grammar_analysis = ai_modules['grammar_analyzer'].analyze_text(test_case['query'])
            print(f"Grammar structures: {grammar_analysis['grammar_structures']}")
            
            # Outline creation
            search_results = [
                "English Grammar in Use - Raymond Murphy",
                "Practical English Usage - Michael Swan",
                "文部科学省 英語教育の手引き - 文部科学省"
            ]
            
            outline = ai_modules['outline_creater'].create_outline(
                query=test_case['query'],
                search_results=search_results,
                grammar_analysis=grammar_analysis
            )
            
            # Verify outline structure
            assert outline is not None
            assert hasattr(outline, 'title')
            assert hasattr(outline, 'section_outlines')
            assert len(outline.section_outlines) > 0
            
            print(f"Outline: {outline.title}")
            print(f"Sections: {len(outline.section_outlines)}")
        
        print(f"\n✅ Multiple grammar topics test PASSED")


if __name__ == "__main__":
    print("🧪 Starting Simple Integration Tests")
    print("=" * 50)
    
    # テストの実行
    pytest.main([__file__, "-v", "--tb=short"]) 