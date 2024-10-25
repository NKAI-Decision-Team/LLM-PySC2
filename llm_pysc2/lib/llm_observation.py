# Copyright 2024, LLM-PySC2 Contributors. All Rights Reserved.
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

from llm_pysc2.lib.knowledge import protoss, zerg, terran
from llm_pysc2.lib.utils import *

from pysc2.lib import features, units, buffs
from pysc2.lib import renderer_human, colors

from PIL import ImageDraw, ImageFont, Image
from loguru import logger
import numpy as np
import pygame
import base64
import math
import glob
import io
import os


knowledge_dict = {}
knowledge_dict.update(protoss.DATA_PROTOSS)
knowledge_dict.update(terran.DATA_TERRAN)
knowledge_dict.update(zerg.DATA_ZERG)
unit_dict = {v: k for k, v in units.Neutral.__dict__.items() if
             isinstance(v, int)}
unit_dict.update({v: k for k, v in units.Protoss.__dict__.items()
                  if isinstance(v, int)})
unit_dict.update({v: k for k, v in units.Terran.__dict__.items()
                  if isinstance(v, int)})
unit_dict.update({v: k for k, v in units.Zerg.__dict__.items() if
                  isinstance(v, int)})


# def get_rgb_screen(obs) -> np.ndarray or None:
#   if hasattr(obs.observation, 'render_data') and hasattr(obs.observation.render_data, 'map'):
#     return obs.observation.render_data.map  # 返回RGB屏幕图像
#   else:
#     return None
#
# def get_rgb_minimap(obs) -> np.ndarray or None:
#   if hasattr(obs.observation, 'render_data') and hasattr(obs.observation.render_data, 'minimap'):
#     return obs.observation.render_data.minimap  # 返回RGB小地图图像
#   else:
#     return None

# def get_feature_map_screen(obs, feature_name: str) -> np.ndarray or None:
#   feature_layer = obs.observation.feature_screen
#   if hasattr(feature_layer, feature_name):
#     return getattr(feature_layer, feature_name)
#   else:
#     return None
#
# def get_feature_map_minimap(obs, feature_name: str) -> np.ndarray or None:
#   feature_layer = obs.observation.feature_minimap
#   if hasattr(feature_layer, feature_name):
#     return getattr(feature_layer, feature_name)
#   else:
#     return None

def get_img_obs_fea(self, obs):

  def draw_coordinate_axes(surf, screen_size):
    """在屏幕上绘制坐标轴和网格线，坐标范围固定为 0 到 128。"""
    # 固定坐标范围为 0 到 screen_size
    coord_range_x = screen_size
    coord_range_y = screen_size
    # 设置刻度和网格线数量
    num_ticks = 9  # 可以根据需要调整，例如设置为 9，则刻度为每 16 个单位
    # 计算固定坐标刻度，例如：[0, 16, 32, ..., 128]
    fixed_ticks_x = np.linspace(0, coord_range_x, num_ticks)
    fixed_ticks_y = np.linspace(0, coord_range_y, num_ticks)
    # 获取图像尺寸
    img_width, img_height = surf.surf.get_size()
    # 将固定坐标映射到图像像素位置
    x_positions = (fixed_ticks_x / coord_range_x) * img_width
    y_positions = (fixed_ticks_y / coord_range_y) * img_height
    # 绘制垂直网格线
    for x in x_positions:
        pygame.draw.line(surf.surf, colors.white, (x, 0), (x, img_height), 1)
    # 绘制水平网格线
    for y in y_positions:
        pygame.draw.line(surf.surf, colors.white, (0, y), (img_width, y), 1)
    # 尝试加载字体
    try:
        font = pygame.font.SysFont('arial', 12)
    except IOError:
        font = pygame.font.SysFont(None, 12)
    # 绘制 X 轴刻度标签
    for x, label in zip(x_positions, fixed_ticks_x.astype(int)):
        text_surface = font.render(str(label), True, colors.white)
        text_rect = text_surface.get_rect()
        # 调整标签位置，防止超出边界
        text_rect.topleft = (x + 2, 2)
        surf.surf.blit(text_surface, text_rect)
    # 绘制 Y 轴刻度标签
    for y, label in zip(y_positions, fixed_ticks_y.astype(int)):
        text_surface = font.render(str(label), True, colors.white)
        text_rect = text_surface.get_rect()
        # 调整标签位置，防止超出边界
        text_rect.topleft = (2, y + 2)
        surf.surf.blit(text_surface, text_rect)
    return surf

  """
  读取最新的综合特征图，并将其编码为 Base64 格式。
  """

  if isinstance(obs, list):
    observation = obs[0].observation
  else:
    observation = obs.observation
    logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: Accessed observation via obs.observation")
  # Log the keys of the observation (for debugging)
  logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: Observation keys: {list(observation.keys())}")

  # get surf from pysc2.lib.renderer_human.draw_screen.surf
  global_surf_screen = renderer_human.global_surf_screen
  if global_surf_screen is None:
    logger.error(f"[ID {self.log_id}] {self.name} enabled img feature map but can't get the img, check if --render in your command")
    return None

  # draw lines
  surf = draw_coordinate_axes(global_surf_screen, self.size_screen)

  # surf to img
  raw_str = pygame.image.tostring(surf.surf, 'RGB')
  img = Image.frombytes('RGB', surf.surf.get_size(), raw_str)

  # Save the image to a byte stream in memory
  buffered = io.BytesIO()
  img.save(buffered, format="PNG")
  buffered.seek(0)
  # Convert image byte stream to Base64 encoded string
  base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

  if self.config.ENABLE_SAVE_IMAGES:
    # Construct the save path, including the log directory, agent name, and "rgb_images" subdirectory
    image_save_dir = os.path.join(self.log_dir_path, f"{self.name}", "fea_images")
    os.makedirs(image_save_dir, exist_ok=True)
    # Construct the file name, including the step
    image_filename = f"fea_screen_loop{self.main_loop_step}_step{self.num_step}.png"
    image_path = os.path.join(image_save_dir, image_filename)
    # Save the image
    try:
      img.save(image_path)
      logger.info(
        f"[ID {self.log_id}] LLMAgent {self.name}: Saved feature map at step {self.num_step}, filename: {image_filename}")
    except Exception as e:
      logger.error(f"[ID {self.log_id}] LLMAgent {self.name}: Failed to save RGB image: {e}")

  return base64_image


# use in SubAgent
def get_img_obs_rgb(self, obs):
  """
  Extracts the RGB image from the observation, adds coordinate axes ranging from 0 to 128,
  and returns the Base64 encoded string of the processed image.
  If saving images is enabled in the configuration, the processed image is saved to a local file.
  """
  # Check the structure of the obs object
  if isinstance(obs, list):
    observation = obs[0].observation
  else:
    observation = obs.observation
    logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: Accessed observation via obs.observation")
  # Log the keys of the observation (for debugging)
  logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: Observation keys: {list(observation.keys())}")

  # Check if 'rgb_screen' is in the observation
  if 'rgb_screen' in observation:
    rgb_screen = observation['rgb_screen']
    logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: 'rgb_screen' is found in the observation.")
  else:
    logger.error(f"[ID {self.log_id}] LLMAgent {self.name}: 'rgb_screen' not found in the observation.")
    return None

  # Convert data type to uint8
  rgb_screen = rgb_screen.astype('uint8')
  # Convert NumPy array to PIL Image object
  rgb_screen = np.array(rgb_screen)[:, :, ::-1]  # BGR to RGB
  img = Image.fromarray(rgb_screen, 'RGB')
  # img = img.convert('RGB')
  # Get image dimensions
  img_width, img_height = img.size
  # Create a drawing object
  draw = ImageDraw.Draw(img)
  # Fixed coordinate range
  coord_range = self.size_screen  # Coordinate axes range from 0 to 128
  # Set the number of ticks and grid lines
  num_ticks = 9  # Adjust as needed
  # Compute fixed coordinate ticks, e.g., [0, 16, 32, ..., 128]
  fixed_ticks = np.linspace(0, coord_range, num_ticks)  # Fixed coordinate ticks
  # Map fixed coordinates to image pixel positions
  x_positions = (fixed_ticks / coord_range) * img_width  # Map to image x-axis positions
  y_positions = (fixed_ticks / coord_range) * img_height  # Map to image y-axis positions

  # Draw vertical grid lines
  for x in x_positions:
    draw.line([(x, 0), (x, img_height)], fill='white', width=1)
  # Draw horizontal grid lines
  for y in y_positions:
    draw.line([(0, y), (img_width, y)], fill='white', width=1)

  # Try to load a font
  try:
    font = ImageFont.truetype("arial.ttf", size=12)
    logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: Loaded 'arial.ttf' font for drawing text.")
  except IOError:
    # Use default font if specified font is not available
    font = ImageFont.load_default()
    logger.warning(f"[ID {self.log_id}] LLMAgent {self.name}: Could not load 'arial.ttf'. Using default font.")

  # Draw X-axis tick labels
  for x, label in zip(x_positions, fixed_ticks.astype(int)):
    # Adjust label position slightly to prevent clipping
    draw.text((x + 2, 2), str(label), fill='white', font=font)
  # Draw Y-axis tick labels
  for y, label in zip(y_positions, fixed_ticks.astype(int)):
    # Adjust label position slightly to prevent clipping
    draw.text((2, y + 2), str(label), fill='white', font=font)

  # Save the image to a byte stream in memory
  buffered = io.BytesIO()
  img.save(buffered, format="PNG")
  buffered.seek(0)

  # Convert image byte stream to Base64 encoded string
  base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
  # Save the image to a local file if saving is enabled in the configuration
  if self.config.ENABLE_SAVE_IMAGES:
    # Get the game loop step from the observation as the step information
    step = observation['game_loop'][0]
    # Construct the save path, including the log directory, agent name, and "rgb_images" subdirectory
    image_save_dir = os.path.join(self.log_dir_path, f"{self.name}", "rgb_images")
    os.makedirs(image_save_dir, exist_ok=True)
    # Construct the file name, including the step
    image_filename = f"rgb_screen_loop{self.main_loop_step}_step{step}.png"
    image_path = os.path.join(image_save_dir, image_filename)
    # Save the image
    try:
      img.save(image_path)
      logger.info(
        f"[ID {self.log_id}] LLMAgent {self.name}: Saved RGB image at step {step}, filename: {image_filename}")
    except Exception as e:
      logger.error(f"[ID {self.log_id}] LLMAgent {self.name}: Failed to save RGB image: {e}")

  return base64_image



def get_game_info(obs, agent) -> str:
  # obtain time info
  game_info = 'Game Info:'
  game_loop = obs.observation.game_loop
  game_s = str(int(game_loop / 22.4 % 60))  # SC2 runs at 22.4 game loops per second
  game_m = str(int(game_loop / 22.4 // 60))  # SC2 runs at 22.4 game loops per second
  if len(game_s) == 1:
    game_s = '0' + game_s
  game_info += f"\n\tTime: {game_m}:{game_s}"
  # obtain player info, for agents except combat group
  if 'CombatGroup' not in agent.name:
    player = obs.observation.player
    game_info += f"\n\tMinerals: {player.minerals}"
    game_info += f"\n\tVespene: {player.vespene}"
    game_info += f"\n\tSupply Total: {player.food_cap}"
    game_info += f"\n\tSupply Left: {player.food_cap - player.food_used}"
    game_info += f"\n\tSupply Used: {player.food_used}"
  return game_info


def get_single_unit_info(unit, team_unit_screen_coord=None, size_screen=None) -> str:

  unit_type_id = unit.unit_type
  unit_name = unit_dict.get(unit_type_id, "Unknown")

  # tag and pos
  unit_info = f"\n\t\tUnit: {unit_name}"
  if unit.unit_type not in UNIT_DONOT_NEED_TAG:
    unit_info += f"    Tag: {hex(unit.tag)}"
  unit_info += f"    ScreenPos: [{unit.x}, {unit.y}]"
  total_health = unit.health + unit.shield
  # distance to current team head unit
  if unit.unit_type not in UNIT_DONOT_NEED_DIS:
    if team_unit_screen_coord is not None and size_screen is not None:
      ratio = int(size_screen / SCREEN_WORLD_GRID)
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
      unit_info += f"    Weapon Locked by GravitonBeam Ability"
    elif unit.weapon_cooldown == 0:
      unit_info += f"    Weapon Ready"
    elif unit.weapon_cooldown > 0:
      unit_info += f"    Weapon Cooldown Time: {unit.weapon_cooldown / 22:.2f}s"
    else:
      pass
  if unit.build_progress == 100 and unit.buff_id_0 != 0:
    unit_info += f"    Buff: {str(buffs.Buffs(unit.buff_id_0))}"
  if unit.build_progress == 100 and unit.buff_id_1 != 0:
    unit_info += f" {str(buffs.Buffs(unit.buff_id_1))}"
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


# 获取所属单位的信息
def get_teams_info_with_knowledge(agent) -> str:

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
        teams_info += f"\n\nTeam {team['name']}-{i + 1} Info:"
      else:
        teams_info += f"\n\nTeam {team['name']} Info:"

      arr = obs.observation['feature_minimap']['camera']
      idx = np.nonzero(arr)  # 获取特征图上非零值的坐标
      minimap_x = int(idx[:][1].mean())
      minimap_y = int(idx[:][0].mean())
      teams_info += f"\n\tTeam minimap position: [{minimap_x}, {minimap_y}]"
      size_screen = obs.observation.feature_screen.height_map.shape[0]

      # controlled units
      for unit_type in ctrl_unit_type:
        for unit in obs.observation.feature_units:
          if unit.unit_type == unit_type and unit.is_on_screen and unit.alliance == features.PlayerRelative.SELF \
              and unit.is_selected and (0 < unit.x < size_screen and 0 < unit.y < size_screen):
            ctrl_units_info += get_single_unit_info(unit)
      if ctrl_units_info != '':
        teams_info += "\n\tControlled Team Units:"
        teams_info += ctrl_units_info

      # ally units
      for unit_type in ally_unit_type:
        for unit in obs.observation.feature_units:
          if unit.unit_type == unit_type and unit.is_on_screen and unit.alliance in [1, 2] and \
              not unit.is_selected and (0 < unit.x < size_screen and 0 < unit.y < size_screen):
            ally_units_info += get_single_unit_info(unit)
      if ally_units_info != '':
        teams_info += "\n\tNearby Ally Units:"
        teams_info += ally_units_info

      # enemy units
      for unit_type in enemy_unit_type:
        for unit in obs.observation.feature_units:
          if unit.unit_type == unit_type and unit.is_on_screen and unit.alliance == features.PlayerRelative.ENEMY and \
              (0 < unit.x < size_screen and 0 < unit.y < size_screen):
            enemy_units_info += get_single_unit_info(unit, ctrl_unit_screen_coord, size_screen)
      if enemy_units_info != '':
        teams_info += "\n\tNearby Enemy Units:"
        teams_info += enemy_units_info

  ctrl_unit_type_total = list(set(ctrl_unit_type_total))
  ally_unit_type_total = list(set(ally_unit_type_total))
  enemy_unit_type_total = list(set(enemy_unit_type_total))
  showed_unit = []

  # controlled units description and abilities
  unit_types_total = ctrl_unit_type_total + ally_unit_type_total + enemy_unit_type_total
  teams_info += f"\n\nRelevant Knowledge:"
  for unit_type in unit_types_total:
    if unit_type not in knowledge_dict.keys():
      logger.warning(f"[ID {agent.log_id}] do not find unit_type {str(unit_type)} in knowledge_dict")
      continue
    if unit_type in showed_unit:
      continue
    if 'Protoss' in str(units.get_unit_type(unit_type)):
      teams_info += f"\n\t{str(units.Protoss(unit_type))}"
    if 'Terran' in str(units.get_unit_type(unit_type)):
      teams_info += f"\n\t{str(units.Terran(unit_type))}"
    if 'Zerg' in str(units.get_unit_type(unit_type)):
      teams_info += f"\n\t{str(units.Zerg(unit_type))}"

    if 'description' in knowledge_dict[unit_type].keys():
      teams_info += f"\n\t\t{knowledge_dict[unit_type]['description']}"
    else:
      logger.error(
        f"[ID {agent.log_id}] do not find description of {str(unit_type)} in knowledge_dict")

    unit_knowledge = knowledge_dict[unit_type]
    teams_info += f"\n\t\tUnit properties: {unit_knowledge['target_self'] + unit_knowledge['type_self']}"
    if 'weapon1_attack_range' in unit_knowledge.keys() and unit_knowledge['weapon1_attack_range'] not in [0, -1]:
      teams_info += f"\n\t\tWeapon info: Attack Range {unit_knowledge['weapon1_attack_range']}"
    if 'target' in unit_knowledge.keys() and len(unit_knowledge['target']) != 0:
      teams_info += f", target: {unit_knowledge['target']}"
    if 'type_anti' in unit_knowledge.keys() and len(unit_knowledge['type_anti']) != 0:
      teams_info += f", anti: {unit_knowledge['type_anti']}"
    if 'weapon1_attack' in unit_knowledge.keys() and unit_knowledge['weapon1_attack'] not in [0, -1]:
      teams_info += f", DPS(damage per second) {int(unit_knowledge['weapon1_attack'] * unit_knowledge['weapon1_attack_times'] / unit_knowledge['weapon1_cooldown'])}"
    if 'weapon1_attack_bonus' in unit_knowledge.keys() and unit_knowledge['weapon1_attack_bonus'] not in [0, -1]:
      teams_info += f", DPS-anti {int((unit_knowledge['weapon1_attack'] + unit_knowledge['weapon1_attack_bonus']) * unit_knowledge['weapon1_attack_times'] / unit_knowledge['weapon1_cooldown'])}"
    if 'ability' in unit_knowledge.keys() and unit_type in ctrl_unit_type_total:
      teams_info += f"\n\t\tunit abilities:"
      for ability in unit_knowledge['ability'].keys():
        teams_info += f"\n\t\t\t{ability}: {unit_knowledge['ability'][ability]}"

    showed_unit.append(unit_type)

  return teams_info


# 根据obs获取合法动作，以文本格式输出，这个需要作为input prompt的一个独立部分
def get_valid_actions_from_obs(obs, agent) -> str:

  text_valid_actions = "\n\nValid Actions:"
  for team in agent.teams:
    team_obs_list = team['obs'] if (len(team['obs']) != 0 and len(team['unit_tags']) != 0) else None
    if team['select_type'] == 'select' and len(team['obs']) != len(team['unit_tags']) or team_obs_list is None:
      continue

    for i in range(len(team_obs_list)):

      # determine current controlled unit types
      ctrl_unit_type = []
      obs = team_obs_list[i]
      for unit in obs.observation.feature_units:
        if unit.is_on_screen and unit.is_selected and unit.tag in team['unit_tags']:
          ctrl_unit_type.append(unit.unit_type)
      ctrl_unit_type = list(set(ctrl_unit_type))

      # determine current team name
      team_name = f"Team {team['name']}-{i+1}" if team['select_type'] == 'select' else f"Team {team['name']}"
      text_valid_actions += f"\n\t{team_name} Valid Actions:"

      # reduce to team action space
      team_action_space = []
      for unit_type in ctrl_unit_type:
        if unit_type in agent.config.AGENTS[agent.name]['action'].keys():
          team_action_space += agent.config.AGENTS[agent.name]['action'][unit_type]
        else:
          logger.error(f"[ID {agent.log_id}] cannot get valid actions of unit_type {unit_type}")

      # reduce to obs.observation.available_actions
      valid_actions = []
      for action in team_action_space:
        valid = True
        for func_triple in action['func']:
          if func_triple[0] not in obs.observation.available_actions:
            valid = False
        if valid:
          valid_actions.append(action)

      # TODO: special actions
      #  这些动作是执行时临时选择建筑的，因此无法在obs中查看合法性，需要根据资源/前置条件/闲置建筑另行判断
      for action in team_action_space:
        if 'Build_' in action['name'] and '_Easy' in action['name']:  # enough minerals and gas, easy mode, do not select worker
          pass
        if 'Train_' in action['name']:  # enough minerals and gas, exist relevant building active == 0, and in power
          pass
        if 'WarpTrain_' in action['name']:  # enough minerals and gas, exist relevant building active == 0, and in power
          pass
        if 'Research_' in  action['name']:  # enough minerals and gas, exist relevant building active == 0, and in power
          pass

      # record valid actions
      for action in valid_actions:
        arg = action['arg']
        if len(arg) == 0:
          text_valid_actions += f"\n\t\t<{action['name']}()>"
        if len(arg) == 1:
          text_valid_actions += f"\n\t\t<{action['name']}({arg[0]})>"
        if len(arg) == 2:
          text_valid_actions += f"\n\t\t<{action['name']}({arg[0]}, {arg[1]})>"
        if len(arg) == 3:
          text_valid_actions += f"\n\t\t<{action['name']}({arg[0]}, {arg[1]}, {arg[2]})>"

  # record action arg explanation
  size_screen = obs.observation.feature_screen.height_map.shape[0]
  size_minimap = obs.observation.feature_minimap.height_map.shape[0]
  text_valid_actions += f"\n\nAction Args: "
  text_valid_actions += f"\n\t(1) tag: tag refers to a hexadecimal number, shape as 0x000000000."
  text_valid_actions += f"\n\t(2) screen: screen refers to a screen coordinate, shape as [x, y], where x and y range from 0 to {size_screen}."
  text_valid_actions += f"\n\t(3) minimap: minimap refers to a minimap coordinate, shape as [x, y], where x and y range from 0 to {size_minimap}."
  text_valid_actions += f"\nFor example, when you want to use an action like <Action_Name(tag, screen)>, you should output like <Action_Name(0x100580001, [37, 55])>; when you want to use an action like <Action_Name(screen)>, you should output like <Action_Name([66, 78])>. "
  text_valid_actions += f"What's more, You need to see clearly whether an action is using screen coordinates or minimap coordinates, If an action name as XXXX_Screen, it uses screen coordinate; if an action name as XXXX_Minimap, it uses minimap coordinate."
  return text_valid_actions


def get_last_action_info(agent) -> str:
  text_last_action = ""
  if isinstance(agent.last_text_a_pro, str) and len(agent.last_text_a_pro) > 0:
    text_last_action += f"\n\nLast Step {agent.last_text_a_pro}"
    text_last_action += f"\nYou need to confirm whether the previous action finished executing, and based on this, determine whether to continue the old strategy or immediately take other actions."
  return text_last_action


def get_task_info(agent) -> (str, int):

  task_info = ''
  for team in agent.config.AGENTS[agent.name]['team']:
    if 'task' in team.keys() and len(team['task']) > 0 and len(team['obs']) > 0:
      change_task = False
      task = None
      if team['select_type'] != 'select' or team['name'] == 'Empty':
        task = team['task'][0]
        obs = team['obs'][0]
        idx = np.nonzero(obs.observation['feature_minimap']['camera'])
        x, y = int(idx[:][1].mean()), int(idx[:][0].mean())
        if task['pos'] is not None:
          dist = math.sqrt((x - task['pos'][0]) ** 2 + (y - task['pos'][1]) ** 2)
          if dist < 4:
            change_task = True
        if len(team['task']) > 1:
          task1 = team['task'][1]
          if task1['time'] is not None and isinstance(task1['time'], str) and ':' in task1['time']:
            game_loop = obs.observation.game_loop
            game_s = int(game_loop / 22 % 60)  # SC2 runs at 22.4 game loops per second
            game_m = int(game_loop / 22 // 60)  # SC2 runs at 22.4 game loops per second
            if int(task1['time'].split(":")[0]) < game_m or \
              (int(task1['time'].split(":")[0]) == game_m and int(task1['time'].split(":")[1]) <= game_s):
              change_task = True
      if team['select_type'] == 'select':
        pass
      if change_task:
        team['task'].pop(0)
      if len(team['task']) > 0 and task is not None:
        if team['name'] != 'Empty':
          task_info += f"\n\tTeam {team['name']}' task: {task['info']}"
        if team['name'] == 'Empty':
          task_info += f"\n\tAgent task: {task['info']}"

  if len(task_info) > 0:
    task_info = f"\n\nTasks:" + task_info

  return task_info


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
    other_agents_info = "\n\nGlobal agent info:" + other_agents_info
  if len(other_agents_unit_knowledge) != 0:
    other_agents_unit_knowledge = f"\n\nRelevant Knowledge:" + other_agents_unit_knowledge

  return other_agents_info + other_agents_unit_knowledge


def get_alert_info(obs) -> str:   # for Commander only
  alert_info = ''

  arr = obs.observation['feature_minimap']['alerts']
  idx = np.nonzero(arr)  # 获取特征图上非零值的坐标
  for i in range(len(idx[0])):
    alert_info += f"\n\tEngage with enemies in minimap [{idx[1][i]}, {idx[0][i]}]"
  if len(alert_info) != 0:
    alert_info = "\n\nAlert Info:" + alert_info
  return alert_info


def get_warp_info(obs) -> str:  # for Developer only
  warp_source_info = ''
  pylon_info = ''
  prism_info = ''

  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.unit_type in [units.Protoss.WarpGate]:
      warp_source_info += f"\n\t{str(units.get_unit_type(unit.unit_type))}, "
      warp_source_info += f""  # Pysc2 do not provide cooldown status of warp gates

    if unit.alliance == features.PlayerRelative.SELF and unit.unit_type == units.Protoss.Pylon:
      pylon_info += f"\n\t{str(units.get_unit_type(unit.unit_type))}, tag:{hex(unit.tag)}"
    if unit.alliance == features.PlayerRelative.SELF and unit.unit_type == units.Protoss.WarpPrismPhasing:
      prism_info += f"\n\t{str(units.get_unit_type(unit.unit_type))}, tag:{hex(unit.tag)}"

  warp_target_info = pylon_info + prism_info
  if len(warp_source_info) > 0:
    warp_source_info = f"\n\nAvailable WarpGate:" + warp_source_info + f"\n{obs.observation.player.warp_gate_count} WarpGate in total"
  if len(warp_target_info) > 0:
    warp_target_info = f"\n\nAvailable WarpTrain Field Provider:" + warp_target_info

  return warp_source_info + warp_target_info


class BaseTranslatorO:

  def __init__(self):
    pass

  def translate(self, agent) -> str:
    return ''


class CombatGroupTranslatorO(BaseTranslatorO):

  def __init__(self, name, log_id, config):
    super(CombatGroupTranslatorO, self).__init__()
    self.agent_name = name
    self.log_id = log_id
    self.config = config
    logger.info(f"[ID {log_id}] {name} CombatGroupTranslatorO initialized")

  def translate(self, agent) -> str:

    obs_list = agent.team_unit_obs_list
    text_obs = ""

    if not isinstance(obs_list, list) or len(obs_list) < 1:
      return f"obs_list error, no obs found"

    # general information
    obs = obs_list[0]
    game_info = get_game_info(obs, agent)
    units_info = get_teams_info_with_knowledge(agent)
    valid_actions = get_valid_actions_from_obs(obs, agent)
    last_action_info = get_last_action_info(agent)
    task_info = get_task_info(agent)
    text_obs = game_info + units_info + valid_actions + last_action_info + task_info

    # add communication info
    if agent.config.ENABLE_COMMUNICATION:
      communication_info = get_communication_info(agent)
      text_obs += communication_info

    # final info
    text_obs += f"\n\nGive each team no more than {agent.config.MAX_NUM_ACTIONS} actions, among which " \
                f"activity release should usually before move and attack."
    if agent.config.ENABLE_COMMUNICATION:
      text_obs += f"\nNow, start generating your analysis, actions and communication:"
    else:
      text_obs += f"\nNow, start generating your analysis and actions:"

    return text_obs


class CommanderTranslatorO(BaseTranslatorO):

  def __init__(self, name, log_id, config):
    super(CommanderTranslatorO, self).__init__()
    self.agent_name = name
    self.log_id = log_id
    self.config = config
    logger.info(f"[ID {log_id}] {name} CommanderTranslatorO initialized")

  def translate(self, agent) -> str:
    obs_list = agent.team_unit_obs_list
    text_obs = ""

    if not isinstance(obs_list, list) or len(obs_list) < 1:
      return f"obs_list error, no obs found"

    # general information
    obs = obs_list[0]
    game_info = get_game_info(obs, agent)
    other_agents_info = get_other_agents_info(agent)
    task_info = get_task_info(agent)
    alert_info = get_alert_info(obs)
    text_obs = game_info + other_agents_info + alert_info + task_info

    # add communication info
    if agent.config.ENABLE_COMMUNICATION:
      communication_info = get_communication_info(agent)
      text_obs += communication_info

    # final info
    text_obs += f"\n\nAs the supreme military commander, you should not directly give actions, instead, tell your subordinates what to do through communication."
    text_obs += f"\nNow, start analysis, making macro decisions in military deployments by sending message to other agents:"

    return text_obs


class DeveloperTranslatorO(BaseTranslatorO):

  def __init__(self, name, log_id, config):
    super(DeveloperTranslatorO, self).__init__()
    self.agent_name = name
    self.log_id = log_id
    self.config = config
    logger.info(f"[ID {log_id}] {name} DeveloperTranslatorO initialized")

  def translate(self, agent) -> str:
    obs_list = agent.team_unit_obs_list
    text_obs = ""

    if not isinstance(obs_list, list) or len(obs_list) < 1:
      return f"obs_list error, no obs found"

    # general information
    obs = obs_list[0]
    game_info = get_game_info(obs, agent)
    # units_info = get_teams_info_with_knowledge(agent)
    valid_actions = get_valid_actions_from_obs(obs, agent)
    last_action_info = get_last_action_info(agent)
    task_info = get_task_info(agent)
    warp_info = get_warp_info(obs)
    text_obs = game_info + valid_actions + last_action_info + task_info + warp_info

    # add communication info
    if agent.config.ENABLE_COMMUNICATION:
      communication_info = get_communication_info(agent)
      text_obs += communication_info

    # final info
    text_obs += f"\n\nAs a senior commander, the max number of your actions is not limited, " \
                f"when you warp units, try to use all the WarpGate as much as possible, " \
                f"and warp all units near a single WarpTrain Field Provider."
    if agent.config.ENABLE_COMMUNICATION:
      text_obs += f"\nNow, start generating your analysis, actions and communication:"
    else:
      text_obs += f"\nNow, start generating your analysis and actions:"

    return text_obs


# TODO: You can specialize your TranslatorO here


PROTOSS_FACTORY = {
  'default': CombatGroupTranslatorO,  # CombatGroup Observation
  'combatgroup': CombatGroupTranslatorO,  # CombatGroup Observation
  'commander': CommanderTranslatorO,  # only information relevant to macro decision, military
  'developer': DeveloperTranslatorO,  # only information relevant to macro decision, development
}
TERRAN_FACTORY = {}
ZERG_FACTORY = {}

FACTORY = {
  'protoss': PROTOSS_FACTORY,
  'terran': TERRAN_FACTORY,
  'zerg': ZERG_FACTORY,
}
