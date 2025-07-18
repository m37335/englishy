# 文法項目の日本語→英語変換辞書
# 今後拡張・メンテナンスしやすい形で定義

grammar_en_map = {
    "仮定法過去": "subjunctive mood",
    "受動態": "passive voice",
    "受け身": "passive voice",
    "比較級": "comparative",
    "最上級": "superlative",
    "関係代名詞": "relative pronoun",
    "不定詞の名詞的用法": "infinitive (noun use)",
    "分詞の形容詞的用法": "participle (adjective use)",
    "三単現": "third person singular",
    "There is are": "there is/are construction",
    "命令文": "imperative sentence",
    "感嘆文": "exclamatory sentence",
    "現在完了進行形": "present perfect continuous",
    # ... 必要に応じて追加 ...
}


def extract_grammar_labels(text: str) -> list:
    """
    入力テキストからgrammar_en_mapに基づき主要文法項目（英語ラベル）を抽出する。
    日本語・英語混在にも対応。
    """
    labels = set()
    # まず日本語→英語変換
    for jp, en in sorted(grammar_en_map.items(), key=lambda x: -len(x[0])):
        if jp in text:
            labels.add(en)
    # 既に英語で含まれている場合も検出
    for en in grammar_en_map.values():
        if en in text:
            labels.add(en)
    return list(labels)


def translate_to_english_grammar(text: str) -> str:
    """
    入力テキストが日本語文法語の場合、対応する英語ラベルを返す（複数マッチ時はスペース区切り）。
    """
    labels = set()
    # 日本語→英語変換
    for jp, en in sorted(grammar_en_map.items(), key=lambda x: -len(x[0])):
        if jp in text:
            labels.add(en)
    # 英語がそのまま入っている場合も検出
    for en in grammar_en_map.values():
        if en in text:
            labels.add(en)
    
    if labels:
        return " ".join(sorted(labels))  # 複数マッチ時はスペース区切りで返す
    return text  # 変換できなければそのまま返す 