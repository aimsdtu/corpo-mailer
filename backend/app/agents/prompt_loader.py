from typing import Any

class PromptLoader:
    def __init__(self, prompt_file: str):
        self.prompt_file = prompt_file
        # load prompts
        raise NotImplementedError

    def get_prompt(self, name: str, **kwargs) -> str:
        raise NotImplementedError
