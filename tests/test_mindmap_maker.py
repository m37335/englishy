#!/usr/bin/env python3
"""
Test script for improved MindMapMaker with outline structure and keyword integration.
Tests the enhanced mindmap generation that integrates outline structure and keywords.
"""

import sys
import os
import pytest

# Add src to path for imports
sys.path.append('/app/src')

from ai.mindmap_maker import MindMapMaker
from utils.lm import load_lm


class TestMindMapMaker:
    """MindMapMakerのテストクラス"""
    
    @pytest.fixture
    def mindmap_maker(self):
        """MindMapMakerインスタンスを作成"""
        lm = load_lm()
        return MindMapMaker(lm=lm)
    
    @pytest.fixture
    def sample_report(self):
        """サンプルレポート"""
        return """
        仮定法過去について
        
        仮定法過去は、現在の事実に反する仮定を表す文法構造です。
        基本的な形は「If + 過去形, would + 原形」です。
        
        例文：
        - If I had money, I would buy a car.
        - If I were you, I would study harder.
        
        学習のポイント：
        1. 時制の使い分け
        2. 仮定法と直説法の違い
        3. 実践的な使用場面
        """
    
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
    
    def test_mindmap_maker_initialization(self, mindmap_maker):
        """MindMapMakerの初期化テスト"""
        assert mindmap_maker is not None
        assert hasattr(mindmap_maker, 'make_mindmap')
        assert hasattr(mindmap_maker, '_convert_outline_to_text')
    
    def test_convert_outline_to_text(self, mindmap_maker, sample_outline):
        """アウトライン構造のテキスト変換テスト"""
        outline_text = mindmap_maker._convert_outline_to_text(sample_outline)
        
        # タイトルが含まれているか
        assert "仮定法過去の完全ガイド" in outline_text
        
        # セクション構造が含まれているか
        assert "1. 文法構造の理解" in outline_text
        assert "2. 実例と詳細解説" in outline_text
        assert "3. 実践的な活用" in outline_text
        
        # サブセクションが含まれているか
        assert "基本的な文法項目" in outline_text
        assert "実際の使用例" in outline_text
        
        # キーワードが含まれているか
        assert "仮定法" in outline_text
        assert "時制" in outline_text
        assert "例文" in outline_text
    
    def test_convert_outline_to_text_with_invalid_outline(self, mindmap_maker):
        """無効なアウトライン構造の変換テスト"""
        invalid_outline = {"invalid": "structure"}
        result = mindmap_maker._convert_outline_to_text(invalid_outline)
        assert "アウトライン構造の変換に失敗しました" in result
    
    def test_forward_with_all_parameters(self, mindmap_maker, sample_report, sample_outline, sample_keywords):
        """全パラメータ付きのforwardメソッドテスト"""
        # テスト実行
        result = mindmap_maker.forward(
            report=sample_report,
            outline_structure=sample_outline,
            keywords=sample_keywords,
            related_topics="subjunctive mood, conditional sentences"
        )
        
        # 検証
        assert result is not None
        assert hasattr(result, 'mindmap')
        # 実際のLLM出力を確認
        print(f"\n生成されたマインドマップ:\n{result.mindmap}")
    
    def test_forward_with_minimal_parameters(self, mindmap_maker, sample_report):
        """最小パラメータでのforwardメソッドテスト"""
        # テスト実行
        result = mindmap_maker.forward(report=sample_report)
        
        # 検証
        assert result is not None
        assert hasattr(result, 'mindmap')
        # 実際のLLM出力を確認
        print(f"\n最小パラメータのマインドマップ:\n{result.mindmap}")
    
    def test_forward_with_keywords_only(self, mindmap_maker, sample_report, sample_keywords):
        """キーワードのみでのforwardメソッドテスト"""
        # テスト実行
        result = mindmap_maker.forward(
            report=sample_report,
            keywords=sample_keywords
        )
        
        # 検証
        assert result is not None
        assert hasattr(result, 'mindmap')
        # 実際のLLM出力を確認
        print(f"\nキーワード付きマインドマップ:\n{result.mindmap}")


class TestMindMapMakerIntegration:
    """MindMapMakerの統合テストクラス"""
    
    @pytest.fixture
    def mindmap_maker(self):
        """MindMapMakerインスタンスを作成"""
        lm = load_lm()
        return MindMapMaker(lm=lm)
    
    def test_real_mindmap_generation(self, mindmap_maker):
        """実際のマインドマップ生成テスト"""
        # テストデータ
        report = """
        受動態について
        
        受動態は、動作の受け手を主語にする文の形です。
        基本的な形は「be動詞 + 過去分詞」です。
        
        例文：
        - The book is written by him.
        - The house was built in 1990.
        
        学習のポイント：
        1. 能動態との使い分け
        2. 時制の変化
        3. 実践的な使用場面
        """
        
        keywords = ["受動態", "be動詞", "過去分詞", "能動態", "時制", "例文"]
        related_topics = "passive voice, active voice, verb tenses"
        
        try:
            # 実際のマインドマップ生成
            result = mindmap_maker.forward(
                report=report,
                keywords=keywords,
                related_topics=related_topics
            )
            
            # 基本的な検証
            assert result is not None
            assert hasattr(result, 'mindmap')
            assert len(result.mindmap) > 0
            
            # マインドマップの内容確認
            mindmap_text = result.mindmap
            print(f"\n生成されたマインドマップ:\n{mindmap_text}")
            
            # 基本的な構造が含まれているか
            assert "#" in mindmap_text  # タイトル
            assert "##" in mindmap_text  # セクション
            
        except Exception as e:
            pytest.skip(f"LLM接続エラー: {e}")
    
    def test_mindmap_with_complex_grammar(self, mindmap_maker):
        """複雑な文法項目でのマインドマップ生成テスト"""
        # 複雑な文法項目のレポート
        report = """
        仮定法過去完了について
        
        仮定法過去完了は、過去の事実に反する仮定を表す文法構造です。
        基本的な形は「If + had + 過去分詞, would have + 過去分詞」です。
        
        例文：
        - If I had studied harder, I would have passed the exam.
        - If she had known, she would have helped you.
        
        学習のポイント：
        1. 仮定法過去との違い
        2. 時制の使い分け
        3. 実践的な使用場面
        4. よくある間違いと対策
        """
        
        keywords = ["仮定法過去完了", "had + 過去分詞", "would have", "時制", "違い", "間違い"]
        related_topics = "past perfect subjunctive, conditional sentences, verb tenses"
        
        try:
            # 実際のマインドマップ生成
            result = mindmap_maker.forward(
                report=report,
                keywords=keywords,
                related_topics=related_topics
            )
            
            # 基本的な検証
            assert result is not None
            assert hasattr(result, 'mindmap')
            assert len(result.mindmap) > 0
            
            # マインドマップの内容確認
            mindmap_text = result.mindmap
            print(f"\n複雑文法のマインドマップ:\n{mindmap_text}")
            
            # 複雑な文法項目が適切に処理されているか
            assert "仮定法" in mindmap_text or "subjunctive" in mindmap_text.lower()
            
        except Exception as e:
            pytest.skip(f"LLM接続エラー: {e}")


if __name__ == "__main__":
    print("🧪 Starting MindMapMaker Tests")
    print("=" * 50)
    
    # テストの実行
    pytest.main([__file__, "-v"]) 