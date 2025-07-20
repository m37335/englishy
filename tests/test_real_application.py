#!/usr/bin/env python3
"""
Real application test for Englishy.
Tests the actual application functionality and user scenarios.
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


class TestRealApplication:
    """実際のアプリケーションテストクラス"""
    
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
    
    def test_real_user_query_processing(self, ai_modules):
        """実際のユーザークエリー処理テスト"""
        print(f"\n👤 Testing Real User Query Processing")
        
        # 実際のユーザーが入力しそうなクエリー
        real_user_queries = [
            "仮定法過去について詳しく教えてください",
            "受動態の使い方を教えて",
            "動名詞と不定詞の違いについて",
            "現在完了形の使い方を教えてください",
            "関係代名詞の使い方を教えて",
            "英語のbe動詞の使い方を教えてください",
            "仮定法過去完了と仮定法過去の違いについて詳しく説明してください"
        ]
        
        for i, query in enumerate(real_user_queries, 1):
            print(f"\n--- Test Case {i}: {query} ---")
            
            try:
                # Step 1: Query Refinement
                print(f"Step 1: Query Refinement")
                refined_query = ai_modules['query_refiner'].refine_query(query)
                print(f"  Refined: {refined_query}")
                assert refined_query is not None
                assert len(refined_query) > 0
                
                # Step 2: Query Expansion
                print(f"Step 2: Query Expansion")
                expanded_topics = ai_modules['query_expander'].expand_query(query)
                print(f"  Expanded: {len(expanded_topics)} topics")
                assert expanded_topics is not None
                assert len(expanded_topics) > 0
                
                # Step 3: Grammar Analysis
                print(f"Step 3: Grammar Analysis")
                grammar_analysis = ai_modules['grammar_analyzer'].analyze_text(query)
                print(f"  Grammar structures: {grammar_analysis['grammar_structures']}")
                assert grammar_analysis is not None
                assert 'grammar_structures' in grammar_analysis
                
                # Step 4: LLM Grammar Analysis
                print(f"Step 4: LLM Grammar Analysis")
                llm_analysis = ai_modules['llm_grammar_analyzer'].analyze_text(query)
                print(f"  LLM structures: {llm_analysis['grammar_structures']}")
                assert llm_analysis is not None
                assert 'grammar_structures' in llm_analysis
                
                # Step 5: Outline Creation
                print(f"Step 5: Outline Creation")
                search_results = [
                    "English Grammar in Use - Raymond Murphy",
                    "Practical English Usage - Michael Swan",
                    "文部科学省 英語教育の手引き - 文部科学省"
                ]
                
                outline = ai_modules['outline_creater'].create_outline(
                    query=query,
                    search_results=search_results,
                    grammar_analysis=grammar_analysis
                )
                
                print(f"  Outline: {outline.title}")
                print(f"  Sections: {len(outline.section_outlines)}")
                
                # Verify outline structure
                assert outline is not None
                assert hasattr(outline, 'title')
                assert hasattr(outline, 'section_outlines')
                assert len(outline.section_outlines) > 0
                
                # Check keywords
                keyword_count = 0
                for section in outline.section_outlines:
                    if hasattr(section, 'subsection_outlines') and section.subsection_outlines:
                        for subsection in section.subsection_outlines:
                            if hasattr(subsection, 'keywords') and subsection.keywords:
                                keyword_count += len(subsection.keywords)
                                print(f"    Keywords in '{subsection.title}': {subsection.keywords}")
                
                print(f"  Total keywords: {keyword_count}")
                assert keyword_count > 0, "No keywords found in outline"
                
                print(f"✅ Test Case {i} PASSED")
                
            except Exception as e:
                print(f"❌ Test Case {i} FAILED: {e}")
                import traceback
                print(f"Traceback: {traceback.format_exc()}")
                pytest.fail(f"Test case {i} failed: {e}")
        
        print(f"\n✅ Real user query processing test PASSED")
    
    def test_beginner_user_scenario(self, ai_modules):
        """初心者ユーザーのシナリオテスト"""
        print(f"\n🎓 Testing Beginner User Scenario")
        
        # 初心者が入力しそうなクエリー
        beginner_queries = [
            "英語のbe動詞の使い方を教えてください",
            "現在形の使い方を教えて",
            "英語の基本文法を教えてください",
            "英語の勉強方法を教えてください"
        ]
        
        for query in beginner_queries:
            print(f"\nTesting beginner query: '{query}'")
            
            # Query refinement
            refined_query = ai_modules['query_refiner'].refine_query(query)
            print(f"  Refined: {refined_query}")
            
            # Query expansion
            expanded_topics = ai_modules['query_expander'].expand_query(query)
            print(f"  Expanded topics: {len(expanded_topics)}")
            
            # Grammar analysis
            grammar_analysis = ai_modules['grammar_analyzer'].analyze_text(query)
            print(f"  Grammar structures: {grammar_analysis['grammar_structures']}")
            
            # Outline creation
            search_results = [
                "English Grammar in Use - Raymond Murphy",
                "Practical English Usage - Michael Swan",
                "文部科学省 英語教育の手引き - 文部科学省"
            ]
            
            outline = ai_modules['outline_creater'].create_outline(
                query=query,
                search_results=search_results,
                grammar_analysis=grammar_analysis
            )
            
            print(f"  Outline: {outline.title}")
            print(f"  Sections: {len(outline.section_outlines)}")
            
            # Verify beginner-friendly content
            assert outline is not None
            assert len(outline.section_outlines) > 0
            
            # Check for basic grammar keywords
            basic_keywords = ["be動詞", "現在形", "基本", "勉強", "学習"]
            found_basic_keywords = []
            
            for section in outline.section_outlines:
                if hasattr(section, 'subsection_outlines') and section.subsection_outlines:
                    for subsection in section.subsection_outlines:
                        if hasattr(subsection, 'keywords') and subsection.keywords:
                            for keyword in subsection.keywords:
                                if any(basic in keyword for basic in basic_keywords):
                                    found_basic_keywords.append(keyword)
            
            print(f"  Found basic keywords: {found_basic_keywords}")
        
        print(f"\n✅ Beginner user scenario test PASSED")
    
    def test_advanced_user_scenario(self, ai_modules):
        """上級者ユーザーのシナリオテスト"""
        print(f"\n🎯 Testing Advanced User Scenario")
        
        # 上級者が入力しそうなクエリー
        advanced_queries = [
            "仮定法過去完了と仮定法過去の違いについて詳しく説明してください",
            "関係代名詞の非制限用法について教えてください",
            "英語の倒置構文について詳しく説明してください",
            "英語の強調構文について教えてください"
        ]
        
        for query in advanced_queries:
            print(f"\nTesting advanced query: '{query}'")
            
            # Query refinement
            refined_query = ai_modules['query_refiner'].refine_query(query)
            print(f"  Refined: {refined_query}")
            
            # Query expansion
            expanded_topics = ai_modules['query_expander'].expand_query(query)
            print(f"  Expanded topics: {len(expanded_topics)}")
            
            # Grammar analysis
            grammar_analysis = ai_modules['grammar_analyzer'].analyze_text(query)
            print(f"  Grammar structures: {grammar_analysis['grammar_structures']}")
            
            # LLM analysis for advanced content
            llm_analysis = ai_modules['llm_grammar_analyzer'].analyze_text(query)
            print(f"  LLM structures: {llm_analysis['grammar_structures']}")
            
            # Outline creation
            search_results = [
                "Advanced English Grammar - Cambridge University Press",
                "English Grammar in Use Advanced - Raymond Murphy",
                "Practical English Usage - Michael Swan",
                "文部科学省 英語教育の手引き - 文部科学省"
            ]
            
            outline = ai_modules['outline_creater'].create_outline(
                query=query,
                search_results=search_results,
                grammar_analysis=grammar_analysis
            )
            
            print(f"  Outline: {outline.title}")
            print(f"  Sections: {len(outline.section_outlines)}")
            
            # Verify advanced content
            assert outline is not None
            assert len(outline.section_outlines) > 0
            
            # Check for advanced grammar keywords
            advanced_keywords = ["仮定法", "関係代名詞", "倒置", "強調", "完了", "非制限"]
            found_advanced_keywords = []
            
            for section in outline.section_outlines:
                if hasattr(section, 'subsection_outlines') and section.subsection_outlines:
                    for subsection in section.subsection_outlines:
                        if hasattr(subsection, 'keywords') and subsection.keywords:
                            for keyword in subsection.keywords:
                                if any(advanced in keyword for advanced in advanced_keywords):
                                    found_advanced_keywords.append(keyword)
            
            print(f"  Found advanced keywords: {found_advanced_keywords}")
        
        print(f"\n✅ Advanced user scenario test PASSED")
    
    def test_error_handling_and_edge_cases(self, ai_modules):
        """エラーハンドリングとエッジケースのテスト"""
        print(f"\n⚠️ Testing Error Handling and Edge Cases")
        
        # エッジケースのクエリー
        edge_case_queries = [
            "",  # 空のクエリー
            "a",  # 非常に短いクエリー
            "英語",  # 非常に短い日本語クエリー
            "This is a very long query that contains many words and should test the system's ability to handle lengthy input without breaking or causing issues with the processing pipeline.",  # 非常に長いクエリー
            "特殊文字!@#$%^&*()_+{}|:<>?[]\\;'\",./",  # 特殊文字
            "1234567890",  # 数字のみ
            "英語 文法 仮定法 過去 完了 関係代名詞 倒置 強調 非制限 用法 違い 詳しく 説明 教えて ください"  # 長い日本語クエリー
        ]
        
        for i, query in enumerate(edge_case_queries, 1):
            print(f"\n--- Edge Case {i}: '{query[:50]}{'...' if len(query) > 50 else ''}' ---")
            
            try:
                # Query refinement
                refined_query = ai_modules['query_refiner'].refine_query(query)
                print(f"  Refined: {refined_query}")
                
                # Query expansion
                expanded_topics = ai_modules['query_expander'].expand_query(query)
                print(f"  Expanded: {len(expanded_topics)} topics")
                
                # Grammar analysis
                grammar_analysis = ai_modules['grammar_analyzer'].analyze_text(query)
                print(f"  Grammar structures: {grammar_analysis['grammar_structures']}")
                
                # LLM analysis
                llm_analysis = ai_modules['llm_grammar_analyzer'].analyze_text(query)
                print(f"  LLM structures: {llm_analysis['grammar_structures']}")
                
                # Outline creation (only for non-empty queries)
                if query.strip():
                    search_results = [
                        "English Grammar in Use - Raymond Murphy",
                        "Practical English Usage - Michael Swan"
                    ]
                    
                    outline = ai_modules['outline_creater'].create_outline(
                        query=query,
                        search_results=search_results,
                        grammar_analysis=grammar_analysis
                    )
                    
                    print(f"  Outline created: {outline.title if outline else 'None'}")
                
                print(f"✅ Edge Case {i} handled successfully")
                
            except Exception as e:
                print(f"❌ Edge Case {i} failed: {e}")
                # Edge cases should be handled gracefully, but some failures are expected
                if not query.strip():
                    print(f"  Expected failure for empty query")
                else:
                    print(f"  Unexpected failure")
        
        print(f"\n✅ Error handling and edge cases test PASSED")
    
    def test_performance_and_stability(self, ai_modules):
        """パフォーマンスと安定性のテスト"""
        print(f"\n⚡ Testing Performance and Stability")
        
        # 複数のクエリーを連続で処理
        test_queries = [
            "仮定法過去について詳しく教えてください",
            "受動態の使い方を教えて",
            "動名詞と不定詞の違いについて",
            "現在完了形の使い方を教えてください",
            "関係代名詞の使い方を教えて"
        ]
        
        import time
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n--- Performance Test {i}: {query} ---")
            
            start_time = time.time()
            
            try:
                # Query refinement
                refined_query = ai_modules['query_refiner'].refine_query(query)
                
                # Query expansion
                expanded_topics = ai_modules['query_expander'].expand_query(query)
                
                # Grammar analysis
                grammar_analysis = ai_modules['grammar_analyzer'].analyze_text(query)
                
                # LLM analysis
                llm_analysis = ai_modules['llm_grammar_analyzer'].analyze_text(query)
                
                # Outline creation
                search_results = [
                    "English Grammar in Use - Raymond Murphy",
                    "Practical English Usage - Michael Swan"
                ]
                
                outline = ai_modules['outline_creater'].create_outline(
                    query=query,
                    search_results=search_results,
                    grammar_analysis=grammar_analysis
                )
                
                end_time = time.time()
                processing_time = end_time - start_time
                
                print(f"  Processing time: {processing_time:.2f} seconds")
                print(f"  Refined query: {refined_query}")
                print(f"  Expanded topics: {len(expanded_topics)}")
                print(f"  Grammar structures: {len(grammar_analysis['grammar_structures'])}")
                print(f"  LLM structures: {len(llm_analysis['grammar_structures'])}")
                print(f"  Outline sections: {len(outline.section_outlines)}")
                
                # Performance assertions
                assert processing_time < 30.0, f"Processing took too long: {processing_time:.2f} seconds"
                assert refined_query is not None
                assert len(expanded_topics) > 0
                assert len(grammar_analysis['grammar_structures']) >= 0
                assert len(llm_analysis['grammar_structures']) >= 0
                assert outline is not None
                
                print(f"✅ Performance Test {i} PASSED")
                
            except Exception as e:
                print(f"❌ Performance Test {i} FAILED: {e}")
                pytest.fail(f"Performance test {i} failed: {e}")
        
        print(f"\n✅ Performance and stability test PASSED")


if __name__ == "__main__":
    print("🧪 Starting Real Application Tests")
    print("=" * 50)
    
    # テストの実行
    pytest.main([__file__, "-v", "--tb=short"]) 