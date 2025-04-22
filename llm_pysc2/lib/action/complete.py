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


from llm_pysc2.lib.action.utils import find_unit_type_the_func_belongs_to
from llm_pysc2.lib.action.target import *


from pysc2.lib import units, actions, features, buffs, upgrades
from pysc2.lib.actions import FUNCTIONS as F

from loguru import logger
import numpy as np
import random
import math
import re


def add_func_for_build(self, obs, action):
  return action

  # action_name = action['name']
  # action_arg = action['arg']
  # action_func = action['func']
  # if self.config.ENABLE_EASY_BUILD:
  #   return action
  # if (not 'Build_' in action_name) or ('Near' not in action_name and 'Screen' not in action_name):
  #   return action
  # if not (len(action['func'][0][2]) == 2 and len(action['func'][0][2][1]) == 2):
  #   return action
  # print(self.size_screen)
  # print(f"add_func_for_build(): screen = action['func'][0][2][1] = {action['func'][0][2][1]}")
  # screen = action['func'][0][2][1]
  # worker_tag = tag_for_closest_screen_worker(obs, screen, self.size_screen)
  #
  # if worker_tag is not None:
  #   full_shape_action = {'name': action_name, 'arg': [], 'func':
  #     [(3, F.select_rect, ['select', int(worker_tag), int(worker_tag)]),
  #      (action['func'][0][0], action['func'][0][1], action['func'][0][2])]}
  # else:
  #   return action

  return full_shape_action

def add_func_for_easy_build(self, obs, action):
  action_name = action['name']
  action_arg = action['arg']
  action_func = action['func']
  if (not 'Build_' in action_name) or ('Near' in action_name or 'Screen' in action_name) or not self.config.ENABLE_EASY_BUILD:
    return action

  target_position_tag, worker_tag = None, None
  # print(action_name)
  if action_name == 'Build_Nexus' or action_name == 'Build_Hatchery' or action_name == 'Build_CommandCenter':
    target_position_tag = tag_for_easy_build_base(obs)
  elif action_name == 'Build_Assimilator' or action_name == 'Build_Refinery' or action_name == 'Build_Extractor':
    target_position_tag = tag_for_easy_build_gas(obs)
  elif action_name == 'Build_Pylon':
    target_position_tag = tag_for_easy_build_pylon(obs)
  elif self.race == 'protoss':
    target_position_tag = tag_for_easy_build_protoss(obs)
  elif self.race == 'terran':
    # TODO: ADD SUPPORT FOR TERRAN EASY BUILD
    logger.error(f"[ID {self.log_id}] Agent {self.name}, add func for terran EASY BUILD actions not realized")
  elif self.race == 'zerg':
    # TODO: ADD SUPPORT FOR ZERG EASY BUILD
    logger.error(f"[ID {self.log_id}] Agent {self.name}, add func for zerg EASY BUILD actions not realized")
  else:
    pass
  worker_tag = tag_for_closest_worker(obs, target_position_tag)

  l = self.size_screen
  dx = int(2 * (random.random() - 0.5) * 0.2 * l)
  dy = int(2 * (random.random() - 0.5) * 0.2 * l)
  # print(target_position_tag)
  # print(worker_tag)
  if target_position_tag is not None and worker_tag is not None:
    full_shape_action = {'name': action_name, 'arg': [], 'func':
      [(573, F.llm_pysc2_move_camera, [int(worker_tag)]),
       (573, F.llm_pysc2_move_camera, [int(worker_tag)]),
       (3, F.select_rect, ['select', int(worker_tag), int(worker_tag)]),
       (573, F.llm_pysc2_move_camera, [int(target_position_tag)]),
       (573, F.llm_pysc2_move_camera, [int(target_position_tag)]),
       (action['func'][0][0], action['func'][0][1], ['now', int(target_position_tag)])]}
  else:
    return action

  return full_shape_action

def add_func_for_easy_warp(self, obs, action):
  pylon_tag = tag_for_easy_warp(obs, self.first_ctrl_base_tag, self.first_oppo_base_tag)
  action_name = action['name']
  action_arg = action['arg']
  action_func = action['func']
  if not ('Warp_' in action_name and 'Near' not in action_name and self.config.ENABLE_EASY_WARP):
    return action

  if pylon_tag is not None:
    full_shape_action = {'name': action['name'], 'arg': [], 'func':
      [(8, F.select_warp_gates, ['select']),
       (573, F.llm_pysc2_move_camera, [int(pylon_tag)]),
       (action['func'][0][0], action['func'][0][1], ['now', int(pylon_tag)])]}
  else:
    full_shape_action = {'name': 'No_Operation', 'arg': [], 'func': [(0, actions.FUNCTIONS.no_op, {})]}

  return full_shape_action


# 补齐拖农民的前置函数
def add_func_for_select_workers(self, obs, action):

  action_name = action['name']
  action_arg = action['arg']
  action_func = action['func']
  if not ('Select_Workers_' in action_name):
    return action

  full_shape_action = None
  logger.debug(self.action_list)

  func_id, func, arg_type = action_func[0]
  source_unit_tag = None
  for unit in obs.observation.raw_units:
    down_bound, up_bound = 0.1 * self.size_screen, 0.9 * self.size_screen
    if unit.alliance == features.PlayerRelative.SELF and unit.unit_type in WORKER_TYPE and \
        unit.is_on_screen and (down_bound < unit.x < up_bound  and down_bound < unit.y < up_bound ):
      source_unit_tag = unit.tag
  if source_unit_tag is None:
    logger.error(
      f"[ID {self.log_id}] Agent {self.name}, Can not find source unit type for func {actions.FUNCTIONS[func_id].name}")
  else:
    logger.debug(f"[ID {self.log_id}] Agent {self.name}, find source unit worker {source_unit_tag}")

  if source_unit_tag is not None:
    full_shape_action = {'name': action_name, 'arg': [], 'func':
      [(2, actions.FUNCTIONS.select_point, ['select_all_type', int(source_unit_tag)])] + action['func']}
  else:
    full_shape_action = {'name': 'No_Operation', 'arg': [], 'func':
      [(0, actions.FUNCTIONS.no_op, {})]}

  return full_shape_action


# 补齐训练和升级的前置函数，移动相机到闲置建筑，并选择该建筑
def add_func_for_train_and_research(self, obs, action):
  # 该函数将train/research动作需要的move_camera和select动作补齐，
  #  补到self.text_func_list中，将它从单一的F.Train_xxx_quick/F.Research_xxx_quick变成三个动作

  action_name = action['name']
  action_arg = action['arg']
  action_func = action['func']
  if not ('Train_' in action_name or 'Research_' in action_name):
    return action

  # full_shape_action = None
  queued_source_unit_tag_list = []  # 已经准备训练/升级单位的建筑，用于避免重复选中
  logger.debug(self.action_list)

  func_id, func, arg_type = action_func[0]
  source_unit_type = find_unit_type_the_func_belongs_to(func_id, self.race)
  source_unit_tag = tag_for_idle_unit(obs, source_unit_type, queued_source_unit_tag_list)

  if source_unit_type is None:
    logger.error(
      f"[ID {self.log_id}] Agent {self.name}, Can not find source unit type for func {actions.FUNCTIONS[func_id].name}")
  elif source_unit_tag is None:
    logger.error(
      f"[ID {self.log_id}] Agent {self.name}, Can not find source unit of {str(units.get_unit_type(source_unit_type))} type")
  else:
    queued_source_unit_tag_list.append(source_unit_tag)

  if source_unit_tag is not None:
    full_shape_action = {'name': action_name, 'arg': [], 'func':
      [(573, actions.FUNCTIONS.llm_pysc2_move_camera, [int(source_unit_tag)]),
       (573, actions.FUNCTIONS.llm_pysc2_move_camera, [int(source_unit_tag)]),
       (2, actions.FUNCTIONS.select_point, ['select', int(source_unit_tag)])] + action['func']}
  else:
    full_shape_action = {'name': 'No_Operation', 'arg': [], 'func':
      [(0, actions.FUNCTIONS.no_op, {})]}

  return full_shape_action


def add_func_for_chrono_boost(self, obs, action):
  action_name = action['name']
  action_arg = action['arg']
  action_func = action['func']
  if not ('ChronoBoost_' in action_name) or self.race != 'protoss':
    return action

  source_unit_tag, target_unit_tag = None, None
  active_buildings_base, active_buildings_military, active_buildings_research = [], [], []
  for unit in obs.observation.raw_units:
    if unit.unit_type == units.Protoss.Nexus and unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100 and unit.energy > 50:
      source_unit_tag = unit.tag
    if unit.unit_type == units.Protoss.Nexus and unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100 and unit.active != 0 and unit.buff_id_0 == 0:
      active_buildings_base.append(unit.tag)
    if unit.unit_type in BUILDING_TYPE_MILITARY and unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100 and unit.active != 0 and unit.buff_id_0 == 0:
      active_buildings_military.append(unit.tag)
    if unit.unit_type in BUILDING_TYPE_RESEARCH and unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100 and unit.active != 0 and unit.buff_id_0 == 0:
      active_buildings_research.append(unit.tag)

  if 'ChronoBoost_Economy' in action_name and len(active_buildings_base) > 0 and len(active_buildings_military) == 0 and len(active_buildings_research) == 0:
    target_unit_tag = active_buildings_base[random.randint(0, len(active_buildings_base) - 1)]
  if 'ChronoBoost_Military' in action_name and len(active_buildings_military) > 0 and len(active_buildings_research) == 0:
    target_unit_tag = active_buildings_military[random.randint(0, len(active_buildings_military) - 1)]
  if 'ChronoBoost_Research' in action_name and len(active_buildings_research) > 0:
    target_unit_tag = active_buildings_research[random.randint(0, len(active_buildings_research) - 1)]

  if source_unit_tag is not None and target_unit_tag is not None:
    full_shape_action = {'name': action_name, 'arg': [], 'func':
      [(573, actions.FUNCTIONS.llm_pysc2_move_camera, [int(source_unit_tag)]),
       (573, actions.FUNCTIONS.llm_pysc2_move_camera, [int(source_unit_tag)]),
       (2, actions.FUNCTIONS.select_point, ['select', int(source_unit_tag)]),
       (573, actions.FUNCTIONS.llm_pysc2_move_camera, [int(target_unit_tag)]),
       (573, actions.FUNCTIONS.llm_pysc2_move_camera, [int(target_unit_tag)]),
       # (187, actions.FUNCTIONS.Effect_ChronoBoost_screen, ['now', int(target_unit_tag)]),
       (527, actions.FUNCTIONS.Effect_ChronoBoostEnergyCost_screen, ['now', int(target_unit_tag)]),
       ]}
  else:
    full_shape_action = {'name': 'No_Operation', 'arg': [], 'func':
      [(0, actions.FUNCTIONS.no_op, {})]}

  return full_shape_action


def add_func_for_easy_control(self, obs, action):  # goto enemy base
  action_name = action['name']
  action_arg = action['arg']
  action_func = action['func']
  if not ('All_Units_' in action_name or '_Scan' in action_name):
    return action

  easy_build = self.config.ENABLE_EASY_BUILD
  easy_control = self.config.ENABLE_EASY_CONTROL
  game_time_s = obs.observation.game_loop / 22.4
  idle_worker_count = obs.observation.player.idle_worker_count
  supply_used = obs.observation.player.food_used
  if 'All_Units_Defend' == action_name and ((game_time_s > 720 and supply_used > 120) or game_time_s > 900):
    action_name = 'All_Units_Attack'

  n_worker = 0
  first_ctrl_base_pos, first_oppo_base_pos = None, None
  target_tag = self.first_oppo_base_tag
  target_tag2 = None  # front line pylon

  enemy_combat_unit_list, enemy_combat_unit_pos_list = [], []
  enemy_building_list, enemy_building_pos_list = [], []
  enemy_worker_list, enemy_worker_pos_list = [], []

  combat_unit_list, combat_unit_pos_list = [], []
  worker_list, worker_pos_list = [], []

  all_defense_building_list, all_defense_building_pos_list = [], []
  all_pylon_list, all_pylon_pos_list = [], []
  all_base_list, all_base_pos_list = [], []
  all_ves_list, all_ves_pos_list = [], []

  for unit in obs.observation.raw_units:
    if unit.unit_type in BUILDING_TYPE and unit.alliance == features.PlayerRelative.ENEMY:
      enemy_building_list.append(unit)
      enemy_building_pos_list.append([unit.x, unit.y])
    if unit.unit_type in WORKER_TYPE and unit.alliance == features.PlayerRelative.ENEMY:
      enemy_worker_list.append(unit)
      enemy_worker_pos_list.append([unit.x, unit.y])
    if (unit.unit_type not in BUILDING_TYPE + WORKER_TYPE or unit.unit_type in BUILDING_TYPE_DEFENSE) and \
        unit.alliance == features.PlayerRelative.ENEMY:
      enemy_combat_unit_list.append(unit)
      enemy_combat_unit_pos_list.append([unit.x, unit.y])

    if unit.unit_type in WORKER_TYPE and unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100:
      n_worker += 1
      worker_list.append(unit)
      worker_pos_list.append([unit.x, unit.y])
    if unit.unit_type not in BUILDING_TYPE + WORKER_TYPE and unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100:
      combat_unit_list.append(unit)
      combat_unit_pos_list.append([unit.x, unit.y])

    if unit.unit_type in BASE_BUILDING_TYPE and unit.alliance == features.PlayerRelative.SELF:
      all_base_list.append(unit)
      all_base_pos_list.append([unit.x, unit.y])
    if unit.unit_type == units.Protoss.Pylon and unit.alliance == features.PlayerRelative.SELF:
      all_pylon_list.append(unit)
      all_pylon_pos_list.append([unit.x, unit.y])
    if unit.unit_type in BUILDING_TYPE_DEFENSE and unit.alliance == features.PlayerRelative.SELF:
      all_defense_building_list.append(unit)
      all_defense_building_pos_list.append([unit.x, unit.y])

    if unit.unit_type in GAS_TYPE:
      all_ves_list.append(unit)
      all_ves_pos_list.append([unit.x, unit.y])
    if unit.tag == self.first_ctrl_base_tag:
      first_ctrl_base_pos = [unit.x, unit.y]
    if unit.tag == self.first_oppo_base_tag:
      first_oppo_base_pos = [unit.x, unit.y]

  # Worker Scan
  if target_tag is None:
    logger.warning(f"[ID {self.log_id}] Agent {self.name}, add_func_for_easy_control(): Can not find enemy base, randomly choice a vespene as target for scan or attack")
    target_tag = all_ves_list[random.randint(0, len(all_ves_list) - 1)].tag
  worker_tag = tag_for_closest_worker(obs, target_tag, mining_only=False)

  # Defend concentrate
  if len(all_defense_building_pos_list) == 0:
    if first_oppo_base_pos is not None:
      d_min, index_min = get_dis_pos_poses1(first_oppo_base_pos, all_pylon_pos_list, flag='min')  # front line pylon
      target_tag2 = all_pylon_list[index_min].tag if d_min != 0 else self.first_oppo_base_tag
    else:
      d_max, indexes_max = get_dis_posse1_poses2(all_base_pos_list, all_pylon_pos_list, flag='max')
      target_tag2 = all_pylon_list[indexes_max[1]].tag if d_max != 0 else self.first_ctrl_base_tag
  else:
    if first_oppo_base_pos is not None:
      d_max, index_max = get_dis_pos_poses1(first_ctrl_base_pos, all_defense_building_pos_list, flag='max')  # front line pylon
      target_tag2 = all_defense_building_list[index_max].tag if d_max != 0 else self.first_oppo_base_tag
    else:
      d_max, indexes_max = get_dis_posse1_poses2(all_base_pos_list, all_defense_building_pos_list, flag='max')
      target_tag2 = all_defense_building_list[indexes_max[1]].tag if d_max != 0 else self.first_ctrl_base_tag

  # Attack Combat / Defend Combat
  a_ = combat_unit_center_pos = list(np.average(np.array(combat_unit_pos_list), axis=0)) if len(combat_unit_pos_list) > 0 else None
  b_ = enemy_combat_unit_center_pos = list(np.average(np.array(enemy_combat_unit_pos_list), axis=0)) if len(enemy_combat_unit_pos_list) > 0 else None
  combat_unit_center_distance = None
  if a_ is not None and b_ is not None:
    combat_unit_center_distance = math.sqrt((a_[0] - b_[0]) ** 2 + (a_[1] - b_[1]) ** 2)

  combat_unit_tag_to_attack = None
  if 'All_Units_Attack' in action_name:
    if combat_unit_center_pos is not None:
      d_min, index_min = get_dis_pos_poses1(combat_unit_center_pos, enemy_combat_unit_pos_list, flag='min')
      if combat_unit_center_distance is not None and (combat_unit_center_distance < 24 or 0 < d_min < 20):  # 已侦查到的主力距离在24单位内或者"主力"15单位距离内有敌人战斗单位
        combat_unit_tag_to_attack = enemy_combat_unit_list[index_min].tag
  if 'All_Units_Defend' in action_name:
    d_min, indexes_min = get_dis_posse1_poses2(all_base_pos_list, enemy_combat_unit_pos_list, flag='min')
    if 0 < d_min < 15:  # "基地"15单位距离内有敌人战斗单位
      unit_ = enemy_combat_unit_list[indexes_min[1]]
      combat_unit_tag_to_attack = unit_.tag
      c_ = combat_unit_pos_to_attack = [int(unit_.x), int(unit_.y)]
      if math.sqrt((c_[0] - b_[0]) ** 2 + (c_[1] - b_[1]) ** 2) > 24:
        combat_unit_tag_to_attack = None  # 攻击对象和已经侦查到的敌方主力相距超过24单位时，大概率是小股侦查，不予理会
    if combat_unit_center_pos is not None:
      d_min, index_min = get_dis_pos_poses1(combat_unit_center_pos, enemy_combat_unit_pos_list, flag='min')
      d_min2, index_min2 = get_dis_pos_poses1(combat_unit_center_pos, all_base_pos_list, flag='min')
      if combat_unit_tag_to_attack is None and combat_unit_center_distance is not None and \
          combat_unit_center_distance < 13 and 0 < d_min2 < 13:  # 主力附近遭遇敌方主力, 且主力距离基地的距离不超过24格
        combat_unit_tag_to_attack = enemy_combat_unit_list[index_min].tag

  full_shape_action = {'name': 'No_Operation', 'arg': [], 'func': [(0, actions.FUNCTIONS.no_op, {})]}

  def funcs_move_camera_to(tag):
    return [(573, F.llm_pysc2_move_camera, [int(tag)]), (573, F.llm_pysc2_move_camera, [int(tag)])]
  def funcs_select_army_and_move_camera_to(tag):
    return [(7, F.select_army, ['select'])] + funcs_move_camera_to(tag)
  def funcs_move_camera_to_and_select_unit(tag):
    return funcs_move_camera_to(tag) + [(2, F.select_point, ['select', int(tag)])]

  if ('All_Units_Attack' in action_name):
    supply = obs.observation.player.food_cap - obs.observation.player.food_used
    if target_tag is not None and obs.observation.player.food_used - n_worker > 50:  #
      if combat_unit_tag_to_attack is not None:
        target_tag = combat_unit_tag_to_attack
        full_shape_action = {'name': action_name, 'arg': [], 'func':
          funcs_select_army_and_move_camera_to(target_tag) + [(12, F.Attack_screen, ['now', int(target_tag)])]}
      else:
        full_shape_action = {'name': action_name, 'arg': [],  'func':
          funcs_select_army_and_move_camera_to(target_tag) + [(13, F.Attack_minimap, ['now', 'here'])]}

  elif ('All_Units_Defend' in action_name):
    if target_tag2 is not None:
      if combat_unit_tag_to_attack is not None:
        target_tag2 = combat_unit_tag_to_attack
        full_shape_action = {'name': action_name, 'arg': [], 'func':
          funcs_select_army_and_move_camera_to(target_tag2) + [(12, F.Attack_screen, ['now', int(target_tag2)])]}
      else:
        full_shape_action = {'name': action_name, 'arg': [], 'func':
          funcs_select_army_and_move_camera_to(target_tag2) + [(331, F.Move_screen, ['now', int(target_tag2)])]}

  elif ('All_Units_Retreat' in action_name):
    if target_tag2 is not None:
      full_shape_action = {'name': action_name, 'arg': [], 'func':
        funcs_select_army_and_move_camera_to(target_tag2) + [(331, F.Move_screen, ['now', int(target_tag2)])]}

  elif ('Worker_Scan' in action_name):  #  and idle_worker_count > 0  # game_time_s < 60 or int(game_time_s) % 90 < 20 or idle_worker_count > 2
      if target_tag is not None and target_tag2 is not None and worker_tag is not None:
        if easy_build and (game_time_s < 60 or int(game_time_s) % 90 < 20 or idle_worker_count > 2):
          full_shape_action = {'name': action_name, 'arg': [], 'func':
            funcs_move_camera_to_and_select_unit(worker_tag) + funcs_move_camera_to(target_tag) + [
              (331, F.Move_screen, ['now', int(target_tag)])]}
        elif not easy_build and idle_worker_count > 0:
          full_shape_action = {'name': action_name, 'arg': [], 'func':
            [(6, F.select_idle_worker, ('select'))] + funcs_move_camera_to(target_tag) + [
              (331, F.Move_screen, ['now', int(target_tag)])]}
        else:
          pass

  elif ('_Scan' in action_name) and int(game_time_s) % 90 < 20:

    if action_name == 'Adept_Scan':
      source_unit_tag, source_unit = tag_for_closest_unit(obs, target_tag, units.Protoss.Adept)
    elif action_name == 'Zealot_Scan':
      source_unit_tag, source_unit = tag_for_closest_unit(obs, target_tag, units.Protoss.Zealot)
    elif action_name == 'Observer_Scan':
      source_unit_tag, source_unit = tag_for_closest_unit(obs, target_tag, units.Protoss.Observer)
    else:
      source_unit_tag, source_unit = None, None

    if source_unit is None:
      print(f"complete.py: source_unit is None")
      return full_shape_action

    d_min, index_min = get_dis_pos_poses1([source_unit.x, source_unit.y], enemy_worker_pos_list, flag='min')
    target_tag, attack_worker = (enemy_worker_list[index_min].tag, True) if d_min != 0 else (target_tag, False)
    print(f"complete.py: {target_tag, target_tag2, worker_tag, combat_unit_tag_to_attack}")
    print(f"complete.py: XXX_Scan {source_unit_tag, source_unit.unit_type, target_tag, attack_worker, d_min}")

    if target_tag is not None and target_tag2 is not None and source_unit_tag is not None:
      if attack_worker:
        full_shape_action = {'name': action_name, 'arg': [], 'func':
          funcs_move_camera_to_and_select_unit(source_unit_tag) + funcs_move_camera_to(target_tag) +
          [(12, F.Attack_screen, ['now', int(target_tag)])]}
      else:
        full_shape_action = {'name': action_name, 'arg': [], 'func':
          funcs_move_camera_to_and_select_unit(source_unit_tag) + funcs_move_camera_to(target_tag) +
          [(13, F.Attack_minimap, ['now', 'here'])]}

  else:
    full_shape_action = {'name': 'No_Operation', 'arg': [], 'func': [
      (0, actions.FUNCTIONS.no_op, [])]}

  return full_shape_action