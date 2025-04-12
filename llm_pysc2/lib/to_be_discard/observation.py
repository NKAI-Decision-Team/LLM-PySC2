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

from llm_pysc2.lib import events
from llm_pysc2.lib.to_be_discard import llm_action
from llm_pysc2.lib.knowledge import protoss, zerg, terran
from llm_pysc2.lib.utils import *

from pysc2.lib import features, units, buffs, actions, upgrades
from pysc2.lib import renderer_human, colors

a = actions.FUNCTIONS
u = upgrades.Upgrades


from PIL import ImageDraw, ImageFont, Image, ImageEnhance
from loguru import logger
import numpy as np
import pygame
import base64
import math
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



def get_img_obs_fea(self, obs):

  def draw_coordinate_axes(surf, screen_size):
    """在屏幕上绘制坐标轴和网格线，坐标范围固定为 0 到 128。"""
    # 固定坐标范围为 0 到 screen_size
    # coord_range_x = screen_size
    # coord_range_y = screen_size
    coord_range_x = 24
    coord_range_y = 24
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


def get_img_obs_fea_map(self, obs, feature_map_name):
  if isinstance(obs, list):
    observation = obs[0].observation
  else:
    observation = obs.observation
    logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: Accessed observation via obs.observation")
  # Log the keys of the observation (for debugging)
  logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: Observation keys: {list(observation.keys())}")

  if feature_map_name in obs.observation.feature_screen._index_names[0].keys():
    feature_map_index = obs.observation.feature_screen._index_names[0][feature_map_name]
    fea_screen = observation.feature_screen[feature_map_index]
  else:
    return None

  # Convert data type to uint8
  # Convert NumPy array to PIL Image object
  # rgb_screen = np.array(rgb_screen)[:, :, ::-1]  # BGR to RGB
  if np.max(fea_screen) - np.min(fea_screen) != 0:
    fea_screen = (fea_screen - np.min(fea_screen)) * (255 / (np.max(fea_screen) - np.min(fea_screen)))
  fea_screen = fea_screen.T
  rgb_screen = np.array([fea_screen, fea_screen, fea_screen]).T
  rgb_screen = rgb_screen.astype('uint8')
  img = Image.fromarray(rgb_screen, 'RGB')
  # img = img.convert('RGB')
  # Get image dimensions
  img_width, img_height = img.size
  # Create a drawing object
  draw = ImageDraw.Draw(img)
  # Fixed coordinate range
  # coord_range = self.size_screen  # Coordinate axes range from 0 to 128
  coord_range = 24  # Coordinate axes range from 0 to 128
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
    image_save_dir = os.path.join(self.log_dir_path, f"{self.name}", f"{feature_map_name}")
    os.makedirs(image_save_dir, exist_ok=True)
    # Construct the file name, including the step
    image_filename = f"{feature_map_name}_loop{self.main_loop_step}_step{step}.png"
    image_path = os.path.join(image_save_dir, image_filename)
    # Save the image
    try:
      img.save(image_path)
      logger.info(
        f"[ID {self.log_id}] LLMAgent {self.name}: Saved RGB image at step {step}, filename: {image_filename}")
    except Exception as e:
      logger.error(f"[ID {self.log_id}] LLMAgent {self.name}: Failed to save RGB image: {e}")

  return base64_image

# use in SubAgent
def get_img_obs_rgb(self, obs):
  """
  Extracts the RGB image from the observation, adds coordinate axes ranging from 0 to {screen_size},
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
  # coord_range = self.size_screen  # Coordinate axes range from 0 to 128
  coord_range = 24  # Coordinate axes range from 0 to 128
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
    image_save_dir = os.path.join(self.log_dir_path, f"{self.name}", "rgb_screen")
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


def get_img_obs_rgb_minimap(self, obs):
  """
  Extracts the RGB image from the observation, adds coordinate axes ranging from 0 to {screen_size},
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
  if 'rgb_minimap' in observation:
    rgb_minimap = observation['rgb_minimap']
    logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: 'rgb_minimap' is found in the observation.")
  else:
    logger.error(f"[ID {self.log_id}] LLMAgent {self.name}: 'rgb_minimap' not found in the observation.")
    return None

  # Convert data type to uint8
  rgb_minimap = rgb_minimap.astype('uint8')
  # Convert NumPy array to PIL Image object
  rgb_minimap = np.array(rgb_minimap)[:, :, ::-1]  # BGR to RGB
  img = Image.fromarray(rgb_minimap, 'RGB')
  img = img.resize((4 * self.size_minimap, 4 * self.size_minimap), resample=Image.LANCZOS)
  enhancer = ImageEnhance.Brightness(img)
  img = enhancer.enhance(factor=3.0)
  # enhancer = ImageEnhance.Contrast(img)
  # img = enhancer.enhance(factor=2.0)
  # enhancer = ImageEnhance.Color(img)
  # img = enhancer.enhance(factor=1.8)

  # img = img.convert('RGB')
  # Get image dimensions
  img_width, img_height = img.size
  # Create a drawing object
  draw = ImageDraw.Draw(img)
  # Fixed coordinate range
  # coord_range = self.size_screen  # Coordinate axes range from 0 to 128
  coord_range = self.size_minimap  # Coordinate axes range from 0 to 128
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
    image_save_dir = os.path.join(self.log_dir_path, f"{self.name}", "rgb_minimap")
    os.makedirs(image_save_dir, exist_ok=True)
    # Construct the file name, including the step
    image_filename = f"rgb_minimap_loop{self.main_loop_step}_step{step}.png"
    image_path = os.path.join(image_save_dir, image_filename)
    # Save the image
    try:
      img.save(image_path)
      logger.info(
        f"[ID {self.log_id}] LLMAgent {self.name}: Saved RGB image at step {step}, filename: {image_filename}")
    except Exception as e:
      logger.error(f"[ID {self.log_id}] LLMAgent {self.name}: Failed to save RGB image: {e}")

  return base64_image



def get_game_info(agent) -> str:
  # obtain time info
  obs = agent.team_unit_obs_list[0]
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
  game_info += f"\n\n"
  return game_info


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
      teams_info += f"\n\tTeam minimap position: [{minimap_x}, {minimap_y}]"
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
      teams_info += f"\n\tTeam screen edge (screen coordinate range valid for actions): {int(edge_l/ratio)} < x < {int(edge_r/ratio)}, {int(edge_u/ratio)} < y < {int(edge_b/ratio)}"
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


def get_condition_elements(agent, obs=None) -> tuple:
  obs = agent.team_unit_obs_list[0] if obs is None else obs
  rc, tc, bc = {}, {}, {}
  rc.update(protoss.protoss_research_conditions)
  rc.update(terran.terran_research_conditions)
  rc.update(zerg.zerg_research_conditions)
  tc.update(protoss.protoss_train_conditions)
  tc.update(terran.terran_train_conditions)
  tc.update(zerg.zerg_train_conditions)
  bc.update(protoss.protoss_build_conditions)
  bc.update(terran.terran_build_conditions)
  bc.update(zerg.zerg_build_conditions)

  easy_build = agent.config.ENABLE_EASY_BUILD

  if agent.race == 'protoss':
    research_actions, train_actions = llm_action.PROTOSS_ACTION_RESEARCH, llm_action.PROTOSS_ACTION_TRAIN
    build_actions = llm_action.PROTOSS_ACTION_BUILD if not easy_build else llm_action.PROTOSS_ACTION_EASY_BUILD
  elif agent.race == 'terran':
    research_actions, train_actions = [], []
    build_actions = []
  elif agent.race == 'zerg':
    research_actions, train_actions = [], []
    build_actions = []
  else:
    research_actions, train_actions = llm_action.PROTOSS_ACTION_RESEARCH, llm_action.PROTOSS_ACTION_TRAIN
    build_actions = llm_action.PROTOSS_ACTION_BUILD if not easy_build else llm_action.PROTOSS_ACTION_EASY_BUILD
    logger.error(f"[ID {agent.log_id}] unknown agent.race: {agent.race}")

  player = obs.observation.player
  m = player.minerals  # mineral
  g = player.vespene  # gas
  s = player.food_cap - player.food_used  # supply
  u = obs.observation.upgrades  # upgrade
  b = []  # building

  obs = agent.team_unit_obs_list[0]
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100 and unit.active == 0 and \
        unit.unit_type in BUILDING_TYPE and unit.unit_type not in b:
      b.append(unit.unit_type)

  ra, ta, = research_actions, train_actions
  ba = build_actions + llm_action.PROTOSS_BASIC_ACTION_2 if agent.name == 'Builder' else build_actions
  return ra, ta, ba, rc, tc, bc, m, g, s, u, b


def map_research_quick_to_level(func_id, u) -> int:
  global_map = {}
  global_map.update(protoss.protoss_map_research_quick_to_level)
  global_map.update(terran.terran_map_research_quick_to_level)
  global_map.update(zerg.zerg_map_research_quick_to_level)
  if func_id in global_map.keys():
    func_id_level_low_to_up = global_map[func_id]
    for func_id_ in func_id_level_low_to_up:
      if func_id_ not in u:
        return func_id_
    return -1
  else:
    return func_id


def all_building_condition_reached(conditions_building_types, curr_building_types):
  for building_type in conditions_building_types:
    if building_type not in curr_building_types:
      return False
  return True


def get_valid_actions_build(agent) -> (list, str):
  obs = agent.team_unit_obs_list[0]
  _, _, ba, _, _, bc, m, g, s, u, b = get_condition_elements(agent)

  building_types = []
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100 and unit.unit_type in BUILDING_TYPE:
      building_types.append(unit.unit_type)

  valid_actions = []
  valid_actions_info = ''
  basic_actions_info = ''


  for action in ba:
    func_id, valid = action['func'][-1][0], True
    arg_to_show = '' if agent.config.ENABLE_EASY_BUILD else action['arg'][0]
    if func_id in bc.keys():
      conditions = bc[func_id]
      # condition = {'m': 175, 'g': 175, 'b': units.Protoss.CyberneticsCore, 'u': u.ProtossAirArmorsLevel1, 't': 215},
      cs = conditions
      valid = False if ('m' in cs.keys() and m < cs['m']) else valid
      valid = False if ('g' in cs.keys() and g < cs['g']) else valid
      valid = False if ('s' in cs.keys() and s < cs['s']) else valid
      valid = False if ('b' in cs.keys() and not all_building_condition_reached(cs['b'], building_types)) else valid
      valid = False if ('u' in cs.keys() and cs['u'] not in u) else valid
      if valid:
        valid_actions.append(action)
        valid_actions_info += f"\n\t\t<{action['name']}({arg_to_show})> \t\t cost: mineral{cs['m']}, gas{cs['g']}, time{cs['t']}s"
    else:
      valid_actions.append(action['name'])
      basic_actions_info += f"\n\t\t<{action['name']}({arg_to_show})> "

  # if valid_actions_info != '':
  #   valid_actions_info = "Valid Research Actions: " + valid_actions_info + "\n\n"
  return valid_actions, basic_actions_info + valid_actions_info


def get_valid_actions_research(agent) -> (list, str):
  obs = agent.team_unit_obs_list[0]
  ra, _, _, rc, _, _, m, g, s, u, b = get_condition_elements(agent)

  building_types = []
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100 and unit.unit_type in BUILDING_TYPE:
      building_types.append(unit.unit_type)

  valid_actions = []
  valid_actions_info = ''
  for action in ra:
    func_id = map_research_quick_to_level(action['func'][0][0], u)
    if func_id == -1:
      continue
    conditions, valid = rc[func_id], True
    # condition = {'m': 175, 'g': 175, 'b': units.Protoss.CyberneticsCore, 'u': u.ProtossAirArmorsLevel1, 't': 215},
    cs = conditions
    valid = False if ('m' in cs.keys() and m < cs['m']) else valid
    valid = False if ('g' in cs.keys() and g < cs['g']) else valid
    valid = False if ('s' in cs.keys() and s < cs['s']) else valid
    valid = False if ('b' in cs.keys() and not all_building_condition_reached(cs['b'], building_types)) else valid
    valid = False if ('u' in cs.keys() and cs['u'] not in u) else valid
    if valid:
      valid_actions.append(action['name'])
      valid_actions_info += f"\n\t\t<{action['name']}()> \t\t cost: mineral{cs['m']}, gas{cs['g']}, time{cs['t']}s"

  # if valid_actions_info != '':
  #   valid_actions_info = "Valid Research Actions: " + valid_actions_info + "\n\n"
  return valid_actions, valid_actions_info


def get_valid_actions_train(agent) -> (list, str):
  obs = agent.team_unit_obs_list[0]
  _, ta, _, _, tc, _, m, g, s, u, b = get_condition_elements(agent)

  building_types = []
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100 and unit.unit_type in BUILDING_TYPE:
      building_types.append(unit.unit_type)

  valid_actions = []
  valid_actions_info = ''
  for action in ta:
    func_id = action['func'][0][0]
    conditions, valid = tc[func_id], True
    # condition = {'m': 125, 'g': 50, 'b': units.Protoss.Gateway, 't': 42, 's': 2},
    cs = conditions
    valid = False if ('m' in cs.keys() and m < cs['m']) else valid
    valid = False if ('g' in cs.keys() and g < cs['g']) else valid
    valid = False if ('s' in cs.keys() and s < cs['s']) else valid
    valid = False if ('b' in cs.keys() and not all_building_condition_reached(cs['b'], building_types)) else valid
    valid = False if ('u' in cs.keys() and cs['u'] not in u) else valid
    if valid:
      valid_actions.append(action['name'])
      valid_actions_info += f"\n\t\t<{action['name']}()> \t\t cost: mineral{cs['m']}, gas{cs['g']}, supply{cs['s']}, time{cs['t']}s"

  # if valid_actions_info != '':
  #   valid_actions_info = "Valid Unit Training Actions: " + valid_actions_info + "\n\n"
  return valid_actions, valid_actions_info


def get_valid_actions_developer(agent):
  teams_valid_actions_info = ''

  if agent.name != 'Developer':
    logger.error(f"[ID {agent.log_id}] LLMAgent {agent.name}: use get_valid_actions_developer but agent name is not Developer")

  for team in agent.teams:
    if team['select_type'] == 'select':
      for i in range(len(team['obs'])):
        teams_valid_actions_info += f"\n\tTeam {team['name']}-{i + 1}:"
    else:
      teams_valid_actions_info += f"\n\tTeam {team['name']}:"

    valid_actions_info = ''
    _, valid_actions_info_  = get_valid_actions_research(agent)
    valid_actions_info += valid_actions_info_
    _, valid_actions_info_  = get_valid_actions_train(agent)
    valid_actions_info += valid_actions_info_
    if agent.config.ENABLE_EASY_BUILD:
      _, valid_actions_info_  = get_valid_actions_build(agent)
      valid_actions_info += valid_actions_info_

    if valid_actions_info == '':
      teams_valid_actions_info += '\n\t\t currently none, build buildings and to unlock training and researching actions.'
    else:
      teams_valid_actions_info += valid_actions_info

  teams_valid_actions_info = 'Valid actions:' + teams_valid_actions_info + '\n\n'
  return teams_valid_actions_info


def get_valid_actions_builder(agent):
  teams_valid_actions_info = ''

  for team in agent.teams:

    if agent.name == 'Builder':
      if team['select_type'] == 'select':
        for i in range(len(team['obs'])):
          teams_valid_actions_info += f"\n\tTeam {team['name']}-{i + 1}:"
      else:
        teams_valid_actions_info += f"\n\tTeam {team['name']}:"
    else:
      teams_valid_actions_info += f"\n\tAgent Builder's probe's valid actions:"

    valid_actions_info = ''
    _, valid_actions_info_ = get_valid_actions_build(agent)
    valid_actions_info += valid_actions_info_

    if valid_actions_info == '':
      teams_valid_actions_info += '\n\t\t currently none, waiting for more resource to unlock build actions.'
    else:
      teams_valid_actions_info += valid_actions_info

  if agent.name == 'Builder':
    teams_valid_actions_info = 'Valid actions:' + teams_valid_actions_info + '\n\n'
  else:
    teams_valid_actions_info = "Agent Builder's Valid actions:" + teams_valid_actions_info + '\n\n'
  return teams_valid_actions_info



# 根据obs获取合法动作，以文本格式输出，这个需要作为input prompt的一个独立部分
def get_valid_actions(agent) -> str:

  text_valid_actions = "Valid Actions:"
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
      team_config = agent.config.AGENTS[agent.name]['team'][team['name']]
      team_action_space = []
      for unit_type in ctrl_unit_type:
        if unit_type in list(team_config['actions'].keys()):
          team_action_space += team_config['actions'][unit_type]
        else:
          logger.error(f"[ID {agent.log_id}] cannot get valid actions of unit_type {unit_type}")

      # reduce to obs.observation.available_actions
      valid_actions = []
      for action in team_action_space:
        valid = True
        # print(action)
        for func_triple in action['func']:
          if func_triple[0] not in obs.observation.available_actions:
            valid = False
        # if 'Attack' in action['name'] and 'Ability' not in action['name']:
        #   valid = llm_action.check_weapon_state(team['obs'][0], 'now', None)
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
  text_valid_actions += "\n\n"
  return text_valid_actions


# record action arg explanation
def get_valid_action_args_explanation(agent):
  obs = agent.team_unit_obs_list[0]
  text_arg_explanation = ''
  size_screen = obs.observation.feature_screen.height_map.shape[0]
  size_minimap = obs.observation.feature_minimap.height_map.shape[0]
  ratio = size_screen / SCREEN_WORLD_GRID

  screen_edge = f"where x and y range from 0 to {int(size_screen/ratio)}."
  if len(agent.teams) > 0:
    team = agent.teams[0]
    if 'l' in team.keys():
      screen_edge = f"{int(team['l']/ratio)} < x < {int(team['r']/ratio)}, {int(team['u']/ratio)} < y < {int(team['b']/ratio)}"
    else:
      screen_edge = f"0 < x < {int(size_screen/ratio)}, 0 < y < {int(size_screen/ratio)}"

  text_arg_explanation += f"Action Args: "
  text_arg_explanation += f"\n\t(1) tag: tag refers to a hexadecimal number, shape as 0x000000000."
  text_arg_explanation += f"\n\t(2) screen: screen refers to a screen coordinate, shape as [x, y], where {screen_edge}."
  text_arg_explanation += f"\n\t(3) minimap: minimap refers to a minimap coordinate, shape as [x, y], where x and y range from 0 to {size_minimap}."
  text_arg_explanation += f"\nFor example, when you want to use an action like <Action_Name(tag, screen)>, you should output like <Action_Name(0x100580001, [12, 16])>; when you want to use an action like <Action_Name(screen)>, you should output like <Action_Name([20, 8])>. "
  text_arg_explanation += f"What's more, You need to see clearly whether an action is using screen coordinates or minimap coordinates, If an action name as XXXX_Screen, it uses screen coordinate; if an action name as XXXX_Minimap, it uses minimap coordinate."
  if len(agent.teams) > 0:
    team = agent.teams[0]
    if 'l' in team.keys():
      if (team['l'] != 0 or team['u'] != 0 or team['r'] != size_screen - 1 or team['b'] != size_screen - 1):
        text_arg_explanation += f"\nWarning! controlled team near the map edge! Pay attention to using coordinates within the boundary!"
  text_arg_explanation += "\n\n"
  return text_arg_explanation


def get_last_action_info(agent) -> str:
  text_last_action = ""
  if isinstance(agent.last_text_a_pro, str) and len(agent.last_text_a_pro) > 0:
    text_last_action += f"Last Step {agent.last_text_a_pro}"
    text_last_action += f"\nYou need to confirm whether the previous action finished executing, and based on this, determine whether to continue the old strategy or immediately take other actions."
    text_last_action += "\n\n"
  return text_last_action


# def get_task_info(agent) -> str:
#
#   task_info = ''
#   for team in agent.config.AGENTS[agent.name]['team'].values():
#     if 'task' in team.keys() and len(team['task']) > 0 and len(team['obs']) > 0:
#       change_task = False
#       task = None
#       if team['select_type'] != 'select' or team['name'] == 'Empty':
#         task = team['task'][0]
#         obs = team['obs'][0]
#         idx = np.nonzero(obs.observation['feature_minimap']['camera'])
#         x, y = int(idx[:][1].mean()), int(idx[:][0].mean())
#         if task['pos'] is not None:
#           dist = math.sqrt((x - task['pos'][0]) ** 2 + (y - task['pos'][1]) ** 2)
#           if dist < 4:
#             change_task = True
#         if len(team['task']) > 1:
#           task1 = team['task'][1]
#           if task1['time'] is not None and isinstance(task1['time'], str) and ':' in task1['time']:
#             game_loop = obs.observation.game_loop
#             game_s = int(game_loop / 22 % 60)  # SC2 runs at 22.4 game loops per second
#             game_m = int(game_loop / 22 // 60)  # SC2 runs at 22.4 game loops per second
#             if int(task1['time'].split(":")[0]) < game_m or \
#               (int(task1['time'].split(":")[0]) == game_m and int(task1['time'].split(":")[1]) <= game_s):
#               change_task = True
#       if team['select_type'] == 'select':
#         pass
#       if change_task:
#         team['task'].pop(0)
#       if len(team['task']) > 0 and task is not None:
#         if team['name'] != 'Empty':
#           task_info += f"\n\tTeam {team['name']}' task: {task['info']}"
#         if team['name'] == 'Empty':
#           task_info += f"\n\tAgent task: {task['info']}"
#
#   if task_info != '':
#     task_info = f"Tasks:" + task_info
#     task_info += "\n\n"
#
#   return task_info


def get_task_info(agent) -> str:
  task_info = ''
  for team in agent.config.AGENTS[agent.name]['team'].values():
    if len(team['obs']) == 0:
      continue
    if isinstance(team['task'], str):
      if team['name'] != 'Empty':
        task_info += f"\n\tTeam {team['name']}' task: {team['task']}"
      if team['name'] == 'Empty':
        task_info += f"\n\tAgent task: {team['task']}"
  if task_info != '':
    task_info = f"Tasks:" + task_info
    task_info += "\nPlease note that **Tasks** are the most important information, all your decisions must aimed at completing the tasks.\n\n"
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
    other_agents_info = "Global agent info:" + other_agents_info + "\n\n"
  if len(other_agents_unit_knowledge) != 0:
    other_agents_unit_knowledge = f"Relevant Knowledge:" + other_agents_unit_knowledge + "\n\n"

  return other_agents_info + other_agents_unit_knowledge


def get_alert_info(agent) -> str:   # for Commander only
  alert_info = ''

  obs = agent.team_unit_obs_list[0]
  arr = obs.observation['feature_minimap']['alerts']
  idx = np.nonzero(arr)  # 获取特征图上非零值的坐标
  for i in range(len(idx[0])):
    alert_info += f"\n\tEngage with enemies in minimap [{idx[1][i]}, {idx[0][i]}]"
  if len(alert_info) != 0:
    alert_info = "Alert Info:" + alert_info +  "\n\n"
  return alert_info


def get_upgrades_info(agent) -> str:
  upgrades_info = ''
  obs = agent.team_unit_obs_list[0]
  for upgrade in obs.observation.upgrades:
    upgrades_info += f"\n\t {str(upgrades.Upgrades(upgrade))}"
  if len(upgrades_info) != 0:
    upgrades_info = "Upgrade Info:" + upgrades_info + "\n\n"
  else:
    upgrades_info = "Upgrade Info:" + "we do not have any technology upgrade" + "\n\n"
  return upgrades_info


def get_warp_info(agent) -> str:  # for Developer only

  obs = agent.team_unit_obs_list[0]
  warp_source_info = ''
  pylon_info = ''
  prism_info = ''

  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100:

      if unit.unit_type in [units.Protoss.WarpGate]:
        warp_source_info += f"\n\t{str(units.get_unit_type(unit.unit_type))}, "
        warp_source_info += f""  # Pysc2 do not provide cooldown status of warp gates
      if unit.unit_type == units.Protoss.Pylon:
        pylon_info += f"\n\t{str(units.get_unit_type(unit.unit_type))}, tag:{hex(unit.tag)}"
      if unit.unit_type == units.Protoss.WarpPrismPhasing:
        prism_info += f"\n\t{str(units.get_unit_type(unit.unit_type))}, tag:{hex(unit.tag)}"

  warp_target_info = pylon_info + prism_info
  if len(warp_source_info) > 0:
    warp_source_info = f"Available WarpGates:\n{obs.observation.player.warp_gate_count} WarpGate in total" + "\n\n"
    warp_target_info = f"Available WarpTrain Field Provider:" + warp_target_info + "\n\n"
  else:
    warp_target_info = ''

  return warp_source_info + warp_target_info


def get_event_info(agent) -> str:
  event_text = ''

  t = agent.main_loop_step
  n, i_list = 1, [1]
  event_dict = events.get_events(agent, t, n, i_list)['1']  # 从锚点s_t-n 往后 1 步

  for team in agent.teams:
    if team['name'] not in event_dict.keys():
      continue
    if len(event_dict[team['name']]) == 0:
      continue
    team_event_text = ''
    team_event = event_dict[team['name']]

    if len(team_event['ctrl']) > 0:
      team_event_text += '\n\t\tControlled Unit Event:'
      for tag in team_event['ctrl'].keys():
        team_event_text += '\n\t\t\t' + team_event['ctrl'][int(tag)]
    if len(team_event['ally']) > 0:
      team_event_text += '\n\t\tAlly Unit Event:'
      for tag in team_event['ally'].keys():
        team_event_text += '\n\t\t\t' + team_event['ally'][int(tag)]
    if len(team_event['enemy']) > 0:
      team_event_text += '\n\t\tEnemy Unit Event:'
      for tag in team_event['enemy'].keys():
        team_event_text += '\n\t\t\t' + team_event['enemy'][int(tag)]

    if team_event_text != '':
      event_text += f"\n\tTeam {team['name']} Event:" + team_event_text

  if event_text != '':
    event_text = "Last Step Event:" + event_text + "\n\n"

  return event_text


def get_action_error_info(agent):
  action_errors = agent.action_errors
  action_error_info = ''

  for key in action_errors.keys():
    action_error_info += f"\n\t<{key}(...)>:"
    for error in action_errors[key]:
      action_error_info += f"\n\t\t{error}"

  if action_error_info != '':
    action_error_info = "Last Step Action Errors:" + action_error_info + "\n\n"
  return action_error_info


def get_ves_and_base_info(agent):

  obs = agent.team_unit_obs_list[0]
  _, _, ves_new_base_tags, ves_near_tags = get_ves_for_base_and_gas_building(obs)

  out_put_info = ''
  if len(ves_new_base_tags) > 0:
    out_put_info += f"Valid tag for new base (Nexus/CommandCenter/Hatchery):"
    for tag in ves_new_base_tags:
      out_put_info += f"\n\t {hex(tag)}"
    out_put_info += f"\n"

  if len(ves_near_tags) > 0:
    out_put_info += f"Valid tag for new gas building (Assimilator/Refinery/Extractor):"
    for tag in ves_near_tags:
      out_put_info += f"\n\t {hex(tag)}"
    out_put_info += f"\n"

  out_put_info += f"\n"
  return out_put_info


def get_unit_count_info(agent, return_type):
  unit_oppo = {}
  unit_self_building = {}
  unit_self_other = {}
  build_process_building = {}
  build_process_other = {}

  unit_count = {}
  unit_count['building_military'], unit_count['num_building_military'] = {}, {}
  unit_count['building_research'], unit_count['num_building_research'] = {}, {}
  unit_count['building_military_idle'], unit_count['num_building_military_idle'] = {}, {}
  unit_count['building_research_idle'], unit_count['num_building_research_idle'] = {}, {}
  unit_count['building_military_working'], unit_count['num_building_military_working'] = {}, {}
  unit_count['building_research_working'], unit_count['num_building_research_working'] = {}, {}
  unit_count['text_building_military'], unit_count['text_building_research'] = {}, {}
  unit_count['text_building_process'], unit_count['text_unbuilding_process'] = {}, {}
  # unit_info = f'unit {hex(unit.tag)}({str(units.get_unit_type(unit.unit_type))})'

  def add_to_dict(my_dict, key, value):
    if key in my_dict.keys():
      my_dict[key].append(value)
    else:
      my_dict[key] = [value]

  obs = agent.team_unit_obs_list[0]
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.ENEMY:
      add_to_dict(unit_oppo, str(units.get_unit_type(unit.unit_type)), unit)
    if unit.alliance == features.PlayerRelative.SELF:
      if unit.build_progress == 100 and unit.unit_type in BUILDING_TYPE:
        add_to_dict(unit_self_building, str(units.get_unit_type(unit.unit_type)), unit)
      if unit.build_progress == 100 and unit.unit_type not in BUILDING_TYPE:
        add_to_dict(unit_self_other, str(units.get_unit_type(unit.unit_type)), unit)
      if unit.build_progress != 100 and unit.unit_type in BUILDING_TYPE:
        add_to_dict(build_process_building, str(units.get_unit_type(unit.unit_type)), unit)
      if unit.build_progress != 100 and unit.unit_type not in BUILDING_TYPE:
        add_to_dict(build_process_other, str(units.get_unit_type(unit.unit_type)), unit)

      if unit.unit_type in BUILDING_TYPE_MILITARY and unit.build_progress == 100:
        add_to_dict(unit_count['building_military'], str(units.get_unit_type(unit.unit_type)), unit)
        if unit.active == 0:
          add_to_dict(unit_count['building_military_idle'], str(units.get_unit_type(unit.unit_type)), unit)
        else:
          add_to_dict(unit_count['building_military_working'], str(units.get_unit_type(unit.unit_type)), unit)
      if unit.unit_type in BUILDING_TYPE_RESEARCH and unit.build_progress == 100:
        add_to_dict(unit_count['building_research'], str(units.get_unit_type(unit.unit_type)), unit)
        if unit.active == 0:
          add_to_dict(unit_count['building_research_idle'], str(units.get_unit_type(unit.unit_type)), unit)
        else:
          add_to_dict(unit_count['building_research_working'], str(units.get_unit_type(unit.unit_type)), unit)

  num_unit_oppo = {}
  num_unit_self_building = {}
  num_unit_self_other = {}
  num_build_process_building = {}
  num_build_process_other = {}
  for key in unit_oppo.keys():
    num_unit_oppo[key] = len(unit_oppo[key])
  for key in unit_self_building.keys():
    num_unit_self_building[key] = len(unit_self_building[key])
  for key in unit_self_other.keys():
    num_unit_self_other[key] = len(unit_self_other[key])

  for key in build_process_building.keys():
    num_build_process_building[key], text_details =len(build_process_building[key]), ''
    for unit in build_process_building[key]:
      text_details += f'{hex(unit.tag)} {unit.build_progress}%' if text_details == '' else f', {hex(unit.tag)} {unit.build_progress}%'
    unit_count['text_building_process'][key] = f"{num_build_process_building[key]} in total ({text_details})"
  for key in build_process_other.keys():
    num_build_process_other[key], text_details = len(build_process_other[key]), ''
    for unit in build_process_other[key]:
      text_details += f'{hex(unit.tag)} {unit.build_progress}%' if text_details == '' else f', {hex(unit.tag)} {unit.build_progress}%'
    unit_count['text_unbuilding_process'][key] = f"{num_build_process_other[key]} in total ({text_details})"

  for key in unit_count['building_military'].keys():
    unit_count['num_building_military'][key] = len(unit_count['building_military'][key])
    unit_count['num_building_military_idle'][key] = len(unit_count['building_military_idle'][key]) if key in unit_count['building_military_idle'].keys() else 0
    unit_count['num_building_military_working'][key] = len(unit_count['building_military_working'][key]) if key in unit_count['building_military_working'].keys() else 0
    unit_count['text_building_military'][key] = f"{unit_count['num_building_military'][key]} ({unit_count['num_building_military_working'][key]} is working, {unit_count['num_building_military_idle'][key]} is idle)"
  for key in unit_count['building_research'].keys():
    unit_count['num_building_research'][key] = len(unit_count['building_research'][key])
    unit_count['num_building_research_idle'][key] = len(unit_count['building_research_idle'][key]) if key in unit_count['building_research_idle'].keys() else 0
    unit_count['num_building_research_working'][key] = len(unit_count['building_research_working'][key]) if key in unit_count['building_research_working'].keys() else 0
    unit_count['text_building_research'][key] = f"{unit_count['num_building_research'][key]} ({unit_count['num_building_research_working'][key]} is working, {unit_count['num_building_research_idle'][key]} is idle)"

  out_put_info = 'Unit Counts:'
  if return_type in [1]:
    out_put_info += f"\n\tOur Unit: \n\t {num_unit_self_other}"
    out_put_info += f"\n\tOur Buildings: \n\t {num_unit_self_building}"
    out_put_info += f"\n\tMilitary Buildings: \n\t {unit_count['text_building_military'] if len(unit_count['text_building_military'].keys()) > 0 else None}"
    out_put_info += f"\n\tResearch Buildings: \n\t {unit_count['text_building_research'] if len(unit_count['text_building_research'].keys()) > 0 else None}"
    out_put_info += f"\n\tOur Unit (in warping/morphing): \n\t {unit_count['text_unbuilding_process'] if len(num_build_process_other.keys()) > 0 else None}"
    out_put_info += f"\n\tOur Buildings (in construction): \n\t {unit_count['text_building_process'] if len(num_build_process_building.keys()) > 0 else None}"
    out_put_info += f"\n\tSpotted Enemy Unit: \n\t {num_unit_oppo}"
  if return_type in [2]:
    out_put_info += f"\n\tOur Unit: \n\t {num_unit_self_other}"
    out_put_info += f"\n\tOur Buildings: \n\t {num_unit_self_building}"
    out_put_info += f"\n\tMilitary Buildings: \n\t {unit_count['text_building_military'] if len(unit_count['text_building_military'].keys()) > 0 else None}"
    out_put_info += f"\n\tResearch Buildings: \n\t {unit_count['text_building_research'] if len(unit_count['text_building_research'].keys()) > 0 else None}"
    out_put_info += f"\n\tOur Unit (in warping/morphing): \n\t {unit_count['text_unbuilding_process'] if len(num_build_process_other.keys()) > 0 else None}"
    out_put_info += f"\n\tOur Buildings (in construction): \n\t {unit_count['text_building_process'] if len(num_build_process_building.keys()) > 0 else None}"
  if return_type in [3]:
    out_put_info += f"\n\tOur Buildings: \n\t {num_unit_self_building}"
    out_put_info += f"\n\tOur Buildings (in construction): \n\t {unit_count['text_building_process'] if len(num_build_process_building.keys()) > 0 else None}"
  out_put_info += '\n\n'

  return out_put_info



class BaseTranslatorO:

  def __init__(self, name, log_id, config):
    self.agent_name = name
    self.log_id = log_id
    self.config = config
    self.loop_step = -1
    self.states = []
    self.state = {}
    self.size_screen = None
    self.size_minimap = None
    self.final_prompt = ''

  def obs_list_safe(self, agent):
    obs_list = agent.team_unit_obs_list
    return False if not isinstance(obs_list, list) or len(obs_list) < 1 else True

  def translate(self, agent) -> str:
    if not self.obs_list_safe(agent):
      return f"obs_list error, no obs found"

    self.state = {
      'game_info': get_game_info(agent),
      'units_info': get_teams_info(agent),
      'event_info': get_event_info(agent),
      'knowledge_info': get_relevant_knowledge(agent),
      'valid_actions': get_valid_actions(agent),
      'valid_args_explanation': get_valid_action_args_explanation(agent),
      'last_action_info': get_last_action_info(agent),
      'last_action_error_info': get_action_error_info(agent),
      'upgrades_info': get_upgrades_info(agent),
      'task_info': get_task_info(agent),
      'final_prompt': self.final_prompt,
    }

    if agent.config.ENABLE_COMMUNICATION:
      # self.state['communication_info'] = get_communication_info(agent)
      self.state['communication_input'] = agent.last_text_c_inp
      self.state['communication_target'] = agent.last_text_c_tar + '\n\n'
    else:
      self.state['communication_input'] = ''
      self.state['communication_target'] = ''

    if self.loop_step != agent.main_loop_step:
      self.loop_step = agent.main_loop_step
      self.states.append(self.state)

    return ''


class CombatGroupTranslatorO(BaseTranslatorO):

  def __init__(self, name, log_id, config):
    super(CombatGroupTranslatorO, self).__init__(name, log_id, config)
    if config.ENABLE_COMMUNICATION:
      self.final_prompt = f"Give each team no more than {config.MAX_NUM_ACTIONS} actions, " \
                          f"these actions will be executed in the following {round(1 / config.MAX_LLM_DECISION_FREQUENCY, 2)} seconds, " \
                          f"among which activity release should usually before attack and move." \
                          f"\nNow, start generating your analysis, strategy, actions and communication:"
    else:
      self.final_prompt = f"Give each team no more than {config.MAX_NUM_ACTIONS} actions, " \
                          f"these actions will be executed in the following {round(1 / config.MAX_LLM_DECISION_FREQUENCY, 2)} seconds, " \
                          f"among which activity release should usually before attack and move." \
                          f"\nNow, start generating your analysis, strategy and actions:"
    logger.info(f"[ID {log_id}] {name} CombatGroupTranslatorO initialized")

  def translate(self, agent) -> str:
    super(CombatGroupTranslatorO, self).translate(agent)
    if not self.obs_list_safe(agent):
      return f"obs_list error, no obs found"

    # observation and relevant info
    self.text_obs = self.state['game_info'] + self.state['units_info'] + self.state['event_info'] + \
                    self.state['valid_actions'] + self.state['valid_args_explanation'] + self.state['last_action_info']
                    # self.state['last_action_error_info']  #  + self.state['knowledge_info']
    self.text_task = self.state['communication_input'] + self.state['communication_target'] + self.state['task_info']
    self.text_prompt = self.text_obs + self.text_task + self.final_prompt

    text_o = self.text_prompt
    return text_o


class CommanderTranslatorO(BaseTranslatorO):

  def __init__(self, name, log_id, config):
    super(CommanderTranslatorO, self).__init__(name, log_id, config)
    if config.ENABLE_COMMUNICATION:
      self.final_prompt = f"As the supreme military commander, you should not directly give actions, " \
                          f"instead, tell your subordinates what to do through communication." \
                          f"\nNow, start analysis, making macro decisions in military deployments by sending message to other agents:"
    else:
      logger.warning(f"[ID {self.log_id}] {self.agent_name} CommanderTranslatorO: Commander can not communicate with other agents due to agent.config.ENABLE_COMMUNICATION=False")
      self.final_prompt = f"As the supreme military commander, you should not directly give actions, " \
                          f"instead, tell your subordinates what to do through communication." \
                          f"\nNow, start analysis, making macro decisions in military deployments by sending message to other agents:"
    logger.info(f"[ID {log_id}] {name} CommanderTranslatorO initialized")

  def translate(self, agent) -> str:
    super(CommanderTranslatorO, self).translate(agent)
    if not self.obs_list_safe(agent):
      return f"obs_list error, no obs found"
    self.states[-1]['unit_count_info'] = get_unit_count_info(agent, return_type=1)
    self.states[-1]['other_agents_info'] = get_other_agents_info(agent)

    # observation
    self.text_obs = self.state['game_info'] + self.states[-1]['other_agents_info'] + self.states[-1]['unit_count_info']
    self.text_task = self.state['communication_input'] + self.state['communication_target'] + self.state['task_info']
    self.text_prompt = self.text_obs + self.text_task + self.final_prompt
    text_o = self.text_prompt

    if not agent.config.ENABLE_COMMUNICATION:
      logger.warning(f"[ID {self.log_id}] {self.agent_name} CommanderTranslatorO: Commander can not communicate with other agents due to agent.config.ENABLE_COMMUNICATION=False")
    return text_o


class DeveloperTranslatorO(BaseTranslatorO):

  def __init__(self, name, log_id, config):
    super(DeveloperTranslatorO, self).__init__(name, log_id, config)
    if config.ENABLE_COMMUNICATION:
      self.final_prompt = f"As a senior commander, the max number of your actions is not limited, " \
                          f"when you warp units, try to use all the WarpGate as much as possible, " \
                          f"and warp all units near a single WarpTrain Field Provider." \
                          f"\nNow, start generating your analysis, actions and communication:"
    else:
      self.final_prompt = f"As a senior commander, the max number of your actions is not limited, " \
                          f"when you warp units, try to use all the WarpGate as much as possible, " \
                          f"and warp all units near a single WarpTrain Field Provider." \
                          f"\nNow, start generating your analysis and actions:"
    logger.info(f"[ID {log_id}] {name} DeveloperTranslatorO initialized")

  def translate(self, agent) -> str:
    super(DeveloperTranslatorO, self).translate(agent)
    if not self.obs_list_safe(agent):
      return f"obs_list error, no obs found"
    self.states[-1]['unit_count_info'] = get_unit_count_info(agent, return_type=2)
    self.states[-1]['valid_actions'] = get_valid_actions_developer(agent) + get_valid_actions_builder(agent)

    # observation
    self.states[-1]['warp_info'] = get_warp_info(agent)
    self.text_obs = self.state['game_info'] + self.states[-1]['unit_count_info'] + \
               self.states[-1]['valid_actions'] + self.state['valid_args_explanation'] + self.state['last_action_info'] + \
               self.states[-1]['warp_info']
    self.text_task = self.state['communication_input'] + self.state['communication_target'] + self.state['task_info']
    self.text_prompt = self.text_obs + self.text_task + self.final_prompt

    if not agent.config.ENABLE_COMMUNICATION:
      logger.warning(f"[ID {self.log_id}] {self.agent_name} DeveloperTranslatorO: Developer can not communicate with other agents due to agent.config.ENABLE_COMMUNICATION=False")
    text_o = self.text_prompt
    return text_o


class BuilderTranslatorO(BaseTranslatorO):
  def __init__(self, name, log_id, config):
    super(BuilderTranslatorO, self).__init__(name, log_id, config)
    if config.ENABLE_COMMUNICATION:
      self.final_prompt = f"As a builder, you need to move the worker to an open location and complete the construction of the building." \
                          f"If you have enough supply (such as more than 10), build base building / gas building / unit training buildings or research building" \
                          f"\nNow, start generating your analysis, actions and communication:"
    else:
      self.final_prompt = f"As a builder, you need to move the worker to an open location and complete the construction of the building." \
                          f"If you have enough supply (such as more than 10), build base building / gas building / unit training buildings or research building" \
                          f"\nNow, start generating your analysis, actions:"
    logger.info(f"[ID {log_id}] {name} DeveloperTranslatorO initialized")

  def translate(self, agent) -> str:
    super(BuilderTranslatorO, self).translate(agent)
    if not self.obs_list_safe(agent):
      return f"obs_list error, no obs found"
    self.states[-1]['unit_count_info'] = get_unit_count_info(agent, return_type=3)
    self.states[-1]['new_base_and_ves_info'] = get_ves_and_base_info(agent)
    self.states[-1]['valid_actions'] = get_valid_actions_builder(agent)

    # observation
    self.text_obs = self.state['game_info'] + self.state['units_info'] + self.states[-1]['unit_count_info'] + self.state['event_info'] + \
               self.states[-1]['valid_actions'] + self.state['valid_args_explanation'] + self.state['last_action_info'] + \
               self.state['last_action_error_info'] + self.states[-1]['new_base_and_ves_info']
    self.text_task = self.state['communication_input'] + self.state['communication_target'] + self.state['task_info']
    self.text_prompt = self.text_obs + self.text_task + self.final_prompt

    if not agent.config.ENABLE_COMMUNICATION:
      logger.warning(f"[ID {self.log_id}] {self.agent_name} DeveloperTranslatorO: Developer can not communicate with other agents due to agent.config.ENABLE_COMMUNICATION=False")
    text_o = self.text_prompt
    return text_o

# TODO: You can specialize your TranslatorO here


PROTOSS_FACTORY = {
  'default': CombatGroupTranslatorO,  # CombatGroup Observation
  'combatgroup': CombatGroupTranslatorO,  # CombatGroup Observation
  'commander': CommanderTranslatorO,  # only information relevant to macro decision, military
  'developer': DeveloperTranslatorO,  # only information relevant to macro decision, development
  'builder': BuilderTranslatorO,
}
TERRAN_FACTORY = {}
ZERG_FACTORY = {}

FACTORY = {
  'protoss': PROTOSS_FACTORY,
  'terran': TERRAN_FACTORY,
  'zerg': ZERG_FACTORY,
}
