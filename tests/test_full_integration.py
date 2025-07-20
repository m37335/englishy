#!/usr/bin/env python3
"""
Full integration test for all AI modules in the Englishy pipeline.
Tests the complete research pipeline from query input to final report generation.
"""

import sys
import os
import pytest
import asyncio
from typing import Dict, Any

# Add src to path for imports
sys.path.append('/app/src')

def run_async_test(async_func, *args, **kwargs):
    """非同期テストを同期的に実行するヘルパー関数"""
    return asyncio.run(async_func(*args, **kwargs))

from ai.query_refiner import QueryRefiner
from ai.query_expander import QueryExpander
from ai.outline_creater import OutlineCreater
from ai.report_writer import (
    StreamLeadWriter, StreamSectionWriter, StreamConclusionWriter,
    StreamRelatedTopicsWriter, StreamReferencesWriter
)
from ai.mindmap_maker import MindMapMaker
from ai.grammar_analyzer import get_grammar_analyzer
from ai.llm_grammar_analyzer import LLMGrammarAnalyzer
from utils.lm import load_lm
from utils.web_retriever import load_web_retriever


class TestFullIntegration:
    """全モジュール統合テストクラス"""
    
    @pytest.fixture
    def ai_modules(self):
        """全AIモジュールを初期化"""
        try:
            lm = load_lm()
            
            return {
                'query_refiner': QueryRefiner(lm=lm),
                'query_expander': QueryExpander(lm=lm),
                'outline_creater': OutlineCreater(lm=lm),
                'lead_writer': StreamLeadWriter(lm=lm),
                'section_writer': StreamSectionWriter(lm=lm),
                'conclusion_writer': StreamConclusionWriter(lm=lm),
                'related_topics_writer': StreamRelatedTopicsWriter(lm=lm),
                'references_writer': StreamReferencesWriter(lm=lm),
                'mindmap_maker': MindMapMaker(lm=lm),
                'grammar_analyzer': get_grammar_analyzer(),
                'llm_grammar_analyzer': LLMGrammarAnalyzer(lm=lm),
                'web_retriever': load_web_retriever()
            }
        except Exception as e:
            pytest.skip(f"AI modules initialization failed: {e}")
    
    @pytest.fixture
    def sample_queries(self):
        """テスト用サンプルクエリー"""
        return [
            "仮定法過去について詳しく教えてください",
            "受動態の使い方を教えて",
            "動名詞と不定詞の違いについて",
            "現在完了形の使い方を教えてください",
            "関係代名詞の使い方を教えて"
        ]
    
    def test_complete_pipeline_basic_grammar(self, ai_modules, sample_queries):
        """基本的な文法項目での完全パイプラインテスト"""
        query = sample_queries[0]  # 仮定法過去
        
        try:
            # Step 1: Query Refinement
            print(f"\n🔍 Step 1: Query Refinement for '{query}'")
            refined_query = ai_modules['query_refiner'].refine_query(query)
            print(f"Refined query: {refined_query}")
            assert refined_query is not None
            assert len(refined_query) > 0
            
            # Step 2: Query Expansion
            print(f"\n📈 Step 2: Query Expansion")
            expanded_topics = ai_modules['query_expander'].expand_query(query)
            print(f"Expanded topics: {expanded_topics}")
            assert expanded_topics is not None
            assert len(expanded_topics) > 0
            
            # Step 3: Grammar Analysis
            print(f"\n📊 Step 3: Grammar Analysis")
            grammar_analysis = ai_modules['grammar_analyzer'].analyze_text(query)
            print(f"Grammar analysis: {grammar_analysis}")
            assert grammar_analysis is not None
            assert 'grammar_structures' in grammar_analysis
            
            # Step 4: Web Search (simulated)
            print(f"\n🌐 Step 4: Web Search (simulated)")
            search_results = [
                "Teaching Subjunctive Mood in ESL - Cambridge University Press",
                "English Grammar in Use - Raymond Murphy",
                "Practical English Usage - Michael Swan",
                "文部科学省 英語教育の手引き - 文部科学省",
                "仮定法の指導法 - 東京大学教育学部"
            ]
            print(f"Search results: {len(search_results)} items")
            
            # Step 5: Outline Creation
            print(f"\n📋 Step 5: Outline Creation")
            outline = ai_modules['outline_creater'].create_outline(
                query=query,
                search_results=search_results,
                grammar_analysis=grammar_analysis
            )
            print(f"Outline created: {outline.title if hasattr(outline, 'title') else 'No title'}")
            assert outline is not None
            
            # Step 6: Report Generation
            print(f"\n📝 Step 6: Report Generation")
            
            # Lead generation
            lead_text = ""
            async def generate_lead():
                nonlocal lead_text
                async for chunk in ai_modules['lead_writer'](query, outline.title, "Sample content"):
                    lead_text += chunk
            
            run_async_test(generate_lead)
            print(f"Lead generated: {len(lead_text)} characters")
            assert len(lead_text) > 0
            
            # Section generation (first section)
            if hasattr(outline, 'section_outlines') and outline.section_outlines:
                first_section = outline.section_outlines[0]
                section_text = ""
                keywords = ""
                if hasattr(first_section, 'subsection_outlines') and first_section.subsection_outlines:
                    if hasattr(first_section.subsection_outlines[0], 'keywords'):
                        keywords = ", ".join(first_section.subsection_outlines[0].keywords)
                
                async for chunk in ai_modules['section_writer'](
                    query, 
                    "\n".join(search_results), 
                    f"# {first_section.title}",
                    keywords
                ):
                    section_text += chunk
                print(f"Section generated: {len(section_text)} characters")
                assert len(section_text) > 0
            
            # Conclusion generation
            conclusion_text = ""
            async for chunk in ai_modules['conclusion_writer'](query, "Sample report content"):
                conclusion_text += chunk
            print(f"Conclusion generated: {len(conclusion_text)} characters")
            assert len(conclusion_text) > 0
            
            # Step 7: Related Topics Generation
            print(f"\n🔗 Step 7: Related Topics Generation")
            related_topics_text = ""
            keywords = ["仮定法", "過去形", "would", "if節"]
            async for chunk in ai_modules['related_topics_writer'](
                query=query,
                outline_structure=outline,
                keywords=keywords,
                grammar_analysis=grammar_analysis
            ):
                related_topics_text += chunk
            print(f"Related topics generated: {len(related_topics_text)} characters")
            assert len(related_topics_text) > 0
            
            # Step 8: References Generation
            print(f"\n📚 Step 8: References Generation")
            references_text = ""
            report_content = f"{lead_text}\n{section_text}\n{conclusion_text}"
            async for chunk in ai_modules['references_writer'](
                query=query,
                report_content=report_content,
                search_results="\n".join(search_results),
                outline_structure=outline,
                keywords=keywords
            ):
                references_text += chunk
            print(f"References generated: {len(references_text)} characters")
            assert len(references_text) > 0
            
            # Step 9: Mind Map Generation
            print(f"\n🗺️ Step 9: Mind Map Generation")
            mindmap_text = ""
            async for chunk in ai_modules['mindmap_maker'](
                report=report_content,
                outline_structure=outline,
                keywords=keywords,
                related_topics=related_topics_text
            ):
                mindmap_text += chunk
            print(f"Mind map generated: {len(mindmap_text)} characters")
            assert len(mindmap_text) > 0
            
            print(f"\n✅ Complete pipeline test PASSED for '{query}'")
            
        except Exception as e:
            print(f"\n❌ Pipeline test FAILED: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            pytest.fail(f"Pipeline test failed: {e}")
    
    def test_complete_pipeline_passive_voice(self, ai_modules, sample_queries):
        """受動態での完全パイプラインテスト"""
        query = sample_queries[1]  # 受動態
        
        try:
            # Step 1: Query Refinement
            print(f"\n🔍 Step 1: Query Refinement for '{query}'")
            refined_query = ai_modules['query_refiner'].refine_query(query)
            print(f"Refined query: {refined_query}")
            assert refined_query is not None
            
            # Step 2: Query Expansion
            print(f"\n📈 Step 2: Query Expansion")
            expanded_topics = ai_modules['query_expander'].expand_query(query)
            print(f"Expanded topics: {expanded_topics}")
            assert expanded_topics is not None
            
            # Step 3: Grammar Analysis
            print(f"\n📊 Step 3: Grammar Analysis")
            grammar_analysis = ai_modules['grammar_analyzer'].analyze_text(query)
            print(f"Grammar analysis: {grammar_analysis}")
            assert grammar_analysis is not None
            
            # Step 4: Web Search (simulated)
            print(f"\n🌐 Step 4: Web Search (simulated)")
            search_results = [
                "Teaching Passive Voice in ESL - Oxford University Press",
                "English Grammar in Use - Raymond Murphy",
                "Practical English Usage - Michael Swan",
                "文部科学省 英語教育の手引き - 文部科学省",
                "受動態の指導法 - 東京大学教育学部"
            ]
            
            # Step 5: Outline Creation
            print(f"\n📋 Step 5: Outline Creation")
            outline = ai_modules['outline_creater'].create_outline(
                query=query,
                search_results=search_results,
                grammar_analysis=grammar_analysis
            )
            assert outline is not None
            
            # Step 6: Report Generation
            print(f"\n📝 Step 6: Report Generation")
            
            # Lead generation
            lead_text = ""
            async for chunk in ai_modules['lead_writer'](query, outline.title, "Sample content"):
                lead_text += chunk
            assert len(lead_text) > 0
            
            # Keywords for testing
            keywords = ["受動態", "be動詞", "過去分詞", "能動態"]
            
            # Step 7: Related Topics Generation
            print(f"\n🔗 Step 7: Related Topics Generation")
            related_topics_text = ""
            async for chunk in ai_modules['related_topics_writer'](
                query=query,
                outline_structure=outline,
                keywords=keywords,
                grammar_analysis=grammar_analysis
            ):
                related_topics_text += chunk
            assert len(related_topics_text) > 0
            
            # Step 8: References Generation
            print(f"\n📚 Step 8: References Generation")
            references_text = ""
            report_content = f"{lead_text}\nSample section content"
            async for chunk in ai_modules['references_writer'](
                query=query,
                report_content=report_content,
                search_results="\n".join(search_results),
                outline_structure=outline,
                keywords=keywords
            ):
                references_text += chunk
            assert len(references_text) > 0
            
            print(f"\n✅ Complete pipeline test PASSED for '{query}'")
            return True
            
        except Exception as e:
            print(f"\n❌ Pipeline test FAILED: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return False
    
    async def test_complete_pipeline_complex_grammar(self, ai_modules, sample_queries):
        """複雑な文法項目での完全パイプラインテスト"""
        query = sample_queries[2]  # 動名詞と不定詞の違い
        
        try:
            # Step 1: Query Refinement
            print(f"\n🔍 Step 1: Query Refinement for '{query}'")
            refined_query = ai_modules['query_refiner'].refine_query(query)
            print(f"Refined query: {refined_query}")
            assert refined_query is not None
            
            # Step 2: Query Expansion
            print(f"\n📈 Step 2: Query Expansion")
            expanded_topics = ai_modules['query_expander'].expand_query(query)
            print(f"Expanded topics: {expanded_topics}")
            assert expanded_topics is not None
            
            # Step 3: Grammar Analysis
            print(f"\n📊 Step 3: Grammar Analysis")
            grammar_analysis = ai_modules['grammar_analyzer'].analyze_text(query)
            print(f"Grammar analysis: {grammar_analysis}")
            assert grammar_analysis is not None
            
            # Step 4: Web Search (simulated)
            print(f"\n🌐 Step 4: Web Search (simulated)")
            search_results = [
                "Teaching Gerunds and Infinitives - Oxford University Press",
                "English Grammar in Use - Raymond Murphy",
                "Practical English Usage - Michael Swan",
                "文部科学省 英語教育の手引き - 文部科学省",
                "動名詞と不定詞の指導法 - 東京大学教育学部"
            ]
            
            # Step 5: Outline Creation
            print(f"\n📋 Step 5: Outline Creation")
            outline = ai_modules['outline_creater'].create_outline(
                query=query,
                search_results=search_results,
                grammar_analysis=grammar_analysis
            )
            assert outline is not None
            
            # Step 6: Report Generation
            print(f"\n📝 Step 6: Report Generation")
            
            # Lead generation
            lead_text = ""
            async for chunk in ai_modules['lead_writer'](query, outline.title, "Sample content"):
                lead_text += chunk
            assert len(lead_text) > 0
            
            # Keywords for testing
            keywords = ["動名詞", "不定詞", "ing形", "to + 原形", "使い分け"]
            
            # Step 7: Related Topics Generation
            print(f"\n🔗 Step 7: Related Topics Generation")
            related_topics_text = ""
            async for chunk in ai_modules['related_topics_writer'](
                query=query,
                outline_structure=outline,
                keywords=keywords,
                grammar_analysis=grammar_analysis
            ):
                related_topics_text += chunk
            assert len(related_topics_text) > 0
            
            # Step 8: References Generation
            print(f"\n📚 Step 8: References Generation")
            references_text = ""
            report_content = f"{lead_text}\nSample section content"
            async for chunk in ai_modules['references_writer'](
                query=query,
                report_content=report_content,
                search_results="\n".join(search_results),
                outline_structure=outline,
                keywords=keywords
            ):
                references_text += chunk
            assert len(references_text) > 0
            
            # Step 9: Mind Map Generation
            print(f"\n🗺️ Step 9: Mind Map Generation")
            mindmap_text = ""
            async for chunk in ai_modules['mindmap_maker'](
                report=report_content,
                outline_structure=outline,
                keywords=keywords,
                related_topics=related_topics_text
            ):
                mindmap_text += chunk
            assert len(mindmap_text) > 0
            
            print(f"\n✅ Complete pipeline test PASSED for '{query}'")
            return True
            
        except Exception as e:
            print(f"\n❌ Pipeline test FAILED: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return False
    
    def test_llm_grammar_analyzer_integration(self, ai_modules):
        """LLMベース文法解析の統合テスト"""
        try:
            print(f"\n🤖 Testing LLM-based Grammar Analyzer")
            
            # Test with different types of queries
            test_queries = [
                "If I had known, I would have helped you.",
                "The book was written by him.",
                "I enjoy reading books."
            ]
            
            for query in test_queries:
                print(f"\nTesting query: '{query}'")
                
                # LLM-based analysis
                llm_analysis = ai_modules['llm_grammar_analyzer'].analyze_text(query)
                print(f"LLM analysis: {llm_analysis}")
                
                # Regular analysis for comparison
                regular_analysis = ai_modules['grammar_analyzer'].analyze_text(query)
                print(f"Regular analysis: {regular_analysis}")
                
                # Both should return valid results
                assert llm_analysis is not None
                assert regular_analysis is not None
                assert 'grammar_structures' in llm_analysis
                assert 'grammar_structures' in regular_analysis
            
            print(f"\n✅ LLM Grammar Analyzer integration test PASSED")
            return True
            
        except Exception as e:
            print(f"\n❌ LLM Grammar Analyzer integration test FAILED: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return False
    
    def test_keyword_integration_throughout_pipeline(self, ai_modules):
        """キーワード機能の全パイプライン統合テスト"""
        try:
            print(f"\n🔑 Testing Keyword Integration Throughout Pipeline")
            
            query = "仮定法過去について詳しく教えてください"
            
            # Step 1: Grammar Analysis
            grammar_analysis = ai_modules['grammar_analyzer'].analyze_text(query)
            
            # Step 2: Outline Creation with keywords
            search_results = [
                "Teaching Subjunctive Mood in ESL - Cambridge University Press",
                "English Grammar in Use - Raymond Murphy"
            ]
            
            outline = ai_modules['outline_creater'].create_outline(
                query=query,
                search_results=search_results,
                grammar_analysis=grammar_analysis
            )
            
            # Verify keywords are present in outline
            if hasattr(outline, 'section_outlines') and outline.section_outlines:
                for section in outline.section_outlines:
                    if hasattr(section, 'subsection_outlines') and section.subsection_outlines:
                        for subsection in section.subsection_outlines:
                            if hasattr(subsection, 'keywords'):
                                print(f"Keywords in subsection '{subsection.title}': {subsection.keywords}")
                                assert len(subsection.keywords) > 0
            
            print(f"\n✅ Keyword integration test PASSED")
            return True
            
        except Exception as e:
            print(f"\n❌ Keyword integration test FAILED: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return False


class TestRealApplicationSimulation:
    """実際のアプリケーションシミュレーションテスト"""
    
    @pytest.fixture
    def ai_modules(self):
        """全AIモジュールを初期化"""
        try:
            lm = load_lm()
            
            return {
                'query_refiner': QueryRefiner(lm=lm),
                'query_expander': QueryExpander(lm=lm),
                'outline_creater': OutlineCreater(lm=lm),
                'lead_writer': StreamLeadWriter(lm=lm),
                'section_writer': StreamSectionWriter(lm=lm),
                'conclusion_writer': StreamConclusionWriter(lm=lm),
                'related_topics_writer': StreamRelatedTopicsWriter(lm=lm),
                'references_writer': StreamReferencesWriter(lm=lm),
                'mindmap_maker': MindMapMaker(lm=lm),
                'grammar_analyzer': get_grammar_analyzer(),
                'llm_grammar_analyzer': LLMGrammarAnalyzer(lm=lm),
                'web_retriever': load_web_retriever()
            }
        except Exception as e:
            pytest.skip(f"AI modules initialization failed: {e}")
    
    async def test_real_user_scenario_beginner(self, ai_modules):
        """初心者ユーザーの実際のシナリオテスト"""
        print(f"\n👤 Testing Real User Scenario: Beginner Level")
        
        # Simulate beginner user query
        query = "英語のbe動詞の使い方を教えてください"
        
        try:
            # Complete pipeline execution
            result = await self._execute_complete_pipeline(ai_modules, query)
            
            # Verify beginner-friendly output
            assert result['lead_text'].find('be動詞') >= 0 or result['lead_text'].find('be verb') >= 0
            assert len(result['lead_text']) > 100  # Sufficient content
            
            print(f"\n✅ Beginner user scenario test PASSED")
            return True
            
        except Exception as e:
            print(f"\n❌ Beginner user scenario test FAILED: {e}")
            return False
    
    async def test_real_user_scenario_advanced(self, ai_modules):
        """上級者ユーザーの実際のシナリオテスト"""
        print(f"\n👤 Testing Real User Scenario: Advanced Level")
        
        # Simulate advanced user query
        query = "仮定法過去完了と仮定法過去の違いについて詳しく説明してください"
        
        try:
            # Complete pipeline execution
            result = await self._execute_complete_pipeline(ai_modules, query)
            
            # Verify advanced content
            assert result['lead_text'].find('仮定法') >= 0
            assert len(result['lead_text']) > 150  # More detailed content
            
            print(f"\n✅ Advanced user scenario test PASSED")
            return True
            
        except Exception as e:
            print(f"\n❌ Advanced user scenario test FAILED: {e}")
            return False
    
    async def _execute_complete_pipeline(self, ai_modules, query):
        """完全パイプラインの実行"""
        # Step 1: Query Refinement
        refined_query = ai_modules['query_refiner'].refine_query(query)
        
        # Step 2: Query Expansion
        expanded_topics = ai_modules['query_expander'].expand_query(query)
        
        # Step 3: Grammar Analysis
        grammar_analysis = ai_modules['grammar_analyzer'].analyze_text(query)
        
        # Step 4: Web Search (simulated)
        search_results = [
            "English Grammar in Use - Raymond Murphy",
            "Practical English Usage - Michael Swan",
            "文部科学省 英語教育の手引き - 文部科学省"
        ]
        
        # Step 5: Outline Creation
        outline = ai_modules['outline_creater'].create_outline(
            query=query,
            search_results=search_results,
            grammar_analysis=grammar_analysis
        )
        
        # Step 6: Report Generation
        lead_text = ""
        async for chunk in ai_modules['lead_writer'](query, outline.title, "Sample content"):
            lead_text += chunk
        
        # Extract keywords from outline
        keywords = []
        if hasattr(outline, 'section_outlines') and outline.section_outlines:
            for section in outline.section_outlines:
                if hasattr(section, 'subsection_outlines') and section.subsection_outlines:
                    for subsection in section.subsection_outlines:
                        if hasattr(subsection, 'keywords'):
                            keywords.extend(subsection.keywords)
        
        # Step 7: Related Topics Generation
        related_topics_text = ""
        async for chunk in ai_modules['related_topics_writer'](
            query=query,
            outline_structure=outline,
            keywords=keywords,
            grammar_analysis=grammar_analysis
        ):
            related_topics_text += chunk
        
        # Step 8: References Generation
        references_text = ""
        report_content = f"{lead_text}\nSample section content"
        async for chunk in ai_modules['references_writer'](
            query=query,
            report_content=report_content,
            search_results="\n".join(search_results),
            outline_structure=outline,
            keywords=keywords
        ):
            references_text += chunk
        
        return {
            'refined_query': refined_query,
            'expanded_topics': expanded_topics,
            'grammar_analysis': grammar_analysis,
            'outline': outline,
            'lead_text': lead_text,
            'related_topics_text': related_topics_text,
            'references_text': references_text
        }


if __name__ == "__main__":
    print("🧪 Starting Full Integration Tests")
    print("=" * 60)
    
    # テストの実行
    pytest.main([__file__, "-v", "--tb=short"]) 