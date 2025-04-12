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


from llm_pysc2.lib.knowledge import DATA_SC2_UNITS
from llm_pysc2.lib.utils import BUFF_TO_TARGET_TYPE, BUILDING_TYPE
from llm_pysc2.lib.action.condition import get_condition_elements, all_building_condition_reached, map_research_quick_to_level

from pysc2.lib import units, features  # actions, features, buffs, upgrades


def check_weapon_state(obs, queued, source_unit_tag, strict=False):
  weapon_ready_unit_tags = []
  cooldown_time_limit = 0 if strict else 0.5
  if queued == 'queued':
    return True
  else:
    for unit in obs.observation.feature_units:
      if unit.is_selected and unit.weapon_cooldown <= cooldown_time_limit:
        weapon_ready_unit_tags.append(unit.tag)
    if (source_unit_tag is not None and source_unit_tag in weapon_ready_unit_tags) or \
        (source_unit_tag is None and len(weapon_ready_unit_tags) > 0):
      return True
    return False

def is_valid_screen_range(obs, screen, size_screen) -> (int, int, int, int):
  arr = obs.observation.feature_screen.buildable
  arr_t = arr.T
  edge_l, edge_r = 0, size_screen - 1
  edge_b, edge_u = size_screen - 1, 0  # y++ from up to down
  for i in range(size_screen):
    x1, y1 = i, i
    x2, y2 = size_screen - 1 - i, size_screen - 1 - i
    if x1 >= x2:
      break
    edge_u = y1 if (edge_u == y1 - 1 and sum(arr[y1][:]) == 0) else edge_u
    edge_b = y2 if (edge_b == y2 + 1 and sum(arr[y2][:]) == 0) else edge_b
    edge_l = x1 if (edge_l == x1 - 1 and sum(arr_t[x1][:]) == 0) else edge_l
    edge_r = x2 if (edge_r == x2 + 1 and sum(arr_t[x2][:]) == 0) else edge_r
  edge_b = edge_b if edge_b == size_screen - 1 else edge_b - int(size_screen / 8)  # /8 3s_vs_3z
  edge_u = edge_u if edge_u == 0 else edge_u + int(size_screen / 8)
  edge_l = edge_l if edge_l == 0 else edge_l + int(size_screen / 8)
  edge_r = edge_r if edge_r == size_screen - 1 else edge_r - int(size_screen / 8)
  return edge_l, edge_r, edge_u, edge_b


def check_attack_target(obs, tag):
  source_unit_types = []
  target_unit_types = []
  available_target_types = []
  target_types = []
  target_unit = None
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.is_on_screen and unit.unit_type not in source_unit_types:
      source_unit_types.append(unit.unit_type)
    if unit.tag == tag and unit.unit_type not in target_unit_types:  # source_unit_types
      target_unit_types.append(unit.unit_type)
      target_unit = unit
  for unit_type in source_unit_types:
    if unit_type in DATA_SC2_UNITS.keys():
      unit_data = DATA_SC2_UNITS[unit_type]
      for available_target_type in unit_data['target']:
        if available_target_type not in available_target_types:
          available_target_types.append(available_target_type)
  for unit_type in target_unit_types:
    if unit_type in DATA_SC2_UNITS.keys():
      unit_data = DATA_SC2_UNITS[unit_type]
      for target_type in unit_data['target_self']:
        if target_type not in target_types:
          target_types.append(target_type)
  # print(available_target_types, target_types)
  if target_unit is not None:
    if target_unit.buff_id_0 in BUFF_TO_TARGET_TYPE.keys() and BUFF_TO_TARGET_TYPE[target_unit.buff_id_0] in available_target_types:
      return True, f''
    if target_unit.buff_id_1 in BUFF_TO_TARGET_TYPE.keys() and BUFF_TO_TARGET_TYPE[target_unit.buff_id_1] in available_target_types:
      return True, f''
  if 'ground' in target_types and 'air' not in target_types and 'ground' not in available_target_types:
    return False, f'Must target air unit'
  if 'air' in target_types and 'ground' not in target_types and 'air' not in available_target_types:
    return False, f'Must target ground unit'
  return True, f''
  # for target_type in target_types:
  #   if target_type in available_target_types:
  #     return True, available_target_types, target_types
  # return False, available_target_types, target_types


def check_scan_action_validity(agent, obs, action_name) -> bool:
  if not ('_Scan' in action_name):
    return True
  if action_name == 'Worker_Scan':
    return True

  if len(action_name.split('_')) == 2:
    unit_name = action_name.split('_')[0]
    for unit in obs.observation.raw_units:
      if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100 and unit.unit_type not in BUILDING_TYPE:
        if str(units.get_unit_type(unit.unit_type)).split('.')[-1] == unit_name:
          return True
  return False


def check_develop_action_validity(agent, obs, action_name) -> bool:
  if not ('Build' in action_name or 'Research' in action_name or 'Train' in action_name or 'Warp' in action_name):
    return True

  ra, ta, ba, rc, tc, bc, m, g, s, u, b = get_condition_elements(agent)
  all_actions = ra + ta + ba
  all_conditions = {}
  all_conditions.update(rc)
  all_conditions.update(tc)
  all_conditions.update(bc)

  building_types = []
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100 and unit.unit_type in BUILDING_TYPE:
      building_types.append(unit.unit_type)

  valid_action_names = []
  for action in all_actions:
    func_id = map_research_quick_to_level(action['func'][-1][0], u)
    if func_id in all_conditions.keys():
      conditions, valid = all_conditions[func_id], True
      # condition = {'m': 125, 'g': 50, 'b': units.Protoss.Gateway, 't': 42, 's': 2},
      cs = conditions
      valid = False if ('m' in cs.keys() and m < cs['m']) else valid
      valid = False if ('g' in cs.keys() and g < cs['g']) else valid
      valid = False if ('s' in cs.keys() and s < cs['s']) else valid
      valid = False if ('b' in cs.keys() and not all_building_condition_reached(cs['b'], building_types)) else valid
      valid = False if ('u' in cs.keys() and cs['u'] not in u) else valid
      if valid:
        valid_action_names.append(action['name'])
    else:
      valid_action_names.append(action['name'])

  return True if action_name in valid_action_names else False


# def check_valid_action_names_build(agent, obs=None) -> (list, str):
#   obs = agent.team_unit_obs_list[0] if obs is None else obs
#   _, _, ba, _, _, bc, m, g, s, u, b = get_condition_elements(agent)
#
#   building_types = []
#   for unit in obs.observation.raw_units:
#     if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100 and unit.unit_type in BUILDING_TYPE:
#       building_types.append(unit.unit_type)
#
#   valid_action_names = []
#   for action in ba:
#     func_id, valid = action['func'][-1][0], True
#     arg_to_show = '' if agent.config.ENABLE_EASY_BUILD else action['arg'][0]
#     if func_id in bc.keys():
#       conditions = bc[func_id]
#       # condition = {'m': 175, 'g': 175, 'b': units.Protoss.CyberneticsCore, 'u': u.ProtossAirArmorsLevel1, 't': 215},
#       cs = conditions
#       valid = False if ('m' in cs.keys() and m < cs['m']) else valid
#       valid = False if ('g' in cs.keys() and g < cs['g']) else valid
#       valid = False if ('s' in cs.keys() and s < cs['s']) else valid
#       valid = False if ('b' in cs.keys() and not all_building_condition_reached(cs['b'], building_types)) else valid
#       valid = False if ('u' in cs.keys() and cs['u'] not in u) else valid
#       if valid:
#         valid_action_names.append(action['name'])
#     else:
#       valid_action_names.append(action['name'])
#
#   return valid_action_names
#
#
# def check_valid_action_names_research(agent, obs=None) -> (list, str):
#   obs = agent.team_unit_obs_list[0] if obs is None else obs
#   ra, _, _, rc, _, _, m, g, s, u, b = get_condition_elements(agent)
#
#   building_types = []
#   for unit in obs.observation.raw_units:
#     if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100 and unit.unit_type in BUILDING_TYPE:
#       building_types.append(unit.unit_type)
#
#   valid_action_names = []
#   for action in ra:
#     func_id = map_research_quick_to_level(action['func'][0][0], u)
#     if func_id == -1:
#       continue
#     conditions, valid = rc[func_id], True
#     # condition = {'m': 175, 'g': 175, 'b': units.Protoss.CyberneticsCore, 'u': u.ProtossAirArmorsLevel1, 't': 215},
#     cs = conditions
#     valid = False if ('m' in cs.keys() and m < cs['m']) else valid
#     valid = False if ('g' in cs.keys() and g < cs['g']) else valid
#     valid = False if ('s' in cs.keys() and s < cs['s']) else valid
#     valid = False if ('b' in cs.keys() and not all_building_condition_reached(cs['b'], building_types)) else valid
#     valid = False if ('u' in cs.keys() and cs['u'] not in u) else valid
#     if valid:
#       valid_action_names.append(action['name'])
#   return valid_action_names
#
#
# def check_valid_action_names_train(agent, obs=None) -> (list, str):
#   obs = agent.team_unit_obs_list[0] if obs is None else obs
#   _, ta, _, _, tc, _, m, g, s, u, b = get_condition_elements(agent)
#
#   building_types = []
#   for unit in obs.observation.raw_units:
#     if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100 and unit.unit_type in BUILDING_TYPE:
#       building_types.append(unit.unit_type)
#
#   valid_action_names = []
#   for action in ta:
#     func_id = action['func'][0][0]
#     conditions, valid = tc[func_id], True
#     # condition = {'m': 125, 'g': 50, 'b': units.Protoss.Gateway, 't': 42, 's': 2},
#     cs = conditions
#     valid = False if ('m' in cs.keys() and m < cs['m']) else valid
#     valid = False if ('g' in cs.keys() and g < cs['g']) else valid
#     valid = False if ('s' in cs.keys() and s < cs['s']) else valid
#     valid = False if ('b' in cs.keys() and not all_building_condition_reached(cs['b'], building_types)) else valid
#     valid = False if ('u' in cs.keys() and cs['u'] not in u) else valid
#     if valid:
#       valid_action_names.append(action['name'])
#
#   return valid_action_names
