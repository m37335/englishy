"""
Language model utilities for Englishy.
"""

import os
import dspy
from typing import Optional

from utils.logging import logger


def load_language_model() -> dspy.LM:
    """Load the configured language model."""
    model_name = os.getenv("ENGLISHY_LM", "openai/gpt-4o-mini")
    
    try:
        if model_name.startswith("openai/"):
            # OpenAI models
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required")
            
            lm = dspy.OpenAI(
                model=model_name.replace("openai/", ""),
                api_key=api_key,
                max_tokens=4000,
                temperature=0.1
            )
            
        elif model_name.startswith("anthropic/"):
            # Anthropic models
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable is required")
            
            lm = dspy.Anthropic(
                model=model_name.replace("anthropic/", ""),
                api_key=api_key,
                max_tokens=4000,
                temperature=0.1
            )
            
        elif model_name.startswith("google/"):
            # Google models
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable is required")
            
            lm = dspy.Google(
                model=model_name.replace("google/", ""),
                api_key=api_key,
                max_tokens=4000,
                temperature=0.1
            )
            
        else:
            # Default to OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required")
            
            lm = dspy.OpenAI(
                model="gpt-4o-mini",
                api_key=api_key,
                max_tokens=4000,
                temperature=0.1
            )
        
        logger.info(f"Loaded language model: {model_name}")
        return lm
        
    except Exception as e:
        logger.error(f"Failed to load language model: {e}")
        raise 