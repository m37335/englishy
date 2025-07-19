import dspy
import litellm
from typing import List, Dict, Any
from .grammar_utils import extract_grammar_labels, translate_to_english_grammar


class GenerateSearchTopics(dspy.Signature):
    """You are an expert in English learning and language education with deep knowledge of international research and methodologies.
    Your task is to generate optimized search topics for web search to find comprehensive English learning materials.
    
    Based on the query and detected grammar structures, create search topics that will effectively retrieve:
    1. Grammar-related educational content
    2. Teaching methodologies and best practices
    3. Research-based learning materials
    4. Practical exercises and examples

    Output format:
    - xxx
    - yyy
    - ...
    - zzz

    Guidelines:
    - Focus on web search optimization (short, specific phrases)
    - Include grammar-specific terms when detected
    - Prioritize educational and research content
    - Make topics self-contained and non-overlapping
    - Limit to maximum 8 topics
    - Use English only for all topics
    """  # noqa: E501

    query = dspy.InputField(desc="User query", format=str)
    grammar_structures = dspy.InputField(desc="Detected grammar structures", format=str)
    topics = dspy.OutputField(desc="Optimized search topics for web search", format=str)


def cleanse_topic(topic: str) -> str:
    """Clean and format a single topic."""
    if topic.startswith("- "):
        topic = topic[2:].strip()
    if topic.startswith('"') and topic.endswith('"'):
        topic = topic[1:-1].strip()
    return topic.strip()


def remove_duplicates(topics: List[str]) -> List[str]:
    """Remove duplicate topics while preserving order."""
    seen = set()
    unique_topics = []
    
    for topic in topics:
        topic_lower = topic.lower().strip()
        if topic_lower not in seen:
            unique_topics.append(topic)
            seen.add(topic_lower)
    
    return unique_topics


def prioritize_topics(topics: List[str]) -> List[str]:
    """Prioritize topics based on educational value and search effectiveness."""
    priority_keywords = [
        'teaching', 'methodology', 'research', 'international', 'advanced',
        'grammar', 'education', 'learning', 'practice', 'exercises'
    ]
    
    priority_topics = []
    secondary_topics = []
    
    for topic in topics:
        # Check if topic contains priority keywords
        if any(keyword in topic.lower() for keyword in priority_keywords):
            priority_topics.append(topic)
        else:
            secondary_topics.append(topic)
    
    # Return prioritized list, limiting to 8 topics
    result = priority_topics + secondary_topics
    return result[:8]


class QueryExpander(dspy.Module):
    """Optimized QueryExpander for web search topic generation."""
    
    def __init__(self, lm):
        self.generate_search_topics = dspy.Predict(GenerateSearchTopics)
        self.lm = lm

    def forward(self, query: str, web_search_results: str = "") -> dspy.Prediction:
        """Generate optimized search topics for web search.
        
        Args:
            query: User's original query
            web_search_results: Web search results (optional, for future enhancement)
            
        Returns:
            dspy.Prediction with topics list
        """
        with dspy.settings.context(lm=self.lm):
            # Extract grammar structures from query using grammar_utils
            grammar_labels = extract_grammar_labels(query)
            grammar_structures = ", ".join(grammar_labels) if grammar_labels else "general English"
            
            # Generate search topics using DSPy
            result = self.generate_search_topics(
                query=query,
                grammar_structures=grammar_structures
            )
            
            # Parse and clean topics
            raw_topics = [cleanse_topic(topic) for topic in result.topics.split("\n")]
            raw_topics = [topic for topic in raw_topics if topic]
            
            # Remove duplicates and prioritize
            unique_topics = remove_duplicates(raw_topics)
            final_topics = prioritize_topics(unique_topics)
            
        return dspy.Prediction(topics=final_topics) 