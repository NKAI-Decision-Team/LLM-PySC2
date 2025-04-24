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


from llm_pysc2.lib.action.utils import find_building_size
from llm_pysc2.lib.utils import *

from loguru import logger

import random
import math



def get_arg_screen_tag_build(obs, tag: int, size_screen, action_name, easy_build=True) -> (tuple, bool):

  if'Build_Nexus' in action_name or 'Build_Hatchery' in action_name or 'Build_CommandCenter' in action_name:
    pysc2_arg, func_valid = get_arg_screen_tag_base_building(obs, tag, size_screen, action_name)
  elif 'Build_Assimilator' in action_name or 'Build_Refinery' in action_name or 'Build_Extractor' in action_name:
    pysc2_arg, func_valid = get_arg_screen_tag_gas_building(obs, tag, size_screen, action_name)
  else:
    screen, unit_type = None, None
    for unit in obs.observation.feature_units:
      if unit.tag == tag:
        screen = [float(unit.x), float(unit.y)]
        unit_type = unit.unit_type
    # this func only called in easy build mode
    pysc2_arg, func_valid = get_arg_screen_build(obs, screen, size_screen, action_name, easy_build, tag=tag)
  if func_valid:
    return pysc2_arg, func_valid
  else:
    return f"auto build position, " + pysc2_arg, func_valid


# Parameter verification, for build
def get_arg_screen_build(obs, screen: list, size_screen, action_name, easy_build=False, tag=None, max_retry=144) -> (tuple, bool):  # 标准建造，校验地点和建造条件
  pos00 = [0, 0]
  if easy_build:
    building_name = action_name.split('_')[1]
    building_size = find_building_size(building_name)
    for unit in obs.observation.raw_units:
      if tag is not None and unit.tag == tag:
        pos00 = [unit.x, unit.y]
  else:
    building_name = action_name.split('_')[1]
    building_size = find_building_size(building_name)

  if building_size == 0:
    return f'Do not find the building named as {building_name}, action_name: {action_name}', False

  if isinstance(screen, list) and len(screen) == 2 and isinstance(screen[0], (int, float)) and isinstance(screen[1], (int, float)):
    x00 = int(min(max(0.1 * size_screen, screen[0] + 0 * (random.randint(0, 10) - 5)), 0.9 * size_screen))
    y00 = int(min(max(0.1 * size_screen, screen[1] + 0 * (random.randint(0, 10) - 5)), 0.9 * size_screen))
    if not easy_build:
      pos00 = [x00, y00]
    ratio = size_screen / SCREEN_WORLD_GRID
    pysc2_arg0, func_valid0 = 'unknown error in arg', False

    screen_m_pos, screen_g_pos, screen_base_pos, screen_pylon_pos, = [], [], [], []
    screen_building1_pos, screen_building2_pos, screen_building3_pos, screen_building5_pos = [], [], [], []
    pylon_in_construction = []
    unit_list = obs.observation.raw_units if easy_build else obs.observation.feature_units
    ratio_ = 1. if easy_build else ratio

    total_base, total_pylon, total_building = [], [], []
    for unit in obs.observation.raw_units:
      if unit.unit_type == units.Protoss.Pylon and unit.alliance in [1] and unit.build_progress != 100:
        pylon_in_construction.append(unit)
      if unit.unit_type == units.Protoss.Pylon and unit.alliance in [1]:
        total_pylon.append(unit)
      if unit.unit_type in BASE_BUILDING_TYPE and unit.alliance in [1]:
        total_base.append(unit)
      if unit.unit_type in BUILDING_TYPE and unit.alliance in [1]:
        total_building.append(unit)

    for unit in unit_list:
      if not unit.is_on_screen:
        continue
      if unit.unit_type in MINERAL_TYPE:
        screen_m_pos.append([unit.x / ratio_, unit.y / ratio_])
        screen_building2_pos.append([unit.x / ratio_, unit.y / ratio_])
      if (unit.unit_type in GAS_BUILDING_TYPE and unit.alliance in [1]) or unit.unit_type in GAS_TYPE:
        screen_g_pos.append([unit.x / ratio_, unit.y / ratio_])
        screen_building3_pos.append([unit.x / ratio_, unit.y / ratio_])
      if unit.unit_type in BASE_BUILDING_TYPE and unit.alliance in [1]:
        screen_base_pos.append([unit.x / ratio_, unit.y / ratio_])
      if unit.unit_type == units.Protoss.Pylon and unit.alliance in [1]:
        screen_pylon_pos.append([unit.x / ratio_, unit.y / ratio_])
      if unit.unit_type in BUILDING_TYPE:
        unit_name = str(units.get_unit_type(unit.unit_type)).split('.')[-1] if len(str(unit.unit_type).split('.')) > 0 else ''
        pos = [unit.x / ratio_, unit.y / ratio_]
        print(f"unit_name={unit_name} pos={pos}")
        if find_building_size(unit_name) == 1:
          screen_building1_pos.append(pos)
        if find_building_size(unit_name) == 2:
          screen_building2_pos.append(pos)
        if find_building_size(unit_name) == 3:
          screen_building3_pos.append(pos)
        if find_building_size(unit_name) == 5:
          screen_building5_pos.append(pos)

    for retry in range(max_retry):
      # r = 12 - retry // 12 - 3 * random.random() if building_name in ['Pylon']
      # rad = 2 * math.pi * random.random()  #  * random.random()  * ((retry % 20) / 20)
      # r = 11 - retry // n - 2 * random.random() if easy_build else retry // n
      # rad = ((retry % n) / n) * math.pi * 2
      if easy_build:
        length, r, rad = SCREEN_WORLD_GRID - 2, 0, 0
        i0, j0 = (0, 0) if retry == 0 else (length * (random.random()-0.5), length * (random.random()-0.5))
        # n = max_retry // 10
        # r = 3 * random.random() + retry // n
        # rad = 2 * math.pi * random.random()
        # i0, j0 = (0, 0) if retry == 0 else (r * math.cos(rad), r * math.sin(rad))
        if building_name in ['Pylon']:
          r = 11 - retry // 12 - 2 * random.random()
          rad = 2 * math.pi * random.random()  #  * random.random()  * ((retry % 20) / 20)
          i0, j0 = (0, 0) if retry == 0 else (r * math.cos(rad), r * math.sin(rad))
      else:
        n = max_retry // 10
        r = 1 * random.random() + retry // n
        rad = 2 * math.pi * random.random()
        i0, j0 = (0, 0) if retry == 0 else (r * math.cos(rad), r * math.sin(rad))

        # length, r, rad = SCREEN_WORLD_GRID, 0, 0
        # i0, j0 = (0, 0) if retry == 0 else (length * (random.random() - 0.5), length * (random.random() - 0.5))
        # if building_name in ['Pylon']:
        #   r = 12 - retry // 12 - 3 * random.random()
        #   rad = 2 * math.pi * random.random()  # * random.random()  * ((retry % 20) / 20)
        #   i0, j0 = (0, 0) if retry == 0 else (r * math.cos(rad), r * math.sin(rad))

      # x0 = int(min(max(0.1 * size_screen, x00 + ratio * i0), 0.9 * size_screen))
      # y0 = int(min(max(0.1 * size_screen, y00 + ratio * j0), 0.9 * size_screen))
      # x1_ = int(min(max(0.1 * size_screen, x0 - ratio * (1 + building_size / 2)), 0.9 * size_screen))
      # y1_ = int(min(max(0.1 * size_screen, y0 - ratio * (1 + building_size / 2)), 0.9 * size_screen))
      # x2_ = int(min(max(0.1 * size_screen, x0 + ratio * (1 + building_size / 2)), 0.9 * size_screen))
      # y2_ = int(min(max(0.1 * size_screen, y0 + ratio * (1 + building_size / 2)), 0.9 * size_screen))
      x0 = int(x00 + ratio * i0)
      y0 = int(y00 + ratio * j0)
      x1_ = int(x0 - ratio * (building_size // 2))
      y1_ = int(y0 - ratio * (building_size // 2))
      x2_ = int(x0 + ratio * (building_size // 2))
      y2_ = int(y0 + ratio * (building_size // 2))
      pysc2_arg, func_valid = (x0, y0), True
      down_bound, up_bound = (0, size_screen - 1) if building_size < 3 else (0.05 * size_screen, 0.95 * size_screen - 1)

      if not (down_bound < min(x0, y0, x1_, y1_, x2_, y2_) and max(x0, y0, x1_, y1_, x2_, y2_) < up_bound):
        pysc2_arg, func_valid = 'position out of boundary', False
        continue
      # x1, x2, y1, y2 = is_valid_screen_range(obs, [x0, y0], size_screen)

      if building_name in POWER_BUILDING_NAMES and obs.observation.feature_screen.power[x0][y0] == 0:
        pysc2_arg, func_valid = f'Build failed! ({int(x0 / ratio)}, {int(y0 / ratio)}) is not in power field, you need to build Pylon first or build near an existing Pylon', False
      if building_name in CREEP_BUILDING_NAMES and obs.observation.feature_screen.creep[x0][y0] == 0:
        pysc2_arg, func_valid = f'Build failed! ({int(x0 / ratio)}, {int(y0 / ratio)}) is not in creep, you need to create creep tumor by Queen', False

      pos0 = [pos00[0] + i0, pos00[1] + j0] if easy_build else [x0 / ratio_, y0 / ratio_]
      d1, d2 = get_dis_pos_poses1(pos0, screen_base_pos, 'min')[0], get_dis_pos_poses1(pos0, screen_m_pos, 'min')[0]
      d3, d4 = get_dis_pos_poses1(pos0, screen_g_pos, 'min')[0], get_dis_pos_poses1(pos0, screen_pylon_pos, 'min')[0]
      db1 = get_dis_pos_poses1_manhattan(pos0, screen_building1_pos, flag='min', axis='xy_max')[0]
      db2 = get_dis_pos_poses1_manhattan(pos0, screen_building2_pos, flag='min', axis='xy_max')[0]
      db3 = get_dis_pos_poses1_manhattan(pos0, screen_building3_pos, flag='min', axis='xy_max')[0]
      db5 = get_dis_pos_poses1_manhattan(pos0, screen_building5_pos, flag='min', axis='xy_max')[0]
      db2_pylon = get_dis_pos_poses1_manhattan(pos0, screen_pylon_pos, flag='min', axis='xy_max')[0]

      if func_valid and building_name == 'Pylon':
        supply = 7 * (1 + len(pylon_in_construction)) + obs.observation.player.food_cap - obs.observation.player.food_used
        if func_valid and len(screen_pylon_pos) != 0 and 0 < d4 < 6 and (len(screen_base_pos) == 0 or len(screen_pylon_pos) / len(screen_base_pos) < 6):  #     len(screen_pylon_pos) / len(screen_base_pos) < 6
          pysc2_arg, func_valid = f"Build failed! Too close to another Pylon", False
        if func_valid and len(total_base) == 1 and len(total_pylon) >= 2:  # and len(total_building) == len(total_pylon) + len(total_base)
          pysc2_arg, func_valid = f"Build failed! Too Many Pylon, you should build Nexus first", False
        if func_valid and 0 < obs.observation.player.food_used <= 50 and supply > 20 and obs.observation.player.minerals < 300:
          pysc2_arg, func_valid = f"Build failed! Too Many Pylon", False
        if func_valid and 50 < obs.observation.player.food_used < 100 and supply > 25 and obs.observation.player.minerals < 500:
          pysc2_arg, func_valid = f"Build failed! Too Many Pylon", False
        if func_valid and 100 <= obs.observation.player.food_used < 150 and supply > 50 and obs.observation.player.minerals < 750:
          pysc2_arg, func_valid = f"Build failed! Too Many Pylon", False
        if func_valid and obs.observation.player.food_cap == 200 and (len(screen_base_pos) != 0 and len(screen_pylon_pos) / len(screen_base_pos) > 6):
          pysc2_arg, func_valid = f"Build failed! Too Many Pylon", False

      if func_valid and 0 < db1 < (building_size + 1) / 2:
        pysc2_arg, func_valid = f"Build failed! Too close to another building", False
      if func_valid and 0 < db2 < (building_size + 2) / 2:
        pysc2_arg, func_valid = f"Build failed! Too close to another building", False
      if func_valid and 0 < db3 < (building_size + 3) / 2:
        pysc2_arg, func_valid = f"Build failed! Too close to another building", False
      if func_valid and 0 < db5 < (building_size + 5) / 2:
        pysc2_arg, func_valid = f"Build failed! Too close to another building", False
      if func_valid and (0 < d1 + d2 < 9):
        pysc2_arg, func_valid = f"Build failed! This location obstructs mining minerals", False
      if func_valid and (0 < d1 + d3 < 9):
        pysc2_arg, func_valid = f"Build failed! This location obstructs mining gas", False
      if func_valid and building_name in POWER_BUILDING_NAMES:
        if len(screen_pylon_pos) != 0 and not 2.0 < d4 < 5.4:  # 2.5 < d4 < 5.5
          pysc2_arg, func_valid = f"Build failed! Too far away from a Pylon", False
      # if func_valid and building_name in POWER_BUILDING_NAMES:
      #   if len(screen_pylon_pos) != 0 and not 0 < db2_pylon < 6:  # 2.5 < d4 < 5.5     0 < db2_pylon < 6
      #     pysc2_arg, func_valid = f"Build failed! Too far away from a Pylon", False


      for i in range(building_size + 1):
        for j in range(building_size + 1):
          if not func_valid:
            continue
          x = int(x1_ + i * ratio)
          y = int(y1_ + j * ratio)
          # x = int(x0 + i * ratio)
          # y = int(y0 + j * ratio)
          # x = int(min(max(0, x), size_screen - 1))
          # y = int(min(max(0, y), size_screen - 1))

          down_bound, up_bound = (0.03 * size_screen, 0.97 * size_screen - 1) if building_size < 3 else (0.05 * size_screen, 0.95 * size_screen - 1)
          if func_valid and not (down_bound < x < up_bound and down_bound <= y < up_bound):
            pysc2_arg, func_valid = 'out of boundary', False
          if func_valid and obs.observation.feature_screen.buildable[x][y] != 1:
            pysc2_arg, func_valid = f'Build failed! Area near ({int(x0 / ratio)}, {int(y0 / ratio)}) not buildable', False
          if func_valid and obs.observation.feature_screen.pathable[x][y] != 1:
            pysc2_arg, func_valid = f'Build failed! Area near ({int(x0 / ratio)}, {int(y0 / ratio)}) not pathable', False
          if func_valid and obs.observation.feature_screen.player_relative[x][y] not in [0, 1]:
            pysc2_arg, func_valid = f'Build failed! Area near ({int(x0 / ratio)}, {int(y0 / ratio)}) blocked', False
          if func_valid and obs.observation.feature_screen.height_map[x][y] != obs.observation.feature_screen.height_map[x00][y00]:
            pysc2_arg, func_valid = f'Build failed! Area ({int(x0 / ratio)}, {int(y0 / ratio)}) in different height', False
          if func_valid and obs.observation.feature_screen.placeholder[x][y] != 0:
            pysc2_arg, func_valid = f'Build failed! Area near ({int(x0 / ratio)}, {int(y0 / ratio)}) blocked by other building', False
      if func_valid or retry == 0:
        print(f"pos00, pos0, d1, d2, d3, d4 = {pos00}, {pos0}, {d1}, {d2}, {d3}, {d4}")
        print(f"db1, db2, db3, db5, n_pylon = {db1}, {db2}, {db3}, {db5} {screen_pylon_pos}")
        print(f"retry {retry}, r = {r}, rad = {rad}, deg = {math.degrees(rad)},  [x00, y00] = [{x00 / ratio}, {y00 / ratio}], [i0, j0] = [{i0}, {j0}], [x0, y0] = [{x0 / ratio}, {y0 / ratio}], pysc2_arg = {pysc2_arg}")
      if retry == 0:
        pysc2_arg0, func_valid0 = pysc2_arg, func_valid
      if not isinstance(pysc2_arg, str):
        return pysc2_arg, func_valid

    return pysc2_arg0, func_valid0
  return f'input arg error: screen={screen}', False


# Parameter verification, tag to screen coordinate, for base building
def get_arg_world_tag_base_building(obs, tag: int, x_offset, y_offset, world_range) -> (tuple, bool):

  def find_nearby_raw_mg(unit_g):
    # unit_info = f'unit {hex(unit_g.tag)}({str(units.get_unit_type(unit_g.unit_type))})'
    # logger.debug(f"[ID 1] find_nearby_world_mg, init g = {unit_info}, {unit_g.x}, {unit_g.y}")
    nearby_resource_unit_dict = {}
    for unit in obs.observation.raw_units:
      if unit.unit_type in MINERAL_TYPE:
        # unit_info = f'unit {hex(unit.tag)}({str(units.get_unit_type(unit.unit_type))})'
        # logger.debug(f"[ID 1] find_nearby_world_mg, m = {unit_info}, {unit.x}, {unit.y}")
        dist = math.sqrt((unit.x - unit_g.x) ** 2 + (unit.y - unit_g.y) ** 2)
        if dist < 16:
          nearby_resource_unit_dict[dist] = unit
      if unit.unit_type in GAS_TYPE:
        # unit_info = f'unit {hex(unit.tag)}({str(units.get_unit_type(unit.unit_type))})'
        # logger.debug(f"[ID 1] find_nearby_world_mg, m = {unit_info}, {unit.x}, {unit.y}")
        dist = math.sqrt((unit.x - unit_g.x) ** 2 + (unit.y - unit_g.y) ** 2)
        if dist < 16:
          nearby_resource_unit_dict[dist] = unit
    return nearby_resource_unit_dict.values()

  def artificial_force_field_iteration_world(unit_list, x, y):
    k, r, m = 0.5, 7, 1
    vespene_r, vespene_m = 8, 1
    mineral_r, mineral_m = 7, 1
    n, bad_n, fx, fy = 0, 0, 0, 0
    for unit in unit_list:
      bad = False
      if unit.unit_type in GAS_TYPE:
        r, m = vespene_r, vespene_m
      if unit.unit_type in MINERAL_TYPE:
        r, m = mineral_r, mineral_m
      d = math.sqrt((unit.x - x) ** 2 + (unit.y - y) ** 2)
      f = k * (r - d) * m
      fx += f * (x - unit.x) / d
      fy += f * (y - unit.y) / d
      n += 1
      if unit.unit_type in GAS_TYPE and not (7 < d < 10):
        bad = True
      if unit.unit_type in MINERAL_TYPE and not (6 < d < 9):
        bad = True
      if bad:
        bad_n += 1
    return (x + fx / n), (y + fy / n), bad_n

  for unit in obs.observation.raw_units:
    if unit.tag == tag:
      unit_info = f'unit {hex(unit.tag)}({str(units.get_unit_type(unit.unit_type))})'
      if unit.unit_type not in GAS_TYPE + MINERAL_TYPE:
        return f'{unit_info} is not VespeneGeyser', False
      mineral_list = find_nearby_raw_mg(unit)
      n, x0, y0 = 0, 0, 0
      for mineral in mineral_list:
        n += 1
        x0 += mineral.x
        y0 += mineral.y
      x0 = x0 / n
      y0 = y0 / n
      # logger.debug(f"[ID 1] x, y, n = {x0, y0, n}")
      for i in range(16):
        x0, y0, bad_n = artificial_force_field_iteration_world(mineral_list, x0, y0)
        # logger.debug(f"[ID 1] i, x, y, bad_n = {i, x0, y0, bad_n}")
      if not (isinstance(x0, float) and isinstance(y0, float)):
        tag = hex(tag) if isinstance(tag, int) else tag
        return f'unknown error in fing base_building position near unit {tag}', False
      x = int(x0 + x_offset)
      y = int(max(0, world_range - y0 + y_offset))
      return (x, y), True
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag} on screen', False


# Parameter verification, tag to screen coordinate, for base building
def get_arg_screen_tag_base_building(obs, tag: int, size_screen, action_name) -> (tuple, bool):
  def find_nearby_screen_mg(unit_g):
    # unit_info = f'unit {hex(unit_g.tag)}({str(units.get_unit_type(unit_g.unit_type))})'
    # logger.debug(f"[ID 1] find_nearby_screen_mg, init g = {unit_info}, {unit_g.x}, {unit_g.y}")
    ratio = size_screen / SCREEN_WORLD_GRID
    nearby_resource_unit_dict = {}
    for unit in obs.observation.feature_units:
      # unit_info = f'unit {hex(unit.tag)}({str(units.get_unit_type(unit.unit_type))})'
      if unit.unit_type in MINERAL_TYPE:
        # logger.debug(f"[ID 1] find_nearby_screen_mg, m = {unit_info}, {unit.x}, {unit.y}")
        dist = math.sqrt((unit.x - unit_g.x) ** 2 + (unit.y - unit_g.y) ** 2)
        if dist < 16 * ratio:
          nearby_resource_unit_dict[dist] = unit
      if unit.unit_type in GAS_TYPE:
        # logger.debug(f"[ID 1] find_nearby_screen_mg, g = {unit_info}, {unit.x}, {unit.y}")
        dist = math.sqrt((unit.x - unit_g.x) ** 2 + (unit.y - unit_g.y) ** 2)
        if dist < 16 * ratio:
          nearby_resource_unit_dict[dist] = unit
    return nearby_resource_unit_dict.values()

  def artificial_force_field_iteration_screen(unit_list, x, y):
    ratio = size_screen / SCREEN_WORLD_GRID
    k, r, m = 0.5, 7 * ratio, 1
    vespene_r, vespene_m = 8 * ratio, 1
    mineral_r, mineral_m = 8 * ratio, 1
    n, bad_n, fx, fy = 0, 0, 0, 0
    for unit in unit_list:
      bad = False
      if unit.unit_type in GAS_TYPE:
        r, m = vespene_r, vespene_m
      if unit.unit_type in MINERAL_TYPE:
        r, m = mineral_r, mineral_m
      d = math.sqrt((unit.x - x) ** 2 + (unit.y - y) ** 2)
      f = k * (r - d) * m
      fx += f * (x - unit.x) / d
      fy += f * (y - unit.y) / d
      n += 1
      if unit.unit_type in GAS_TYPE and not (7 * ratio < d < 10 * ratio):
        bad = True
      if unit.unit_type in MINERAL_TYPE and not (7 * ratio < d < 9 * ratio):
        bad = True
      if bad:
        bad_n += 1
    return (x + fx / n), (y + fy / n), bad_n

  building_name = action_name.split('_Screen')[0].split('_')[1]  # Build/Lock
  building_size = find_building_size(building_name)
  for unit in obs.observation.feature_units:
    if unit.tag == tag or (unit.unit_type in GAS_TYPE + MINERAL_TYPE and unit.is_on_screen):
      unit_info = f'unit {hex(unit.tag)}({str(units.get_unit_type(unit.unit_type))})'
      if unit.unit_type not in GAS_TYPE + MINERAL_TYPE:
        return f'{unit_info} is not VespeneGeyser', False
      mineral_gas_list = find_nearby_screen_mg(unit)
      n, x0, y0 = 0, 0, 0
      for mineral in mineral_gas_list:
        n += 1
        x0 += mineral.x
        y0 += mineral.y
      x = x0 / n
      y = y0 / n
      bad_n = len(mineral_gas_list)
      # logger.debug(f"[ID 1] x, y, n = {x, y, n}")
      for i in range(32):
        x, y, bad_n = artificial_force_field_iteration_screen(mineral_gas_list, x, y)
        # logger.debug(f"[ID 1] i, x, y, bad_n = {i, x, y, bad_n}")
      if not (isinstance(x, float) and isinstance(y, float)):
        tag = hex(tag) if isinstance(tag, int) else tag
        return f'unknown error in find base_building position near unit {tag}', False
      if not ((0 < x < size_screen) and (0 < y < size_screen)):
        return f'unknown error in find base_building position near unit {tag}', False
      x, y = int(min(max(0., x), size_screen - 1)), int(min(max(0., y), size_screen - 1))
      if bad_n >= 3:
        return f'({x}, {y}) may be a bad position for base building', False
      if not (0 < x < size_screen and 0 < y < size_screen):
        return f'({x}, {y}) too close to screen edge', False
      if obs.observation.feature_screen.buildable[x][y] != 1:
        return f'area near ({x}, {y}) not buildable', False
      if obs.observation.feature_screen.pathable[x][y] != 1:
        return f'area near ({x}, {y}) not pathable', False
      if obs.observation.feature_screen.player_relative[x][y] not in [0, 1]:
        return f'area near ({x}, {y}) not blocked', False
      if unit.is_on_screen and (0 < x < size_screen and 0 < y < size_screen):
        return (x, y), True
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag} on screen', False


def get_arg_screen_tag_gas_building(obs, tag: int, size_screen, action_name) -> (tuple, bool):

  # find vesoene gesyer raw_unit
  unit_r = None
  for unit in obs.observation.raw_units:
    if unit.tag == tag:
      unit_r = unit
  if unit_r is None:
    tag = hex(tag) if isinstance(tag, int) else tag
    return f'cannot find unit {tag}', False
  # confirm if is possible to construct
  for unit in obs.observation.feature_units:
    if unit.tag == tag:
      unit_info = f'unit {hex(unit.tag)}({str(units.get_unit_type(unit.unit_type))})'
      base_nearby = False
      for unit_ in obs.observation.raw_units:
        if unit_.alliance == features.PlayerRelative.SELF and unit_.unit_type in BASE_BUILDING_TYPE and \
            math.sqrt((unit_.x - unit_r.x) ** 2 + (unit_.y - unit_r.y) ** 2) < 10:
          base_nearby = True
      if not base_nearby:
        return f'{unit_info} is far away from our base building', False
      if unit.unit_type not in GAS_TYPE:
        return f'{unit_info} is not VespeneGeyser(342 344 608 880 881)', False
      if unit.is_on_screen and (0 < unit.x < size_screen and 0 < unit.y < size_screen):
        return (unit.x, unit.y), True
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag} on screen', False

