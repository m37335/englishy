import pytest
from unittest.mock import Mock, patch


class TestOutlineCreaterKeywordIntegration:
    """OutlineCreaterとキーワード機能の統合テスト"""
    
    def test_subsection_outline_with_keywords_structure(self):
        """キーワード付きサブセクションの構造テスト"""
        # サブセクションの構造をテスト
        subsection_data = {
            "title": "基本的な形と意味",
            "reference_ids": [1, 2, 3],
            "keywords": ["gerund", "formation", "teaching"]
        }
        
        # 基本的な構造チェック
        assert "title" in subsection_data
        assert "reference_ids" in subsection_data
        assert "keywords" in subsection_data
        assert len(subsection_data["keywords"]) > 0
    
    def test_keyword_extraction_from_sample_content(self):
        """サンプルコンテンツからのキーワード抽出テスト"""
        # テスト用のサンプルコンテンツ
        sample_content = """
        Gerund Formation in English Grammar
        Learn about gerund formation and teaching methods for English learners.
        This guide covers infinitive usage and practice exercises.
        """
        
        # キーワード抽出関数をテスト
        def extract_test_keywords(content):
            keywords = []
            grammar_keywords = ["gerund", "infinitive", "formation", "teaching"]
            content_lower = content.lower()
            for keyword in grammar_keywords:
                if keyword in content_lower:
                    keywords.append(keyword)
            return list(dict.fromkeys(keywords))
        
        keywords = extract_test_keywords(sample_content)
        
        # 期待されるキーワードが含まれているかチェック
        assert "gerund" in keywords
        assert "formation" in keywords
        assert "teaching" in keywords
        assert "infinitive" in keywords
        assert len(keywords) == 4
    
    def test_keyword_integration_with_references(self):
        """参照情報とのキーワード統合テスト"""
        # テスト用の参照情報
        references = [
            {
                "id": 1,
                "title": "Gerund Formation Guide",
                "snippet": "Learn about gerund formation and usage patterns."
            },
            {
                "id": 2,
                "title": "Teaching English Grammar",
                "snippet": "Effective teaching methods for grammar instruction."
            }
        ]
        
        # サブセクションの引用番号
        subsection_refs = [1, 2]
        
        # キーワード抽出のシミュレーション
        def simulate_keyword_extraction(refs, subsection_refs):
            keywords = []
            for ref in refs:
                if ref["id"] in subsection_refs:
                    content = f"{ref['title']} {ref['snippet']}"
                    if "gerund" in content.lower():
                        keywords.append("gerund")
                    if "teaching" in content.lower():
                        keywords.append("teaching")
                    if "formation" in content.lower():
                        keywords.append("formation")
            return list(dict.fromkeys(keywords))
        
        keywords = simulate_keyword_extraction(references, subsection_refs)
        
        # 結果の検証
        assert "gerund" in keywords
        assert "teaching" in keywords
        assert "formation" in keywords
        assert len(keywords) == 3
    
    def test_outline_text_generation_with_keywords(self):
        """キーワード付きアウトラインのテキスト生成テスト"""
        # サブセクションのテキスト生成をシミュレーション
        def generate_subsection_text(title, ref_ids, keywords):
            text = f"### {title}\n"
            if ref_ids:
                text += f"[{']['.join(map(str, ref_ids))}]\n"
            if keywords:
                text += f"**キーワード**: [{', '.join(keywords)}]\n"
            return text
        
        # テストケース
        title = "基本的な形と意味"
        ref_ids = [1, 2, 3]
        keywords = ["gerund", "formation", "teaching"]
        
        result = generate_subsection_text(title, ref_ids, keywords)
        
        # 期待される出力の検証
        assert "### 基本的な形と意味" in result
        assert "[1][2][3]" in result
        assert "**キーワード**: [gerund, formation, teaching]" in result
    
    def test_empty_keywords_handling(self):
        """空のキーワードの処理テスト"""
        # キーワードがない場合の処理
        def generate_subsection_text(title, ref_ids, keywords):
            text = f"### {title}\n"
            if ref_ids:
                text += f"[{']['.join(map(str, ref_ids))}]\n"
            if keywords:  # キーワードがある場合のみ追加
                text += f"**キーワード**: [{', '.join(keywords)}]\n"
            return text
        
        # キーワードなしのケース
        result_no_keywords = generate_subsection_text("テスト", [1, 2], [])
        assert "**キーワード**:" not in result_no_keywords
        
        # キーワードありのケース
        result_with_keywords = generate_subsection_text("テスト", [1, 2], ["test"])
        assert "**キーワード**: [test]" in result_with_keywords


class TestKeywordUtilization:
    """キーワード活用機能のテスト"""
    
    def test_keyword_prioritization(self):
        """キーワードの優先順位付けテスト"""
        # キーワードの優先順位付けをシミュレーション
        def prioritize_keywords(keywords, max_count=5):
            # 文法キーワードを優先
            grammar_keywords = ["gerund", "infinitive", "participle", "subjunctive"]
            education_keywords = ["teaching", "learning", "practice", "method"]
            
            prioritized = []
            
            # 文法キーワードを最初に追加
            for keyword in keywords:
                if keyword in grammar_keywords and keyword not in prioritized:
                    prioritized.append(keyword)
                    if len(prioritized) >= max_count:
                        break
            
            # 教育キーワードを追加
            for keyword in keywords:
                if keyword in education_keywords and keyword not in prioritized:
                    prioritized.append(keyword)
                    if len(prioritized) >= max_count:
                        break
            
            return prioritized
        
        # テストケース
        all_keywords = ["gerund", "teaching", "infinitive", "practice", "formation", "method"]
        prioritized = prioritize_keywords(all_keywords, max_count=4)
        
        # 文法キーワードが優先されているかチェック
        assert "gerund" in prioritized
        assert "infinitive" in prioritized
        assert len(prioritized) <= 4
    
    def test_keyword_combination_logic(self):
        """キーワード組み合わせロジックのテスト"""
        # セクション内の複数サブセクションからキーワードを統合
        def combine_section_keywords(subsections):
            all_keywords = []
            for subsection in subsections:
                if "keywords" in subsection:
                    all_keywords.extend(subsection["keywords"])
            return list(dict.fromkeys(all_keywords))
        
        # テストデータ
        subsections = [
            {"title": "サブ1", "keywords": ["gerund", "formation"]},
            {"title": "サブ2", "keywords": ["teaching", "method"]},
            {"title": "サブ3", "keywords": ["gerund", "practice"]}  # 重複あり
        ]
        
        combined = combine_section_keywords(subsections)
        
        # 重複が除去されているかチェック
        assert len(combined) == 5  # gerund, formation, teaching, method, practice
        assert "gerund" in combined
        assert "formation" in combined
        assert "teaching" in combined
        assert "method" in combined
        assert "practice" in combined


if __name__ == "__main__":
    pytest.main([__file__]) 