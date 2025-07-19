import pytest


def extract_keywords_from_content(content: str) -> list[str]:
    """コンテンツからキーワードを抽出する"""
    keywords = []
    
    # 文法関連キーワード
    grammar_keywords = [
        "gerund", "infinitive", "participle", "subjunctive", "modal verb",
        "relative pronoun", "passive voice", "active voice", "present perfect",
        "past perfect", "future perfect", "conditional", "imperative", "interrogative",
        "動名詞", "不定詞", "分詞", "仮定法", "助動詞", "関係代名詞", "受動態", "能動態",
        "現在完了形", "過去完了形", "未来完了形", "条件法", "命令法", "疑問文"
    ]
    
    # 教育関連キーワード
    education_keywords = [
        "teaching", "learning", "education", "student", "practice", "exercise",
        "method", "approach", "technique", "strategy", "difficulty", "mistake",
        "指導", "学習", "教育", "生徒", "練習", "演習", "方法", "アプローチ",
        "テクニック", "戦略", "困難", "間違い", "理解", "応用"
    ]
    
    # コンテンツからキーワードを検索
    content_lower = content.lower()
    for keyword in grammar_keywords + education_keywords:
        if keyword.lower() in content_lower:
            keywords.append(keyword)
    
    # 重複を除去して上位10個まで返す
    unique_keywords = list(dict.fromkeys(keywords))[:10]
    return unique_keywords


def extract_keywords_from_references(references: list[dict], subsection_reference_ids: list[int]) -> list[str]:
    """参照情報からサブセクション用のキーワードを抽出"""
    keywords = []
    
    for ref in references:
        # サブセクションの引用番号と一致するかチェック
        ref_id = ref.get('id', 0)
        if ref_id in subsection_reference_ids:
            # タイトルとスニペットからキーワード抽出
            content = f"{ref.get('title', '')} {ref.get('snippet', '')}"
            ref_keywords = extract_keywords_from_content(content)
            keywords.extend(ref_keywords)
    
    # 重複を除去して上位5個まで返す
    unique_keywords = list(dict.fromkeys(keywords))[:5]
    return unique_keywords


class TestKeywordExtraction:
    """キーワード抽出機能のテスト"""
    
    def test_extract_keywords_from_content_grammar(self):
        """文法関連キーワードの抽出テスト"""
        content = "This article explains gerund formation and infinitive usage in English grammar."
        keywords = extract_keywords_from_content(content)
        
        assert "gerund" in keywords
        assert "infinitive" in keywords
        assert len(keywords) > 0
    
    def test_extract_keywords_from_content_education(self):
        """教育関連キーワードの抽出テスト"""
        content = "Teaching methods for learning English grammar with practice exercises."
        keywords = extract_keywords_from_content(content)
        
        assert "teaching" in keywords
        assert "learning" in keywords
        assert "practice" in keywords
        assert len(keywords) > 0
    
    def test_extract_keywords_from_content_japanese(self):
        """日本語キーワードの抽出テスト"""
        content = "動名詞の指導方法と不定詞との違いについて学習します。"
        keywords = extract_keywords_from_content(content)
        
        assert "動名詞" in keywords
        assert "不定詞" in keywords
        assert "指導" in keywords
        assert "学習" in keywords
    
    def test_extract_keywords_from_content_no_keywords(self):
        """キーワードが見つからない場合のテスト"""
        content = "This is a general article about weather and cooking."
        keywords = extract_keywords_from_content(content)
        
        assert len(keywords) == 0
    
    def test_extract_keywords_from_content_duplicate_removal(self):
        """重複キーワードの除去テスト"""
        content = "gerund gerund infinitive infinitive participle"
        keywords = extract_keywords_from_content(content)
        
        # 重複が除去されていることを確認
        assert len(keywords) == len(set(keywords))
        assert "gerund" in keywords
        assert "infinitive" in keywords
        assert "participle" in keywords


class TestKeywordExtractionFromReferences:
    """参照情報からのキーワード抽出テスト"""
    
    def test_extract_keywords_from_references_matching_ids(self):
        """引用番号が一致する場合のキーワード抽出"""
        subsection_reference_ids = [1, 2]
        
        references = [
            {
                "id": 1,
                "title": "Gerund Formation Guide",
                "snippet": "Learn about gerund formation and usage patterns."
            },
            {
                "id": 2,
                "title": "Teaching Gerunds",
                "snippet": "Effective teaching methods for gerund instruction."
            },
            {
                "id": 3,
                "title": "Unrelated Content",
                "snippet": "This content should not be included."
            }
        ]
        
        keywords = extract_keywords_from_references(references, subsection_reference_ids)
        
        # 主要なキーワードが含まれていることを確認
        assert "gerund" in keywords
        assert "teaching" in keywords
        # formation または method のいずれかが含まれていることを確認
        assert any(keyword in keywords for keyword in ["formation", "method"])
        assert len(keywords) <= 5  # 上位5個まで
    
    def test_extract_keywords_from_references_no_matching_ids(self):
        """引用番号が一致しない場合のテスト"""
        subsection_reference_ids = [1, 2]
        
        references = [
            {
                "id": 3,
                "title": "Unrelated Content",
                "snippet": "This content should not be included."
            }
        ]
        
        keywords = extract_keywords_from_references(references, subsection_reference_ids)
        
        assert len(keywords) == 0
    
    def test_extract_keywords_from_references_empty_references(self):
        """空の参照リストの場合のテスト"""
        subsection_reference_ids = [1, 2]
        
        keywords = extract_keywords_from_references([], subsection_reference_ids)
        
        assert len(keywords) == 0


if __name__ == "__main__":
    pytest.main([__file__]) 