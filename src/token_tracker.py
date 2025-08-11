# FILE: src/token_tracker.py
# PURPOSE: A simple class to track token usage across the pipeline.

class TokenUsageTracker:
    """A simple class to track token usage across the pipeline."""
    def __init__(self):
        self.embedding_tokens = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0

    @property
    def total_tokens(self):
        return self.embedding_tokens + self.prompt_tokens + self.completion_tokens

    def add_embedding_tokens(self, count: int):
        self.embedding_tokens += count

    def add_completion_usage(self, usage):
        """Adds token usage from an OpenAI completion response."""
        if usage:
            self.prompt_tokens += usage.prompt_tokens
            self.completion_tokens += usage.completion_tokens

    def display_usage(self):
        """Prints a formatted summary of token usage."""
        print("\n" + "=" * 50)
        print("? TOKEN USAGE SUMMARY")
        print("-" * 50)
        print(f"Embedding Tokens:          {self.embedding_tokens}")
        print(f"LLM Prompt Tokens:         {self.prompt_tokens}")
        print(f"LLM Completion Tokens:     {self.completion_tokens}")
        print("-" * 50)
        print(f"Total Tokens Consumed:     {self.total_tokens}")
        print("=" * 50)
