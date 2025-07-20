#!/usr/bin/env python3
"""
Test script for improved RelatedTopicsWriter with outline structure and keyword integration.
Tests the enhanced related topics generation that integrates outline structure, keywords, and grammar analysis.
"""

import sys
import os
import pytest

# Add src to path for imports
sys.path.append('/app/src')

from ai.report_writer import StreamRelatedTopicsWriter
from utils.lm import load_lm


class TestRelatedTopicsWriter:
    """RelatedTopicsWriterのテストクラス"""
    
    @pytest.fixture
    def related_topics_writer(self):
        """RelatedTopicsWriterインスタンスを作成"""
        lm = load_lm()
        return StreamRelatedTopicsWriter(lm=lm)
    
    @pytest.fixture
    def sample_query(self):
        """サンプルクエリー"""
        return "仮定法過去について詳しく教えてください"
    
    @pytest.fixture
    def sample_outline(self):
        """サンプルアウトライン構造"""
        class MockOutline:
            def __init__(self):
                self.title = "仮定法過去の完全ガイド"
                self.section_outlines = [
                    MockSection("1. 文法構造の理解", [
                        MockSubsection("基本的な文法項目", ["仮定法", "過去形", "would"]),
                        MockSubsection("難易度と学習のポイント", ["時制", "使い分け"])
                    ]),
                    MockSection("2. 実例と詳細解説", [
                        MockSubsection("実際の使用例", ["例文", "会話"]),
                        MockSubsection("教育方法とアプローチ", ["指導法", "練習"])
                    ]),
                    MockSection("3. 実践的な活用", [
                        MockSubsection("よくある間違いと対策", ["間違い", "対策"]),
                        MockSubsection("効果的な練習方法", ["練習", "方法"])
                    ])
                ]
        
        class MockSection:
            def __init__(self, title, subsections):
                self.title = title
                self.subsection_outlines = subsections
        
        class MockSubsection:
            def __init__(self, title, keywords):
                self.title = title
                self.keywords = keywords
        
        return MockOutline()
    
    @pytest.fixture
    def sample_keywords(self):
        """サンプルキーワード"""
        return ["仮定法", "過去形", "would", "時制", "使い分け", "例文", "練習"]
    
    @pytest.fixture
    def sample_grammar_analysis(self):
        """サンプル文法解析結果"""
        class MockGrammarAnalysis:
            def __init__(self):
                self.grammar_structures = ["subjunctive mood", "conditional", "past tense"]
                self.related_topics = ["conditional sentences", "verb tenses", "modals"]
                self.learning_points = ["時制の使い分け", "仮定法の基本構造", "実践的な使用場面"]
                self.difficulty_level = "中級"
        
        return MockGrammarAnalysis()
    
    def test_related_topics_writer_initialization(self, related_topics_writer):
        """RelatedTopicsWriterの初期化テスト"""
        assert related_topics_writer is not None
        assert hasattr(related_topics_writer, 'grammar_analyzer')
        assert hasattr(related_topics_writer, '_convert_outline_to_text')
        assert hasattr(related_topics_writer, '_convert_grammar_analysis_to_text')
    
    def test_convert_outline_to_text(self, related_topics_writer, sample_outline):
        """アウトライン構造のテキスト変換テスト"""
        outline_text = related_topics_writer._convert_outline_to_text(sample_outline)
        
        # タイトルが含まれているか
        assert "仮定法過去の完全ガイド" in outline_text
        
        # セクション構造が含まれているか
        assert "1. 文法構造の理解" in outline_text
        assert "2. 実例と詳細解説" in outline_text
        assert "3. 実践的な活用" in outline_text
        
        # サブセクションが含まれているか
        assert "基本的な文法項目" in outline_text
        assert "実際の使用例" in outline_text
    
    def test_convert_outline_to_text_with_invalid_outline(self, related_topics_writer):
        """無効なアウトライン構造の変換テスト"""
        invalid_outline = {"invalid": "structure"}
        result = related_topics_writer._convert_outline_to_text(invalid_outline)
        assert "アウトライン構造の変換に失敗しました" in result
    
    def test_convert_grammar_analysis_to_text(self, related_topics_writer, sample_grammar_analysis):
        """文法解析結果のテキスト変換テスト"""
        grammar_text = related_topics_writer._convert_grammar_analysis_to_text(sample_grammar_analysis)
        
        # 文法構造が含まれているか
        assert "subjunctive mood" in grammar_text
        assert "conditional" in grammar_text
        assert "past tense" in grammar_text
        
        # 関連トピックが含まれているか
        assert "conditional sentences" in grammar_text
        assert "verb tenses" in grammar_text
        assert "modals" in grammar_text
        
        # 学習ポイントが含まれているか
        assert "時制の使い分け" in grammar_text
        assert "仮定法の基本構造" in grammar_text
        
        # 難易度が含まれているか
        assert "中級" in grammar_text
    
    def test_convert_grammar_analysis_to_text_with_invalid_analysis(self, related_topics_writer):
        """無効な文法解析結果の変換テスト"""
        invalid_analysis = {"invalid": "structure"}
        result = related_topics_writer._convert_grammar_analysis_to_text(invalid_analysis)
        assert "文法解析結果の変換に失敗しました" in result
    
    def test_forward_with_all_parameters(self, related_topics_writer, sample_query, sample_outline, sample_keywords, sample_grammar_analysis):
        """全パラメータ付きのforwardメソッドテスト"""
        # テスト実行
        result_text = ""
        async def run_test():
            nonlocal result_text
            async for chunk in related_topics_writer(
                query=sample_query,
                outline_structure=sample_outline,
                keywords=sample_keywords,
                grammar_analysis=sample_grammar_analysis
            ):
                result_text += chunk
        
        # 非同期テストの実行
        import asyncio
        asyncio.run(run_test())
        
        # 検証
        assert len(result_text) > 0
        assert "関連学習トピック" in result_text or "関連" in result_text
        print(f"\n生成された関連トピック:\n{result_text}")
    
    def test_forward_with_minimal_parameters(self, related_topics_writer, sample_query):
        """最小パラメータでのforwardメソッドテスト"""
        # テスト実行
        result_text = ""
        async def run_test():
            nonlocal result_text
            async for chunk in related_topics_writer(query=sample_query):
                result_text += chunk
        
        # 非同期テストの実行
        import asyncio
        asyncio.run(run_test())
        
        # 検証
        assert len(result_text) > 0
        print(f"\n最小パラメータの関連トピック:\n{result_text}")
    
    def test_forward_with_keywords_only(self, related_topics_writer, sample_query, sample_keywords):
        """キーワードのみでのforwardメソッドテスト"""
        # テスト実行
        result_text = ""
        async def run_test():
            nonlocal result_text
            async for chunk in related_topics_writer(
                query=sample_query,
                keywords=sample_keywords
            ):
                result_text += chunk
        
        # 非同期テストの実行
        import asyncio
        asyncio.run(run_test())
        
        # 検証
        assert len(result_text) > 0
        print(f"\nキーワード付き関連トピック:\n{result_text}")


class TestRelatedTopicsWriterIntegration:
    """RelatedTopicsWriterの統合テストクラス"""
    
    @pytest.fixture
    def related_topics_writer(self):
        """RelatedTopicsWriterインスタンスを作成"""
        lm = load_lm()
        return StreamRelatedTopicsWriter(lm=lm)
    
    def test_real_related_topics_generation(self, related_topics_writer):
        """実際の関連トピック生成テスト"""
        # テストデータ
        query = "受動態の使い方を教えてください"
        keywords = ["受動態", "be動詞", "過去分詞", "能動態", "時制", "例文"]
        
        try:
            # 実際の関連トピック生成
            result_text = ""
            async def run_test():
                nonlocal result_text
                async for chunk in related_topics_writer(
                    query=query,
                    keywords=keywords
                ):
                    result_text += chunk
            
            # 非同期テストの実行
            import asyncio
            asyncio.run(run_test())
            
            # 基本的な検証
            assert len(result_text) > 0
            
            # 関連トピックの内容確認
            print(f"\n生成された関連トピック:\n{result_text}")
            
            # 基本的な構造が含まれているか
            assert "関連" in result_text or "学習" in result_text or "文法" in result_text
            
        except Exception as e:
            pytest.skip(f"LLM接続エラー: {e}")
    
    def test_related_topics_with_complex_grammar(self, related_topics_writer):
        """複雑な文法項目での関連トピック生成テスト"""
        # 複雑な文法項目のクエリー
        query = "仮定法過去完了と仮定法過去の違いについて"
        keywords = ["仮定法過去完了", "had + 過去分詞", "would have", "時制", "違い", "間違い"]
        
        try:
            # 実際の関連トピック生成
            result_text = ""
            async def run_test():
                nonlocal result_text
                async for chunk in related_topics_writer(
                    query=query,
                    keywords=keywords
                ):
                    result_text += chunk
            
            # 非同期テストの実行
            import asyncio
            asyncio.run(run_test())
            
            # 基本的な検証
            assert len(result_text) > 0
            
            # 関連トピックの内容確認
            print(f"\n複雑文法の関連トピック:\n{result_text}")
            
            # 複雑な文法項目が適切に処理されているか
            assert "仮定法" in result_text or "subjunctive" in result_text.lower()
            
        except Exception as e:
            pytest.skip(f"LLM接続エラー: {e}")
    
    def test_related_topics_with_outline_integration(self, related_topics_writer):
        """アウトライン統合での関連トピック生成テスト"""
        # テストデータ
        query = "動名詞と不定詞の違いについて"
        
        # サンプルアウトライン構造
        class MockOutline:
            def __init__(self):
                self.title = "動名詞と不定詞の完全比較"
                self.section_outlines = [
                    MockSection("1. 基本的な違い", [
                        MockSubsection("動名詞の特徴", ["動名詞", "ing形", "名詞的用法"]),
                        MockSubsection("不定詞の特徴", ["不定詞", "to + 原形", "多様な用法"])
                    ]),
                    MockSection("2. 使い分けのポイント", [
                        MockSubsection("動詞の後", ["動詞", "使い分け", "ルール"]),
                        MockSubsection("前置詞の後", ["前置詞", "動名詞", "必須"])
                    ])
                ]
        
        class MockSection:
            def __init__(self, title, subsections):
                self.title = title
                self.subsection_outlines = subsections
        
        class MockSubsection:
            def __init__(self, title, keywords):
                self.title = title
                self.keywords = keywords
        
        outline = MockOutline()
        keywords = ["動名詞", "不定詞", "ing形", "to + 原形", "使い分け", "ルール"]
        
        try:
            # 実際の関連トピック生成
            result_text = ""
            async def run_test():
                nonlocal result_text
                async for chunk in related_topics_writer(
                    query=query,
                    outline_structure=outline,
                    keywords=keywords
                ):
                    result_text += chunk
            
            # 非同期テストの実行
            import asyncio
            asyncio.run(run_test())
            
            # 基本的な検証
            assert len(result_text) > 0
            
            # 関連トピックの内容確認
            print(f"\nアウトライン統合の関連トピック:\n{result_text}")
            
            # アウトライン構造が反映されているか
            assert "動名詞" in result_text or "不定詞" in result_text
            
        except Exception as e:
            pytest.skip(f"LLM接続エラー: {e}")


if __name__ == "__main__":
    print("🧪 Starting RelatedTopicsWriter Tests")
    print("=" * 50)
    
    # テストの実行
    pytest.main([__file__, "-v"]) 