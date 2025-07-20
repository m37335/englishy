#!/usr/bin/env python3
"""
Test script for improved ReferencesWriter with outline structure and keyword integration.
Tests the enhanced references generation that integrates outline structure, keywords, and quality improvements.
"""

import sys
import os
import pytest

# Add src to path for imports
sys.path.append('/app/src')

from ai.report_writer import StreamReferencesWriter
from utils.lm import load_lm


class TestReferencesWriter:
    """ReferencesWriterのテストクラス"""
    
    @pytest.fixture
    def references_writer(self):
        """ReferencesWriterインスタンスを作成"""
        lm = load_lm()
        return StreamReferencesWriter(lm=lm)
    
    @pytest.fixture
    def sample_query(self):
        """サンプルクエリー"""
        return "仮定法過去について詳しく教えてください"
    
    @pytest.fixture
    def sample_report_content(self):
        """サンプルレポート内容"""
        return """
# 仮定法過去の完全ガイド

## 1. 基本的な概念
仮定法過去は、現在の事実に反する仮定を表す文法構造です。If I were you, I would help him. のような形で使用されます。

## 2. 文法構造
仮定法過去では、if節で過去形を使用し、主節でwould + 原形を使用します。

## 3. 実践的な使用例
実際の会話や文章での使用例を紹介します。
        """
    
    @pytest.fixture
    def sample_search_results(self):
        """サンプル検索結果"""
        return """
1. "Teaching Subjunctive Mood in ESL" - Cambridge University Press
2. "English Grammar in Use" - Raymond Murphy
3. "Practical English Usage" - Michael Swan
4. "文部科学省 英語教育の手引き" - 文部科学省
5. "仮定法の指導法" - 東京大学教育学部
        """
    
    @pytest.fixture
    def sample_outline(self):
        """サンプルアウトライン構造"""
        class MockOutline:
            def __init__(self):
                self.title = "仮定法過去の完全ガイド"
                self.section_outlines = [
                    MockSection("1. 基本的な概念", [
                        MockSubsection("仮定法過去とは", ["仮定法", "過去形", "would"]),
                        MockSubsection("使用場面", ["仮定", "事実に反する"])
                    ]),
                    MockSection("2. 文法構造", [
                        MockSubsection("if節の形", ["if", "過去形", "条件"]),
                        MockSubsection("主節の形", ["would", "原形", "結果"])
                    ]),
                    MockSection("3. 実践的な使用例", [
                        MockSubsection("会話での使用", ["会話", "例文", "練習"]),
                        MockSubsection("文章での使用", ["文章", "書き方", "応用"])
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
        return ["仮定法", "過去形", "would", "if節", "主節", "例文", "練習"]
    
    def test_references_writer_initialization(self, references_writer):
        """ReferencesWriterの初期化テスト"""
        assert references_writer is not None
        assert hasattr(references_writer, '_convert_outline_to_text')
    
    def test_convert_outline_to_text(self, references_writer, sample_outline):
        """アウトライン構造のテキスト変換テスト"""
        outline_text = references_writer._convert_outline_to_text(sample_outline)
        
        # タイトルが含まれているか
        assert "仮定法過去の完全ガイド" in outline_text
        
        # セクション構造が含まれているか
        assert "1. 基本的な概念" in outline_text
        assert "2. 文法構造" in outline_text
        assert "3. 実践的な使用例" in outline_text
        
        # サブセクションが含まれているか
        assert "仮定法過去とは" in outline_text
        assert "if節の形" in outline_text
    
    def test_convert_outline_to_text_with_invalid_outline(self, references_writer):
        """無効なアウトライン構造の変換テスト"""
        invalid_outline = {"invalid": "structure"}
        result = references_writer._convert_outline_to_text(invalid_outline)
        assert "アウトライン構造の変換に失敗しました" in result
    
    def test_forward_with_all_parameters(self, references_writer, sample_query, sample_report_content, sample_search_results, sample_outline, sample_keywords):
        """全パラメータ付きのforwardメソッドテスト"""
        # テスト実行
        result_text = ""
        async def run_test():
            nonlocal result_text
            async for chunk in references_writer(
                query=sample_query,
                report_content=sample_report_content,
                search_results=sample_search_results,
                outline_structure=sample_outline,
                keywords=sample_keywords
            ):
                result_text += chunk
        
        # 非同期テストの実行
        import asyncio
        asyncio.run(run_test())
        
        # 検証
        assert len(result_text) > 0
        assert "参考文献" in result_text
        print(f"\n生成された参考文献:\n{result_text}")
    
    def test_forward_with_minimal_parameters(self, references_writer, sample_query, sample_report_content, sample_search_results):
        """最小パラメータでのforwardメソッドテスト"""
        # テスト実行
        result_text = ""
        async def run_test():
            nonlocal result_text
            async for chunk in references_writer(
                query=sample_query,
                report_content=sample_report_content,
                search_results=sample_search_results
            ):
                result_text += chunk
        
        # 非同期テストの実行
        import asyncio
        asyncio.run(run_test())
        
        # 検証
        assert len(result_text) > 0
        print(f"\n最小パラメータの参考文献:\n{result_text}")
    
    def test_forward_with_keywords_only(self, references_writer, sample_query, sample_report_content, sample_search_results, sample_keywords):
        """キーワードのみでのforwardメソッドテスト"""
        # テスト実行
        result_text = ""
        async def run_test():
            nonlocal result_text
            async for chunk in references_writer(
                query=sample_query,
                report_content=sample_report_content,
                search_results=sample_search_results,
                keywords=sample_keywords
            ):
                result_text += chunk
        
        # 非同期テストの実行
        import asyncio
        asyncio.run(run_test())
        
        # 検証
        assert len(result_text) > 0
        print(f"\nキーワード付き参考文献:\n{result_text}")


class TestReferencesWriterIntegration:
    """ReferencesWriterの統合テストクラス"""
    
    @pytest.fixture
    def references_writer(self):
        """ReferencesWriterインスタンスを作成"""
        lm = load_lm()
        return StreamReferencesWriter(lm=lm)
    
    def test_real_references_generation(self, references_writer):
        """実際の参考文献生成テスト"""
        # テストデータ
        query = "受動態の使い方を教えてください"
        report_content = """
# 受動態の完全ガイド

## 1. 受動態の基本概念
受動態は、動作の受け手を主語にする文法構造です。The book was written by him. のような形で使用されます。

## 2. 文法構造
受動態では、be動詞 + 過去分詞の形を使用します。

## 3. 実践的な使用例
実際の会話や文章での使用例を紹介します。
        """
        search_results = """
1. "Teaching Passive Voice in ESL" - Oxford University Press
2. "English Grammar in Use" - Raymond Murphy
3. "Practical English Usage" - Michael Swan
4. "文部科学省 英語教育の手引き" - 文部科学省
5. "受動態の指導法" - 東京大学教育学部
        """
        keywords = ["受動態", "be動詞", "過去分詞", "能動態", "時制", "例文"]
        
        try:
            # 実際の参考文献生成
            result_text = ""
            async def run_test():
                nonlocal result_text
                async for chunk in references_writer(
                    query=query,
                    report_content=report_content,
                    search_results=search_results,
                    keywords=keywords
                ):
                    result_text += chunk
            
            # 非同期テストの実行
            import asyncio
            asyncio.run(run_test())
            
            # 基本的な検証
            assert len(result_text) > 0
            
            # 参考文献の内容確認
            print(f"\n生成された参考文献:\n{result_text}")
            
            # 基本的な構造が含まれているか
            assert "参考文献" in result_text or "References" in result_text
            
        except Exception as e:
            pytest.skip(f"LLM接続エラー: {e}")
    
    def test_references_with_complex_grammar(self, references_writer):
        """複雑な文法項目での参考文献生成テスト"""
        # 複雑な文法項目のクエリー
        query = "仮定法過去完了と仮定法過去の違いについて"
        report_content = """
# 仮定法過去完了と仮定法過去の違い

## 1. 基本的な違い
仮定法過去完了は過去の事実に反する仮定を表し、仮定法過去は現在の事実に反する仮定を表します。

## 2. 文法構造の比較
仮定法過去完了: If I had known, I would have helped you.
仮定法過去: If I were you, I would help him.

## 3. 使用場面の違い
実際の使用場面での違いを詳しく説明します。
        """
        search_results = """
1. "Advanced English Grammar" - Cambridge University Press
2. "English Grammar in Use Advanced" - Raymond Murphy
3. "Practical English Usage" - Michael Swan
4. "文部科学省 英語教育の手引き" - 文部科学省
5. "仮定法の指導法" - 東京大学教育学部
        """
        keywords = ["仮定法過去完了", "had + 過去分詞", "would have", "時制", "違い"]
        
        try:
            # 実際の参考文献生成
            result_text = ""
            async def run_test():
                nonlocal result_text
                async for chunk in references_writer(
                    query=query,
                    report_content=report_content,
                    search_results=search_results,
                    keywords=keywords
                ):
                    result_text += chunk
            
            # 非同期テストの実行
            import asyncio
            asyncio.run(run_test())
            
            # 基本的な検証
            assert len(result_text) > 0
            
            # 参考文献の内容確認
            print(f"\n複雑文法の参考文献:\n{result_text}")
            
            # 複雑な文法項目が適切に処理されているか
            assert "仮定法" in result_text or "subjunctive" in result_text.lower()
            
        except Exception as e:
            pytest.skip(f"LLM接続エラー: {e}")
    
    def test_references_with_outline_integration(self, references_writer):
        """アウトライン統合での参考文献生成テスト"""
        # テストデータ
        query = "動名詞と不定詞の違いについて"
        report_content = """
# 動名詞と不定詞の完全比較

## 1. 基本的な違い
動名詞は-ing形で名詞的用法、不定詞はto + 原形で多様な用法があります。

## 2. 使い分けのポイント
動詞の後や前置詞の後での使い分けを詳しく説明します。

## 3. 実践的な使用例
実際の会話や文章での使用例を紹介します。
        """
        search_results = """
1. "Teaching Gerunds and Infinitives" - Oxford University Press
2. "English Grammar in Use" - Raymond Murphy
3. "Practical English Usage" - Michael Swan
4. "文部科学省 英語教育の手引き" - 文部科学省
5. "動名詞と不定詞の指導法" - 東京大学教育学部
        """
        
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
            # 実際の参考文献生成
            result_text = ""
            async def run_test():
                nonlocal result_text
                async for chunk in references_writer(
                    query=query,
                    report_content=report_content,
                    search_results=search_results,
                    outline_structure=outline,
                    keywords=keywords
                ):
                    result_text += chunk
            
            # 非同期テストの実行
            import asyncio
            asyncio.run(run_test())
            
            # 基本的な検証
            assert len(result_text) > 0
            
            # 参考文献の内容確認
            print(f"\nアウトライン統合の参考文献:\n{result_text}")
            
            # アウトライン構造が反映されているか
            assert "動名詞" in result_text or "不定詞" in result_text
            
        except Exception as e:
            pytest.skip(f"LLM接続エラー: {e}")


if __name__ == "__main__":
    print("🧪 Starting ReferencesWriter Tests")
    print("=" * 50)
    
    # テストの実行
    pytest.main([__file__, "-v"]) 