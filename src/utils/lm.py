"""
Language model utilities for Englishy.
"""

import os
import dspy


def load_lm(model_name: str = None, **kwargs) -> dspy.LM:
    """
    Load a language model for DSPy.
    
    Args:
        model_name: Model name (e.g., "openai/gpt-4o-mini")
        **kwargs: Additional arguments for LM initialization
    
    Returns:
        DSPy LM instance
    """
    if model_name is None:
        model_name = os.getenv("ENGLISHY_LM", "openai/gpt-4o-mini")
    
    # Default parameters
    kwargs = dict(max_tokens=8192, temperature=0.0, cache=False, **kwargs)
    
    # Parse provider and model
    assert len(model_name.split("/")) == 2, f"Invalid model name format: {model_name}"
    provider = model_name.split("/")[0]
    
    if provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return dspy.LM(model_name, api_key=api_key, **kwargs)
    
    elif provider == "anthropic":
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        return dspy.LM(model_name, api_key=api_key, **kwargs)
    
    elif provider == "gemini":
        api_key = os.environ.get("GOOGLE_AI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_AI_API_KEY environment variable is required")
        return dspy.LM(model_name, api_key=api_key, **kwargs)
    
    else:
        raise ValueError(f"Unsupported provider: {provider}. Supported providers: [openai, anthropic, gemini]") 