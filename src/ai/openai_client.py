"""
OpenAI API client for Englishy.
"""

import os
import openai
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class OpenAIClient:
    """OpenAI API client for English learning tasks."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the OpenAI client."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def analyze_english_query(self, query: str, level: str = "beginner") -> Dict[str, Any]:
        """
        Analyze an English learning query and provide structured response.
        
        Args:
            query: The user's learning query
            level: Learning level (beginner, intermediate, advanced)
        
        Returns:
            Dictionary containing analysis results
        """
        try:
            system_prompt = f"""You are an expert English teacher and learning assistant. 
            Analyze the following query and provide a comprehensive learning plan.
            
            Learning Level: {level}
            
            Provide your response in the following JSON format:
            {{
                "learning_objectives": ["objective1", "objective2"],
                "key_concepts": ["concept1", "concept2"],
                "difficulty_level": "beginner/intermediate/advanced",
                "estimated_study_time": "X hours",
                "prerequisites": ["prerequisite1", "prerequisite2"],
                "learning_path": [
                    {{"step": 1, "title": "Step 1", "description": "Description"}},
                    {{"step": 2, "title": "Step 2", "description": "Description"}}
                ],
                "resources_needed": ["resource1", "resource2"],
                "practice_exercises": ["exercise1", "exercise2"]
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Parse the response
            content = response.choices[0].message.content
            # TODO: Add proper JSON parsing with error handling
            return {
                "raw_response": content,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error in analyze_english_query: {e}")
            return {
                "error": str(e),
                "status": "error"
            }
    
    def generate_english_report(self, query: str, search_results: List[str], 
                              style: str = "beginner") -> Dict[str, Any]:
        """
        Generate a comprehensive English learning report.
        
        Args:
            query: Original learning query
            search_results: List of search results to incorporate (limited to 10)
            style: Report style (beginner, intermediate, advanced)
        
        Returns:
            Dictionary containing the generated report
        """
        try:
            # Limit search results to 10 items
            limited_results = search_results[:10]
            
            system_prompt = f"""You are an expert English teacher creating a comprehensive learning report.
            
            Style: {style}
            
            Create a detailed report that includes:
            1. Introduction and learning objectives
            2. Key concepts and explanations
            3. Practical examples and exercises
            4. Common mistakes and how to avoid them
            5. Practice activities
            6. Additional resources and next steps
            7. References section with proper citations
            
            Format the response as markdown with clear sections.
            Include proper citations for all sources used."""
            
            # Combine query and search results
            content = f"Query: {query}\n\nSearch Results:\n" + "\n".join(limited_results)
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            return {
                "report": response.choices[0].message.content,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error in generate_english_report: {e}")
            return {
                "error": str(e),
                "status": "error"
            }
    
    def create_practice_exercises(self, topic: str, level: str = "beginner") -> Dict[str, Any]:
        """
        Create practice exercises for a specific English topic.
        
        Args:
            topic: The English topic to create exercises for
            level: Difficulty level
        
        Returns:
            Dictionary containing exercises
        """
        try:
            system_prompt = f"""Create engaging English practice exercises for the topic: {topic}
            
            Level: {level}
            
            Provide exercises in this format:
            {{
                "vocabulary_exercises": [
                    {{"word": "word", "definition": "definition", "example": "example"}}
                ],
                "grammar_exercises": [
                    {{"question": "question", "answer": "answer", "explanation": "explanation"}}
                ],
                "conversation_practice": [
                    {{"scenario": "scenario", "dialogue": "dialogue", "key_phrases": ["phrase1", "phrase2"]}}
                ],
                "writing_prompts": [
                    {{"prompt": "prompt", "word_count": "X words", "focus": "focus area"}}
                ]
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Create exercises for: {topic}"}
                ],
                temperature=0.8,
                max_tokens=2000
            )
            
            return {
                "exercises": response.choices[0].message.content,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error in create_practice_exercises: {e}")
            return {
                "error": str(e),
                "status": "error"
            }
    
    def generate_references(self, query: str, report_content: str, 
                          search_results: List[str]) -> Dict[str, Any]:
        """
        Generate a comprehensive references list for the report.
        
        Args:
            query: Original learning query
            report_content: The generated report content
            search_results: List of search results used
        
        Returns:
            Dictionary containing the generated references
        """
        try:
            system_prompt = """You are an expert in academic writing and reference management.
            
            Create a comprehensive references list for an English learning report.
            
            Include the following sections:
            1. Academic Sources - Books, journal articles, research papers
            2. Online Resources - Educational websites, learning platforms
            3. Government Guidelines - Official educational standards and guidelines
            4. Teaching Materials - Textbooks, workbooks, practice materials
            
            Format references in standard academic format:
            - Books: Author, A. (Year). Title. Publisher.
            - Articles: Author, A. (Year). Title. Journal, Volume(Issue), Pages.
            - Websites: Site Name. (Access Date). URL
            
            Focus on reliable, recent sources suitable for middle and high school students."""
            
            content = f"""Query: {query}
            
            Report Content: {report_content[:2000]}...
            
            Search Results Used: {chr(10).join(search_results[:10])}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content}
                ],
                temperature=0.5,
                max_tokens=2000
            )
            
            return {
                "references": response.choices[0].message.content,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error in generate_references: {e}")
            return {
                "error": str(e),
                "status": "error"
            } 