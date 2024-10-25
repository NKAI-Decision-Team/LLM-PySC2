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


from llm_pysc2.lib.llm_communicate import communication_info_transmission
from llm_pysc2.lib.data_recorder import DataRecorder
from llm_pysc2.agents.main_agent_funcs import *
from llm_pysc2.agents.configs import ProtossAgentConfig
from llm_pysc2.agents.llm_pysc2_agent import LLMAgent

from pysc2.agents import base_agent
from pysc2.lib import actions

from collections import deque
from shutil import copyfile
from loguru import logger
import threading
import datetime
import random
import time
import sys
import os


llm_pysc2_global_log_id = 0


# multi thread query, target function
def thread_act(agent, obs):
  agent.query(obs)


# Main Agent, for interacting with pysc2 env
class MainAgent(base_agent.BaseAgent):

  def __init__(self, config=ProtossAgentConfig(), SubAgent=LLMAgent):
    super(MainAgent, self).__init__()
    """initalize the main agent"""
    self.start_time = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    self.config = config
    self.AGENT_NAMES = list(self.config.AGENTS.keys())
    self.race = self.config.race
    self._initialize_variables()
    self._initialize_logger()
    self.config.auto_check(self.log_id)
    self._initialize_agents(SubAgent)
    self._initialize_data_recorder()
    logger.success(f"[ID {self.log_id}] Main Agent successfully initialized!")

  def _logger_filter_function(self, record):
    return f"[ID {self.log_id}]" in record["message"]

  def _initialize_variables(self):
    self.main_loop_lock = False
    self.main_loop_step_old = 0
    self.main_loop_step = 0
    self.game_time_last = 0

    self.unit_selected_tag_list = []
    self.temp_team_unit_tags = None
    self.temp_head_unit_tag = None
    self.temp_curr_unit_tag = None
    self.temp_head_unit = None
    self.temp_curr_unit = None

    self.agent_id = 0
    self.size_screen = 0
    self.size_minimap = 0
    self.camera_threshold = 0.15
    self.select_rect_threshold = 1

    self.num_step = -1
    self.world_range = 0
    self.world_x_offset = 0
    self.world_y_offset = 0
    self.world_xy_calibration = False
    self.first_select_unit_tag = None
    self.last_two_camera_pos = deque(maxlen=2)
    self.last_two_camera_pos.append([-1, -1])
    self.last_two_camera_pos.append([-1, -1])

    self.new_unit_tag = None
    self.new_unit_type = None
    self.temp_flag = None
    self.unit_uid = list()
    self.unit_uid_dead = list()
    self.unit_uid_disappear = list()
    self.unit_uid_appear = list()
    self.unit_uid_total = list()
    self.unit_disappear_steps = dict()

    # self.possible_disappear_unit_list = list()
    self.func_id_history = deque(maxlen=20)
    self.obs_history = deque(maxlen=5)

    self.nexus_info_dict = {}
    self.possible_working_place_tag_list = []
    self.possible_working_place_nexus = []
    self.stop_worker_nexus_tag = None
    self.stop_worker_at = None
    self.stop_worker = None
    self.idle_nexus = None

  def _initialize_logger(self):

    global llm_pysc2_global_log_id

    time.sleep(random.random())
    base_log_dir = f"{os.path.dirname(os.path.abspath(__file__))}/../../llm_log"
    if not os.path.exists(base_log_dir):
      os.mkdir(base_log_dir)
    if not os.path.exists(base_log_dir + f"/log_show.py"):
      copyfile(f"{os.path.dirname(os.path.abspath(__file__))}/../lib/log_show.py", base_log_dir + f"/log_show.py")
    if not os.path.exists(base_log_dir + f"/log_analyse.py"):
      copyfile(f"{os.path.dirname(os.path.abspath(__file__))}/../lib/log_analyse.py", base_log_dir + f"/log_analyse.py")

    self.log_id = -1
    while True:
      self.log_id += 1
      self.log_dir_path = f"{os.path.dirname(os.path.abspath(__file__))}/../../llm_log/{self.start_time}-{self.log_id}"
      if not os.path.exists(self.log_dir_path) and self.log_id == llm_pysc2_global_log_id + 1:
        llm_pysc2_global_log_id += 1
        self.log_error_path = self.log_dir_path + f"/log_error.txt"
        self.log_success_path = self.log_dir_path + f"/log_success.txt"
        self.log_debug_path = self.log_dir_path + f"/log_debug.txt"
        self.log_info_path = self.log_dir_path + f"/log_info.txt"
        os.mkdir(self.log_dir_path)
        break

    if not os.path.exists(self.log_error_path):
      with open(self.log_error_path, 'w') as f:
        print(self.start_time, file=f)
    if not os.path.exists(self.log_success_path):
      with open(self.log_success_path, 'w') as f:
        print(self.start_time, file=f)
    if not os.path.exists(self.log_debug_path):
      with open(self.log_debug_path, 'w') as f:
        print(self.start_time, file=f)
    if not os.path.exists(self.log_info_path):
      with open(self.log_info_path, 'w') as f:
        print(self.start_time, file=f)

    logger.add(self.log_error_path, level="ERROR", rotation="100 MB", catch=True, filter=self._logger_filter_function)
    logger.add(self.log_success_path, level="SUCCESS", rotation="100 MB", catch=True, filter=self._logger_filter_function)
    logger.add(self.log_debug_path, level="DEBUG", rotation="100 MB", catch=True, filter=self._logger_filter_function)
    logger.add(self.log_info_path, level="INFO", rotation="100 MB", catch=True, filter=self._logger_filter_function)
    if self.log_id == 1:
      try:
        logger.remove(handler_id=0)
        logger.add(sys.stderr, level="INFO", catch=True, filter=self._logger_filter_function)
      except:
        pass

  def _initialize_agents(self, SubAgent):
    self.agents = {}
    self.agents_query_llm_times = {}
    self.agents_executing_times = {}

    for agent_name in self.AGENT_NAMES:
      self.agents[agent_name] = SubAgent(agent_name, self.log_id, self.start_time, self.config)
      self.agents[agent_name].enable = True if (agent_name in ['Commander', 'Developer']) else False
      # self.agents[agent_name].flag_enable_empty_unit_group = True if (agent_name in ['Developer']) else False
      for team in self.config.AGENTS[agent_name]['team']:
        if team['name'] == 'Empty' and len(team['unit_type']) == 0:
          self.agents[agent_name].flag_enable_empty_unit_group = True
      self.agents_query_llm_times[agent_name] = 0
      self.agents_executing_times[agent_name] = 0
      self.agents[agent_name].log_id = self.log_id

  def _initialize_data_recorder(self):
    self.data_recorder = DataRecorder(self.log_dir_path, save_level=0)

  def _all_agent_query_llm_finished(self):
    for agent_name in self.AGENT_NAMES:
      agent = self.agents[agent_name]
      if agent.enable and agent.query_llm_times == self.main_loop_step:
        return False
    return True

  def _all_agent_waiting_response_finished(self):
    for agent_name in self.AGENT_NAMES:
      agent = self.agents[agent_name]
      if agent.enable and (agent.query_llm_times == self.main_loop_step + 1) and agent._is_waiting_response():
        return False
    return True

  def _all_agent_executing_finished(self):
    for agent_name in self.AGENT_NAMES:
      agent = self.agents[agent_name]
      if agent.enable and agent.executing_times == self.main_loop_step:
        return False
    return True

  def step(self, obs):
    super(MainAgent, self).step(obs)

    # main agent control data updates
    agent_name = None
    self.obs_history.append(obs)
    self.data_recorder.step(obs, self.episodes, self.steps)
    if len(self.func_id_history) > 0 and self.func_id_history[-1] == 573:
      self.camera_threshold += 0.05
    elif len(self.func_id_history) > 0 and self.func_id_history[-1] == 3:
      self.select_rect_threshold *= 2
    else:
      self.select_rect_threshold = 1 * int(self.size_screen / 128) if self.size_screen != 0 else 1
      self.camera_threshold = 0.15
    if self.main_loop_step_old != self.main_loop_step:
      self.main_loop_step_old = self.main_loop_step
      self.main_loop_lock = False
      logger.success(f"[ID {self.log_id}] " + '========== ' + '==' * 25 + f" Loop {self.main_loop_step} " + '==' * 25 + ' ==========')
    logger.success(f"[ID {self.log_id}] " + '---------- ' + '--' * 25 + f" Step {self.steps} " + '--' * 25 + ' ----------')
    func_id, func_call = (0, actions.FUNCTIONS.no_op())

    # initial steps and camera calibration (necessary)
    func_call = main_agent_func0(self, obs)
    if func_call is not None:
      logger.success(f"[ID {self.log_id}] main_agent_func0: Func Call {func_call}")
      return func_call

    # unit grouping, add to relevant agent.teams (necessary)
    func_call = main_agent_func1(self, obs)
    if func_call is not None:
      logger.success(f"[ID {self.log_id}] main_agent_func1: Func Call {func_call}")
      return func_call

    # auto worker-management (optional)
    func_call = main_agent_func2(self, obs)
    if func_call is not None:
      logger.success(f"[ID {self.log_id}] main_agent_func2: Func Call {func_call}")
      return func_call

    # auto worker-training (optional)
    func_call = main_agent_func3(self, obs)
    if func_call is not None:
      logger.success(f"[ID {self.log_id}] main_agent_func3: Func Call {func_call}")
      return func_call

    # auto team gathering (optional)
    func_call = main_agent_func4(self, obs)
    if func_call is not None:
      logger.success(f"[ID {self.log_id}] main_agent_func4: Func Call {func_call}")
      return func_call

    # SubAgent data update
    for agent_name in self.AGENT_NAMES:
      agent = self.agents[agent_name]
      agent.num_step = self.steps
      agent.main_loop_step = self.main_loop_step
      agent.world_range = self.world_range
      agent.world_x_offset = self.world_x_offset
      agent.world_y_offset = self.world_y_offset
      agent.size_screen = self.size_screen
      agent.size_minimap = self.size_minimap
      agent.update(obs)
    for agent_name in self.AGENT_NAMES:
      agent = self.agents[agent_name]
      agent.other_agents = {}
      if agent.name in ['Commander', 'Developer']:
        for agent_name2 in self.AGENT_NAMES:
          if agent_name2 not in ['Commander', 'Developer']:
            agent.other_agents[agent_name2] = self.agents[agent_name2]

    # critical data log
    main_agent_func_critical_data_log(self, obs)

    # LLM decision frequency control
    game_time_s = obs.observation.game_loop / 22.4
    if not self.main_loop_lock and game_time_s - self.game_time_last < 1 / self.config.MAX_LLM_DECISION_FREQUENCY:
      logger.warning(f"[ID {self.log_id}] Reach MAX_LLM_DECISION_FREQUENCY! return no_op()")
      func_id, func_call = (0, actions.FUNCTIONS.no_op())
      self.func_id_history.append(func_id)
      return func_call

    # skip main loop if no agent enabled
    all_agent_disabled = True
    for agent_name in self.AGENT_NAMES:
      if self.agents[agent_name].enable:
        all_agent_disabled = False
    if all_agent_disabled:
      logger.warning(f"[ID {self.log_id}] All agent disabled! return no_op()")
      func_id, func_call = (0, actions.FUNCTIONS.no_op())
      self.func_id_history.append(func_id)
      return func_call

    # communication and ready to enter main loop
    if self.main_loop_lock is False:
      self.main_loop_lock = True
      self.game_time_last = game_time_s
      communication_info_transmission(self)
      logger.success(f"[ID {self.log_id}] 7.0 Main Loop Lock! Ignore outer-loop actions. ")


    # Main Loop
    t0 = float(time.time())
    while float(time.time()) - t0 < self.config.MAX_LLM_WAITING_TIME:
      time.sleep(0.001)

      agent_name = self.AGENT_NAMES[self.agent_id]
      agent = self.agents[self.AGENT_NAMES[self.agent_id]]
      func_id, func_call = (None, None)

      if not agent.enable:  # agent finished query, skip current agent
        self.agent_id = (self.agent_id + 1) % len(self.AGENT_NAMES)
        continue

      if not self._all_agent_query_llm_finished():

        if not agent._is_waiting_query():
          logger.error(f"[ID {self.log_id}] 7.0 Agent {agent_name}: status should not exist")
          logger.debug(f"[ID {self.log_id}]     Agent Info: {len(agent.func_list)} {len(agent.action_list)} {len(agent.action_lists)} {agent.is_waiting}")
          # for team in agent.teams:
          #   logger.debug(f"[ID {self.log_id}]     Team Infos:{team}")
          agent.func_list, agent.action_list, agent.action_lists = [], [], []  #  TODO: Test this
          self.agent_id = (self.agent_id + 1) % len(self.AGENT_NAMES)
          # continue

        else:  # collect obs and query llm
          logger.info(f"[ID {self.log_id}] 7.1 Agent {agent_name}: query status")

          # agent teams' obses all collected, start query llm
          if agent._is_all_my_teams_ready_to_query():
            if agent.flag_enable_empty_unit_group:  # Commander Developer最后一个单位群是空群，用于作战部署或发布训练/研究动作
              logger.info(f"[ID {self.log_id}] 7.1.1 Agent {agent_name}: Add obs for empty_unit_group")
              for team in agent.teams:
                if team['name'] == 'Empty':
                  agent.team_unit_obs_list.append(obs)
                  team['obs'].append(obs)
            logger.info(f"[ID {self.log_id}] 7.1.2 Agent {agent_name}: Obs prepared, try calling LLM api")
            logger.debug(f"[ID {self.log_id}] len(agent.team_unit_obs_list) = {len(agent.team_unit_obs_list)}")
            logger.debug(f"[ID {self.log_id}] len(agent.team_unit_tag_list) = {len(agent.team_unit_tag_list)}")
            logger.debug(f"[ID {self.log_id}] len(agent.team_unit_team_list) = {len(agent.team_unit_team_list)}")
            agent.thread = threading.Thread(target=thread_act, args=(agent, obs))
            agent.thread.start()
            agent.query_llm_times += 1
            self.agent_id = (self.agent_id + 1) % len(self.AGENT_NAMES)
            self.unit_selected_tag_list = []
            if self._all_agent_query_llm_finished():
              logger.success(f"[ID {self.log_id}] 7.2 All Agent waiting for response")

          else:
            # obtain team and head unit tag
            logger.debug(f"[ID {self.log_id}] Agent {agent_name} status: 7.1.3")
            team, tag = agent._get_unobsed_team_and_unit_tag()

            # Move camera
            func_id, func_call = get_camera_func_smart(self, obs, tag, threshold=self.camera_threshold)
            if func_id == 573:
              logger.success(f"[ID {self.log_id}] 7.1.4 Func Call: {func_call}")
              self.func_id_history.append(func_id)
              return func_call

            # Find team head unit
            unit_f = None
            for unit in obs.observation.feature_units:
              if unit.tag == tag:
                unit_f = unit
            if unit_f is None:
              logger.error(f"[ID {self.log_id}] Agent {agent_name}: unit of tag {tag} not found")
              logger.error(f"[ID {self.log_id}]                     relative team = {team}")
              logger.error(f"[ID {self.log_id}] unit_f is None")
              if tag in team['unit_tags']:
                team['unit_tags'].remove(tag)
              if tag in agent.unit_tag_list:
                agent.unit_tag_list.remove(tag)
              agent.update(obs)
              time.sleep(1)
              continue

            # Select unit
            if not unit_f.is_selected:
              logger.debug(f"[ID {self.log_id}] Agent {agent_name} status: 7.1.5")
              if team['select_type'] == 'select':
                logger.debug(f"[ID {self.log_id}] Agent {agent_name} status: 7.1.5.1")
                if self.func_id_history[-1] in [2, 3]:
                  d = self.select_rect_threshold
                  x1, x2 = min(max(0, unit_f.x - d), self.size_screen), min(max(0, unit_f.x + d), self.size_screen)
                  y1, y2 = min(max(0, unit_f.y - d), self.size_screen), min(max(0, unit_f.y + d), self.size_screen)
                  func_id, func_call = (3, actions.FUNCTIONS.select_rect('select', (x1, y1), (x2, y2)))
                else:
                  x, y = min(max(0, unit_f.x), self.size_screen), min(max(0, unit_f.y), self.size_screen)
                  func_id, func_call = (2, actions.FUNCTIONS.select_point('select', (x, y)))
                logger.success(f"[ID {self.log_id}] 7.1.5.1 Agent {agent_name}: Func Call: {func_call}")
                self.func_id_history.append(func_id)
                return func_call
              elif team['select_type'] == 'select_all_type':
                logger.debug(f"[ID {self.log_id}] Agent {agent_name} status: 7.1.5.2")
                if self.func_id_history[-1] in [2, 3]:
                  d = self.select_rect_threshold
                  x1, x2 = min(max(0, unit_f.x - d), self.size_screen), min(max(0, unit_f.x + d), self.size_screen)
                  y1, y2 = min(max(0, unit_f.y - d), self.size_screen), min(max(0, unit_f.y + d), self.size_screen)
                  func_id, func_call = (3, actions.FUNCTIONS.select_rect('select', (x1, y1), (x2, y2)))
                else:
                  x, y = min(max(0, unit_f.x), self.size_screen), min(max(0, unit_f.y), self.size_screen)
                  func_id, func_call = (2, actions.FUNCTIONS.select_point('select_all_type', (x, y)))
                logger.success(f"[ID {self.log_id}] 7.1.5.1 Agent {agent_name}: Func Call: {func_call}")
                self.func_id_history.append(func_id)
                return func_call
              elif team['select_type'] == 'group':
                logger.debug(f"[ID {self.log_id}] Agent {agent_name} status: 7.1.5.3")
                func_id, func_call = (4, actions.FUNCTIONS.select_control_group('recall', int(team['game_group'])))
                logger.success(f"[ID {self.log_id}] 7.1.5.1 Agent {agent_name}: Func Call: {func_call}")
                self.func_id_history.append(func_id)
                return func_call
              else:
                logger.error(f"[ID {self.log_id}] 7.1.2.4 Agent {agent_name}: Un-Recogniziable select type")
                time.sleep(5)  # this error may lead to endless loop
                pass

            # # Recheck all required unit selected (Warning: May Lead To Possible Endless Loop)
            # for unit in obs.observation.feature_units:
            #   if team['select_type'] == 'select_all_type' and \
            #       unit.unit_type == unit_f.unit_type and not unit.is_selected and \
            #       0.15 * self.size_screen < unit.x < 0.85 * self.size_screen and \
            #       0.15 * self.size_screen < unit.y < 0.85 * self.size_screen:
            #     logger.debug(f"[ID {self.log_id}] Agent {agent_name} status: 7.1.5.4")
            #     func_id, func_call = (2, actions.FUNCTIONS.select_point('select_all_type', (unit_f.x, unit_f.y)))
            #     logger.success(f"[ID {self.log_id}] 7.1.5.4 Agent {agent_name}: Func Call: {func_call}")
            #     self.func_id_history.append(func_id)
            #     return func_call

            # collect obs for the team
            if unit_f.is_selected:
              logger.info(f"[ID {self.log_id}] 7.1.6 Agent {agent_name}: collect obs for team {team['name']}")
              logger.info("--" * 25)
              team['unit_tags_selected'] = []
              for unit in obs.observation.raw_units:
                if unit.tag == tag:
                  x, y = get_camera_xy(self, unit.x, unit.y)
                  team['pos'].append([x, y])
                if unit.is_selected and unit.is_on_screen:
                  team['unit_tags_selected'].append(unit.tag)
              team['obs'].append(obs)
              agent.team_unit_obs_list.append(obs)  # collect team obs
              agent.team_unit_tag_list.append(tag)
              agent.team_unit_team_list.append(team['name'])

              idx = np.nonzero(obs.observation['feature_minimap']['camera'])  # 获取特征图上非零值的坐标
              minimap_x, minimap_y = int(idx[:][1].mean()), int(idx[:][0].mean())
              team['minimap_pos'].append([minimap_x, minimap_y])

      elif not self._all_agent_waiting_response_finished():
        continue

      elif not self._all_agent_executing_finished():

        # agent's teams' actions all executed
        if not agent._is_executing_actions():
          logger.info(f"[ID {self.log_id}] 7.3.0 Agent {agent_name}: finished executing!")
          agent.executing_times = self.main_loop_step + 1
          agent.team_unit_obs_list = []
          agent.team_unit_tag_list = []
          agent.team_unit_team_list = []
          for i in range(len(agent.teams)):
            agent.teams[i]['obs'] = []
            agent.teams[i]['pos'] = []
            # agent.teams[i]['unit_tags_selected'] = []
          self.agent_id = (self.agent_id + 1) % len(self.AGENT_NAMES)
          continue

        else:
          logger.info(f"[ID {self.log_id}] 7.3.1 Agent {agent_name}: executing status")

          # obtain actions of next team
          if len(agent.func_list) == 0 and len(agent.action_list) == 0 and len(agent.action_lists) > 0:

            # standard team
            if len(agent.team_unit_tag_list) != 0:  # not (agent.flag_enable_empty_unit_group) or
              logger.debug(f"[ID {self.log_id}] Agent {agent_name}, status: 7.3.1.1")
              agent.action_list = agent.action_lists.pop(0)
              agent.team_unit_tag_curr = agent.team_unit_tag_list.pop(0)
              agent.team_unit_team_curr = agent.team_unit_team_list.pop(0)
            # empty team  (only for spesified empty team)
            else:
              logger.debug(f"[ID {self.log_id}] Agent {agent_name}, status: 7.3.1.2")
              agent.action_list = agent.action_lists.pop(0)

          # empty team excuting actions (only for spesified empty team)
          if (agent.flag_enable_empty_unit_group and len(agent.team_unit_tag_list) == 0):
            logger.debug(f"[ID {self.log_id}] Agent {agent_name}, status: 7.3.5")
            func_id, func_call = agent.get_func(obs)
            self.func_id_history.append(func_id)

          # standard team excuting actions
          else:

            # get current action name and args
            if len(agent.func_list) == 0 and len(agent.action_list) != 0:
              agent.curr_action_name = agent.action_list[0]['name']
              agent.curr_action_args = agent.action_list[0]['arg']

            # obtain team and head unit tag
            logger.debug(f"[ID {self.log_id}] Agent {agent_name} status: 7.3.2")
            team, tag = agent._get_unacted_team_and_unit_tag()
            if tag == None:  # single select team, unit dead / multi select team, all unit dead, relese actions
              agent.func_list = []
              agent.action_list = []
              continue
            unit_f = None
            unit_r = None
            for unit in obs.observation.raw_units:
              if unit.tag == tag:
                unit_r = unit

            if len(agent.func_list) == 0 and ('Select_Unit_' not in agent.curr_action_name):

              # Move camera
              func_id, func_call = get_camera_func_smart(self, obs, tag, threshold=self.camera_threshold, team=team)
              if func_id == 573:
                logger.success(f"[ID {self.log_id}] 7.3.2.0 Agent {agent_name}: Func Call: {func_call}")
                self.func_id_history.append(func_id)
                return func_call

              # Find team head unit
              for unit in obs.observation.feature_units:
                if unit.tag == tag:
                  unit_f = unit
              if unit_f is None:
                logger.error(f"[ID {self.log_id}] 7.3.2.1 Agent {agent_name}: unit of tag {tag} not found")
                logger.error(f"[ID {self.log_id}]         relative team = {team['name']} {team['unit_tags']}")
                func_id, func_call = agent.get_func(obs)  # 销掉这个动作
                logger.error(f"[ID {self.log_id}] 7.3.4 Agent {agent_name}: Func Call: {func_call}")
                self.func_id_history.append(func_id)
                time.sleep(1)

              # Unit select
              if (unit_f is not None and not unit_f.is_selected):
                logger.debug(f"[ID {self.log_id}] Agent {agent_name} status: 7.3.3")
                if team['select_type'] == 'select':
                  logger.debug(f"[ID {self.log_id}] Agent {agent_name} status: 7.3.3.1")
                  if self.func_id_history[-1] in [2, 3]:
                    d = self.select_rect_threshold
                    x1, x2 = min(max(0, unit_f.x - d), self.size_screen), min(max(0, unit_f.x + d), self.size_screen)
                    y1, y2 = min(max(0, unit_f.y - d), self.size_screen), min(max(0, unit_f.y + d), self.size_screen)
                    func_id, func_call = (3, actions.FUNCTIONS.select_rect('select', (x1, y1), (x2, y2)))
                  else:
                    x, y = min(max(0, unit_f.x), self.size_screen), min(max(0, unit_f.y), self.size_screen)
                    func_id, func_call = (2, actions.FUNCTIONS.select_point('select', (x, y)))
                  logger.success(f"[ID {self.log_id}] Agent {agent_name}: Func Call: {func_call}")
                  self.func_id_history.append(func_id)
                  return func_call
                elif team['select_type'] == 'select_all_type':
                  logger.debug(f"[ID {self.log_id}] Agent {agent_name} status: 7.3.3.2")
                  if self.func_id_history[-1] in [2, 3]:
                    d = self.select_rect_threshold
                    x1, x2 = min(max(0, unit_f.x - d), self.size_screen), min(max(0, unit_f.x + d), self.size_screen)
                    y1, y2 = min(max(0, unit_f.y - d), self.size_screen), min(max(0, unit_f.y + d), self.size_screen)
                    func_id, func_call = (3, actions.FUNCTIONS.select_rect('select', (x1, y1), (x2, y2)))
                  else:
                    x, y = min(max(0, unit_f.x), self.size_screen), min(max(0, unit_f.y), self.size_screen)
                    func_id, func_call = (2, actions.FUNCTIONS.select_point('select_all_type', (x, y)))
                  logger.success(f"[ID {self.log_id}] Agent {agent_name}: Func Call: {func_call}")
                  self.func_id_history.append(func_id)
                  return func_call
                elif team['select_type'] == 'group':
                  logger.debug(f"[ID {self.log_id}] Agent {agent_name} status: 7.3.3.3")
                  func_id, func_call = (4, actions.FUNCTIONS.select_control_group('recall', int(team['game_group'])))
                  logger.success(f"[ID {self.log_id}] Agent {agent_name}: Func Call: {func_call}")
                  self.func_id_history.append(func_id)
                  return func_call
                else:
                  logger.error(f"[ID {self.log_id}] 7.3.3.4 Agent {agent_name}: un-recogniziable select type")
                  time.sleep(5)  # this error may lead to endless loop
                  pass

              # # Recheck all required unit selected (Warning: May Lead To Possible Endless Loop)
              # for unit in obs.observation.feature_units:
              #   if team['select_type'] == 'select_all_type' and \
              #       unit.unit_type == unit_f.unit_type and not unit.is_selected and \
              #       0.15 * self.size_screen < unit.x < 0.85 * self.size_screen and \
              #       0.15 * self.size_screen < unit.y < 0.85 * self.size_screen:
              #     logger.debug(f"[ID {self.log_id}] Agent {agent_name} status: 7.3.3.5")
              #     x, y = min(max(0, unit_f.x), self.size_screen), min(max(0, unit_f.y), self.size_screen)
              #     func_id, func_call = (2, actions.FUNCTIONS.select_point('select_all_type', (x, y)))
              #     logger.success(f"[ID {self.log_id}] 7.3.3.5 Agent {agent_name}: Func Call: {func_call}")
              #     self.func_id_history.append(func_id)
              #     return func_call

            # get pysc2 function of current action
            if (unit_f is not None and unit_f.is_selected) or \
              ('Select_Unit_' in agent.curr_action_name) or \
              len(agent.func_list) != 0:
              func_id, func_call = agent.get_func(obs)
              logger.info(f"[ID {self.log_id}] 7.3.4 Agent {agent_name}: agent.get_func(obs): get {func_call}")
              self.func_id_history.append(func_id)

            # mark units that finished excution
            for unit in obs.observation.raw_units:
              if unit.is_selected and unit.is_on_screen:
                self.unit_selected_tag_list.append(unit.tag)
            self.unit_selected_tag_list = list(set(self.unit_selected_tag_list))

      else:
        # all agent' teams finished excution, release main_loop_lock to enable auto management fo workers, bases, etc.
        logger.success(f"[ID {self.log_id}] 7.3.5 Agent {agent_name}: One loop finished, release self.main_loop_lock")
        self.main_loop_step += 1
        self.main_loop_lock = False  # release main_loop_lock to enable auto management
        func_id, func_call = (0, actions.FUNCTIONS.no_op())
        self.func_id_history.append(func_id)
        return func_call

      # execute function of current agent's current action
      if func_id != 0:
        if func_id in obs.observation.available_actions:
          logger.success(f"[ID {self.log_id}] 7.4 Agent {agent_name} Func Call: {func_call}")
          self.func_id_history.append(func_id)
          return func_call
        else:
          if func_id is not None:
            logger.error(f"[ID {self.log_id}] 7.5.1 Agent {agent_name} Func Call Invalid, Skipped: {func_call}")

    # execute no-operation function while reach waiting time
    func_id, func_call = (0, actions.FUNCTIONS.no_op())
    logger.warning(f"[ID {self.log_id}] Reach MAX_LLM_WAITING_TIME! {agent_name} Call no_op()")
    logger.warning(f"[ID {self.log_id}] Func Call: {func_call}")
    self.func_id_history.append(func_id)
    return func_call
