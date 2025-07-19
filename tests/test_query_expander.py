"""
Test cases for improved QueryExpander module.
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai.query_expander import QueryExpander, cleanse_topic, remove_duplicates, prioritize_topics


class TestQueryExpander:
    """Test cases for QueryExpander class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_lm = Mock()
        self.expander = QueryExpander(lm=self.mock_lm)
    
    def test_cleanse_topic(self):
        """Test topic cleansing functionality."""
        # Test with dash prefix
        assert cleanse_topic("- subjunctive mood teaching") == "subjunctive mood teaching"
        
        # Test with quotes
        assert cleanse_topic('"passive voice exercises"') == "passive voice exercises"
        
        # Test with extra whitespace
        assert cleanse_topic("  grammar practice  ") == "grammar practice"
        
        # Test normal topic
        assert cleanse_topic("English learning methods") == "English learning methods"
    
    def test_remove_duplicates(self):
        """Test duplicate removal functionality."""
        topics = [
            "subjunctive mood",
            "Subjunctive Mood",  # Case variation
            "passive voice",
            "subjunctive mood",  # Exact duplicate
            "grammar practice"
        ]
        
        result = remove_duplicates(topics)
        expected = ["subjunctive mood", "passive voice", "grammar practice"]
        
        assert result == expected
        assert len(result) == 3
    
    def test_prioritize_topics(self):
        """Test topic prioritization functionality."""
        topics = [
            "general English",
            "teaching methodology",
            "grammar practice",
            "basic vocabulary",
            "research findings",
            "simple exercises"
        ]
        
        result = prioritize_topics(topics)
        
        # Priority topics should come first
        assert "teaching methodology" in result[:3]
        assert "grammar practice" in result[:3]
        assert "research findings" in result[:3]
        
        # Should limit to 8 topics
        assert len(result) <= 8
    
    def test_prioritize_topics_with_many_topics(self):
        """Test topic prioritization with more than 8 topics."""
        topics = [
            "topic1", "topic2", "topic3", "topic4", "topic5",
            "topic6", "topic7", "topic8", "topic9", "topic10"
        ]
        
        result = prioritize_topics(topics)
        
        # Should limit to 8 topics
        assert len(result) == 8
    
    def test_prioritize_topics_with_priority_keywords(self):
        """Test topic prioritization with priority keywords."""
        topics = [
            "basic English",
            "advanced teaching methodology",
            "simple grammar",
            "research-based learning",
            "basic practice"
        ]
        
        result = prioritize_topics(topics)
        
        # Priority topics should come first
        priority_topics = ["advanced teaching methodology", "research-based learning"]
        for topic in priority_topics:
            assert topic in result[:3]


class TestQueryExpanderIntegration:
    """Integration tests for QueryExpander."""
    
    def test_end_to_end_topic_generation(self):
        """Test end-to-end topic generation process."""
        # This test would require actual LM integration
        # For now, we'll test the component functions
        topics = [
            "subjunctive mood teaching",
            "Subjunctive Mood Teaching",  # Duplicate
            "passive voice exercises",
            "basic grammar",
            "advanced teaching methodology",
            "simple practice"
        ]
        
        # Test the full pipeline
        cleaned = [cleanse_topic(topic) for topic in topics]
        unique = remove_duplicates(cleaned)
        prioritized = prioritize_topics(unique)
        
        # Verify results
        assert len(prioritized) <= 8
        assert "subjunctive mood teaching" in prioritized
        assert "passive voice exercises" in prioritized
        assert "advanced teaching methodology" in prioritized
        
        # Verify no duplicates
        assert len(prioritized) == len(set(prioritized))
    
    def test_grammar_utils_integration(self):
        """Test integration with grammar_utils functions."""
        from ai.grammar_utils import extract_grammar_labels, translate_to_english_grammar
        
        # Test grammar extraction
        query = "仮定法過去について"
        grammar_labels = extract_grammar_labels(query)
        assert isinstance(grammar_labels, list)
        
        # Test translation
        translated = translate_to_english_grammar(query)
        assert isinstance(translated, str)
        assert "subjunctive" in translated.lower()


if __name__ == "__main__":
    pytest.main([__file__]) 