import os

class LLMClient:
    def __init__(self, api_key=None, provider="openai"):
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.provider = provider

    def refine_content(self, raw_content):
        # Rule 1: Fix broken hyphenation at end of lines
        refined = raw_content.replace("-\n", "")
        
        # Rule 2: Basic whitespace cleanup
        lines = [line.strip() for line in refined.split("\n") if line.strip()]
        refined = "\n".join(lines)
        
        return refined

    def refine_with_llm(self, text):
        if not self.api_key:
            return self.refine_content(text)
        return text
