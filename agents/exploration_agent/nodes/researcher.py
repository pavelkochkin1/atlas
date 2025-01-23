from exploration_agent.model import gigachat_model
from exploration_agent.nodes.prompts import research_prompt

agent_researcher = research_prompt | gigachat_model
