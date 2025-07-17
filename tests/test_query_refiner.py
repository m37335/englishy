import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from ai.query_refiner import GrammarAwareQueryRefiner
import pytest

@pytest.fixture
def refiner():
    return GrammarAwareQueryRefiner(lm=None)

def test_translate_to_english(refiner):
    cases = [
        ("仮定法過去", "subjunctive mood"),
        ("受動態", "passive voice"),
        ("受け身", "passive voice"),
        ("現在完了進行形", "present perfect continuous"),
        ("比較級", "comparative"),
        ("最上級", "superlative"),
        ("関係代名詞", "relative pronoun"),
        ("不定詞の名詞的用法", "infinitive (noun use)"),
        ("分詞の形容詞的用法", "participle (adjective use)"),
        ("三単現", "third person singular"),
        ("There is are", "there is/are construction"),
        ("命令文", "imperative sentence"),
        ("感嘆文", "exclamatory sentence"),
    ]
    for jp, expected in cases:
        result = refiner._translate_to_english(jp)
        assert expected in result, f"{jp} → {result} (expected: {expected})"

def test_translate_mixed_sentence(refiner):
    jp = "これは仮定法過去と受動態の例です。"
    result = refiner._translate_to_english(jp)
    assert "subjunctive mood" in result
    assert "passive voice" in result 