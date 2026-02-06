from app.agents.llm import LLMInterface
from app.agents.prompt_loader import PromptLoader

class TemplateAgentHost:
    def __init__(self, llm: LLMInterface, prompt_loader: PromptLoader):
        self.llm = llm
        self.prompt_loader = prompt_loader

    def generate_template(self, requirements: str) -> str:
        raise NotImplementedError
