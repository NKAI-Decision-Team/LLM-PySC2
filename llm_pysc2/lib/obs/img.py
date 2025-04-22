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


from pysc2.lib import renderer_human, colors

from PIL import ImageDraw, ImageFont, Image, ImageEnhance
from loguru import logger
import numpy as np
import pygame
import base64
import math
import copy
import io
import os



def get_img_obs_rgb_fea(self, obs):

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

  if feature_map_name in ['buildable']:
    feature_map_index1 = obs.observation.feature_screen._index_names[0]['pathable']
    feature_map_index2 = obs.observation.feature_screen._index_names[0]['buildable']
    fea_screen1 = observation.feature_screen[feature_map_index1]
    fea_screen2 = observation.feature_screen[feature_map_index2]
    fea_screen = (fea_screen1 + fea_screen2) - 1.0
    fea_screen = (fea_screen + abs(fea_screen)) / 2.0

  # Convert data type to uint8
  # Convert NumPy array to PIL Image object
  # rgb_screen = np.array(rgb_screen)[:, :, ::-1]  # BGR to RGB
  if np.max(fea_screen) - np.min(fea_screen) != 0:
    fea_screen = (fea_screen - np.min(fea_screen)) * (192 / (np.max(fea_screen) - np.min(fea_screen)))
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
def get_img_obs_rgb_screen(self, obs):
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
  # enhancer = ImageEnhance.Brightness(img)
  # img = enhancer.enhance(factor=3.0)
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