#!/usr/bin/env python3
"""
Test script for AI modules in Englishy.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from ai.query_refiner import QueryRefiner
from ai.query_expander import QueryExpander
from ai.outline_creater import OutlineCreater
from ai.mindmap_maker import MindMapMaker
from ai.report_writer import StreamLeadWriter, StreamSectionWriter, StreamConclusionWriter
from app.utils.lm import load_language_model
from utils.logging import logger


def test_query_refiner():
    """Test query refinement."""
    print("🧪 Testing Query Refiner...")
    
    try:
        lm = load_language_model()
        refiner = QueryRefiner(lm)
        
        test_query = "How to learn English grammar effectively?"
        result = refiner.forward(test_query)
        
        print(f"✅ Original query: {test_query}")
        print(f"✅ Refined query: {result.refined_query}")
        return True
        
    except Exception as e:
        print(f"❌ Query refiner test failed: {e}")
        return False


def test_query_expander():
    """Test query expansion."""
    print("\n🧪 Testing Query Expander...")
    
    try:
        lm = load_language_model()
        expander = QueryExpander(lm)
        
        test_query = "English grammar learning"
        test_web_results = """
        Result 1:
        Title: 10 Essential English Grammar Rules
        Content: Learn the most important grammar rules for English learners...
        
        Result 2:
        Title: Best English Learning Apps 2024
        Content: Top-rated apps for learning English grammar and vocabulary...
        """
        
        result = expander.forward(test_query, test_web_results)
        
        print(f"✅ Original query: {test_query}")
        print(f"✅ Expanded topics: {result.topics}")
        return True
        
    except Exception as e:
        print(f"❌ Query expander test failed: {e}")
        return False


def test_outline_creater():
    """Test outline creation."""
    print("\n🧪 Testing Outline Creator...")
    
    try:
        lm = load_language_model()
        creator = OutlineCreater(lm)
        
        test_query = "English grammar basics"
        test_topics = ["grammar rules", "parts of speech", "sentence structure"]
        test_references = [
            "[1] Basic English Grammar Rules\nEssential grammar concepts for beginners...",
            "[2] Parts of Speech in English\nUnderstanding nouns, verbs, adjectives...",
            "[3] Sentence Structure Guide\nHow to construct proper English sentences..."
        ]
        
        result = creator.forward(test_query, test_topics, test_references)
        
        print(f"✅ Query: {test_query}")
        print(f"✅ Outline title: {result.outline.title}")
        print(f"✅ Number of sections: {len(result.outline.section_outlines)}")
        return True
        
    except Exception as e:
        print(f"❌ Outline creator test failed: {e}")
        return False


def test_mindmap_maker():
    """Test mind map generation."""
    print("\n🧪 Testing Mind Map Maker...")
    
    try:
        lm = load_language_model()
        maker = MindMapMaker(lm)
        
        test_report = """
        # English Grammar Learning Guide
        
        This comprehensive guide covers essential English grammar concepts for learners.
        
        ## Basic Grammar Rules
        Understanding fundamental grammar rules is crucial for English learners.
        
        ## Parts of Speech
        Nouns, verbs, adjectives, and other parts of speech form the building blocks of English.
        
        ## Sentence Structure
        Proper sentence structure helps convey meaning clearly and effectively.
        """
        
        result = maker.forward(test_report)
        
        print(f"✅ Generated mind map length: {len(result.mindmap)} characters")
        print(f"✅ Mind map preview: {result.mindmap[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ Mind map maker test failed: {e}")
        return False


async def test_report_writers():
    """Test report writing components."""
    print("\n🧪 Testing Report Writers...")
    
    try:
        lm = load_language_model()
        
        # Test lead writer
        lead_writer = StreamLeadWriter(lm)
        test_query = "English grammar learning"
        test_title = "Complete English Grammar Guide"
        test_draft = "This guide covers essential grammar concepts..."
        
        lead_content = ""
        async for chunk in lead_writer(test_query, test_title, test_draft):
            lead_content += chunk
        
        print(f"✅ Lead writer: Generated {len(lead_content)} characters")
        
        # Test section writer
        section_writer = StreamSectionWriter(lm)
        test_references = "[1] Grammar Rule 1\n[2] Grammar Rule 2"
        test_section_outline = "## Basic Grammar\n### Nouns\n[1][2]"
        
        section_content = ""
        async for chunk in section_writer(test_query, test_references, test_section_outline):
            section_content += chunk
        
        print(f"✅ Section writer: Generated {len(section_content)} characters")
        
        # Test conclusion writer
        conclusion_writer = StreamConclusionWriter(lm)
        test_report_draft = f"{lead_content}\n\n{section_content}"
        
        conclusion_content = ""
        async for chunk in conclusion_writer(test_query, test_report_draft):
            conclusion_content += chunk
        
        print(f"✅ Conclusion writer: Generated {len(conclusion_content)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Report writers test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 Starting AI Module Tests for Englishy")
    print("=" * 50)
    
    # Check environment
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable is required")
        return
    
    results = []
    
    # Run tests
    results.append(test_query_refiner())
    results.append(test_query_expander())
    results.append(test_outline_creater())
    results.append(test_mindmap_maker())
    
    # Run async test
    try:
        async_result = asyncio.run(test_report_writers())
        results.append(async_result)
    except Exception as e:
        print(f"❌ Async test failed: {e}")
        results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed. Please check the configuration.")


if __name__ == "__main__":
    main() 