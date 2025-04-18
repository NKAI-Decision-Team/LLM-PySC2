# Copyright 2025, LLM-PySC2 Contributors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from llm_pysc2.lib.knowledge import unit_dict, knowledge_dict
from llm_pysc2.lib.utils import *

from pysc2.lib import features
from loguru import logger


def get_single_unit_info(unit, size_screen, team_unit_screen_coord=None) -> str:

  unit_type_id = unit.unit_type
  unit_name = unit_dict.get(unit_type_id, "Unknown")
  ratio = size_screen / SCREEN_WORLD_GRID

  # tag and pos
  if unit.alliance == features.PlayerRelative.ENEMY:
    unit_info = f"\n\t\tEnemy Unit: {unit_name}"
  else:
    unit_info = f"\n\t\tUnit: {unit_name}"
  if unit.unit_type not in UNIT_DONOT_NEED_TAG:
    unit_info += f"    Tag: {hex(unit.tag)}"
  unit_info += f"    ScreenPos: [{int(unit.x/ratio)}, {int(unit.y/ratio)}]"
  total_health = unit.health + unit.shield
  # distance to current team head unit
  if unit.unit_type not in UNIT_DONOT_NEED_DIS:
    if team_unit_screen_coord is not None and size_screen is not None:
      dist = math.sqrt((team_unit_screen_coord[0] - unit.x) ** 2 + (team_unit_screen_coord[1] - unit.y) ** 2) / ratio
      unit_info += f"    Distance: {int(dist)}"
  # health, energy, build_progress, weapon_cooldown
  unit_info += f"    Health: {total_health}"
  if unit.unit_type in knowledge_dict.keys():
    total_health_max = knowledge_dict[unit.unit_type]['health'] + knowledge_dict[unit.unit_type]['shield']
    if total_health_max > 0:
      unit_info += f"({int(100 * total_health / total_health_max)} %)"
  if unit.energy > 0:
    unit_info += f"    Energy: {unit.energy}"
  if unit.build_progress < 100:
    unit_info += f"    Build_progress: {unit.energy}%"
  if unit.build_progress == 100 and unit.alliance == features.PlayerRelative.SELF and unit.is_selected and \
      unit.unit_type in knowledge_dict.keys() and 'weapon1_attack' in knowledge_dict[unit.unit_type].keys() \
      and knowledge_dict[unit.unit_type]['weapon1_attack'] not in [0, -1]:
    if unit.unit_type == units.Protoss.Phoenix and unit.order_id_0 == 32:
      unit_info += f"    Cannot attack because of maintaining GravitonBeam on enemy unit (cannot move at the same time)"
    # elif unit.weapon_cooldown == 0:
    #   unit_info += f"    Weapon Ready"
    # elif unit.weapon_cooldown > 0:
    #   unit_info += f"    Weapon Waiting For Cooldown: {unit.weapon_cooldown / 22:.2f}s"
    else:
      pass
  try:
    if unit.build_progress == 100 and unit.buff_id_0 != 0:
      unit_info += f"    Buff: {str(buffs.Buffs(unit.buff_id_0))}"
    if unit.build_progress == 100 and unit.buff_id_1 != 0:
      unit_info += f" {str(buffs.Buffs(unit.buff_id_1))}"
  except:
    pass
  return unit_info


def get_single_unit_type_knowledge(unit_type, log_id) -> str:
  unit_type_knowledge = ''

  if unit_type not in knowledge_dict.keys():
    logger.warning(f"[ID {log_id}] do not find unit_type {str(unit_type)} in knowledge_dict")
    return ''
  if 'Protoss' in str(units.get_unit_type(unit_type)):
    unit_type_knowledge += f"\n\t{str(units.Protoss(unit_type))}"
  if 'Terran' in str(units.get_unit_type(unit_type)):
    unit_type_knowledge += f"\n\t{str(units.Terran(unit_type))}"
  if 'Zerg' in str(units.get_unit_type(unit_type)):
    unit_type_knowledge += f"\n\t{str(units.Zerg(unit_type))}"

  if 'description' in knowledge_dict[unit_type].keys():
    unit_type_knowledge += f"\n\t\t{knowledge_dict[unit_type]['description']}"
  else:
    logger.error(
      f"[ID {log_id}] do not find description of {str(unit_type)} in knowledge_dict")

  unit_knowledge = knowledge_dict[unit_type]
  unit_type_knowledge += f"\n\t\tUnit properties: {unit_knowledge['target_self'] + unit_knowledge['type_self']}"
  if 'weapon1_attack_range' in unit_knowledge.keys() and unit_knowledge['weapon1_attack_range'] not in [0, -1]:
    unit_type_knowledge += f"\n\t\tWeapon info: Attack Range {unit_knowledge['weapon1_attack_range']}"
  if 'target' in unit_knowledge.keys() and len(unit_knowledge['target']) != 0:
    unit_type_knowledge += f", target: {unit_knowledge['target']}"
  if 'type_anti' in unit_knowledge.keys() and len(unit_knowledge['type_anti']) != 0:
    unit_type_knowledge += f", anti: {unit_knowledge['type_anti']}"
  if 'weapon1_attack' in unit_knowledge.keys() and unit_knowledge['weapon1_attack'] not in [0, -1]:
    unit_type_knowledge += f", DPS(damage per second) {int(unit_knowledge['weapon1_attack'] * unit_knowledge['weapon1_attack_times'] / unit_knowledge['weapon1_cooldown'])}"
  if 'weapon1_attack_bonus' in unit_knowledge.keys() and unit_knowledge['weapon1_attack_bonus'] not in [0, -1]:
    unit_type_knowledge += f", DPS-anti {int((unit_knowledge['weapon1_attack'] + unit_knowledge['weapon1_attack_bonus']) * unit_knowledge['weapon1_attack_times'] / unit_knowledge['weapon1_cooldown'])}"
  if 'ability' in unit_knowledge.keys():
    unit_type_knowledge += f"\n\t\tunit abilities:"
    for ability in unit_knowledge['ability'].keys():
      unit_type_knowledge += f"\n\t\t\t{ability}: {unit_knowledge['ability'][ability]}"

  return unit_type_knowledge


# 获取所属单位的信息和相关知识
def get_teams_info_with_knowledge(agent) -> str:
  info = ''
  info += get_teams_info(agent)
  info += get_relevant_knowledge(agent)
  return info


# 获取所属单位的信息
def get_teams_info(agent) -> str:

  teams_info = ''
  ctrl_unit_type_total = []
  ally_unit_type_total = []
  enemy_unit_type_total = []
  unit_types_total = []

  # 获取小队单位的信息，对于单选型小队，一个单位算一队
  for team in agent.teams:
    team_obs_list = team['obs'] if (len(team['obs']) != 0 and len(team['unit_tags']) != 0) else None
    if team['select_type'] == 'select' and len(team['obs']) != len(team['unit_tags']):
      continue
    if team_obs_list is None:
      continue

    for i in range(len(team_obs_list)):

      ctrl_unit_type = []
      ally_unit_type = []
      enemy_unit_type = []
      ctrl_unit_tags = []
      ally_unit_tags = []
      enemy_unit_tags = []

      obs = team_obs_list[i]
      curr_team_head_unit = None

      ctrl_unit_screen_coord = [0, 0]
      for unit in obs.observation.feature_units:
        if unit.is_on_screen and unit.is_selected and unit.tag in team['unit_tags']:
          ctrl_unit_type.append(unit.unit_type)
          ctrl_unit_tags.append(unit.tag)
          ctrl_unit_screen_coord[0] += unit.x
          ctrl_unit_screen_coord[1] += unit.y
          if team['select_type'] != 'select' and unit.tag == team['unit_tags'][0]:
            curr_team_head_unit = unit
          if team['select_type'] == 'select' and unit.tag == team['unit_tags'][i]:
            curr_team_head_unit = unit
        if unit.is_on_screen and unit.alliance in [1, 2] and not unit.is_selected:
          ally_unit_type.append(unit.unit_type)
          ally_unit_tags.append(unit.tag)
        if unit.is_on_screen and unit.alliance == features.PlayerRelative.ENEMY:
          if unit.unit_type in [units.Zerg.Larva]:
            continue
          enemy_unit_type.append(unit.unit_type)
          enemy_unit_tags.append(unit.tag)

      if len(ctrl_unit_tags) > 0:
        ctrl_unit_screen_coord[0] = ctrl_unit_screen_coord[0] / len(ctrl_unit_tags)
        ctrl_unit_screen_coord[1] = ctrl_unit_screen_coord[1] / len(ctrl_unit_tags)
      else:
        ctrl_unit_screen_coord = None

      # 去重
      ctrl_unit_type = list(set(ctrl_unit_type))
      ally_unit_type = list(set(ally_unit_type))
      enemy_unit_type = list(set(enemy_unit_type))
      ctrl_unit_type_total += ctrl_unit_type
      ally_unit_type_total += ally_unit_type
      enemy_unit_type_total += enemy_unit_type

      # 输出文本初始化
      ctrl_units_info = ''
      ally_units_info = ''
      enemy_units_info = ''

      if team['select_type'] == 'select':
        teams_info += f"Team {team['name']}-{i + 1} Info:"
      else:
        teams_info += f"Team {team['name']} Info:"

      arr = obs.observation['feature_minimap']['camera']
      idx = np.nonzero(arr)  # 获取特征图上非零值的坐标
      minimap_x = int(idx[:][1].mean())
      minimap_y = int(idx[:][0].mean())
      teams_info += f"\n\tTeam minimap position: [{minimap_x}, {minimap_y}] (minimap coordinate valid range for actions: 0 < x < {agent.size_minimap}, 0 < y < {agent.size_minimap})"
      size_screen = obs.observation.feature_screen.height_map.shape[0]

      arr = obs.observation.feature_screen.buildable
      arr_t = arr.T
      edge_l, edge_r = 0, size_screen - 1
      edge_b, edge_u = size_screen - 1, 0    # y++ from up to down
      for i in range(size_screen):
        x1, y1 = i, i
        x2, y2 = size_screen - 1 - i, size_screen - 1 - i
        if x1 >= x2:
          break
        edge_u = y1 if (sum(arr[y1][:]) == 0 and edge_u == y1 - 1) else edge_u
        edge_b = y2 if (sum(arr[y2][:]) == 0 and edge_b == y2 + 1) else edge_b
        edge_l = x1 if (sum(arr_t[x1][:]) == 0 and edge_l == x1 - 1) else edge_l
        edge_r = x2 if (sum(arr_t[x2][:]) == 0 and edge_r == x2 + 1) else edge_r
      team['b'] = edge_b = edge_b if edge_b == size_screen - 1 else edge_b - int(size_screen / 6)  # /6
      team['u'] = edge_u = edge_u if edge_u == 0 else edge_u + int(size_screen / 6)
      team['l'] = edge_l = edge_l if edge_l == 0 else edge_l + int(size_screen / 6)
      team['r'] = edge_r = edge_r if edge_r == size_screen - 1 else edge_r - int(size_screen / 6)
      ratio = size_screen / SCREEN_WORLD_GRID
      teams_info += f"\n\tTeam screen edge (screen coordinate valid range for actions: {int(edge_l/ratio)} < x < {int(edge_r/ratio)}, {int(edge_u/ratio)} < y < {int(edge_b/ratio)})"
      if (team['l'] != 0 or team['u'] != 0 or team['r'] != size_screen - 1 or team['b'] != size_screen - 1):
        teams_info += f"\nWarning! controlled team near the map edge! Pay attention to using coordinates within the boundary!({int(edge_l/ratio)} < x < {int(edge_r/ratio)}, {int(edge_u/ratio)} < y < {int(edge_b/ratio)})"

      # controlled units
      for unit_type in ctrl_unit_type:
        for unit in obs.observation.feature_units:
          if unit.unit_type == unit_type and unit.is_on_screen and unit.alliance == features.PlayerRelative.SELF \
              and unit.tag in team['unit_tags'] and (0 < unit.x < size_screen and 0 < unit.y < size_screen):
            ctrl_units_info += get_single_unit_info(unit, size_screen)
      if ctrl_units_info != '':
        teams_info += "\n\tControlled Team Units:"
        teams_info += ctrl_units_info

      # ally units
      for unit_type in ally_unit_type:
        for unit in obs.observation.feature_units:
          if unit.unit_type == unit_type and unit.is_on_screen and unit.alliance in [1, 2] and \
              unit.tag not in team['unit_tags'] and (0 < unit.x < size_screen and 0 < unit.y < size_screen):
            ally_units_info += get_single_unit_info(unit, size_screen)
      if ally_units_info != '':
        teams_info += "\n\tNearby Ally Units:"
        teams_info += ally_units_info

      # enemy units
      for unit_type in enemy_unit_type:
        for unit in obs.observation.feature_units:
          if unit.unit_type == unit_type and unit.is_on_screen and unit.alliance == features.PlayerRelative.ENEMY and \
              (0 < unit.x < size_screen and 0 < unit.y < size_screen):
            enemy_units_info += get_single_unit_info(unit, size_screen, ctrl_unit_screen_coord)
      if enemy_units_info != '':
        teams_info += "\n\tNearby Enemy Units:"
        teams_info += enemy_units_info
    teams_info += "\n"

  teams_info += '\n'
  return teams_info


# 获取相关知识
def get_relevant_knowledge(agent) -> str:

  knowledge_info = ''
  ctrl_unit_type_total = []
  ally_unit_type_total = []
  enemy_unit_type_total = []
  unit_types_total = []

  # 获取小队单位的信息，对于单选型小队，一个单位算一队
  for team in agent.teams:
    team_obs_list = team['obs'] if (len(team['obs']) != 0 and len(team['unit_tags']) != 0) else None
    if team['select_type'] == 'select' and len(team['obs']) != len(team['unit_tags']):
      continue
    if team_obs_list is None:
      continue

    for i in range(len(team_obs_list)):

      ctrl_unit_type = []
      ally_unit_type = []
      enemy_unit_type = []
      ctrl_unit_tags = []
      ally_unit_tags = []
      enemy_unit_tags = []

      obs = team_obs_list[i]
      curr_team_head_unit = None

      ctrl_unit_screen_coord = [0, 0]
      for unit in obs.observation.feature_units:
        if unit.is_on_screen and unit.is_selected and unit.tag in team['unit_tags']:
          ctrl_unit_type.append(unit.unit_type)
          ctrl_unit_tags.append(unit.tag)
          ctrl_unit_screen_coord[0] += unit.x
          ctrl_unit_screen_coord[1] += unit.y
          if team['select_type'] != 'select' and unit.tag == team['unit_tags'][0]:
            curr_team_head_unit = unit
          if team['select_type'] == 'select' and unit.tag == team['unit_tags'][i]:
            curr_team_head_unit = unit
        if unit.is_on_screen and unit.alliance in [1, 2] and not unit.is_selected:
          ally_unit_type.append(unit.unit_type)
          ally_unit_tags.append(unit.tag)
        if unit.is_on_screen and unit.alliance == features.PlayerRelative.ENEMY:
          if unit.unit_type in [units.Zerg.Larva]:
            continue
          enemy_unit_type.append(unit.unit_type)
          enemy_unit_tags.append(unit.tag)

      if len(ctrl_unit_tags) > 0:
        ctrl_unit_screen_coord[0] = ctrl_unit_screen_coord[0] / len(ctrl_unit_tags)
        ctrl_unit_screen_coord[1] = ctrl_unit_screen_coord[1] / len(ctrl_unit_tags)
      else:
        ctrl_unit_screen_coord = None

      # 去重
      ctrl_unit_type = list(set(ctrl_unit_type))
      ally_unit_type = list(set(ally_unit_type))
      enemy_unit_type = list(set(enemy_unit_type))
      ctrl_unit_type_total += ctrl_unit_type
      ally_unit_type_total += ally_unit_type
      enemy_unit_type_total += enemy_unit_type

  ctrl_unit_type_total = list(set(ctrl_unit_type_total))
  ally_unit_type_total = list(set(ally_unit_type_total))
  enemy_unit_type_total = list(set(enemy_unit_type_total))
  showed_unit = []

  # controlled units description and abilities
  unit_types_total = ctrl_unit_type_total + ally_unit_type_total + enemy_unit_type_total
  knowledge_info += f"Relevant Knowledge:"
  for unit_type in unit_types_total:
    if unit_type not in knowledge_dict.keys():
      logger.warning(f"[ID {agent.log_id}] do not find unit_type {str(unit_type)} in knowledge_dict")
      continue
    if unit_type in showed_unit:
      continue
    if 'Protoss' in str(units.get_unit_type(unit_type)):
      knowledge_info += f"\n\t{str(units.Protoss(unit_type))}"
    if 'Terran' in str(units.get_unit_type(unit_type)):
      knowledge_info += f"\n\t{str(units.Terran(unit_type))}"
    if 'Zerg' in str(units.get_unit_type(unit_type)):
      knowledge_info += f"\n\t{str(units.Zerg(unit_type))}"

    if 'description' in knowledge_dict[unit_type].keys():
      knowledge_info += f"\n\t\t{knowledge_dict[unit_type]['description']}"
    else:
      logger.error(
        f"[ID {agent.log_id}] do not find description of {str(unit_type)} in knowledge_dict")

    unit_knowledge = knowledge_dict[unit_type]
    knowledge_info += f"\n\t\tUnit properties: {unit_knowledge['target_self'] + unit_knowledge['type_self']}"
    if 'weapon1_attack_range' in unit_knowledge.keys() and unit_knowledge['weapon1_attack_range'] not in [0, -1]:
      knowledge_info += f"\n\t\tWeapon info: Attack Range {unit_knowledge['weapon1_attack_range']}"
    if 'target' in unit_knowledge.keys() and len(unit_knowledge['target']) != 0:
      knowledge_info += f", target: {unit_knowledge['target']}"
    if 'type_anti' in unit_knowledge.keys() and len(unit_knowledge['type_anti']) != 0:
      knowledge_info += f", anti: {unit_knowledge['type_anti']}"
    if 'weapon1_attack' in unit_knowledge.keys() and unit_knowledge['weapon1_attack'] not in [0, -1]:
      knowledge_info += f", DPS(damage per second) {int(unit_knowledge['weapon1_attack'] * unit_knowledge['weapon1_attack_times'] / unit_knowledge['weapon1_cooldown'])}"
    if 'weapon1_attack_bonus' in unit_knowledge.keys() and unit_knowledge['weapon1_attack_bonus'] not in [0, -1]:
      knowledge_info += f", DPS-anti {int((unit_knowledge['weapon1_attack'] + unit_knowledge['weapon1_attack_bonus']) * unit_knowledge['weapon1_attack_times'] / unit_knowledge['weapon1_cooldown'])}"
    if 'ability' in unit_knowledge.keys() and unit_type in ctrl_unit_type_total:
      knowledge_info += f"\n\t\tunit abilities:"
      for ability in unit_knowledge['ability'].keys():
        knowledge_info += f"\n\t\t\t{ability}: {unit_knowledge['ability'][ability]}"

    showed_unit.append(unit_type)
  knowledge_info += "\n\n"
  return knowledge_info