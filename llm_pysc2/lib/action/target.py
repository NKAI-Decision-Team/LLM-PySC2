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


from llm_pysc2.lib.utils import *

from pysc2.lib import features # units, actions, features, buffs, upgrades


from loguru import logger
import numpy as np
import random
import math
import re


def tag_for_idle_unit(obs, unit_type, queued_source_unit_tag_list):
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100 and unit.active == 0 \
        and unit_type is not None and unit.unit_type == unit_type and unit.tag not in queued_source_unit_tag_list:
      return unit.tag
  return None


def tag_for_easy_build_protoss(obs):  # 查找周围空间较大的pylon的screen坐标(先求tag再screen), 然后通过随机坐标甩到周围去
  all_building_list, all_resource_list, base_list, pylon_list = [], [], [], []
  all_building_pos_list, all_resource_pos_list, base_pos_list, pylon_pos_list = [], [], [], []
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF:  #  and unit.build_progress == 100
      if unit.unit_type in MINERAL_TYPE + GAS_TYPE + GAS_BUILDING_TYPE:
        all_resource_list.append(unit)
        all_resource_pos_list.append([unit.x, unit.y])
      if unit.unit_type in BUILDING_TYPE:
        all_building_list.append(unit)
        all_building_pos_list.append([unit.x, unit.y])
      if unit.unit_type in BASE_BUILDING_TYPE:
        base_list.append(unit)
        base_pos_list.append([unit.x, unit.y])
      if unit.unit_type in [units.Protoss.Pylon]:
        pylon_list.append(unit)
        pylon_pos_list.append([unit.x, unit.y])

  counts, index = get_nearby_unit_num_of_unit(all_building_pos_list, base_pos_list, r=12, flag='min')
  tag = None if counts == 0 else base_list[index].tag

  if counts <= 16 and tag is not None:
    return base_list[random.randint(0, len(base_list) - 1)].tag
  # if 8 < counts <= 16 and tag is not None:
  #   return tag
  # if 10 < counts <= 16 and tag is not None:
  #   return base_list[random.randint(0, len(base_list) - 1)].tag
  if counts > 16 and tag is not None:
    unit_pos_list = all_resource_pos_list + all_resource_pos_list + all_building_pos_list
    counts, index = get_nearby_unit_num_of_unit(unit_pos_list, pylon_pos_list, r=7, flag='min')
    tag = None if counts == 0 else pylon_list[index].tag
    if 1 < counts < 4:
      return tag
    else:
      return base_list[random.randint(0, len(base_list) - 1)].tag


def tag_for_easy_build_pylon(obs):  # 查找周围空间较大的nexus的screen坐标(先求tag再screen), 然后通过随机坐标甩到周围去
  base_list, pylon_list = [], []
  base_pos_list, pylon_pos_list = [], []
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF:  #  and unit.build_progress == 100
      if unit.unit_type in BASE_BUILDING_TYPE:
        base_list.append(unit)
        base_pos_list.append([unit.x, unit.y])
      if unit.unit_type in [units.Protoss.Pylon]:
        pylon_list.append(unit)
        pylon_pos_list.append([unit.x, unit.y])
  counts, index = get_nearby_unit_num_of_unit(base_pos_list + pylon_pos_list, base_pos_list, r=12, flag='min')
  tag_for_base = None if counts == 0 else base_list[index].tag
  return tag_for_base

def tag_for_easy_build_base(obs):  # 查找最近的nexus坐标，和obs中的函数一个原理
  ves_new_base, ves_near, _, _ = get_ves_for_base_and_gas_building(obs)
  tag_for_base = None if len(ves_new_base) == 0 else ves_new_base[0].tag
  return tag_for_base

def tag_for_easy_build_gas(obs):  # 查找最近的vespene坐标，和obs中的函数一个原理
  ves_new_base, ves_near, _, _ = get_ves_for_base_and_gas_building(obs)
  tag_for_ves = None if len(ves_near) == 0 else ves_near[0].tag
  return tag_for_ves

def tag_for_easy_warp(obs, first_ctrl_base_tag='', first_oppo_base_tag=''):  # 查找距离一矿次远的水晶塔的tag
  first_ctrl_base_pos, first_oppo_base_pos = None, None
  all_unit_list, base_list, pylon_list = [], [], []
  all_unit_tag_list, base_tag_list, pylon_tag_list = [], [], []
  all_unit_pos_list, base_pos_list, pylon_pos_list = [], [], []
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100:
      all_unit_list.append(unit)
      all_unit_tag_list.append(unit.tag)
      all_unit_pos_list.append([unit.x, unit.y])
      if unit.unit_type in BASE_BUILDING_TYPE:
        base_list.append(unit)
        base_tag_list.append(unit.tag)
        base_pos_list.append([unit.x, unit.y])
      if unit.unit_type in [units.Protoss.Pylon, units.Protoss.WarpPrismPhasing]:
        pylon_list.append(unit)
        pylon_tag_list.append(unit.tag)
        pylon_pos_list.append([unit.x, unit.y])
      # if unit.tag == first_ctrl_base_tag:
      #   first_ctrl_base_pos = [unit.x, unit.y]
      # if unit.tag == first_oppo_base_tag:
      #   first_oppo_base_pos = [unit.x, unit.y]

  tag_for_pylon = None
  if tag_for_pylon is None:
    counts, index = get_nearby_unit_num_of_unit(all_unit_pos_list, pylon_pos_list, r=7, flag='min')
    tag_for_pylon = None if counts == 0 else pylon_list[index].tag

  # if first_oppo_base_pos is not None:
  #   d_min, index_min = get_dis_pos_poses1(first_oppo_base_pos, base_pos_list, 'min')
  #   tag_for_pylon = None if d_min == 0 else pylon_list[index_min].tag

  return tag_for_pylon


def tag_for_closest_unit(obs, tag, unit_type):
  target_unit = None
  unit_list, unit_pos_list = [], []
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100:
      if unit.unit_type == unit_type:
        unit_list.append(unit)
        unit_pos_list.append([unit.x, unit.y])
    if unit.tag == tag:
      target_unit = unit
  if target_unit is None or len(unit_list) == 0:
    return None, None
  pos = [target_unit.x, target_unit.y]
  d_min, index_min = get_dis_pos_poses1(pos, unit_pos_list, flag='min')
  tag_for_unit = None if d_min == 0 else unit_list[index_min].tag
  source_unit = None if d_min == 0 else unit_list[index_min]
  return tag_for_unit, source_unit


def tag_for_closest_worker(obs, tag, mining_only=True):
  target_unit = None
  worker_list, worker_pos_list = [], []
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100:
      if unit.unit_type in WORKER_TYPE:
        if mining_only and unit.order_id_0 in [356, 357, 358, 359, 102, 103, 154, 360, 361, 362]:
          worker_list.append(unit)
          worker_pos_list.append([unit.x, unit.y])
        if not mining_only:
          worker_list.append(unit)
          worker_pos_list.append([unit.x, unit.y])
  for unit in obs.observation.raw_units:
    if unit.tag == tag:
      target_unit = unit
  if target_unit is None or len(worker_list) == 0:
    return None
  pos = [target_unit.x, target_unit.y]
  d_min, index_min = get_dis_pos_poses1(pos, worker_pos_list, flag='min')
  tag_for_worker = None if d_min == 0 else worker_list[index_min].tag
  return tag_for_worker

def tag_for_closest_screen_worker(obs, screen, size_screen, mining_only=True):
  worker_list, worker_pos_list = [], []
  down_bound, up_bound = 0.1 * size_screen, 0.9 * size_screen
  for unit in obs.observation.feature_units:
    if not unit.is_on_screen or not (down_bound < unit.x < up_bound and down_bound < unit.y < up_bound):
      continue
    if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100:
      if unit.unit_type in WORKER_TYPE:
        if mining_only and unit.order_id_0 in [356, 357, 358, 359, 102, 103, 154, 360, 361, 362]:
          worker_list.append(unit)
          worker_pos_list.append([unit.x, unit.y])
        if not mining_only:
          worker_list.append(unit)
          worker_pos_list.append([unit.x, unit.y])

  d_min, index_min = get_dis_pos_poses1(screen, worker_pos_list, flag='min')
  tag_for_worker = None if d_min == 0 else worker_list[index_min].tag
  return tag_for_worker