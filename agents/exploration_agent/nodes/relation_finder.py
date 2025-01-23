from exploration_agent.model import gigachat_model
from exploration_agent.nodes.prompts import relation_prompt

relation_finder = relation_prompt | gigachat_model
