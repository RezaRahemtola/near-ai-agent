from libertai_agents.agents import ChatAgent
from libertai_agents.models import get_model
from libertai_agents.models.models import ModelConfiguration

from src.tools import TOOLS

agent = ChatAgent(model=get_model("NousResearch/Hermes-3-Llama-3.1-8B",
                                  custom_configuration=ModelConfiguration(
                                      vm_url="http://localhost:8080/completion",
                                      context_length=16_000)
                                  ),
                  system_prompt="You are a helpful assistant",
                  tools=TOOLS)

app = agent.app


@app.get("/")
async def root():
    return {"message": "Hello from Near Agent!"}
