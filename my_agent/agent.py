from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

root_agent = Agent(
    model=LiteLlm(model="ollama_chat/gpt-oss:20b"),
    name="SysAdminAgent",
    description="A helpful assistant for administrating Linux-based operating systems.",
    instruction="Answer user questions to the best of your knowledge."
)