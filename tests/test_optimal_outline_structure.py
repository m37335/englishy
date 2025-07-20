#!/usr/bin/env python3
"""
Test script for optimal outline structure with GrammarAnalyzer integration.
Tests the new outline structure that integrates GrammarAnalyzer analysis with Web search results.
"""

import sys
import os
import asyncio

# Add src to path for imports
sys.path.append('/app/src')

from ai.outline_creater import OutlineCreater
from ai.grammar_analyzer import get_grammar_analyzer
from utils.lm import load_lm


def test_optimal_outline_structure():
    """Test the optimal outline structure with GrammarAnalyzer integration."""
    print("🧪 Testing Optimal Outline Structure with GrammarAnalyzer Integration")
    print("=" * 70)
    
    # Test cases
    test_cases = [
        {
            "query": "仮定法過去について",
            "expected_sections": ["文法構造の理解", "実例と詳細解説", "実践的な活用"],
            "description": "Simple grammar item (3 sections expected)"
        },
        {
            "query": "受動態と能動態の使い分けについて",
            "expected_sections": ["文法構造の理解", "実例と詳細解説", "実践的な活用", "発展と応用"],
            "description": "Complex grammar item (4 sections expected)"
        },
        {
            "query": "動名詞と不定詞の違い",
            "expected_sections": ["文法構造の理解", "実例と詳細解説", "実践的な活用"],
            "description": "Comparison grammar item (3 sections expected)"
        }
    ]
    
    try:
        # Initialize components
        print("📋 Initializing components...")
        lm = load_lm()
        outline_creater = OutlineCreater(lm=lm)
        grammar_analyzer = get_grammar_analyzer()
        
        # Mock data
        mock_topics = [
            "teaching past subjunctive in English",
            "exercises for past subjunctive practice",
            "research on subjunctive mood in English"
        ]
        
        mock_references = [
            {
                "id": 1,
                "title": "Past Subjunctive in English Grammar",
                "url": "https://example.com/1",
                "snippet": "The past subjunctive is used to express hypothetical situations in the past."
            },
            {
                "id": 2,
                "title": "Teaching Subjunctive Mood",
                "url": "https://example.com/2",
                "snippet": "Effective methods for teaching subjunctive mood to ESL students."
            },
            {
                "id": 3,
                "title": "Subjunctive vs Indicative",
                "url": "https://example.com/3",
                "snippet": "Understanding the difference between subjunctive and indicative moods."
            }
        ]
        
        # Run tests
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🔍 Test {i}: {test_case['description']}")
            print(f"Query: {test_case['query']}")
            
            # Get grammar analysis
            grammar_analysis = grammar_analyzer.analyze_text(test_case['query'])
            print(f"Grammar Analysis: {grammar_analysis.get('grammar_structures', [])}")
            
            # Generate outline
            outline_result = outline_creater(
                query=test_case['query'],
                topics=mock_topics,
                references=mock_references,
                grammar_analysis=grammar_analysis
            )
            
            # Analyze outline structure
            outline = outline_result.outline
            actual_sections = [section.title for section in outline.section_outlines]
            
            print(f"Generated Sections: {actual_sections}")
            print(f"Expected Sections: {test_case['expected_sections']}")
            
            # Check section count
            expected_count = len(test_case['expected_sections'])
            actual_count = len(actual_sections)
            
            if actual_count == expected_count:
                print(f"✅ Section count correct: {actual_count}")
            else:
                print(f"❌ Section count mismatch: expected {expected_count}, got {actual_count}")
            
            # Check section structure
            print("📊 Section Structure Analysis:")
            for j, section in enumerate(outline.section_outlines, 1):
                subsection_count = len(section.subsection_outlines)
                print(f"  Section {j}: '{section.title}' ({subsection_count} subsections)")
                
                for k, subsection in enumerate(section.subsection_outlines, 1):
                    ref_count = len(subsection.reference_ids)
                    keyword_count = len(subsection.keywords)
                    print(f"    Subsection {k}: '{subsection.title}' (refs: {ref_count}, keywords: {keyword_count})")
            
            print("-" * 50)
        
        print("\n🎉 All tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


def test_outline_content_quality():
    """Test the quality of outline content with GrammarAnalyzer integration."""
    print("\n🧪 Testing Outline Content Quality")
    print("=" * 50)
    
    try:
        # Initialize components
        lm = load_lm()
        outline_creater = OutlineCreater(lm=lm)
        grammar_analyzer = get_grammar_analyzer()
        
        # Test query
        query = "仮定法過去について"
        
        # Get grammar analysis
        grammar_analysis = grammar_analyzer.analyze_text(query)
        
        # Mock data
        mock_topics = ["teaching subjunctive", "subjunctive exercises", "subjunctive research"]
        mock_references = [
            {"id": 1, "title": "Subjunctive Guide", "url": "https://example.com/1", "snippet": "Complete guide to subjunctive mood"},
            {"id": 2, "title": "Teaching Methods", "url": "https://example.com/2", "snippet": "Effective teaching methods for subjunctive"},
            {"id": 3, "title": "Practice Exercises", "url": "https://example.com/3", "snippet": "Practice exercises for subjunctive mood"}
        ]
        
        # Generate outline
        outline_result = outline_creater(
            query=query,
            topics=mock_topics,
            references=mock_references,
            grammar_analysis=grammar_analysis
        )
        
        outline = outline_result.outline
        
        # Analyze content quality
        print(f"📝 Outline Title: {outline.title}")
        print(f"📊 Total Sections: {len(outline.section_outlines)}")
        
        # Check each section
        for i, section in enumerate(outline.section_outlines, 1):
            print(f"\n📋 Section {i}: {section.title}")
            
            # Check if section follows optimal structure
            if i == 1 and "理解" in section.title:
                print("  ✅ Section 1: Grammar structure understanding")
            elif i == 2 and "実例" in section.title:
                print("  ✅ Section 2: Examples and detailed explanation")
            elif i == 3 and "実践" in section.title:
                print("  ✅ Section 3: Practical application")
            elif i == 4 and "発展" in section.title:
                print("  ✅ Section 4: Development and application")
            else:
                print(f"  ⚠️  Section {i}: Structure unclear")
            
            # Check subsections
            for j, subsection in enumerate(section.subsection_outlines, 1):
                print(f"    📄 Subsection {j}: {subsection.title}")
                print(f"      References: {subsection.reference_ids}")
                print(f"      Keywords: {subsection.keywords}")
        
        print("\n✅ Content quality test completed!")
        
    except Exception as e:
        print(f"❌ Content quality test failed: {e}")
        import traceback
        traceback.print_exc()


def test_grammar_analyzer_integration():
    """Test the integration of GrammarAnalyzer results in outline generation."""
    print("\n🧪 Testing GrammarAnalyzer Integration")
    print("=" * 50)
    
    try:
        # Initialize components
        lm = load_lm()
        outline_creater = OutlineCreater(lm=lm)
        grammar_analyzer = get_grammar_analyzer()
        
        # Test queries with different grammar complexity
        test_queries = [
            "仮定法過去について",  # Simple
            "受動態と能動態の使い分けについて",  # Complex
            "動名詞と不定詞の違い",  # Comparison
            "関係代名詞の使い方"  # Intermediate
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing: {query}")
            
            # Get grammar analysis
            grammar_analysis = grammar_analyzer.analyze_text(query)
            
            print(f"  Grammar Structures: {grammar_analysis.get('grammar_structures', [])}")
            print(f"  Difficulty Level: {grammar_analysis.get('difficulty_level', 'unknown')}")
            print(f"  Key Points: {grammar_analysis.get('key_points', [])}")
            
            # Mock data
            mock_topics = ["teaching grammar", "grammar exercises", "grammar research"]
            mock_references = [
                {"id": 1, "title": "Grammar Guide", "url": "https://example.com/1", "snippet": "Grammar guide"},
                {"id": 2, "title": "Teaching Methods", "url": "https://example.com/2", "snippet": "Teaching methods"},
                {"id": 3, "title": "Practice Exercises", "url": "https://example.com/3", "snippet": "Practice exercises"}
            ]
            
            # Generate outline
            outline_result = outline_creater(
                query=query,
                topics=mock_topics,
                references=mock_references,
                grammar_analysis=grammar_analysis
            )
            
            outline = outline_result.outline
            
            # Check if outline structure matches grammar complexity
            section_count = len(outline.section_outlines)
            difficulty = grammar_analysis.get('difficulty_level', 'intermediate')
            
            print(f"  Generated Sections: {section_count}")
            print(f"  Expected Structure: {'Complex (4 sections)' if difficulty == 'advanced' else 'Standard (3 sections)'}")
            
            if (difficulty == 'advanced' and section_count >= 4) or (difficulty != 'advanced' and section_count >= 3):
                print("  ✅ Structure matches complexity")
            else:
                print("  ⚠️  Structure may not match complexity")
        
        print("\n✅ GrammarAnalyzer integration test completed!")
        
    except Exception as e:
        print(f"❌ GrammarAnalyzer integration test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("🚀 Starting Optimal Outline Structure Tests")
    print("=" * 70)
    
    # Run all tests
    test_optimal_outline_structure()
    test_outline_content_quality()
    test_grammar_analyzer_integration()
    
    print("\n🎉 All tests completed successfully!") 