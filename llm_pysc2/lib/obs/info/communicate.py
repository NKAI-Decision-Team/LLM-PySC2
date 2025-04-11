

from llm_pysc2.lib.obs.info.team_unit import get_single_unit_type_knowledge
from pysc2.lib import units


def get_communication_info(agent) -> str:
  communication_info = agent.last_text_c_inp + agent.last_text_c_tar
  return communication_info

def get_other_agents_info(agent) -> str:  # for Commander only
  other_agents_info = ''
  other_agents = agent.other_agents

  other_agents_unit_knowledge = ''
  showed_unit_type = []

  for agent_name in other_agents.keys():
    agent_ = other_agents[agent_name]
    other_agent_info = ''
    for team in agent_.teams:
      if team['name'] == 'Empty':
        continue

      if agent_.enable and len(team['unit_tags']) != 0 and team['select_type'] != 'select':
        other_agent_info += f"\n\t\tTeam {team['name']}: {str(units.get_unit_type(team['unit_type'][0]))} x{len(team['unit_tags'])}"
        if len(team['minimap_pos']) == 1:
          other_agent_info += f", minimap position {team['minimap_pos'].pop(0)}"
          if team['unit_type'][0] not in showed_unit_type:
            other_agents_unit_knowledge += get_single_unit_type_knowledge(team['unit_type'][0], agent.log_id)
            showed_unit_type.append(team['unit_type'][0])

      if agent_.enable and len(team['unit_tags']) != 0 and team['select_type'] == 'select':
        for i in range(len(team['unit_tags'])):
          other_agent_info += f"\n\t\tTeam {team['name']}-{i}: {str(units.get_unit_type(team['unit_type'][0]))} x1"
          if len(team['minimap_pos']) + i == len(team['unit_tags']):
            other_agent_info += f", minimap position {team['minimap_pos'].pop(0)}"
            if team['unit_type'][0] not in showed_unit_type:
              other_agents_unit_knowledge += get_single_unit_type_knowledge(team['unit_type'][0], agent.log_id)
              showed_unit_type.append(team['unit_type'][0])

    if len(other_agent_info) != 0:
      other_agent_info = f'\n\tAgent {agent_name}:' + other_agent_info
    other_agents_info += other_agent_info

  if len(other_agents_info) != 0:
    other_agents_info = "Global agent info:" + other_agents_info + "\n\n"
  if len(other_agents_unit_knowledge) != 0:
    other_agents_unit_knowledge = f"Relevant Knowledge:" + other_agents_unit_knowledge + "\n\n"

  return other_agents_info + other_agents_unit_knowledge