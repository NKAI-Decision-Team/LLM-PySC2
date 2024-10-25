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


import time

from pysc2.lib import features, actions
from llm_pysc2.lib.utils import *
from loguru import logger


def get_camera_xy(self, raw_x, raw_y):
  x = max(0, raw_x + self.world_x_offset)
  y = max(0, self.world_range - raw_y + self.world_y_offset)
  return x, y


def get_camera_func_smart(self, obs, tag, threshold=0.15, team=None):
  unit_r = None
  unit_f = None
  for unit in obs.observation.raw_units:
    if unit.tag == tag:
      unit_r = unit
  for unit in obs.observation.feature_units:
    if unit.tag == tag:
      unit_f = unit

  # 动作时，使用观测时锚定的坐标
  if team is not None:
    unit_ = None

    logger.debug(f"[ID {self.log_id}] get_camera_func_smart(): team['obs'] mode")
    agent_name = self.AGENT_NAMES[self.agent_id]
    if len(team['obs']) != len(team['pos']):
      logger.error(f"[ID {self.log_id}] {agent_name} {team['name']} len(team['obs']) != len(team['pos'])")
    # elif unit_r is None:
    #     logger.error(f"[ID {self.log_id}] {agent_name} {team['name']} cannot find unit {str(units.get_unit_type(unit.unit_type))} {hex(tag)}")
    else:
      for i in range(len(team['obs'])):
        obs_old = team['obs'][i]
        unit_selected_in_obs = False

        for unit_ in obs_old.observation.feature_units:
          if unit_.tag == tag and unit_.is_selected and unit_.alliance == features.PlayerRelative.SELF and unit_.tag in \
              team['unit_tags']:
            unit_selected_in_obs = True
            break
        if unit_selected_in_obs:
          x, y = team['pos'][i][0], team['pos'][i][1]
          if self.last_two_camera_pos[0][0] == self.last_two_camera_pos[1][0] == x and \
              self.last_two_camera_pos[0][1] == self.last_two_camera_pos[1][1] == y:
            logger.debug(f"[ID {self.log_id}] {agent_name} {team['name']}: camera in correct position")
            return (0, actions.FUNCTIONS.no_op())
          else:
            unit_type = unit_.unit_type if unit_ is not None else None
            logger.info(f"[ID {self.log_id}] {agent_name} {team['name']}: use obs position ({x}, {y}) for unit {str(units.get_unit_type(unit_type))} {hex(tag)}")
            self.last_two_camera_pos.append([x, y])
            return (573, actions.FUNCTIONS.llm_pysc2_move_camera((x, y)))

      unit_type = unit_.unit_type if unit_ is not None else None
      logger.error(f"[ID {self.log_id}] {agent_name} {team['name']} cannot find unit {str(units.get_unit_type(unit_type))} {hex(tag)}")

  logger.debug(f"[ID {self.log_id}] get_camera_func_smart(): standard mode")
  if (unit_r is not None) and unit_f is None:
    x, y = get_camera_xy(self, unit_r.x, unit_r.y)
    logger.info(f"[ID {self.log_id}] get_camera_func_smart(): (unit_r is not None) and unit_f is None")
    self.last_two_camera_pos.append([x, y])
    return (573, actions.FUNCTIONS.llm_pysc2_move_camera((x, y)))  # 有这个单位，但是屏幕上没找到
  elif (unit_r is not None) and (unit_f is not None) and \
      not (abs(unit_f.x - self.size_screen / 2) < threshold * self.size_screen and
           abs(unit_f.y - self.size_screen / 2) < threshold * self.size_screen):
    # not (threshold * self.size_screen < unit_f.x < (1 - threshold) * self.size_screen and
    #      threshold * self.size_screen < unit_f.y < (1 - threshold) * self.size_screen):
    x, y = get_camera_xy(self, unit_r.x, unit_r.y)
    logger.info(f"[ID {self.log_id}] get_camera_func_smart(): unit_f {str(units.get_unit_type(unit_f.unit_type))} "
                f"{hex(unit_f.tag)} not near screen center, {unit_f.x} {unit_f.y}")
    self.last_two_camera_pos.append([x, y])
    return (573, actions.FUNCTIONS.llm_pysc2_move_camera((x, y)))  # 有这个单位，屏幕上找到了，但太偏了
  else:
    return (0, actions.FUNCTIONS.no_op())  # 不动相机


def get_new_unit_agent(self, obs, unit) -> str:  # 编队逻辑函数
  if not unit.alliance == features.PlayerRelative.SELF or unit.build_progress != 100:
    return f'unit build_progress {unit.build_progress} != 100'
  # 空降部队编队
  for agent_name in self.AGENT_NAMES:
    if not agent_name in self.config.AGENTS_ALWAYS_DISABLE and \
        unit.unit_type in self.agents[agent_name].available_unit_type and \
        (agent_name == 'Airborne'):
      # possible_transport_unit = self.agents[agent_name].unit_raw_list
      possible_transport_unit = obs.observation.raw_units
      dist_min = 999999
      for unit_ in possible_transport_unit:
        if unit_.unit_type in TRANSPORTER_TYPE and unit_.alliance == features.PlayerRelative.SELF \
            and unit_.health > 0 and unit_.tag in self.unit_uid:  # 确认一下该运输单位还活着
          dist = get_dist(unit, unit_)
          if dist < dist_min:
            dist_min = dist

      if dist_min < 4:  # 出现在运输单位附近4距离内的默认为空降兵
        return agent_name

  for agent_name in self.AGENT_NAMES:
    if agent_name in self.config.AGENTS_ALWAYS_DISABLE:
      continue
    if not unit.unit_type in self.agents[agent_name].available_unit_type:
      continue
    if unit.unit_type in WORKER_TYPE:
      if 'CombatGroup' in agent_name and len(self.agents[agent_name].unit_tag_list) < 1:
        return agent_name  # 侦察农民
      if agent_name == 'Builder' and len(
          self.agents[agent_name].unit_tag_list) < obs.observation.player.food_workers / 30:
        return agent_name  # 建造农民
      continue
    if agent_name == 'Defender' and len(self.agents[agent_name].unit_tag_list) < obs.observation.player.food_army / 15:
      return agent_name  # 守备部队
    if agent_name == 'Developer':
      return agent_name  # 后勤部队
    if agent_name == 'Commander':
      return agent_name  # 指挥所
    if 'CombatGroup' in agent_name:
      return agent_name  # 标准作战小组
    continue
    # if (unit.unit_type in self.agents[agent_name].available_unit_type) and ('CombatGroup' in agent_name) and (unit.unit_type in WORKER_TYPE) and len(self.agents[agent_name].unit_tag_list) != 0:
    #     continue # 一个作战小组最多一个probe
    # if (unit.unit_type in self.agents[agent_name].available_unit_type) and ('CombatGroup' in agent_name):
    #     return agent_name
    # if (unit.unit_type in self.agents[agent_name].available_unit_type) and ('CombatGroup' not in agent_name):
    #     return agent_name
  return f'Can not find an agent the unit belongs to, unit {str(units.get_unit_type(unit.unit_type))}({unit.unit_type}) {str(hex(unit.tag))}'


def main_agent_func0(self, obs):
  func_id, func_call = (None, None)

  self.size_screen = obs.observation.feature_screen.height_map.shape[0]
  self.size_minimap = obs.observation.feature_minimap.height_map.shape[0]

  # region 1初始动作
  # 选择枢纽，训练probe，加速枢纽
  if self.race == 'protoss' and self.config.ENABLE_INIT_STEPS:
    if self.num_step == 0:
      for unit in obs.observation.feature_units:
        if unit.alliance == features.PlayerRelative.SELF and unit.unit_type in BASE_BUILDING_TYPE:
          x, y = min(max(0, unit.x), self.size_screen), min(max(0, unit.y), self.size_screen)
          func_id, func_call = (2, actions.FUNCTIONS.select_point('select', (x, y)))
          logger.info(f"[ID {self.log_id}] 1.1.1 Func Call: {func_call}")
          func_call = func_call if func_id in obs.observation.available_actions else actions.FUNCTIONS.no_op()
          func_id = func_id if func_id in obs.observation.available_actions else 0
          self.func_id_history.append(func_id)
          return func_call
    if self.num_step == 1:
      for unit in obs.observation.feature_units:
        if unit.alliance == features.PlayerRelative.SELF and unit.unit_type in BASE_BUILDING_TYPE:
          func_id, func_call = (485, actions.FUNCTIONS.Train_Probe_quick('now'))
          logger.info(f"[ID {self.log_id}] 1.1.2 Func Call: {func_call}")
          func_call = func_call if func_id in obs.observation.available_actions else actions.FUNCTIONS.no_op()
          func_id = func_id if func_id in obs.observation.available_actions else 0
          self.func_id_history.append(func_id)
          return func_call
    if self.num_step == 2:
      for unit in obs.observation.feature_units:
        if unit.alliance == features.PlayerRelative.SELF and unit.unit_type in BASE_BUILDING_TYPE:
          func_id, func_call = (343, actions.FUNCTIONS.Rally_Workers_screen('now', (unit.x, unit.y)))
          logger.info(f"[ID {self.log_id}] 1.1.3 Func Call: {func_call}")
          func_call = func_call if func_id in obs.observation.available_actions else actions.FUNCTIONS.no_op()
          func_id = func_id if func_id in obs.observation.available_actions else 0
          self.func_id_history.append(func_id)
          return func_call
    if self.num_step == 3:
      for unit in obs.observation.feature_units:
        if unit.alliance == features.PlayerRelative.SELF and unit.unit_type in BASE_BUILDING_TYPE:
          func_id, func_call = (
            527, actions.FUNCTIONS.Effect_ChronoBoostEnergyCost_screen('now', (unit.x, unit.y)))
          logger.info(f"[ID {self.log_id}] 1.1.4 Func Call: {func_call}")
          func_call = func_call if func_id in obs.observation.available_actions else actions.FUNCTIONS.no_op()
          func_id = func_id if func_id in obs.observation.available_actions else 0
          self.func_id_history.append(func_id)
          return func_call
  if self.race == 'zerg' and self.config.ENABLE_INIT_STEPS:
    pass
  if self.race == 'terran' and self.config.ENABLE_INIT_STEPS:
    pass
  # endregion

  # region 2相机校准(不要对nexus校准，而是对任意的第一个单位校准)
  if self.world_range == 0:
    self.size_screen = obs.observation.feature_screen.height_map.shape[0]
    self.size_minimap = obs.observation.feature_minimap.height_map.shape[0]
    unit_raw_x = None
    for unit in obs.observation.raw_units:
      if unit.alliance == features.PlayerRelative.SELF:
        self.first_select_unit_tag = unit.tag
        self.first_select_unit_type = unit.unit_type
    for unit in obs.observation.raw_units:
      if unit.alliance == features.PlayerRelative.SELF and unit.unit_type in BASE_BUILDING_TYPE:
        self.first_select_unit_tag = unit.tag
        self.first_select_unit_type = unit.unit_type
    for unit in obs.observation.raw_units:
      if unit.tag == self.first_select_unit_tag:
        unit_raw_x = unit.x

    # arr = obs.observation['feature_minimap']['camera']
    arr = obs.observation['feature_minimap']['player_relative']
    idx = np.nonzero(arr)  # 获取特征图上非零值的坐标
    minimap_x_predict = idx[:][1].mean()
    minimap_y_predict = idx[:][0].mean()
    self.world_range = round(int((self.size_minimap / minimap_x_predict) * unit_raw_x) / 32) * 32
    # self.world_y_offset = self.world_range
    logger.info(f"[ID {self.log_id}] 2.1 正在确定xy世界坐标范围：{self.world_range} ")

  # time.sleep(0.5)

  if self.world_xy_calibration == False:
    unit_f = None
    unit_r = None
    for unit in obs.observation.feature_units:
      if unit.tag == self.first_select_unit_tag:
        unit_f = unit
    for unit in obs.observation.raw_units:
      if unit.tag == self.first_select_unit_tag:
        unit_r = unit
    self.world_xy_calibration = True
    if unit_f is not None:
      offset_min = 0.5 * 128 / self.size_screen
      offset_x = (SCREEN_WORLD_GRID / 4) * abs(unit_f.x - self.size_screen / 2) / self.size_screen
      offset_y = (SCREEN_WORLD_GRID / 4) * abs(unit_f.y - self.size_screen / 2) / self.size_screen
      if unit_f.x > self.size_screen * 0.53:
        self.world_x_offset += max(offset_min, offset_x)
        self.world_xy_calibration = False
        logger.debug("a1 unit_f.x > self.size_screen * 0.52")
      if unit_f.x < self.size_screen * 0.47:
        self.world_x_offset -= max(offset_min, offset_x)
        self.world_xy_calibration = False
        logger.debug("b1 unit_f.x < self.size_screen * 0.48")
      if unit_f.y > self.size_screen * 0.53:
        self.world_y_offset -= max(offset_min, offset_y)
        self.world_xy_calibration = False
        logger.debug("c1 unit_f.y > self.size_screen * 0.52")
      if unit_f.y < self.size_screen * 0.47:
        self.world_y_offset += max(offset_min, offset_y)
        self.world_xy_calibration = False
        logger.debug("d1 unit_f.y < self.size_screen * 0.48")
      logger.info(
        f"[ID {self.log_id}] 2.2 正在校准xy世界坐标：校准完成{self.world_xy_calibration} x偏移量{self.world_x_offset} y偏移量{self.world_y_offset}")
      logger.info(f"[ID {self.log_id}] 2.2                 unit_f.x={unit_f.x} unit_f.y={unit_f.y}")
      logger.info(
        f"[ID {self.log_id}] 2.2                 unit_type={self.first_select_unit_type} unit_tag={self.first_select_unit_tag}")
      x, y = get_camera_xy(self, unit_r.x, unit_r.y)
      func_id, func_call = (573, actions.FUNCTIONS.llm_pysc2_move_camera((x, y)))  # 修改了pysc2的action
      logger.info(f"[ID {self.log_id}] 2.2 Func Call: {func_call}")
      self.func_id_history.append(func_id)
      return func_call
    else:
      self.world_xy_calibration = False

      arr = obs.observation['feature_minimap']['camera']
      idx = np.nonzero(arr)  # 获取特征图上非零值的坐标
      minimap_camera_x_predict = idx[:][1].mean()
      minimap_camera_y_predict = idx[:][0].mean()

      arr = obs.observation['feature_minimap']['player_relative']
      arr = np.where(arr == features.PlayerRelative.SELF, 1, 0)
      idx = np.nonzero(arr)  # 获取特征图上非零值的坐标
      minimap_unit_x_predict = idx[:][1].mean()
      minimap_unit_y_predict = idx[:][0].mean()

      if minimap_camera_x_predict > minimap_unit_x_predict + self.size_minimap * 0.1:
        x, y = get_camera_xy(self, unit_r.x, unit_r.y)
        if 0 < x:
          self.world_x_offset -= max(6, 0.5 * self.world_range * abs(
            minimap_camera_x_predict - minimap_unit_x_predict) / self.size_minimap)
        self.world_xy_calibration = False
        logger.debug("a2 minimap_camera_x_predict > minimap_unit_x_predict + self.size_minimap * 0.1")
      if minimap_camera_x_predict < minimap_unit_x_predict - self.size_minimap * 0.1:
        x, y = get_camera_xy(self, unit_r.x, unit_r.y)
        if x < self.world_range + 64:
          self.world_x_offset += max(6, 0.5 * self.world_range * abs(
            minimap_camera_x_predict - minimap_unit_x_predict) / self.size_minimap)
        self.world_xy_calibration = False
        logger.debug("b2 minimap_camera_x_predict < minimap_unit_x_predict - self.size_minimap * 0.1")
      if minimap_camera_y_predict > minimap_unit_y_predict + self.size_minimap * 0.1:
        x, y = get_camera_xy(self, unit_r.x, unit_r.y)
        if y < self.world_range + 64:
          self.world_y_offset += max(6, 0.5 * self.world_range * abs(
            minimap_camera_y_predict - minimap_unit_y_predict) / self.size_minimap)
        self.world_xy_calibration = False
        logger.debug("c2 minimap_camera_y_predict > minimap_unit_y_predict + self.size_minimap * 0.1")
      if minimap_camera_y_predict < minimap_unit_y_predict - self.size_minimap * 0.1:
        x, y = get_camera_xy(self, unit_r.x, unit_r.y)
        if 0 < y:
          self.world_y_offset -= max(6, 0.5 * self.world_range * abs(
            minimap_camera_y_predict - minimap_unit_y_predict) / self.size_minimap)
        self.world_xy_calibration = False
        logger.debug("d2 minimap_camera_y_predict < minimap_unit_y_predict - self.size_minimap * 0.1")

      logger.info(
        f"[ID {self.log_id}] 2.3 正在校准xy世界坐标：校准完成{self.world_xy_calibration} x偏移量{self.world_x_offset} y偏移量{self.world_y_offset}")
      logger.info(
        f"[ID {self.log_id}] 2.3                 minimap_camera_x_predict={minimap_camera_x_predict} minimap_camera_y_predict={minimap_camera_y_predict}")
      logger.info(
        f"[ID {self.log_id}] 2.3                 minimap_unit_x_predict={minimap_unit_x_predict} minimap_unit_y_predict={minimap_unit_y_predict}")
      logger.info(
        f"[ID {self.log_id}] 2.3                 unit_type={self.first_select_unit_type} unit_tag={self.first_select_unit_tag}")

      x, y = get_camera_xy(self, unit_r.x, unit_r.y)
      func_id, func_call = (573, actions.FUNCTIONS.llm_pysc2_move_camera((x, y)))  # 修改了pysc2的action
      logger.info(f"[ID {self.log_id}] 2.3 Func Call: {func_call}")
      self.func_id_history.append(func_id)
      return func_call
  # endregion

  return func_call


def main_agent_func1(self, obs):
  func_id, func_call = (None, None)

  # region 3新生产单位编组 死亡单位的剔除
  # 检测两步之间己方新增的单位和消失的单位
  unit_uid_ = list()
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100:
      unit_uid_.append(unit.tag)
    if unit.tag in self.unit_uid and unit.tag not in unit_uid_:
      self.unit_uid_disappear.append(unit.tag)
    if unit.tag not in self.unit_uid and unit.tag in unit_uid_:
      self.unit_uid_appear.append(unit.tag)
  # for tag in self.unit_uid:
  #     if tag not in unit_uid_:
  #         self.unit_uid_disappear.append(tag)
  # for tag in unit_uid_:
  #     if tag not in self.unit_uid:
  #         self.unit_uid_appear.append(tag)
  self.unit_uid = unit_uid_

  # 单位消失步数记录判断
  for tag in self.unit_uid_total:
    if tag not in self.unit_uid:
      if tag in self.unit_disappear_steps.keys():
        self.unit_disappear_steps[tag] += 1
      else:
        self.unit_disappear_steps[tag] = 1
    else:
      if tag in self.unit_disappear_steps.keys():
        self.unit_disappear_steps.pop(tag)

  # 验证可能消失的单位是否真的消失了，只保留真正消失了的
  # possible_disappear_unit_list_ = []
  # possible_disappear_unit_tag_list_ = []
  # for unit in self.possible_disappear_unit_list:
  #     if unit.tag not in self.unit_uid:
  #         possible_disappear_unit_list_.append(unit)
  #         possible_disappear_unit_tag_list_.append(unit.tag)
  # self.possible_disappear_unit_list = possible_disappear_unit_list_
  # self.possible_disappear_unit_tag_list = possible_disappear_unit_tag_list_
  # # print(f"self.possible_disappear_unit_list = {self.possible_disappear_unit_list}")
  #
  # for unit in obs.observation.raw_units:  # 如果附近有可进入单位（含建筑），如运输机、瓦斯气站，则该单位可能消失
  #     if unit.tag not in get_tag_list(self.possible_disappear_unit_list) and \
  #             (unit.alliance == features.PlayerRelative.SELF) and \
  #             (unit.unit_type not in ACCESSBLE_UNIT_TYPE) and \
  #             (unit.build_progress == 100):
  #         nearby_unit_list = get_nearby_unit_list(unit, obs.observation.raw_units, dist=2.4)
  #         for unit_ in nearby_unit_list:
  #             if (unit_.alliance == features.PlayerRelative.SELF) and \
  #                     (unit_.unit_type in ACCESSBLE_UNIT_TYPE) and \
  #                     (unit_.build_progress == 100):
  #                 self.possible_disappear_unit_list.append(unit)
  #                 self.possible_disappear_unit_tag_list.append(unit.tag)
  # # print(f"self.possible_disappear_unit_list = {self.possible_disappear_unit_list}")

  # 新单位的编队编组
  if not self.main_loop_lock:
    while len(self.unit_uid_appear) != 0:
      # logger.info(f"[ID {self.log_id}] MainAgent Status 3.0 ")
      logger.info(f"[ID {self.log_id}] self.unit_uid_appear = {self.unit_uid_appear}")
      curr_unit = None
      for unit in obs.observation.raw_units:
        if unit.tag == self.unit_uid_appear[0]:
          curr_unit = unit

      if curr_unit is None:  # TODO: 确认这样是否有问题。为什么会找不到self.unit_uid_appear[0]对应的单位
        logger.error(f"[ID {self.log_id}] 3.0 unit {self.unit_uid_appear[0]} not find")
        self.unit_uid_appear.remove(self.unit_uid_appear[0])
        continue

      # 临时消失的单位：gas_building里面出来的单位/载具里面出来的单位
      if (curr_unit.tag in self.unit_uid_appear) and (curr_unit.tag in self.unit_uid_total):
        logger.info(f"[ID {self.log_id}] 3.1 {str(units.get_unit_type(curr_unit.unit_type))} {curr_unit.tag} re-appear")
        # print('--' * 25)
        # for agent_name in self.AGENT_NAMES:
        #     if curr_unit.tag in self.agents[agent_name].unit_tag_list_history:
        #         self.agents[agent_name].unit_tag_list.append(curr_unit.tag)
        # self.unit_uid_appear.remove(curr_unit.tag)
        # continue

      # 获取所属小组，若没有所属小组，直接处理掉
      agent_name = get_new_unit_agent(self, obs, curr_unit)  # 编队逻辑在此函数中设置
      logger.info(f"[ID {self.log_id}] agent_name = {agent_name}")
      logger.info(f"[ID {self.log_id}] curr_unit = {str(units.get_unit_type(curr_unit.unit_type))} {curr_unit.tag}")
      if agent_name not in self.config.AGENTS:
        logger.debug(f"[ID {self.log_id}] 3.2 skip {str(units.get_unit_type(curr_unit.unit_type))} {curr_unit.tag}")
        self.unit_uid_appear.remove(curr_unit.tag)
        # print('--' * 25)
        continue

      # 移动相机
      if not curr_unit.is_selected:
        func_id, func_call = get_camera_func_smart(self, obs, curr_unit.tag)
        if func_id == 573:
          logger.info(f"[ID {self.log_id}] 3.3 Func Call: {func_call}")
          self.func_id_history.append(func_id)
          return func_call

        # 选择单位
        unit_f = None
        for unit in obs.observation.feature_units:
          if curr_unit.tag == unit.tag:
            unit_f = unit

        if not unit_f.is_selected:
          if self.func_id_history[-1] in [2, 3]:
            d = self.select_rect_threshold
            x1, x2 = min(max(0, unit_f.x - d), self.size_screen), min(max(0, unit_f.x + d), self.size_screen)
            y1, y2 = min(max(0, unit_f.y - d), self.size_screen), min(max(0, unit_f.y + d), self.size_screen)
            func_id, func_call = (3, actions.FUNCTIONS.select_rect('select', (x1, y1), (x2, y2)))
          else:
            x, y = min(max(0, unit_f.x), self.size_screen), min(max(0, unit_f.y), self.size_screen)
            func_id, func_call = (2, actions.FUNCTIONS.select_point('select', (x, y)))
          logger.info(f"[ID {self.log_id}] 3.4.1 Func Call: {func_call}")
          self.func_id_history.append(func_id)
          return func_call

        # if curr_unit.unit_type in WORKER_TYPE:
        #     func_id, func_call = (2, actions.FUNCTIONS.select_point('select', (unit_f.x, unit_f.y)))
        #     logger.info(f"[ID {self.log_id}] 3.4.1 Func Call: {func_call}")
        #     self.func_id_history.append(func_id)
        #     return func_call
        # else:
        #     func_id, func_call = (2, actions.FUNCTIONS.select_point('select_all_type', (unit_f.x, unit_f.y)))
        #     logger.info(f"[ID {self.log_id}] 3.4.2 Func Call: {func_call}")
        #     self.func_id_history.append(func_id)
        #     return func_call

      chosen_team = None
      unit_in_team = False
      for team in self.agents[agent_name].teams:  #
        if curr_unit.tag in team['unit_tags']:
          unit_in_team = True
          chosen_team = team

      # 查找相关小组
      if not unit_in_team:
        relevant_team_list = []
        relevant_team_unit_num = []
        for team in self.agents[agent_name].teams:
          if curr_unit.unit_type in team['unit_type']:
            relevant_team_list.append(team)
            relevant_team_unit_num.append(len(team['unit_tags']))

        if len(relevant_team_unit_num) == 0:
          logger.debug(f"[ID {self.log_id}] self.agents[{agent_name}].teams: {self.agents[agent_name].teams}")

        # 加入小组
        if max(relevant_team_unit_num) == 0:  # 小组全空
          idx = 0
          relevant_team_list[idx]['unit_tags'].append(curr_unit.tag)
          chosen_team = relevant_team_list[0]
        else:
          if relevant_team_list[0]['select_type'] == 'group':  # 平均分配 哪组单位最少给哪组
            relevant_team_dist = get_relevant_team_dist(relevant_team_list, obs, curr_unit)
            if min(relevant_team_unit_num) < 4:  # 平均分组
              idx = relevant_team_unit_num.index(min(relevant_team_unit_num))
              relevant_team_list[idx]['unit_tags'].append(curr_unit.tag)
              chosen_team = relevant_team_list[idx]
            else:  # 分到最近的组
              idx = relevant_team_dist.index(min(relevant_team_dist))
              relevant_team_list[idx]['unit_tags'].append(curr_unit.tag)
              chosen_team = relevant_team_list[idx]
          else:
            relevant_team_dist = get_relevant_team_dist(relevant_team_list, obs, curr_unit)
            if min(relevant_team_dist) < 15:  # 近距离
              idx = relevant_team_dist.index(min(relevant_team_dist))
              relevant_team_list[idx]['unit_tags'].append(curr_unit.tag)
              chosen_team = relevant_team_list[idx]
            elif 0 in relevant_team_unit_num:
              idx = relevant_team_unit_num.index(0)
              relevant_team_list[idx]['unit_tags'].append(curr_unit.tag)
              chosen_team = relevant_team_list[idx]
            else:
              idx = relevant_team_dist.index(min(relevant_team_dist))
              relevant_team_list[idx]['unit_tags'].append(curr_unit.tag)
              chosen_team = relevant_team_list[idx]

      # 移动到小组head的位置(可能是自己，但会不是空小组)
      if chosen_team['select_type'] == 'select_all_type':
        head_unit_tag = chosen_team['unit_tags'][0]
        # 相机移动
        func_id, func_call = get_camera_func_smart(self, obs, head_unit_tag)
        if func_id == 573:
          logger.info(f"[ID {self.log_id}] 3.5 Func Call: {func_call}")
          self.func_id_history.append(func_id)
          return func_call

      # 加入到单位列表
      self.agents[agent_name].unit_tag_list.append(curr_unit.tag)
      self.agents[agent_name].unit_raw_list.append(curr_unit)
      logger.info(
        f"[ID {self.log_id}] 3.6 Finished dealling with {str(units.get_unit_type(curr_unit.unit_type))} {curr_unit.tag}")
      self.unit_uid_appear.remove(curr_unit.tag)

      # 加入编组
      if chosen_team['game_group'] != -1:
        func_id, func_call = (4, actions.FUNCTIONS.select_control_group('append', int(chosen_team['game_group'])))
        logger.info(f"[ID {self.log_id}] 3.7.1 Func Call: {func_call}")
        func_call = func_call if func_id in obs.observation.available_actions else actions.FUNCTIONS.no_op()
        func_id = func_id if func_id in obs.observation.available_actions else 0
        self.func_id_history.append(func_id)
        return func_call
      if chosen_team['select_type'] == 'select_all_type':  # 聚拢单位的功能放到locked_func4
        # 找到单位
        unit_f = None
        for unit in obs.observation.feature_units:
          if unit.tag == head_unit_tag and unit.unit_type not in UNIT_DONOT_NEED_GATHER:
            unit_f = unit
        if unit_f is not None:
          func_id, func_call = (331, actions.FUNCTIONS.Move_screen('now', (unit_f.x, unit_f.y)))
          logger.info(f"[ID {self.log_id}] 3.7.2 Func Call: {func_call}")
          func_call = func_call if func_id in obs.observation.available_actions else actions.FUNCTIONS.no_op()
          func_id = func_id if func_id in obs.observation.available_actions else 0
          self.func_id_history.append(func_id)
          return func_call
      else:
        pass

  # 死亡单位的处理
  if not self.main_loop_lock:
    for tag in self.unit_disappear_steps.keys():
      if self.unit_disappear_steps[tag] < 40:
        if tag in self.unit_uid_disappear:
          self.unit_uid_disappear.remove(tag)
      else:
        if tag not in self.unit_uid_disappear:
          self.unit_uid_disappear.append(tag)
      for key in self.nexus_info_dict.keys():
        if tag in self.nexus_info_dict[key]['worker_m_tag_list']:
          self.nexus_info_dict[key]['worker_m_tag_list'].remove(tag)
        if tag in self.nexus_info_dict[key]['worker_g_tag_list']:
          self.nexus_info_dict[key]['worker_g_tag_list'].remove(tag)
        if tag in self.nexus_info_dict[key]['worker_g1_tag_list']:
          self.nexus_info_dict[key]['worker_g1_tag_list'].remove(tag)
        if tag in self.nexus_info_dict[key]['worker_g2_tag_list']:
          self.nexus_info_dict[key]['worker_g2_tag_list'].remove(tag)

  # 死亡单位剔除出agent的unit_list
  if len(self.unit_disappear_steps.keys()) != 0:
    for agent_name in self.AGENT_NAMES:
      agent = self.agents[agent_name]
      unit_tag_list = []
      for tag in agent.unit_tag_list:
        if tag not in self.unit_disappear_steps.keys():
          unit_tag_list.append(tag)
      agent.unit_tag_list = unit_tag_list
  # print(f"temp debug {self.unit_disappear_steps.keys()}")

  self.unit_uid_total = set(list(self.unit_uid) + list(self.unit_uid_total))

  return func_call


def main_agent_func2(self, obs):
  func_id, func_call = (None, None)

  # region 4处理闲置的工人和超采的工人
  # 获取主矿附近的基本经济信息
  for nexus in obs.observation.raw_units:
    if nexus.alliance == features.PlayerRelative.SELF and nexus.unit_type in BASE_BUILDING_TYPE and nexus.build_progress == 100:
      if str(nexus.tag) not in self.nexus_info_dict.keys():
        self.nexus_info_dict[str(nexus.tag)] = {
          'nexus': nexus,
          'x': nexus.x,
          'y': nexus.y,
          'gas_building_1': None,
          'gas_building_2': None,
          'nearby_gas_building_tag_list': [],
          'nearby_mineral_tag_list': [],
          # 'nearby_worker_tag_list': [],
          'num_worker_m_max': 0,
          'num_worker_g_max': 0,

          'worker_m_tag_list': [],
          'worker_g_tag_list': [],
          'worker_g1_tag_list': [],
          'worker_g2_tag_list': [],
          'num_worker_m': 0,  # mineral
          'num_worker_g': 0,  # gas
        }
      # 查找附近的水晶矿、建成的气站、工人
      for unit in get_nearby_unit_list(nexus, obs.observation.raw_units, dist=10):
        if unit.alliance == features.PlayerRelative.SELF and unit.unit_type in GAS_BUILDING_TYPE and unit.build_progress == 100:
          if unit.tag not in self.nexus_info_dict[str(nexus.tag)]['nearby_gas_building_tag_list']:
            self.nexus_info_dict[str(nexus.tag)]['nearby_gas_building_tag_list'].append(unit.tag)
          if self.nexus_info_dict[str(nexus.tag)]['gas_building_1'] is None:
            self.nexus_info_dict[str(nexus.tag)]['gas_building_1'] = unit
          else:
            if self.nexus_info_dict[str(nexus.tag)]['gas_building_1'].tag != unit.tag:
              self.nexus_info_dict[str(nexus.tag)]['gas_building_2'] = unit
        if unit.unit_type in MINERAL_TYPE:
          if unit.tag not in self.nexus_info_dict[str(nexus.tag)]['nearby_mineral_tag_list']:
            self.nexus_info_dict[str(nexus.tag)]['nearby_mineral_tag_list'].append(unit.tag)
        # if unit.alliance == features.PlayerRelative.SELF and unit.unit_type in WORKER_TYPE:
        #     nexus_info['nearby_worker_tag_list'].append(unit.tag)

      # print(f"nexus {nexus.tag} {nexus.x} {nexus.x}, nearby_mineral_tag_list: {nexus_info['nearby_mineral_tag_list']}")
      self.nexus_info_dict[str(nexus.tag)]['num_worker_m_max'] = min(16, 2 * len(
        self.nexus_info_dict[str(nexus.tag)]['nearby_mineral_tag_list']))
      self.nexus_info_dict[str(nexus.tag)]['num_worker_g_max'] = min(6, 3 * len(
        self.nexus_info_dict[str(nexus.tag)]['nearby_gas_building_tag_list']))

  # 抱着矿或者气的单位，确定工作场所
  for worker in obs.observation.raw_units:
    # 离职处理
    if worker.alliance == features.PlayerRelative.SELF and worker.unit_type in WORKER_TYPE and \
        worker.order_id_0 not in [356, 357, 358, 359, 102, 103, 154, 360, 361, 362]:  # Harvest/HarvestReturn
      for key in self.nexus_info_dict.keys():
        if worker.tag in self.nexus_info_dict[key]['worker_m_tag_list']:
          self.nexus_info_dict[key]['worker_m_tag_list'].remove(worker.tag)
        if worker.tag in self.nexus_info_dict[key]['worker_g_tag_list']:
          self.nexus_info_dict[key]['worker_g_tag_list'].remove(worker.tag)
        if worker.tag in self.nexus_info_dict[key]['worker_g1_tag_list']:
          self.nexus_info_dict[key]['worker_g1_tag_list'].remove(worker.tag)
        if worker.tag in self.nexus_info_dict[key]['worker_g2_tag_list']:
          self.nexus_info_dict[key]['worker_g2_tag_list'].remove(worker.tag)

    if worker.alliance == features.PlayerRelative.SELF and worker.unit_type in WORKER_TYPE and \
        worker.order_id_0 in [356, 357, 358, 359, 102, 103, 154, 360, 361, 362] and \
        worker.buff_id_0 in [271, 274]:
      worker_to = None
      worker_base_tag = None
      # 查找返回类型（抱着矿还是抱着气） TODO: add黄金矿和紫色气，但这些东西可能导致pysc2特征图失效，谨慎添加
      if worker.buff_id_0 in [271]:
        worker_to = 'm'
      elif worker.buff_id_0 in [274]:
        worker_to = 'g'
        dist_min = 999999
        closest_gas_building_tag = None
        for unit_ in obs.observation.raw_units:
          if unit_.alliance == features.PlayerRelative.SELF and unit_.unit_type in GAS_BUILDING_TYPE and \
              unit_.build_progress == 100:
            dist = math.sqrt((worker.x - unit_.x) ** 2 + (worker.y - unit_.y) ** 2)
            if dist < dist_min:
              dist_min = dist
              closest_gas_building_tag = unit_.tag
        if closest_gas_building_tag is not None:
          worker_to = closest_gas_building_tag
      else:
        continue
      # 查找最近的基地
      if worker_to is not None:
        dist_min = 999999
        # worker_base_tag = self.nexus_info_dict.keys()[0]
        for nexus_tag in self.nexus_info_dict.keys():
          nexus_info = self.nexus_info_dict[nexus_tag]
          dist = math.sqrt((worker.x - nexus_info['x']) ** 2 + (worker.y - nexus_info['y']) ** 2)
          if dist < dist_min:
            dist_min = dist
            worker_base_tag = nexus_tag

      # 从原单位去除
      for key in self.nexus_info_dict.keys():
        if worker.tag in self.nexus_info_dict[key]['worker_m_tag_list']:
          self.nexus_info_dict[key]['worker_m_tag_list'].remove(worker.tag)
        if worker.tag in self.nexus_info_dict[key]['worker_g_tag_list']:
          self.nexus_info_dict[key]['worker_g_tag_list'].remove(worker.tag)
        if worker.tag in self.nexus_info_dict[key]['worker_g1_tag_list']:
          self.nexus_info_dict[key]['worker_g1_tag_list'].remove(worker.tag)
        if worker.tag in self.nexus_info_dict[key]['worker_g2_tag_list']:
          self.nexus_info_dict[key]['worker_g2_tag_list'].remove(worker.tag)
      # 加入到基地的所属工人
      if worker_to == 'm':
        self.nexus_info_dict[str(worker_base_tag)]['worker_m_tag_list'].append(worker.tag)
      elif worker_to is not None:
        self.nexus_info_dict[str(worker_base_tag)]['worker_g_tag_list'].append(worker.tag)
        if self.nexus_info_dict[str(worker_base_tag)]['gas_building_1'] is not None and \
            self.nexus_info_dict[str(worker_base_tag)]['gas_building_1'].tag == worker_to:
          self.nexus_info_dict[str(worker_base_tag)]['worker_g1_tag_list'].append(worker.tag)
        if self.nexus_info_dict[str(worker_base_tag)]['gas_building_2'] is not None and \
            self.nexus_info_dict[str(worker_base_tag)]['gas_building_2'].tag == worker_to:
          self.nexus_info_dict[str(worker_base_tag)]['worker_g2_tag_list'].append(worker.tag)
      else:
        print(
          f"worker {worker.tag} closest nexus {worker_base_tag} worker_to {worker_to} {type(worker_to)}, unknown working position")

  # 去除重复单位
  # print(self.nexus_info_dict.keys())
  # print(worker.tag, worker_base_tag)
  for key in self.nexus_info_dict.keys():
    self.nexus_info_dict[key]['worker_m_tag_list'] = list(set(self.nexus_info_dict[key]['worker_m_tag_list']))
    self.nexus_info_dict[key]['worker_g_tag_list'] = list(set(self.nexus_info_dict[key]['worker_g_tag_list']))
    self.nexus_info_dict[key]['worker_g1_tag_list'] = list(set(self.nexus_info_dict[key]['worker_g1_tag_list']))
    self.nexus_info_dict[key]['worker_g2_tag_list'] = list(set(self.nexus_info_dict[key]['worker_g2_tag_list']))
    self.nexus_info_dict[key]['num_worker_m'] = len(self.nexus_info_dict[key]['worker_m_tag_list'])
    self.nexus_info_dict[key]['num_worker_g'] = len(self.nexus_info_dict[key]['worker_g_tag_list'])

  # 选出仍有工作岗位的工作场所
  for nexus in obs.observation.raw_units:
    if nexus.alliance == features.PlayerRelative.SELF and nexus.unit_type in BASE_BUILDING_TYPE and nexus.build_progress == 100:
      nexus_info = self.nexus_info_dict[str(nexus.tag)]
      if nexus_info['num_worker_g_max'] == 0:
        if nexus_info['num_worker_m'] < nexus_info['num_worker_m_max']:
          self.possible_working_place_nexus.append(nexus_info['nexus'])
          self.possible_working_place_tag_list.append(nexus_info['nearby_mineral_tag_list'])
      elif nexus_info['num_worker_m_max'] == 0:
        if nexus_info['num_worker_g'] < nexus_info['num_worker_g_max']:
          self.possible_working_place_nexus.append(nexus_info['nexus'])
          if len(nexus_info['worker_g1_tag_list']) < 3:
            self.possible_working_place_tag_list.append([nexus_info['gas_building_1'].tag])
          else:
            self.possible_working_place_tag_list.append([nexus_info['gas_building_2'].tag])
      elif nexus_info['num_worker_m_max'] != 0 and nexus_info['num_worker_g_max'] != 0:
        if nexus_info['num_worker_m'] / nexus_info['num_worker_m_max'] <= nexus_info['num_worker_g'] / \
            nexus_info['num_worker_g_max']:  # 选择去剩余岗位数更大的
          if nexus_info['num_worker_m'] < nexus_info['num_worker_m_max']:
            self.possible_working_place_nexus.append(nexus_info['nexus'])
            self.possible_working_place_tag_list.append(nexus_info['nearby_mineral_tag_list'])
        else:
          if len(nexus_info['worker_g1_tag_list']) < 3:
            self.possible_working_place_nexus.append(nexus_info['nexus'])
            self.possible_working_place_tag_list.append([nexus_info['gas_building_1'].tag])
          if len(nexus_info['worker_g1_tag_list']) >= 3 and len(nexus_info['worker_g2_tag_list']) < 3 and \
              nexus_info['num_worker_g_max'] == 6:
            self.possible_working_place_nexus.append(nexus_info['nexus'])
            self.possible_working_place_tag_list.append([nexus_info['gas_building_2'].tag])
      else:
        pass

  # 显示分析情况
  self.is_all_nexus_full = True
  for key in self.nexus_info_dict.keys():
    nexus_info = self.nexus_info_dict[key]
    if nexus_info['num_worker_m'] < nexus_info['num_worker_m_max'] or \
        nexus_info['num_worker_g'] < nexus_info['num_worker_g_max'] or \
        (nexus_info['num_worker_g_max'] == 6 and (
            len(nexus_info['worker_g1_tag_list']) < 3 or len(nexus_info['worker_g2_tag_list']) < 3)):
      self.is_all_nexus_full = False
    # from pprint import pprint
    # pprint(nexus_info)
    # print(f"mineral: {nexus_info['num_worker_m']}/{nexus_info['num_worker_m_max']}")
    # print(f"vespene: {len(nexus_info['worker_g1_tag_list'])}+{len(nexus_info['worker_g2_tag_list'])}/{nexus_info['num_worker_g_max']}")
    # print('--' * 25)

  # 闲置的工人重新加入到工作
  if not self.main_loop_lock and self.config.ENABLE_AUTO_WORKER_MANAGE:
    if actions.FUNCTIONS.select_idle_worker.id in obs.observation.available_actions and \
        len(self.possible_working_place_nexus) > 0:

      # 选中工人
      if not (len(obs.observation.single_select) == 1 and
              obs.observation.single_select[0].unit_type in WORKER_TYPE and
              obs.observation.single_select[0].player_relative == features.PlayerRelative.SELF) \
          or (6 not in list(self.func_id_history)):
        func_id, func_call = (6, actions.FUNCTIONS.select_idle_worker('select'))  # 选择一个闲置单位、
        logger.info(f"[ID {self.log_id}] 4.1.1 Func Call: {func_call}")
        func_call = func_call if func_id in obs.observation.available_actions else actions.FUNCTIONS.no_op()
        func_id = func_id if func_id in obs.observation.available_actions else 0
        self.func_id_history.append(func_id)
        return func_call
      if len(obs.observation.single_select) == 1 and \
          obs.observation.single_select[0].unit_type in WORKER_TYPE and \
          obs.observation.single_select[0].player_relative == features.PlayerRelative.SELF and \
          6 in list(self.func_id_history):
        worker = None
        for unit in obs.observation.feature_units:
          if unit.is_selected:
            worker = unit
        for agent_name in self.AGENT_NAMES:
          if 'CombatGroup' in agent_name and worker is not None and worker.tag in self.agents[
            agent_name].unit_tag_list_history:
            func_id, func_call = (274, actions.FUNCTIONS.HoldPosition_quick('now'))  # 站住即可，不要去采集资源
            logger.info(f"[ID {self.log_id}] 4.1.2 Func Call: {func_call}")
            func_call = func_call if func_id in obs.observation.available_actions else actions.FUNCTIONS.no_op()
            func_id = func_id if func_id in obs.observation.available_actions else 0
            self.func_id_history.append(func_id)
            return func_call
      # 选择有工位的、最近的主矿
      min_dist = 999
      min_dist_nexus_i = 0
      source_worker = None
      target_nexus = None
      target_working_position = None
      possible_working_place_nexus_tag_list = get_tag_list(self.possible_working_place_nexus)
      for unit in obs.observation.raw_units:
        if unit.is_selected:
          source_worker = unit
      if source_worker is None:
        logger.critical(f"Do not find any idle worker !")
      else:
        for unit in obs.observation.raw_units:
          if unit.tag in possible_working_place_nexus_tag_list:
            dist = get_dist(source_worker, unit)
            if dist < min_dist:
              min_dist = dist
              target_nexus = unit

        idx = possible_working_place_nexus_tag_list.index(target_nexus.tag)
        working_place_unit_tag_list = self.possible_working_place_tag_list[idx]

        # # 相机移动到主矿
        # if not target_nexus.is_on_screen:
        #     x, y = get_camera_xy(self, target_nexus.x, target_nexus.y)
        #     func_id, func_call = (573, actions.FUNCTIONS.llm_pysc2_move_camera((x, y)))
        #     logger.info(f"[ID {self.log_id}] 4.1.3 Func Call: {func_call}")
        #     self.func_id_history.append(func_id)
        #     return func_call
        # if target_nexus.is_on_screen:
        #     unit = get_feature_unit_list_of_tags(obs, target_nexus.tag)[0]
        #     if not (0.45 * self.size_screen < unit.x < 0.55 * self.size_screen and 0.45 * self.size_screen < unit.y < 0.55 * self.size_screen):
        #         x, y = get_camera_xy(self, target_nexus.x, target_nexus.y)
        #         func_id, func_call = (573, actions.FUNCTIONS.llm_pysc2_move_camera((x, y)))
        #         logger.info(f"[ID {self.log_id}] 4.1.4 Func Call: {func_call}")
        #         self.func_id_history.append(func_id)
        #         return func_call

        # 相机移动
        working_place_unit_list = get_raw_unit_list_of_tags(obs, working_place_unit_tag_list)
        if len(working_place_unit_tag_list) == 0 or len(working_place_unit_list) == 0:
          print(working_place_unit_tag_list)
          print(working_place_unit_list)
        target_working_position = working_place_unit_list[0]
        func_id, func_call = get_camera_func_smart(self, obs, target_working_position.tag)
        if func_id == 573:
          logger.info(f"[ID {self.log_id}] 4.1.3 Func Call: {func_call}")
          self.func_id_history.append(func_id)
          return func_call

        # 选择工位
        working_place_unit_list = get_feature_unit_list_of_tags(obs, working_place_unit_tag_list)
        for unit in working_place_unit_list:
          if unit.is_on_screen and (0 < unit.x < self.size_screen and 0 < unit.y < self.size_screen):
            # 从原单位去除
            for key in self.nexus_info_dict.keys():
              worker = source_worker
              if worker.tag in self.nexus_info_dict[key]['worker_m_tag_list']:
                self.nexus_info_dict[key]['worker_m_tag_list'].remove(worker.tag)
              if worker.tag in self.nexus_info_dict[key]['worker_g_tag_list']:
                self.nexus_info_dict[key]['worker_g_tag_list'].remove(worker.tag)
              if worker.tag in self.nexus_info_dict[key]['worker_g1_tag_list']:
                self.nexus_info_dict[key]['worker_g1_tag_list'].remove(worker.tag)
              if worker.tag in self.nexus_info_dict[key]['worker_g2_tag_list']:
                self.nexus_info_dict[key]['worker_g2_tag_list'].remove(worker.tag)
            # 前往时就设定为新工位的成员，避免到位前的延迟导致的逻辑bug
            if target_working_position.unit_type in MINERAL_TYPE:
              self.nexus_info_dict[str(target_nexus.tag)]['worker_m_tag_list'].append(source_worker.tag)
            if target_working_position.unit_type in GAS_BUILDING_TYPE:
              self.nexus_info_dict[str(target_nexus.tag)]['worker_g_tag_list'].append(source_worker.tag)
              gas_building_1 = self.nexus_info_dict[str(target_nexus.tag)]['gas_building_1']
              gas_building_2 = self.nexus_info_dict[str(target_nexus.tag)]['gas_building_2']
              if gas_building_1 is not None and gas_building_1.tag == target_working_position.tag:
                self.nexus_info_dict[str(target_nexus.tag)]['worker_g1_tag_list'].append(source_worker.tag)
              if gas_building_2 is not None and gas_building_2.tag == target_working_position.tag:
                self.nexus_info_dict[str(target_nexus.tag)]['worker_g2_tag_list'].append(source_worker.tag)
            self.nexus_info_dict[str(target_nexus.tag)]['num_worker_m'] = len(
              self.nexus_info_dict[str(target_nexus.tag)]['worker_m_tag_list'])
            self.nexus_info_dict[str(target_nexus.tag)]['num_worker_g'] = len(
              self.nexus_info_dict[str(target_nexus.tag)]['worker_g_tag_list'])
            # 将闲置工人派遣到新的工作岗位
            func_id, func_call = (264, actions.FUNCTIONS.Harvest_Gather_screen('now', (unit.x, unit.y)))  # 选择一个闲置单位、
            logger.info(f"[ID {self.log_id}] 4.1.5 Func Call: {func_call}")
            self.possible_working_place_nexus = []
            self.possible_working_place_tag_list = []
            func_call = func_call if func_id in obs.observation.available_actions else actions.FUNCTIONS.no_op()
            func_id = func_id if func_id in obs.observation.available_actions else 0
            self.func_id_history.append(func_id)
            return func_call

      # for unit in obs.observation.feature_units:
      #     if unit.tag in working_place_unit_tag_list:
      #         print(f"unit {units.get_unit_type(unit.unit_type)} {unit.tag} {unit.x} {unit.y}")
      #
      # input("waiting here")
      # print(f"working_place_unit_tag_list = {working_place_unit_tag_list}")
      # print(f"working_place_unit_list = {working_place_unit_list}")
      # for unit in working_place_unit_list:
      #     print(f"unit {units.get_unit_type(unit.unit_type)} {unit.tag} {unit.x} {unit.y}")

  # 超采的工人停止工作，进入闲置状态，然后自动重新分配工作
  if not self.main_loop_lock and self.config.ENABLE_AUTO_WORKER_TRAINING and self.is_all_nexus_full is False:
    for key in self.nexus_info_dict.keys():
      nexus_info = self.nexus_info_dict[key]

      if self.stop_worker_nexus_tag is None:
        if len(nexus_info['worker_g2_tag_list']) > 3:
          self.stop_worker_nexus_tag = nexus_info['nexus'].tag
          self.stop_worker_at = 'g2'
        if len(nexus_info['worker_g1_tag_list']) > 3:
          self.stop_worker_nexus_tag = nexus_info['nexus'].tag
          self.stop_worker_at = 'g1'
        if nexus_info['num_worker_m'] > nexus_info['num_worker_m_max']:
          self.stop_worker_nexus_tag = nexus_info['nexus'].tag
          self.stop_worker_at = 'm'

      nexus = nexus_info['nexus']
      if self.stop_worker_nexus_tag is not None and self.stop_worker_nexus_tag == nexus.tag:
        # print(self.stop_worker_nexus_tag)
        # print(get_raw_unit_list_of_tags(obs, self.stop_worker_nexus_tag))

        if self.stop_worker is None:
          unit_list = []
          if self.stop_worker_at == 'm':
            unit_list = get_raw_unit_list_of_tags(obs, nexus_info['worker_m_tag_list'])
          if self.stop_worker_at == 'g1':
            unit_list = get_raw_unit_list_of_tags(obs, nexus_info['worker_g1_tag_list'])
          if self.stop_worker_at == 'g2':
            unit_list = get_raw_unit_list_of_tags(obs, nexus_info['worker_g2_tag_list'])
          self.stop_worker = unit_list[0] if len(unit_list) > 0 else None

        if self.stop_worker is not None:

          stop_worker_unit_list = get_raw_unit_list_of_tags(obs, self.stop_worker.tag)
          # nexus_unit_list = get_raw_unit_list_of_tags(obs, nexus.tag)

          if len(stop_worker_unit_list) == 1:
            self.stop_worker = stop_worker_unit_list[0]

            # nexus = nexus_unit_list[0]
            # if not nexus.is_on_screen:
            #     x, y = get_camera_xy(self, nexus.x, nexus.y)
            #     func_id, func_call = (573, actions.FUNCTIONS.llm_pysc2_move_camera((x, y)))
            #     logger.info(f"[ID {self.log_id}] 4.2.1 Func Call: {func_call}")
            #     self.func_id_history.append(func_id)
            #     return func_call

            if not self.stop_worker.is_on_screen:
              x, y = get_camera_xy(self, self.stop_worker.x, self.stop_worker.y)
              func_id, func_call = (573, actions.FUNCTIONS.llm_pysc2_move_camera((x, y)))
              logger.info(f"[ID {self.log_id}] 4.2.2 Func Call: {func_call}, stop worker at {self.stop_worker_at}")
              self.func_id_history.append(func_id)
              return func_call
            if self.stop_worker.is_on_screen:
              for unit in get_feature_unit_list_of_tags(obs, self.stop_worker.tag):
                if not (
                    0.25 * self.size_screen < unit.x < 0.75 * self.size_screen and 0.25 * self.size_screen < unit.y < 0.75 * self.size_screen):
                  x, y = get_camera_xy(self, self.stop_worker.x, self.stop_worker.y)
                  func_id, func_call = (573, actions.FUNCTIONS.llm_pysc2_move_camera((x, y)))
                  logger.info(f"[ID {self.log_id}] 4.2.3 Func Call: {func_call}, stop worker at {self.stop_worker_at}")
                  self.func_id_history.append(func_id)
                  return func_call

            # # 相机移动
            # func_id, func_call = get_camera_func_smart(self, obs, self.stop_worker.tag)
            # if func_id == 573:
            #     logger.info(f"[ID {self.log_id}] 4.2.3 Func Call: {func_call}, stop worker at {self.stop_worker_at}")
            #     self.func_id_history.append(func_id)
            #     return func_call

            if not self.stop_worker.is_selected:
              for unit in get_feature_unit_list_of_tags(obs, self.stop_worker.tag):
                if unit.tag == self.stop_worker.tag:
                  x, y = min(max(0, unit.x), self.size_screen), min(max(0, unit.y), self.size_screen)
                  func_id, func_call = (2, actions.FUNCTIONS.select_point('select', (unit.x, unit.y)))
                  logger.info(f"[ID {self.log_id}] 4.2.4 Func Call: {func_call}, stop worker at {self.stop_worker_at}")
                  self.func_id_history.append(func_id)
                  return func_call
            else:
              unit = get_feature_unit_list_of_tags(obs, self.stop_worker.tag)[0]
              # func_id, func_call = (274, actions.FUNCTIONS.HoldPosition_quick('now"))
              func_id, func_call = (453, actions.FUNCTIONS.Stop_quick('now'))
              logger.info(f"[ID {self.log_id}] 4.2.5 Func Call: {func_call}, stop worker at {self.stop_worker_at}")
              self.stop_worker_nexus_tag = None
              self.stop_worker_at = None
              self.stop_worker = None
              self.func_id_history.append(func_id)
              func_call = func_call if func_id in obs.observation.available_actions else actions.FUNCTIONS.no_op()
              func_id = func_id if func_id in obs.observation.available_actions else 0
              self.func_id_history.append(func_id)
              return func_call

          else:
            self.stop_worker_nexus_tag = None
            self.stop_worker_at = None
            self.stop_worker = None
  # endregion

  return func_call


def main_agent_func3(self, obs):
  func_id, func_call = (None, None)

  # region 5自动工人生产 （5.1神族Probe，5.2人族SCV，5.3虫族工蜂；主智能体不负责神族星灵加速/人族矿骡生产/虫族女王产卵）
  if not self.main_loop_lock and self.config.ENABLE_AUTO_WORKER_TRAINING:
    if len(self.possible_working_place_nexus) > 0 and self.race == 'zerg':
      num_larva_to_drone = 0
      for unit in obs.observation.raw_units:
        if unit.alliance == features.PlayerRelative.SELF and unit.unit_type in BASE_BUILDING_TYPE and \
            (unit.build_progress == 100 and (not self.is_all_nexus_full) and
             obs.observation.player.minerals > 100 and obs.observation.player.food_workers < 75
             and obs.observation.player.food_cap > obs.observation.player.food_used):

          if 467 in obs.observation.available_actions:
            func_id, func_call = (467, actions.FUNCTIONS.Train_Drone_quick('now'))
            logger.info(f"[ID {self.log_id}] 5.1.1 Func Call: {func_call}")
            func_call = func_call if func_id in obs.observation.available_actions else actions.FUNCTIONS.no_op()
            func_id = func_id if func_id in obs.observation.available_actions else 0
            self.func_id_history.append(func_id)
            return func_call
          if 9 in obs.observation.available_actions:
            func_id, func_call = (9, actions.FUNCTIONS.select_larva())
            logger.info(f"[ID {self.log_id}] 5.1.2 Func Call: {func_call}")
            func_call = func_call if func_id in obs.observation.available_actions else actions.FUNCTIONS.no_op()
            func_id = func_id if func_id in obs.observation.available_actions else 0
            self.func_id_history.append(func_id)
            return func_call

    if len(self.possible_working_place_nexus) > 0 and self.race in ['terran', 'protoss']:
      for unit in obs.observation.raw_units:
        if self.idle_nexus is None and \
          unit.alliance == features.PlayerRelative.SELF and unit.unit_type in BASE_BUILDING_TYPE and \
            (unit.build_progress == 100 and unit.active == 0 and (not self.is_all_nexus_full) and
            obs.observation.player.minerals > 100 and obs.observation.player.food_workers < 75
            and obs.observation.player.food_cap > obs.observation.player.food_used):
          self.idle_nexus = unit
        if self.idle_nexus is not None and self.idle_nexus.tag == unit.tag and not \
            (unit.build_progress == 100 and unit.active == 0 and (not self.is_all_nexus_full) and
             obs.observation.player.minerals > 100 and obs.observation.player.food_workers < 75
             and obs.observation.player.food_cap > obs.observation.player.food_used):
          self.idle_nexus = None
        if self.idle_nexus is not None and unit.tag == self.idle_nexus.tag:
          if not unit.is_on_screen:
            x, y = get_camera_xy(self, unit.x, unit.y)
            func_id, func_call = (573, actions.FUNCTIONS.llm_pysc2_move_camera((x, y)))
            logger.info(f"[ID {self.log_id}] 5.2.1 Func Call: {func_call}")
            self.func_id_history.append(func_id)
            return func_call
          if unit.is_on_screen and not unit.is_selected:
            for unit_ in get_feature_unit_list_of_tags(obs, unit.tag):
              if unit_.tag == unit.tag and not (
                  0.25 * self.size_screen < unit_.x < 0.75 * self.size_screen and 0.25 * self.size_screen < unit_.y < 0.75 * self.size_screen):
                x, y = get_camera_xy(self, unit.x, unit.y)
                func_id, func_call = (573, actions.FUNCTIONS.llm_pysc2_move_camera((x, y)))
                logger.info(f"[ID {self.log_id}] 5.2.2.1 Func Call: {func_call}")
                self.func_id_history.append(func_id)
                return func_call
              if unit_.tag == unit.tag and (
                  0.25 * self.size_screen < unit_.x < 0.75 * self.size_screen and 0.25 * self.size_screen < unit_.y < 0.75 * self.size_screen):
                func_id, func_call = (2, actions.FUNCTIONS.select_point('select', (unit_.x, unit_.y)))
                logger.info(f"[ID {self.log_id}] 5.2.2.2 Func Call: {func_call}")
                self.func_id_history.append(func_id)
                return func_call
          if unit.is_selected:
            self.idle_nexus = None
            if self.race == 'protoss':
              func_id, func_call = (485, actions.FUNCTIONS.Train_Probe_quick('now'))
            elif self.race == 'terran':
              func_id, func_call = (490, actions.FUNCTIONS.Train_SCV_quick('now'))
            else:
              func_id, func_call = (0, actions.FUNCTIONS.on_op())
            logger.info(f"[ID {self.log_id}] 5.2.3 Func Call: {func_call}")
            func_call = func_call if func_id in obs.observation.available_actions else actions.FUNCTIONS.no_op()
            func_id = func_id if func_id in obs.observation.available_actions else 0
            self.func_id_history.append(func_id)
            return func_call
  # endregion

  return func_call


def get_select_func_smart(obs, log_id, tags, size_screen, strict: "0, 1, 2" = 0, disable_rect=False,
                          disable_all_type=False
                          ):
  """
      0 尽量多选中，少选中不希望的，多选也没事
      1 该选的全部都要选中，不该选的多选也没事，暂不支持，涉及到多次选择，可能多选很多东西
      2 该选的全部都要选中，不该选的全部都要去掉，暂不支持，可能因为多选了或者选不中而死循环
  """
  unit_selected_list = []
  unit_todelete_list = []
  unit_toselect_list = []
  unit_toselect_list_building = []
  unit_expected_type_num = {}
  unit_unexpected_type_num = {}
  unit_expected_type = []
  unit_expected_type_building = []
  unit_unexpected_in_rect = []
  unit_unexpected_same_type = []
  enable_select_all_rect = True if not disable_rect else False
  enable_select_all_type = True if not disable_all_type else False
  rect_screen_x, rect_screen_y, rect_screen2_x, rect_screen2_y = 999999, 999999, -1, -1
  # 找出已选的和未选的
  for unit in obs.observation.feature_units:
    if unit.order_id_0 == 547:
      continue
    if unit.tag in tags and unit.is_on_screen and unit.is_selected:
      unit_selected_list.append(unit)
    if unit.tag in tags and unit.is_on_screen and not unit.is_selected:
      unit_toselect_list.append(unit)
      if unit.unit_type not in unit_expected_type:
        unit_expected_type.append(unit.unit_type)
      if unit.unit_type not in unit_expected_type_num.keys():
        unit_expected_type_num[unit.unit_type] = 1
        unit_unexpected_type_num[unit.unit_type] = 0
      else:
        unit_expected_type_num[unit.unit_type] += 1
      if unit.unit_type not in unit_expected_type_building and unit.unit_type in BUILDING_TYPE:
        unit_expected_type_building.append(unit.unit_type)
      if unit.unit_type in unit_expected_type_building:
        unit_toselect_list_building.append(unit)
      if unit.x < rect_screen_x:
        rect_screen_x = unit.x
      if unit.x > rect_screen2_x:
        rect_screen2_x = unit.x
      if unit.y < rect_screen_y:
        rect_screen_y = unit.y
      if unit.y > rect_screen2_y:
        rect_screen2_y = unit.y
    if unit.tag not in tags and unit.is_on_screen and unit.is_selected:
      unit_todelete_list.append(unit)
  # 找出矩形内不该被选中的、同类型全选不该被选中的
  for unit in obs.observation.feature_units:
    if unit.order_id_0 == 547:
      continue
    if unit.tag not in tags and unit.unit_type in unit_expected_type:
      unit_unexpected_same_type.append(unit)
      if unit.unit_type not in unit_unexpected_type_num.keys():
        unit_unexpected_type_num[unit.unit_type] = 1
      else:
        unit_unexpected_type_num[unit.unit_type] += 1
    if unit.tag not in tags and (rect_screen_x <= unit.x <= rect_screen2_x) and (
        rect_screen_y <= unit.y <= rect_screen2_y) and \
        unit.alliance == features.PlayerRelative.SELF and unit.unit_type not in BUILDING_TYPE:
      unit_unexpected_in_rect.append(unit)

  # 这一部分计算操作数什么的可能不是很严格，不等于最优状况下的操作数
  # 计算操作数
  num_act_select = len(unit_toselect_list)
  num_act_select_all_type = len(unit_expected_type)
  num_act_select_rect = 1 + len(unit_expected_type_building)
  # 计算计算单次操作最大选中数量
  num_unit_select = 1
  # num_unit_select_all_type = max(unit_expected_type_num.values())
  num_unit_select_rect = len(unit_toselect_list) - len(unit_toselect_list_building)  # 绝不使用矩形去选建筑，可能选不中死循环
  # 计算单次操作最大误选数量
  num_wrong_select = 0
  # num_wrong_select_all_type = max(unit_unexpected_type_num.values())
  num_wrong_select_rect = len(unit_unexpected_in_rect)
  # 计算全选单位类型的净增加选中量
  unit_expected_type_num_real = {}
  max_unit_type, max_num = None, -1
  for unit_type in unit_expected_type_num.keys():
    unit_expected_type_num_real[unit_type] = unit_expected_type_num[unit_type] - unit_unexpected_type_num[unit_type]
    if unit_expected_type_num_real[unit_type] > max_num:
      max_num = unit_expected_type_num_real[unit_type]
      max_unit_type = unit_type

  if len(unit_toselect_list) != 0:
    logger.debug(f"in get_select_func_smart: "
                 f"\na = {1} / {len(unit_toselect_list)} "
                 f"\nb = {max_num} / {len(unit_toselect_list)} "
                 f"\nc = {num_unit_select_rect - num_wrong_select_rect - 0.5} / {len(unit_toselect_list)}")
  else:
    logger.error(f"[ID {log_id}] in get_select_func_smart: a = {1} / {len(unit_toselect_list)}")
    logger.error(f"[ID {log_id}]                           b = {max_num} / {len(unit_toselect_list)}")
    logger.error(
      f"[ID {log_id}]                           c = {num_unit_select_rect - num_wrong_select_rect - 0.5} / {len(unit_toselect_list)}")
    return (0, actions.FUNCTIONS.no_op())

  # 选择单位
  if strict == 0:
    # 计算剩余操作数
    a = 1 / num_act_select
    b = max_num / num_act_select
    c = (num_unit_select_rect - num_wrong_select_rect - 0.5) / num_act_select  # 矩形apm更高，权重上减0.5
    abc_list = [a, b, c]

    unit = unit_toselect_list[0]
    if a == max(abc_list):
      flag_select = 'select' if len(unit_selected_list) == 0 else 'add'
      x0, y0 = max(0, min(unit.x - 0.1, size_screen)), max(0, min(unit.y - 0.1, size_screen))
      x1, y1 = max(0, min(unit.x + 0.1, size_screen)), max(0, min(unit.y + 0.1, size_screen))
      return (3, actions.FUNCTIONS.select_rect(flag_select, (x0, y0), (x1, y1)))  # 单选
    if b == max(abc_list):
      unit_type, min_dist = None, 99999
      flag_select = 'select_all_type' if len(unit_selected_list) == 0 else 'add_all_type'
      for unit in unit_toselect_list:
        if unit.unit_type == max_unit_type:
          x0, y0 = max(0, min(unit.x, size_screen)), max(0, min(unit.y, size_screen))
          return (2, actions.FUNCTIONS.select_point(flag_select, (x0, y0)))  # 同类全选
    if c == max(abc_list) and (rect_screen_x < rect_screen2_x) and (rect_screen_x < rect_screen2_x):
      flag_select = 'select' if len(unit_selected_list) == 0 else 'add'
      x0, y0 = max(0, min(rect_screen_x, size_screen)), max(0, min(rect_screen_y, size_screen))
      x1, y1 = max(0, min(rect_screen2_x, size_screen)), max(0, min(rect_screen2_y, size_screen))
      return (3, actions.FUNCTIONS.select_rect(flag_select, (x0, y0), (x1, y1)))  # 矩形全选
  elif strict == 1:
    return (0, actions.FUNCTIONS.no_op())
  elif strict == 2:
    return (0, actions.FUNCTIONS.no_op())
  else:
    return (0, actions.FUNCTIONS.no_op())
  return (0, actions.FUNCTIONS.no_op())


def main_agent_func4(self, obs):
  func_id, func_call = (None, None)

  # 小队聚拢模块
  self.flag_locked_func4 = False

  # 第一次交互LLM前无需进行单位聚拢
  if self.main_loop_step == 0:
    return func_call

  # for unit in obs.observation.raw_units:  # main_loop_lock放锁之后，大部分情况只有最后一个小组的单位被select
  #     self.unit_selected_tag_list = []
  #     if unit.is_selected:
  #         self.unit_selected_tag_list.append(unit.tag)

  if not self.main_loop_lock:

    # 走散的单位聚拢到head单位
    unselected_unit_num = None
    for agent_name in self.AGENT_NAMES:
      if self.temp_head_unit_tag is not None:
        break
      else:
        agent = self.agents[agent_name]
        for team in agent.teams:
          team_unit_tags = team['unit_tags']
          if team['select_type'] == 'select':
            break
          else:
            unselected_unit_num = 0
            for unit_tag in team['unit_tags']:
              if unit_tag not in team['unit_tags_selected']:
                unselected_unit_num += 1
            if 0 < unselected_unit_num < len(team['unit_tags']):
              self.temp_head_unit_tag = team['unit_tags'][0]
              self.temp_team_unit_tags = team['unit_tags']
              logger.debug(f"[ID {self.log_id}] main_agent_func4: Agent {agent_name} team {team['name']} need to gather")

    # print(f"locked_func_4: unselected_unit_num {unselected_unit_num} {len(self.temp_team_unit_tags)} {len(self.unit_selected_tag_list)}")
    # time.sleep(5)

    if self.temp_head_unit_tag is not None:
      for unit in obs.observation.raw_units:
        if unit.tag in self.temp_team_unit_tags and unit.tag not in self.unit_selected_tag_list and \
            unit.order_id_0 != 547 and self.temp_curr_unit_tag is None:
          self.temp_curr_unit_tag = unit.tag
          logger.debug(f"[ID {self.log_id}] main_agent_func4: find temp_curr_unit_tag {unit.unit_type} {unit.tag} {unit.x} {unit.y}")
          # time.sleep(5)
      # if self.temp_curr_unit_tag is None:
      #     print(f"locked_func_4: cannot find temp_curr_unit_tag")
      #     time.sleep(5)
      # for tag in self.temp_team_unit_tags:
      #     if tag not in self.unit_selected_tag_list and self.temp_curr_unit_tag is None:
      #         self.temp_curr_unit_tag = tag
      for unit in obs.observation.raw_units:
        if self.temp_head_unit_tag is not None and unit.tag == self.temp_head_unit_tag:
          self.temp_head_unit = unit
        if self.temp_curr_unit_tag is not None and unit.tag == self.temp_curr_unit_tag:
          self.temp_curr_unit = unit

    if self.temp_head_unit is not None and self.temp_curr_unit is not None:
      self.flag_locked_func4 = True

      # 选取单位
      if not self.temp_curr_unit.is_selected:

        # 移动相机到走散的单位
        func_id, func_call = get_camera_func_smart(self, obs, self.temp_curr_unit.tag, threshold=0.35)
        if func_id == 573:
          logger.info(f"[ID {self.log_id}] main_agent_func4: camera to curr unit, Func Call: {func_call}")
          self.func_id_history.append(func_id)
          # time.sleep(5)
          return func_call

        # 根据单位选取方案选择该单位
        # unit_f = None
        # for unit in obs.observation.feature_units:
        #     if unit.tag == self.temp_curr_unit_tag:
        #         unit_f = unit
        # 判断屏幕附近有无未选中的单位
        screen_team_unit_unselected = []
        for unit in obs.observation.feature_units:
          if unit.tag in self.temp_team_unit_tags and unit.is_on_screen and not unit.is_selected:
            screen_team_unit_unselected.append(unit)
        # if unit_f is None:
        #     logger.error(f"[ID {self.log_id}] locked_func_4: curr unit of tag {tag} not found, unit_f is None")
        #     self.unit_selected_tag_list.append(self.temp_curr_unit_tag)
        #     self.temp_head_unit_tag = None
        #     self.temp_curr_unit_tag = None
        #     self.temp_head_unit = None
        #     self.temp_curr_unit = None
        if len(screen_team_unit_unselected) > 0:
          func_id, func_call = get_select_func_smart(obs, self.log_id, self.temp_team_unit_tags, self.size_screen)
          if func_id != 0:
            logger.debug(f"[ID {self.log_id}] main_agent_func4: get_select_func_smart call func {func_call}")
          if func_id == 0:
            unit_f = screen_team_unit_unselected[0]
            x, y = min(max(0, unit_f.x), self.size_screen), min(max(0, unit_f.y), self.size_screen)
            func_id, func_call = (2, actions.FUNCTIONS.select_point('toggle', (x, y)))
            logger.debug(f"[ID {self.log_id}] main_agent_func4: get_select_func_smart return func_id=0")
          logger.info(f"[ID {self.log_id}] main_agent_func4: smart select curr unit, Func Call: {func_call}")
          self.func_id_history.append(func_id)
          return func_call

      # # 全选校验
      # if self.temp_curr_unit.is_selected and self.temp_curr_unit.is_on_screen:
      #     unit_f = None
      #     for unit in obs.observation.feature_units:
      #         if unit.tag == self.temp_curr_unit_tag:
      #             unit_f = unit
      #     for unit in obs.observation.feature_units:
      #         if unit.unit_type == unit_f.unit_type and not unit.is_selected and \
      #                 0.25 * self.size_screen < unit.x < 0.75 * self.size_screen and \
      #                 0.25 * self.size_screen < unit.y < 0.75 * self.size_screen:
      #             logger.info(f"[ID {self.log_id}] locked_func_4: re—select")
      #             func_id, func_call = (2, actions.FUNCTIONS.select_point('select_all_type', (unit_f.x, unit_f.y)))
      #             logger.info(f"[ID {self.log_id}] locked_func_4: re—select, Func Call: {func_call}")
      #             # time.sleep(5)
      #             self.func_id_history.append(func_id)
      #             return func_call

      # 移动相机到小组的head单位

      func_id, func_call = get_camera_func_smart(self, obs, self.temp_head_unit.tag)
      if func_id == 573:
        logger.info(f"[ID {self.log_id}] main_agent_func4: camera to head unit, Func Call: {func_call}")
        self.func_id_history.append(func_id)
        # time.sleep(5)
        return func_call

      # 令该单位追随小组的head单位
      unit_f = None
      for unit in obs.observation.feature_units:
        if unit.tag == self.temp_head_unit_tag:
          unit_f = unit
      if unit_f is None:
        logger.error(f"[ID {self.log_id}] main_agent_func4: head unit of tag {self.temp_head_unit_tag} not found, unit_f is None")
        self.unit_selected_tag_list.append(self.temp_curr_unit_tag)
      else:
        func_id, func_call = (331, actions.FUNCTIONS.Move_screen('now', (unit_f.x, unit_f.y)))
        logger.info(f"[ID {self.log_id}] main_agent_func4: move to head unit, Func Call: {func_call}")

        # 选中的单位加入到unit_selected_tag_list
        self.flag_locked_func4 = False
        for unit in obs.observation.raw_units:
          if unit.is_selected:
            self.unit_selected_tag_list.append(unit.tag)
        self.temp_head_unit_tag = None
        self.temp_curr_unit_tag = None
        self.temp_head_unit = None
        self.temp_curr_unit = None
        # time.sleep(5)
        func_call = func_call if func_id in obs.observation.available_actions else actions.FUNCTIONS.no_op()
        func_id = func_id if func_id in obs.observation.available_actions else 0
        self.func_id_history.append(func_id)
        return func_call

    if self.flag_locked_func4:
      # else:
      logger.error(f"[ID {self.log_id}] main_agent_func4: Something wrong")
      logger.error(f"[ID {self.log_id}]                   self.unit_selected_tag_list = {self.unit_selected_tag_list}")
      logger.error(f"[ID {self.log_id}]                   len(self.unit_selected_tag_list) = {len(self.unit_selected_tag_list)}")
      logger.error(f"[ID {self.log_id}]                   self.temp_head_unit_tag = {self.temp_head_unit_tag}")
      logger.error(f"[ID {self.log_id}]                   self.temp_curr_unit_tag = {self.temp_curr_unit_tag}")
      logger.error(f"[ID {self.log_id}]                   self.temp_head_unit = {self.temp_head_unit}")
      logger.error(f"[ID {self.log_id}]                   self.temp_curr_unit = {self.temp_curr_unit}")
      if self.temp_curr_unit_tag is not None:
        self.unit_selected_tag_list.append(self.temp_curr_unit_tag)
      self.temp_head_unit_tag = None
      self.temp_curr_unit_tag = None
      self.temp_head_unit = None
      self.temp_curr_unit = None
      time.sleep(5)

  return func_call


def main_agent_func_critical_data_log(self, obs):
  func_id, func_call = (None, None)
  status1_agent_names = []
  status2_agent_names = []
  status3_agent_names = []
  for agent_name in self.AGENT_NAMES:
    agent = self.agents[agent_name]
    if agent.enable:
      if agent._is_waiting_query():
        status1_agent_names.append(agent_name)
        logger.debug(f"[ID {self.log_id}] Agent {agent_name} Status = [1] is_waiting_query")
      if agent._is_waiting_response():
        status2_agent_names.append(agent_name)
        logger.debug(f"[ID {self.log_id}] Agent {agent_name} Status = [2] is_waiting_response")
      if agent._is_executing_actions():
        status3_agent_names.append(agent_name)
        logger.debug(f"[ID {self.log_id}] Agent {agent_name} Status = [3] is_executing_actions")
      logger.debug(
        f"[ID {self.log_id}]       num Units = {len(agent.unit_tag_list)} {len(agent.unit_tag_list_history)}")
      logger.debug(
        f"[ID {self.log_id}]       num Actions = {len(agent.func_list)} {len(agent.action_list)} {len(agent.action_lists)}")
      logger.debug(f"[ID {self.log_id}]       Actions = {agent.action_list}")  # 可能打印出来非常长非常混乱
      for team in agent.teams:
        if len(team['unit_tags']) != 0:
          logger.debug(f"[ID {self.log_id}]       Team = team_name:{team['name']} "
                       f"unit_type:{team['unit_type']} game_group:{team['game_group']} "
                       f"select_type:{team['select_type']} num_obs:{len(team['obs'])} num_pos:{len(team['pos'])}")
          logger.debug(
            f"[ID {self.log_id}]              unit_tags:{team['unit_tags']} unit_tags_selected:{team['unit_tags_selected']}")
  logger.debug(f"[ID {self.log_id}] " + "--" * 25)
  logger.debug(f"[ID {self.log_id}] Loop{self.main_loop_step} Main Status = "
               f"{not self._all_agent_query_llm_finished()} "
               f"{not self._all_agent_waiting_response_finished()} "
               f"{not self._all_agent_executing_finished()}")
  game_second = str(int(obs.observation.game_loop / 22.4) % 60)
  game_second = game_second if len(game_second) == 2 else '0' + game_second
  logger.info(f"[ID {self.log_id}] GameTime {int(obs.observation.game_loop / 22.4 / 60)}:{game_second} "
              f"Loop{self.main_loop_step} Main Status = "
              f"[1]{len(status1_agent_names)} (_is_waiting_query) "
              f"[2]{len(status2_agent_names)} (_is_waiting_response) "
              f"[3]{len(status3_agent_names)} (_is_executing_actions) ")
  logger.debug(f"[ID {self.log_id}]     self.unit_selected_tag_list  = {self.unit_selected_tag_list}")
  logger.debug(f"[ID {self.log_id}] len(self.unit_selected_tag_list) = {len(self.unit_selected_tag_list)}")
  logger.debug(f"[ID {self.log_id}] " + "--" * 25)
  last_20_func = list(self.func_id_history)
  if 0 in last_20_func:
    last_20_func.remove(0)
  if len(set(last_20_func)) == 1 and len(last_20_func) >= 20:
    logger.error(f"[ID {self.log_id}] Detect Possible Endless Loop !")
    logger.error(f"[ID {self.log_id}] last 20 funcs: {actions.FUNCTIONS[self.func_id_history[0]]}")
    time.sleep(1)
  return func_call
