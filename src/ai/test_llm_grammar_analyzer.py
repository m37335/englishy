import os
import pytest
import llm_grammar_analyzer

@pytest.fixture(scope="module")
def analyzer():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set")
    return llm_grammar_analyzer.LLMGrammarAnalyzer(api_key=api_key)

def test_basic_grammar_analysis(analyzer):
    text = "If I had known, I would have helped you."
    result = analyzer.analyze_text(text)
    assert "grammar_structures" in result
    assert any("subjunctive" in s or "conditional" in s for s in result["grammar_structures"])
    assert "related_topics" in result
    assert isinstance(result["related_topics"], list)
    assert "key_points" in result
    assert isinstance(result["key_points"], list)
    print(result) 