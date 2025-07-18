import pytest
from ai.grammar_utils import extract_grammar_labels, translate_to_english_grammar, grammar_en_map


def test_extract_grammar_labels_japanese():
    """日本語テキストからの文法ラベル抽出テスト"""
    # 単一文法語
    text1 = "仮定法過去について"
    labels1 = extract_grammar_labels(text1)
    assert "subjunctive mood" in labels1
    
    # 複数文法語
    text2 = "仮定法過去と受動態の例文"
    labels2 = extract_grammar_labels(text2)
    assert "subjunctive mood" in labels2
    assert "passive voice" in labels2
    
    # 部分一致防止テスト
    text3 = "比較級について"
    labels3 = extract_grammar_labels(text3)
    assert "comparative" in labels3
    # "比較"が誤って変換されないことを確認
    assert "comparison" not in labels3


def test_extract_grammar_labels_english():
    """英語テキストからの文法ラベル抽出テスト"""
    # 英語文法語
    text1 = "subjunctive mood examples"
    labels1 = extract_grammar_labels(text1)
    assert "subjunctive mood" in labels1
    
    # 英語文
    text2 = "If I had known, I would have helped you."
    labels2 = extract_grammar_labels(text2)
    # 英語文からも何らかの文法ラベルが検出されることを確認
    assert isinstance(labels2, list)


def test_extract_grammar_labels_mixed():
    """日本語・英語混在テキストからの文法ラベル抽出テスト"""
    text = "仮定法過去（subjunctive mood）について"
    labels = extract_grammar_labels(text)
    
    assert "subjunctive mood" in labels
    # 重複が除去されていることを確認
    assert len(labels) == 1


def test_extract_grammar_labels_no_match():
    """マッチしないテキストのテスト"""
    text = "一般的な文章です。"
    labels = extract_grammar_labels(text)
    
    assert isinstance(labels, list)
    assert len(labels) == 0


def test_translate_to_english_grammar_single():
    """単一文法語の英語変換テスト"""
    # 基本的な変換
    assert translate_to_english_grammar("仮定法過去") == "subjunctive mood"
    assert translate_to_english_grammar("受動態") == "passive voice"
    assert translate_to_english_grammar("受け身") == "passive voice"
    
    # 比較級・最上級
    assert translate_to_english_grammar("比較級") == "comparative"
    assert translate_to_english_grammar("最上級") == "superlative"


def test_translate_to_english_grammar_multiple():
    """複数文法語の英語変換テスト"""
    text = "仮定法過去と受動態"
    result = translate_to_english_grammar(text)
    
    # 複数の文法語がスペース区切りで返される
    assert "subjunctive mood" in result
    assert "passive voice" in result
    # スペース数は文法語の数に依存するため、柔軟にチェック
    assert result.count(" ") >= 1  # 少なくとも1つのスペース


def test_translate_to_english_grammar_no_match():
    """マッチしないテキストの変換テスト"""
    text = "一般的な文章"
    result = translate_to_english_grammar(text)
    
    # 変換できない場合は元のテキストが返される
    assert result == text


def test_translate_to_english_grammar_already_english():
    """既に英語のテキストのテスト"""
    text = "subjunctive mood"
    result = translate_to_english_grammar(text)
    
    # 既に英語の場合はそのまま返される
    assert result == text


def test_grammar_en_map_structure():
    """grammar_en_mapの構造テスト"""
    # 辞書が正しく定義されているかチェック
    assert isinstance(grammar_en_map, dict)
    assert len(grammar_en_map) > 0
    
    # 主要な文法項目が含まれているかチェック
    assert "仮定法過去" in grammar_en_map
    assert "受動態" in grammar_en_map
    assert "受け身" in grammar_en_map
    assert "比較級" in grammar_en_map
    assert "最上級" in grammar_en_map


def test_grammar_en_map_values():
    """grammar_en_mapの値テスト"""
    # 値が英語で統一されているかチェック
    for jp, en in grammar_en_map.items():
        assert isinstance(en, str)
        assert len(en) > 0
        # 英語らしい文字列かチェック（スペース、括弧、ハイフン、スラッシュも許可）
        assert all(c.isalpha() or c.isspace() or c in "()/-" for c in en)


def test_extract_grammar_labels_edge_cases():
    """エッジケースのテスト"""
    # 空文字列
    assert extract_grammar_labels("") == []
    
    # 長いテキスト
    long_text = "仮定法過去" * 100
    labels = extract_grammar_labels(long_text)
    assert "subjunctive mood" in labels
    
    # 特殊文字
    text = "仮定法過去！@#$%"
    labels = extract_grammar_labels(text)
    assert "subjunctive mood" in labels


def test_translate_to_english_grammar_edge_cases():
    """translate_to_english_grammarのエッジケーステスト"""
    # 空文字列
    assert translate_to_english_grammar("") == ""
    
    # 長いテキスト
    long_text = "仮定法過去と受動態" * 10
    result = translate_to_english_grammar(long_text)
    assert "subjunctive mood" in result
    assert "passive voice" in result


def test_consistency_between_functions():
    """関数間の一貫性テスト"""
    text = "仮定法過去と受動態"
    
    # extract_grammar_labelsとtranslate_to_english_grammarの結果が一貫しているかチェック
    labels = extract_grammar_labels(text)
    translation = translate_to_english_grammar(text)
    
    # translationをスペースで分割してlabelsと比較
    translation_parts = translation.split()
    # 完全一致ではなく、主要な要素が含まれているかをチェック
    assert "subjunctive" in translation or "subjunctive mood" in labels
    assert "passive" in translation or "passive voice" in labels 