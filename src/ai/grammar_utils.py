import re
from typing import List

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

# 英語文から文法構造を検出するパターン
english_grammar_patterns = {
    "subjunctive mood": [
        r'\bif\b.*\b(would|could|should|might)\b',
        r'\b(were|had)\b.*\bif\b',
        r'\b(wish|hope)\b.*\b(were|had)\b'
    ],
    "passive voice": [
        r'\b(am|is|are|was|were)\s+\w+ed\b',
        r'\b(has|have|had)\s+been\s+\w+ed\b'
    ],
    "present perfect": [
        r'\b(have|has)\s+\w+ed\b'
    ],
    "present perfect continuous": [
        r'\b(have|has)\s+been\s+\w+ing\b'
    ],
    "present continuous": [
        r'\b(am|is|are)\s+\w+ing\b'
    ],
    "past continuous": [
        r'\b(was|were)\s+\w+ing\b'
    ],
    "relative pronoun": [
        r'\b(who|which|that|whose)\b'
    ],
    "infinitive": [
        r'\bto\s+\w+\b'
    ],
    "gerund": [
        r'\b\w+ing\b'
    ],
    "modal verb": [
        r'\b(can|could|will|would|should|may|might|must)\b'
    ],
    "conditional": [
        r'\bif\b.*\b(will|would|can|could)\b'
    ]
}


def extract_grammar_labels(text: str) -> List[str]:
    """
    入力テキストから主要文法項目（英語ラベル）を抽出する。
    日本語・英語混在にも対応し、英語文からも自動検出。
    """
    labels = set()
    
    # 1. 日本語→英語変換
    for jp, en in sorted(grammar_en_map.items(), key=lambda x: -len(x[0])):
        if jp in text:
            labels.add(en)
    
    # 2. 既に英語で含まれている場合も検出
    for en in grammar_en_map.values():
        if en in text:
            labels.add(en)
    
    # 3. 英語文から文法構造を自動検出
    english_structures = _detect_english_grammar_structures(text)
    labels.update(english_structures)
    
    return list(labels)


def _detect_english_grammar_structures(text: str) -> List[str]:
    """
    英語文から文法構造を自動検出する
    """
    detected_structures = []
    
    # 各文法パターンをチェック
    for structure_name, patterns in english_grammar_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                detected_structures.append(structure_name)
                break  # この構造が見つかったら次の構造に進む
    
    return detected_structures


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