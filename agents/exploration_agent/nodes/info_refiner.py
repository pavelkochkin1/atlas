from exploration_agent.model import gigachat_model
from exploration_agent.nodes.prompts import teams_refiner

team_refiner = teams_refiner | gigachat_model
