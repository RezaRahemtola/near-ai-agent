from libertai_agents.agents import ChatAgent
from libertai_agents.models import get_model
from libertai_agents.models.models import ModelConfiguration


async def get_current_temperature(location: str, unit: str) -> float:
    """
    Get the current temperature at a location.

    Args:
        location: The location to get the temperature for, in the format "City, Country"
        unit: The unit to return the temperature in. (choices: ["celsius", "fahrenheit"])
    Returns:
        The current temperature at the specified location in the specified units, as a float.
    """
    return 22.  # A real function should probably actually get the temperature!


agent = ChatAgent(model=get_model("NousResearch/Hermes-3-Llama-3.1-8B",
                                  custom_configuration=ModelConfiguration(
                                      vm_url="http://localhost:8080/completion",
                                      context_length=16_000)
                                  ),
                  system_prompt="You are a helpful assistant",
                  tools=[get_current_temperature])

app = agent.app


@app.get("/")
async def root():
    return {"message": "Hello from Near Agent!"}
