from exploration_agent.model import gigachat_model
from exploration_agent.nodes.prompts import unify_prompt

agent_unifier = unify_prompt | gigachat_model
