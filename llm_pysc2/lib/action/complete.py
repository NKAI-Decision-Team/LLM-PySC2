

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
  action_name = action['name']
  action_arg = action['arg']
  action_func = action['func']
  if self.config.ENABLE_EASY_BUILD:
    return action
  if (not 'Build_' in action_name) or ('Near' not in action_name and 'Screen' not in action_name):
    return action
  if not (len(action['func'][0][2]) == 2 and len(action['func'][0][2][1]) == 2):
    print(f"add_func_for_build(): screen = action['func'][0][2][1] = {action['func'][0][2][1]}")
    return action
  print(self.size_screen)
  print(f"add_func_for_build(): screen = action['func'][0][2][1] = {action['func'][0][2][1]}")
  screen = action['func'][0][2][1]
  worker_tag = tag_for_closest_screen_worker(obs, screen, self.size_screen)

  if worker_tag is not None:
    full_shape_action = {'name': action_name, 'arg': [], 'func':
      [(3, F.select_rect, ['select', int(worker_tag), int(worker_tag)]),
       (action['func'][0][0], action['func'][0][1], action['func'][0][2])]}
  else:
    return action

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


def add_func_for_easy_control(self, obs, action):  # goto enemy base
  action_name = action['name']
  action_arg = action['arg']
  action_func = action['func']
  if not ('All_Units_Attack' in action_name or 'Worker_Scan' in action_name or
          'All_Units_Retreat' in action_name or 'All_Units_Concentrate' in action_name or 'All_Units_Defend' in action_name):
    return action

  n_worker = 0
  for unit in obs.observation.raw_units:
    if unit.unit_type in WORKER_TYPE and unit.alliance == features.PlayerRelative.SELF:
      n_worker += 1

  first_ctrl_base_pos, first_oppo_base_pos = None, None
  target_tag = self.first_oppo_base_tag
  target_tag2 = None  # front line pylon
  all_pylon_list, all_pylon_pos_list = [], []
  all_base_list, all_base_pos_list = [], []
  all_ves_list, all_ves_pos_list = [], []
  for unit in obs.observation.raw_units:
    if unit.unit_type in BASE_BUILDING_TYPE and unit.alliance == features.PlayerRelative.SELF:
      all_base_list.append(unit)
      all_base_pos_list.append([unit.x, unit.y])
    if unit.unit_type == units.Protoss.Pylon and unit.alliance == features.PlayerRelative.SELF:
      all_pylon_list.append(unit)
      all_pylon_pos_list.append([unit.x, unit.y])
    if unit.unit_type in GAS_TYPE:
      all_ves_list.append(unit)
      all_ves_pos_list.append([unit.x, unit.y])
    if unit.tag == self.first_ctrl_base_tag:
      first_ctrl_base_pos = [unit.x, unit.y]
    if unit.tag == self.first_oppo_base_tag:
      first_oppo_base_pos = [unit.x, unit.y]

  if target_tag is None:
    logger.warning(f"[ID {self.log_id}] Agent {self.name}, add_func_for_easy_control(): Can not find enemy base, randomly choice a vespene as target for scan or attack")
    target_tag = all_ves_list[random.randint(0, len(all_ves_list) - 1)].tag

  worker_tag = tag_for_closest_worker(obs, target_tag, mining_only=False)

  # if first_ctrl_base_pos is not None:
  #   d_max, index_max = get_dis_pos_poses1(first_ctrl_base_pos, all_pylon_pos_list, flag='max')
  #   target_tag2 = all_pylon_list[index_max].tag if d_max != 0 else self.first_ctrl_base_tag
  if first_oppo_base_pos is not None:
    d_min, index_min = get_dis_pos_poses1(first_oppo_base_pos, all_pylon_pos_list, flag='min')  # front line pylon
    target_tag2 = all_pylon_list[index_min].tag if d_min != 0 else self.first_oppo_base_tag
  else:
    d_max, indexes_max = get_dis_posse1_poses2(all_base_pos_list, all_pylon_pos_list)
    target_tag2 = all_pylon_list[indexes_max[1]].tag if d_max != 0 else self.first_ctrl_base_tag

  full_shape_action = {'name': 'No_Operation', 'arg': [], 'func': [(0, actions.FUNCTIONS.no_op, {})]}
  if ('All_Units_Attack' in action_name):
    supply = obs.observation.player.food_cap - obs.observation.player.food_used
    print(target_tag, target_tag2, worker_tag)
    if target_tag is not None:  # and obs.observation.player.food_used - n_worker > 100 or supply < 10
      full_shape_action = {'name': action_name, 'arg': [], 'func': [
        (7, F.select_army, ['select']),
        (573, F.llm_pysc2_move_camera, [int(target_tag)]),
        (573, F.llm_pysc2_move_camera, [int(target_tag)]),
        (13, F.Attack_minimap, ('now', 'here')),
        # (12, F.Attack_screen, ('now', int(target_tag)))
      ]}
  elif ('Worker_Scan' in action_name):
    print(target_tag, target_tag2, worker_tag)
    if target_tag is not None and target_tag2 is not None and worker_tag is not None:
      full_shape_action = {'name': action_name, 'arg': [], 'func':
        [(573, F.llm_pysc2_move_camera, [int(worker_tag)]),
         (573, F.llm_pysc2_move_camera, [int(worker_tag)]),
         (2, F.select_point, ['select', int(worker_tag)]),
         (573, F.llm_pysc2_move_camera, [int(target_tag)]),
         (573, F.llm_pysc2_move_camera, [int(target_tag)]),
         (331, F.Move_screen, ('now', int(target_tag))),
         ]}
  elif ('All_Units_Retreat' in action_name or 'All_Units_Defend' in action_name):
    if target_tag2 is not None:
      full_shape_action = {'name': action_name, 'arg': [], 'func': [
        (7, F.select_army, ['select']),
        (573, F.llm_pysc2_move_camera, [int(target_tag2)]),
        (573, F.llm_pysc2_move_camera, [int(target_tag2)]),
        (331, F.Move_screen, ('now', int(target_tag2))),
        ]}
  else:
    full_shape_action = {'name': 'No_Operation', 'arg': [], 'func': [
      (0, actions.FUNCTIONS.no_op, [])]}
  return full_shape_action