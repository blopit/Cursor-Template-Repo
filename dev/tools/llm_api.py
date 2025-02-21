"""LLM API integration module."""
from typing import Optional, Dict, Any
import os
import openai
import anthropic
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def query_llm(
    prompt: str,
    provider: str = "openai",
    model: Optional[str] = None,
    **kwargs: Any
) -> str:
    """Query an LLM provider with the given prompt."""
    if provider == "openai":
        return _query_openai(prompt, model, **kwargs)
    elif provider == "anthropic":
        return _query_anthropic(prompt, model, **kwargs)
    elif provider == "google":
        return _query_google(prompt, model, **kwargs)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def _query_openai(
    prompt: str,
    model: Optional[str] = None,
    **kwargs: Any
) -> str:
    """Query OpenAI's API."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OpenAI API key not found in environment")
    
    model = model or "gpt-4o"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        **kwargs
    )
    return response.choices[0].message.content

def _query_anthropic(
    prompt: str,
    model: Optional[str] = None,
    **kwargs: Any
) -> str:
    """Query Anthropic's API."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Anthropic API key not found in environment")
    
    client = anthropic.Client(api_key=api_key)
    model = model or "claude-3-sonnet-20240229"
    
    response = client.messages.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        **kwargs
    )
    return response.content[0].text

def _query_google(
    prompt: str,
    model: Optional[str] = None,
    **kwargs: Any
) -> str:
    """Query Google's Generative AI API."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API key not found in environment")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model or "gemini-pro")
    
    response = model.generate_content(prompt, **kwargs)
    return response.text 