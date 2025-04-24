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


from pysc2.lib import units

from llm_pysc2.lib.action.check import check_attack_target, is_valid_screen_range
from llm_pysc2.lib.utils import SCREEN_WORLD_GRID, BOOSTABLE_TYPE, TRANSPORTER_TYPE

import numpy as np
import random
import math


def get_arg_world_tag(obs, tag: int, x_offset, y_offset, world_range) -> (tuple, bool):  # 获取指定tag单位的世界坐标
  for unit in obs.observation.raw_units:
    if unit.tag == tag:
      x = unit.x + x_offset
      y = max(0, world_range - unit.y + y_offset)
      return (x, y), True
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag}', False


def get_arg_world(obs, world: list, x_offset, y_offset, world_range) -> (tuple, bool):  # 获取指定tag单位的世界坐标
  if isinstance(world, list) and len(world) == 2 and isinstance(world[0], (int, float)) and isinstance(world[1],(int, float)):
    x = world[0]
    y = world[1]
    # there is no need for Move_Minimap action due to pretreatment
    return (x, y), True
  return f'wrong world position={world}', False


def get_arg_minimap_here(obs, size_minimap, action_name) -> (tuple, bool):
  arr = obs.observation['feature_minimap']['camera']
  idx = np.nonzero(arr)  # 获取特征图上非零值的坐标
  minimap_camera_x_predict = idx[:][1].mean()
  minimap_camera_y_predict = idx[:][0].mean()
  minimap = [int(minimap_camera_x_predict), int(minimap_camera_y_predict)]
  if 0 < minimap[0] < size_minimap and 0 < minimap[1] < size_minimap:
    return minimap, True
  return f'wrong minimap position={minimap}', False

# Parameter verification
def get_arg_minimap(obs, minimap: list, size_minimap, action_name) -> (tuple, bool):  # 小地图坐标，校验范围
  if isinstance(minimap, list) and len(minimap) == 2 and isinstance(minimap[0], (int, float)) and isinstance(minimap[1], (int, float)):
    x = int(min(max(0, minimap[0]), size_minimap))
    y = int(min(max(0, minimap[1]), size_minimap))
    if 'Attack' in action_name and obs.observation.feature_minimap.player_relative[x][y] in [1, 2]:
      return f'minimap ({x}, {y}) is alliance, can not attack alliance', False
    if 'Load' in action_name and obs.observation.feature_minimap.player_relative[x][y] not in [1, 2]:
      return f'minimap ({x}, {y}) is not alliance, can not load the target', False
    if 'Follow' in action_name and obs.observation.feature_minimap.player_relative[x][y] not in [1, 2]:
      return f'minimap ({x}, {y}) is not alliance, can not follow the target', False
    # there is no need for Move_Minimap action due to pretreatment
    return (x, y), True
  return f'input arg error: minimap={minimap}', False


# Parameter verification
def get_arg_screen(obs, screen: list, size_screen, action_name) -> (tuple, bool):  # 屏幕坐标，校验范围
  if isinstance(screen, list) and len(screen) == 2 and isinstance(screen[0], (int, float)) and isinstance(screen[1], (int, float)):
    x = int(min(max(0, screen[0]), size_screen))
    y = int(min(max(0, screen[1]), size_screen))
    ratio = size_screen / SCREEN_WORLD_GRID
    if 'Attack' in action_name and obs.observation.feature_screen.player_relative[x][y] in [1, 2]:
      return f'screen ({x}, {y}) is alliance, can not attack alliance', False
    if 'Load' in action_name and obs.observation.feature_screen.player_relative[x][y] not in [1, 2]:
      return f'screen ({x}, {y}) is not alliance, can not load the target', False
    if 'Follow' in action_name and obs.observation.feature_screen.player_relative[x][y] not in [1, 2]:
      return f'screen ({x}, {y}) is not alliance, can not follow the target', False
    if 'Move' in action_name:
      x1, x2, y1, y2 = is_valid_screen_range(obs, [x, y], size_screen)
      if not ((x1 <= x <= x2) or (y1 <= y <= y2)):
        return f'Move failed! x({int(x/ratio)}) and y({int(y/ratio)}) coordinate exceeds the boundary, valid ranges are **{int(x1/ratio)}<x<{int(x2/ratio)}**, **{int(y1/ratio)}<y<{int(y2/ratio)}**', False
      if not (x1 <= x <= x2):
        return f"Move failed! x({int(x/ratio)}) exceeds the boundary, valid range is **{int(x1/ratio)}<x<{int(x2/ratio)}**", False
      if not (y1 <= y <= y2):
        return f"Move failed! y({int(y/ratio)}) exceeds the boundary, valid range is **{int(y1/ratio)}<y<{int(y2/ratio)}**", False
    return (x, y), True
  return f'input arg error: screen={screen}', False


# Parameter verification, tag to screen coordinate
def get_arg_screen_tag(obs, tag: int, size_screen, action_name) -> (tuple, bool):  # 获取指定tag单位的屏幕坐标
  for unit in obs.observation.feature_units:
    if unit.tag == tag:
      unit_info = f'unit {hex(tag)}({str(units.get_unit_type(unit.unit_type))})'
      if 'Attack' in action_name:
        if unit.alliance in [1, 2]:
          return f'{unit_info} is alliance', False
        target_can_be_attack, error_info = check_attack_target(obs, tag)
        if not target_can_be_attack:
          return f'{error_info}: {unit_info}', False
      if 'Load' in action_name and unit.alliance not in [1]:
        return f'{unit_info} is not alliance', False
      if 'Follow' in action_name and unit.alliance not in [1, 2]:
        return f'{unit_info} is not alliance', False
      if 'MassRecall' in action_name and unit.alliance not in [1]:
        return f'{unit_info} is not alliance', False
      if 'Chrono_Boost' in action_name and (unit.alliance not in [1] or unit.unit_type not in BOOSTABLE_TYPE):
        return f'{unit_info} is not boostable', False
      if 'Board_' in action_name and (unit.alliance not in [1] or unit.unit_type not in TRANSPORTER_TYPE):
        return f'{unit_info} is not a transporter', False
      if unit.is_on_screen and (0 < unit.x < size_screen and 0 < unit.y < size_screen):
        return (unit.x, unit.y), True
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag} on screen', False


# Parameter verification, tag to rect screen coordinates
def get_arg_screen_tag_sclect_rect(obs, tag: int, size_screen, func_arg_name) -> (tuple, bool):  # 获取指定tag附近单位群的中心坐标
  for unit in obs.observation.feature_units:
    if unit.tag == tag:
      unit_info = f'unit {hex(tag)}({str(units.get_unit_type(unit.unit_type))})'
      if unit.alliance not in [1]:
        return f'{unit_info} is not alliance, can not select the unit', False
      if not (0 < unit.x < size_screen and 0 < unit.y < size_screen):
        return f'{unit_info} ({unit.x}, {unit.y})) not no screen', False
      if func_arg_name == 'screen' and unit.is_on_screen:
        x = max(0, min(int(unit.x - size_screen / 64), size_screen - 1))
        y = max(0, min(int(unit.y - size_screen / 64), size_screen - 1))
        return (x, y), True
      if func_arg_name == 'screen2' and unit.is_on_screen:
        x = max(0, min(int(unit.x + size_screen / 64), size_screen - 1))
        y = max(0, min(int(unit.y + size_screen / 64), size_screen - 1))
        return (x, y), True
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag} on screen', False


# Parameter verification, tag to screen coordinate, for recall
def get_arg_screen_tag_recall(obs, tag: int, size_screen, action_name) -> (tuple, bool):  # 获取指定tag附近单位群的中心坐标
  for unit in obs.observation.feature_units:
    if unit.tag == tag:
      unit_info = f'unit {hex(unit.tag)}({str(units.get_unit_type(unit.unit_type))})'
      if unit.alliance not in [1]:
        return f'{unit_info} is not alliance', False
      if unit.is_on_screen and (0 < unit.x < size_screen and 0 < unit.y < size_screen):
        return (unit.x, unit.y), True
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag} on screen', False


# Parameter verification, tag to screen coordinate, for warp
def get_arg_screen_tag_warp(obs, tag: int, size_screen, action_name) -> (tuple, bool):  # 获取指定tag附近可折跃单位的坐标
  n = 0
  for unit in obs.observation.feature_units:
    max_try = 72
    if unit.tag == tag:
      unit_info = f'unit {hex(unit.tag)}({str(units.get_unit_type(unit.unit_type))})'
      if unit.unit_type not in [units.Protoss.Pylon, units.Protoss.WarpPrismPhasing]:
        return f'{unit_info} is not Pylon(60) or WarpPrismPhasing(136)', False
      elif unit.alliance not in [1]:
        return f'{unit_info} is not alliance', False
      else:
        radius = [2, 3, 4, 5, 6] if unit.unit_type == units.Protoss.Pylon else [1, 2, 3]
        angles = [0, 45, 90, 135, 180, 225, 270, 315]
        while n < max_try:
          r = radius[random.randint(0, len(radius) - 1)]
          a = angles[random.randint(0, len(angles) - 1)]
          x = int(unit.x + r * (size_screen / SCREEN_WORLD_GRID) * math.cos(math.radians(a)))
          y = int(unit.y + r * (size_screen / SCREEN_WORLD_GRID) * math.sin(math.radians(a)))
          if (0 < x < size_screen and 0 < y < size_screen) and \
              obs.observation.feature_screen.power[x][y] == 1 and \
              obs.observation.feature_screen.pathable[x][y] == 1 and \
              obs.observation.feature_screen.unit_type[x][y] == 0 and \
              obs.observation.feature_screen.build_progress[x][y] == 0 and \
              obs.observation.feature_screen.unit_shields[x][y] == 0:
            return (x, y), True
          else:
            n = n + 1
  if n == 36:
    return f'cannot find valid position to warp unit', False
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag} on screen', False