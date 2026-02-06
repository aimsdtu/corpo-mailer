from app.agents.llm import LLMInterface
from app.agents.prompt_loader import PromptLoader

class MailAgentHost:
    def __init__(self, llm: LLMInterface, prompt_loader: PromptLoader):
        self.llm = llm
        self.prompt_loader = prompt_loader

    def compose_email(self, context: dict) -> str:
        raise NotImplementedError
