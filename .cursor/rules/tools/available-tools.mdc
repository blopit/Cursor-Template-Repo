---
description: Available tools and their usage
globs: tools/*
---
# Available Tools

## Screenshot Verification
Tools for capturing and verifying web page screenshots using LLMs.

### Screenshot Capture
```bash
venv/bin/python tools/screenshot_utils.py URL [--output OUTPUT] [--width WIDTH] [--height HEIGHT]
```

### LLM Verification with Images
```bash
venv/bin/python tools/llm_api.py --prompt "Your verification question" --provider {openai|anthropic} --image path/to/screenshot.png
```

Example workflow:
```python
from screenshot_utils import take_screenshot_sync
from llm_api import query_llm

screenshot_path = take_screenshot_sync('https://example.com', 'screenshot.png')
response = query_llm(
    "What is the background color and title of this webpage?",
    provider="openai",
    image_path=screenshot_path
)
```

## LLM Integration
Access to various LLM providers for text processing and analysis.

### Command Line Usage
```bash
venv/bin/python ./tools/llm_api.py --prompt "Your prompt" --provider "anthropic"
```

### Supported Providers
- OpenAI (default, gpt-4o)
- Azure OpenAI (configured via AZURE_OPENAI_MODEL_DEPLOYMENT)
- DeepSeek (deepseek-chat)
- Anthropic (claude-3-sonnet-20240229)
- Gemini (gemini-pro)
- Local LLM (Qwen/Qwen2.5-32B-Instruct-AWQ)

## Web Browser
Tool for web scraping and content extraction.

```bash
venv/bin/python ./tools/web_scraper.py --max-concurrent 3 URL1 URL2 URL3
```

## Search Engine
Tool for web search operations.

```bash
venv/bin/python ./tools/search_engine.py "your search keywords"
```

Output format:
```
URL: https://example.com
Title: Search result title
Snippet: Search result snippet
```

## Usage Notes
- Always use the Python virtual environment in `./venv`
- For complex tasks, prefer using the Python APIs directly from the tool files
- Handle different character encodings properly for international queries
- Add appropriate debug information to stderr while keeping stdout clean 
