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

from llm_pysc2.cfg import AgentConfig, ProtossAgentConfig
from llm_pysc2.lib import llm_client, llm_observation, llm_action, llm_prompt, llm_communicate, task, utils, events

from pysc2.lib import actions

from pprint import pprint
from collections import deque
from shutil import copyfile
from loguru import logger
import threading
import time
import json
import math
import copy
import os



class LLMAgent:
  def __init__(self,
               name: str,
               log_id: int,
               start_time: str,
               config: "AgentConfig" = ProtossAgentConfig(),
               ):

    # basic info
    self.name = name
    self.log_id = log_id
    self.config = config
    self.start_time = start_time
    self.race = self.config.race

    self.available_unit_type = []
    for team in self.config.AGENTS[self.name]['team'].values():
      self.available_unit_type += team['unit_type']

    # llm client, obs wrapper and action recognizer initialize
    basic_prompt = self.config.AGENTS[self.name]['llm']['basic_prompt']
    translator_o = self.config.AGENTS[self.name]['llm']['translator_o']
    translator_a = self.config.AGENTS[self.name]['llm']['translator_a']
    communicator = self.config.communicator
    self.api_key = self.config.AGENTS[self.name]['llm']['api_key']
    self.api_base = self.config.AGENTS[self.name]['llm']['api_base']
    self.model_name = self.config.AGENTS[self.name]['llm']['model_name']

    self.basic_prompt = llm_prompt.FACTORY[self.race][basic_prompt](name, log_id, config)
    self.translator_a = llm_action.FACTORY[self.race][translator_a](name, log_id, config)
    self.translator_o = llm_observation.FACTORY[self.race][translator_o](name, log_id, config)
    self.communicator = llm_communicate.FACTORY[self.race][communicator](name, log_id, config)

    if self.model_name not in llm_client.FACTORY.keys():
      logger.error(f"Do not find model name {self.model_name} in llm_pysc2.lib.llm_client.FACTORY: \n{llm_client.FACTORY.keys()}")
      logger.error(f"model_name set as gpt-3.5-turbo")
      self.model_name = 'gpt-3.5-turbo'
      time.sleep(3)
    self.client = llm_client.FACTORY[self.model_name](name, log_id, config)  # edit it to change llm client
    self.client.system_prompt = self.basic_prompt.sp
    self.client.example_i_prompt = self.basic_prompt.eip
    self.client.example_o_prompt = self.basic_prompt.eop

    # llm query thread initialize
    self.thread = None
    self.lock = threading.Lock()
    self.enable = False
    self.engage = False
    self.is_waiting = False

    # variables for main agent control
    self.num_step = -1
    self.main_loop_step = 0
    self.query_llm_times = 0
    self.executing_times = 0

    # map info
    self.world_range = -1
    self.world_x_offset = -1
    self.world_y_offset = -1
    self.size_screen = 0
    self.size_minimap = 0

    # unit info
    self.unit_tag_list_history = []
    self.unit_raw_list = []
    self.unit_tag_list = []

    # team info
    # [{'name': 'Z1', 'unit_type': [units.Protoss.Zealot], 'game_group': 1, 'select_type': 'group',
    #   'unit_tags': [0x00012c0001, 0x00013a0001, 0x0001500001], 'unit_tags_selected': [0x00012c0001],
    #   'obs':[], 'pos':[]}],
    self.flag_enable_empty_unit_group = False if self.name not in ['Commander', 'Developer'] else True
    self.teams = list(self.config.AGENTS[self.name]['team'].values())
    self.teams_history = {}
    for team in self.teams:
      team['unit_tags'] = []
      team['unit_tags_selected'] = []
      team['edge'] = {'l': None, 'r': None, 'u': None, 'b': None}  # map edge, screen coordinate, update in get text obs
      team['obs_last'] = []
      team['obs'] = []  # collected observation
      team['pos'] = []  # camera coordinate
      team['minimap_pos'] = []  # for commander, get global deployment info
      team['camera_move'] = []  # stage of collect obs
      team['state'] = []  # processed after o translator, a structured dict
      team['raw_text_actions'] = []  # processed after o translator, a text
    self.team_unit_obs_list = []
    self.team_unit_tag_list = []
    self.team_unit_team_list = []
    self.team_unit_tag_curr = None
    self.team_unit_team_curr = None

    # obs
    # self.agent_data_dict = {}
    self.last_text_o = ''

    # action
    self.action_lists = []
    self.action_list = []
    self.func_list = []
    self.curr_action_name = ''
    self.curr_action_args = []
    self.last_text_a_raw = ''
    self.last_text_a_pro = ''
    self.first_action = True
    self.action_errors = {}
    self.raw_text_a = ''

    # communication
    self.communication_message_i = {}
    self.communication_message_o = {}
    self.last_text_c_inp = ''
    self.last_text_c_tar = ''
    self.last_text_c_out = ''

    # log
    current_dir = os.path.dirname(os.path.abspath(__file__))
    self.current_dir = current_dir
    self.log_dir_path = f"{current_dir}/../../llm_log/{self.start_time}-{self.log_id}"
    self.history_func_path = f"{current_dir}/../../llm_log/{self.start_time}-{self.log_id}/{self.name}/a_his.txt"
    logger.success(f"[ID {self.log_id}] Agent {self.name} successfully initialized!")

  # check if team_unit_tag_list contains all necessary unit
  def _is_all_my_teams_ready_to_query(self):
    for team in self.teams:
      # True: all unit in team_unit_tag_list
      if team['select_type'] == 'select':
        ready = True
        for unit_tag in team['unit_tags']:
          if unit_tag not in self.team_unit_tag_list:
            ready = False
      # True: at least one unit in team_unit_tag_list
      else:
        ready = False
        for unit_tag in team['unit_tags']:
          if unit_tag in self.team_unit_tag_list:
            ready = True
      if len(team['unit_tags']) != 0 and not ready:
        logger.debug(
          f"[ID {self.log_id}] LLMAgent {self.name}, in _is_all_my_teams_ready_to_query(): team {team['name']} not ready")
        logger.debug(
          f"[ID {self.log_id}] LLMAgent {self.name}, in _is_all_my_teams_ready_to_query(): team['unit_tags'] = {team['unit_tags']}, self.team_unit_tag_list = {self.team_unit_tag_list}")
        return False
    return True

  # get a team and its head unit to collect obs (strict pop-up order)
  def _get_unobsed_team_and_unit_tag(self):
    logger.debug(
      f"[ID {self.log_id}] LLMAgent {self.name}, in _get_unobsed_team_and_unit_tag(): self.team_unit_tag_list = {self.team_unit_tag_list}")
    for team in self.teams:
      logger.debug(
        f"[ID {self.log_id}] LLMAgent {self.name}, in _get_unobsed_team_and_unit_tag(): team['name'] = {team['name']}, team['unit_tags'] = {team['unit_tags']}")
      if team['select_type'] == 'select':
        for unit_tag in team['unit_tags']:
          if unit_tag not in self.team_unit_tag_list:
            return team, unit_tag
      else:
        if len(team['unit_tags']) > 0:
          unit_tag = team['unit_tags'][0]
          if unit_tag not in self.team_unit_tag_list:
            return team, unit_tag
    return None, None

  # get a team and its head unit to execute actions (strict pop-up order)
  def _get_unacted_team_and_unit_tag(self):
    for team in self.teams:
      if self.team_unit_team_curr == team['name']:
        if team['select_type'] == 'select':
          if self.team_unit_tag_curr in team['unit_tags']:
            return team, self.team_unit_tag_curr
          else:
            return team, None
        else:
          if self.team_unit_tag_curr in team['unit_tags']:
            return team, self.team_unit_tag_curr
          elif len(team['unit_tags']) > 0:
            return team, team['unit_tags'][0]
          else:
            return team, None
    return None, None

  # agent data update
  def update(self, obs):
    self.size_screen = obs.observation.feature_screen.height_map.shape[0]
    self.size_minimap = obs.observation.feature_minimap.height_map.shape[0]
    self.translator_o.size_screen = self.size_screen
    self.translator_a.size_screen = self.size_screen
    self.translator_o.size_minimap = self.size_minimap
    self.translator_a.size_minimap = self.size_minimap

    # enable agent if it has unit
    if self.enable is False and len(self.unit_tag_list) > 0:
      self.enable = True
      self.query_llm_times = self.main_loop_step
      self.executing_times = self.main_loop_step
    if len(self.unit_tag_list) == 0 and 'CombatGroup' in self.name:
      self.enable = False
    if self.name in self.config.AGENTS_ALWAYS_DISABLE:
      self.enable = False
    # game_time_s = obs.observation.game_loop / 22.4
    # if self.name in ['Builder', 'Developer'] and game_time_s < 10:  #建造小队
    #   self.enable = False
    # if self.name in ['CombatGroup4'] and game_time_s < 30:  #侦查小队
    #   self.enable = False

    # store all the unit tags
    for tag in self.unit_tag_list:
      if tag not in self.unit_tag_list_history:
        self.unit_tag_list_history.append(tag)

    # store all the raw unit by tags
    self.unit_raw_list = []
    for unit in obs.observation.raw_units:
      if unit.tag in self.unit_tag_list:
        self.unit_raw_list.append(unit)

    # delete dead units and change head unit to the closest one (if former head unit dead)
    for team in self.teams:
      for unit_tag in team['unit_tags']:
        if unit_tag not in self.unit_tag_list and unit_tag == team['unit_tags'][0]:
          unit_r = None
          unit_h = None
          dist_min = 99999
          for unit in self.unit_raw_list:
            if unit.tag == unit_tag:
              unit_r = unit
          if unit_r is None:
            logger.warning(
              f"[ID {self.log_id}] Agent {self.name} team {team['name']} head unit {unit_tag} do not exist")
            team['unit_tags'].remove(unit_tag)
            continue
          for unit in self.unit_raw_list:
            if unit.tag in self.unit_tag_list and unit.tag in team['unit_tags']:
              dist = math.sqrt((unit.x - unit_r.x) ** 2 + (unit.y - unit_r.y) ** 2)
              if dist < dist_min:
                dist_min = dist
                unit_h = unit
          if unit_h is not None:
            team['unit_tags'].remove(unit_h.tag)
            team['unit_tags'] = [unit_h.tag] + team['unit_tags']

        if unit_tag not in self.unit_tag_list:
          team['unit_tags'].remove(unit_tag)
        team['unit_tags'] = list(set(team['unit_tags']))

    # clear communication info for disabled agent
    if not self.enable:
      self.last_text_c_inp = ''
      self.last_text_c_tar = ''

    # log
    if self.name not in self.config.AGENTS_ALWAYS_DISABLE and self.enable:
      if not os.path.exists(self.log_dir_path + f"/{self.name}"):
        os.mkdir(self.log_dir_path + f"/{self.name}")
        copyfile(self.current_dir + f"/../../llm_log/log_show.py", self.log_dir_path + f"/{self.name}/log_show.py")
      if not os.path.exists(self.log_dir_path + f"/{self.name}/o.txt"):
        utils.write_to_file('', self.log_dir_path + f"/{self.name}/o.txt")
        utils.write_to_file('', self.log_dir_path + f"/{self.name}/a_his.txt")
        utils.write_to_file('', self.log_dir_path + f"/{self.name}/a_raw.txt")
        utils.write_to_file('', self.log_dir_path + f"/{self.name}/a_pro.txt")
        utils.write_to_file('', self.log_dir_path + f"/{self.name}/cost.txt")
        utils.write_to_file(self.basic_prompt.sp, self.log_dir_path + f"/{self.name}/prompt.txt")
        utils.write_to_file('-' * 50 + "example input prompt" + '-' * 50, self.log_dir_path + f"/{self.name}/prompt.txt")
        utils.write_to_file(self.basic_prompt.eip, self.log_dir_path + f"/{self.name}/prompt.txt")
        utils.write_to_file('-' * 50 + "example output prompt" + '-' * 50, self.log_dir_path + f"/{self.name}/prompt.txt")
        utils.write_to_file(self.basic_prompt.eop, self.log_dir_path + f"/{self.name}/prompt.txt")
        if self.config.LLM_SIMULATION_TIME > 0:
          utils.write_to_file('', self.log_dir_path + f"/{self.name}/a_inp.txt")
        if self.config.ENABLE_COMMUNICATION:
          utils.write_to_file('', self.log_dir_path + f"/{self.name}/c_inp.txt")
          utils.write_to_file('', self.log_dir_path + f"/{self.name}/c_out.txt")

  def _before_query(self, obs):
    while self.is_waiting is False:
      with self.lock:
        self.is_waiting = True
    # if obs.observation.map_name not in task.FACTORY.keys():
    #   logger.error(f"task description is not realised in llm_pysc2.lib.task")
    #   raise AssertionError("task description is not realised in llm_pysc2.lib.task")
    if obs.observation.map_name not in task.FACTORY.keys():
      logger.warning(f"task description is not realised in llm_pysc2.lib.task, use default task")
      task_dict = task.FACTORY['default'](self)
    else:
      task_dict = task.FACTORY[obs.observation.map_name](self)  # return dict[team_name]='text_task_description'
    logger.debug(f'task_dict={task_dict}')
    logger.success(f"[ID {self.log_id}] LLMAgent {self.name}: LLM Interaction Start")
    self.teams_history[self.main_loop_step] = copy.deepcopy(self.teams)
    text_o = self.get_text_o(obs)
    base64_images = self.get_img_o(obs)  # return None if img observation disabled
    self.get_text_c_inp()
    return text_o, base64_images


  def _after_query(self, raw_text_a, obs):
    self.get_info_c_out(raw_text_a)
    action_lists, action_list_dict = self.get_func_a(raw_text_a, obs)
    logger.success(f"[ID {self.log_id}] LLMAgent {self.name}: LLM Interaction Finished")
    logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: Listen to {self.communication_message_i}")
    logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: Send info to {self.communication_message_o}")
    utils.write_to_file('--' * 50, self.history_func_path)
    self.first_action = True
    self.action_errors = {}
    for team in self.teams:
      team['obs_last'] = team['obs']
      team['raw_text_actions'] = raw_text_a
      team['state'] = self.translator_o.state
      self.teams_history[self.main_loop_step] = copy.deepcopy(self.teams)
      # print(self.teams_history.keys())
    while self.is_waiting is True:
      with self.lock:
        self.is_waiting = False
        self.action_lists = action_lists

  # TODO: Main API Func, receive obs and get actions
  def query(self, obs) -> None:
    logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: start collect obs")
    text_o, base64_images = self._before_query(obs)
    logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: finished collect obs, text_o: \n{text_o}")

    self.raw_text_a = self.get_text_a(text_o, base64_images)  # query the llm and get response
    if self.name not in self.config.AGENTS_ALWAYS_DISABLE and self.enable:
      utils.write_to_file(json.dumps({self.main_loop_step: text_o}), self.log_dir_path + f"/{self.name}/o.txt")

    self._after_query(self.raw_text_a, obs)


  # query step1: all teams' pysc2 obs to a llm obs text (or multimodal llm text)
  def get_text_o(self, obs) -> str:
    text_o = self.translator_o.translate(self)
    self.last_text_o = text_o
    return text_o

  def get_img_o(self, obs):
    base64_images = {}
    if self.config.AGENTS[self.name]['llm']['img_rgb']:
      base64_images['screen'] = llm_observation.get_img_obs_rgb(self, obs)
      base64_images['minimap'] = llm_observation.get_img_obs_rgb_minimap(self, obs)
      if 'feature_map_names' in self.config.AGENTS[self.name]['llm'].keys():
        feature_map_names = self.config.AGENTS[self.name]['llm']['feature_map_names']
      else:
        feature_map_names = []
      for feature_map_name in feature_map_names:
        base64_images[feature_map_name] = llm_observation.get_img_obs_fea_map(self, obs, feature_map_name)
    elif self.config.AGENTS[self.name]['llm']['img_fea']:
      base64_images['screen'] = llm_observation.get_img_obs_fea(self, obs)
    else:
      base64_images = None
    return base64_images

  # query step2: communicate with llm and get text actions
  def get_text_a(self, text_o: str, base64_images:"Dict or None"=None) -> str:
    text_a = ''
    if self.config.LLM_SIMULATION_TIME > 0:
      # pprint(base64_images)
      # self.client.wrap_message(text_o, base64_images)
      # for message in self.client.messages:
      #   pprint(message, width=200)
      logger.warning(f"[ID {self.log_id}] LLM SIMULATION MODE, no remote llm involved")
      time.sleep(self.config.LLM_SIMULATION_TIME)  # simulate llm response, for debug
      if self.name not in self.config.AGENTS_ALWAYS_DISABLE and self.enable:
        with open(self.log_dir_path + f"/{self.name}/a_inp.txt", "r") as f:
          text_a = f.read()  # simulate llm response by reading text in a_inp.txt
    else:
      if base64_images is not None and 'minimap' in base64_images.keys() and 'screen' in base64_images.keys():
        text_a = self.client.query(text_o, base64_images=base64_images)  # Communicate with VLM
        logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: Screen and Minimap images provided to LLM.")
      elif base64_images is not None and 'screen' in base64_images.keys():
        text_a = self.client.query(text_o, base64_images=base64_images)  # Communicate with VLM
        logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: Screen Image provided to LLM.")
      else:
        text_a = self.client.query(text_o)  # Communicate with LLM
        logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: No image provided to LLM.")


    logger.debug(f"[ID {self.log_id}] LLMAgent {self.name} get_text_a(): Query finished.")
    self.last_text_a_raw = text_a
    return text_a

  # query step3: text action to pysc2 functions
  def get_func_a(self, raw_text_a, obs) -> (list, dict):
    new_action_lists = []
    action_list_dict = {}
    processed_text_a = ''

    # try:
    #   new_action_lists, action_list_dict, processed_text_a = self.translator_a.translate(raw_text_a)
    #   print(f"\nprocessed_text_a=\n{processed_text_a}")
    # except Exception as e:
    #   logger.error(f"[ID {self.log_id}] Error in {self.name} get_func_a(): {e}")
    new_action_lists, action_list_dict, processed_text_a = self.translator_a.translate(raw_text_a, obs)
    logger.debug(f"\nprocessed_text_a=\n{processed_text_a}")
    self.last_text_a_pro = processed_text_a

    if self.name not in self.config.AGENTS_ALWAYS_DISABLE and self.enable:
      path = self.log_dir_path + f"/{self.name}/a_raw.txt"
      utils.write_to_file(json.dumps({self.main_loop_step: raw_text_a}), path)
      path = self.log_dir_path + f"/{self.name}/a_pro.txt"
      utils.write_to_file(json.dumps({self.main_loop_step: processed_text_a}), path)
      c = self.client
      path = self.log_dir_path + f"/{self.name}/cost.txt"
      client_cost = f"time={c.query_time:.2f}, ave_time={c.ave_query_time:.2f}, " \
                    f"token_in={c.query_token_in}, ave_token_in={c.ave_query_token_in:.2f}, " \
                    f"token_out={c.query_token_out}, ave_token_out = {c.ave_query_token_out:.2f}"
      utils.write_to_file(json.dumps({self.main_loop_step: client_cost}), path)

    return new_action_lists, action_list_dict

  # get text shaped communication
  def get_text_c_inp(self) -> None:
    # The function of get_text_c_inp is actually completed by the main agent
    if self.name not in self.config.AGENTS_ALWAYS_DISABLE and self.enable and self.config.ENABLE_COMMUNICATION:
      path = self.log_dir_path + f"/{self.name}/c_inp.txt"
      utils.write_to_file(json.dumps({self.main_loop_step: self.last_text_c_inp}), path)

  # get channel listen to and sort information to sent out
  def get_info_c_out(self, raw_text_a) -> None:
    self.communication_message_i, self.communication_message_o, self.last_text_c_out = self.communicator.send(raw_text_a)
    if self.name not in self.config.AGENTS_ALWAYS_DISABLE and self.enable and self.config.ENABLE_COMMUNICATION:
      path = self.log_dir_path + f"/{self.name}/c_out.txt"
      utils.write_to_file(json.dumps({self.main_loop_step: self.last_text_c_out}), path)

  def _is_waiting_query(self) -> bool:
    action_lists = self._get_action_lists()
    is_waiting = self._get_flag_is_waiting()
    flag = True if (len(self.func_list) == 0 and len(self.action_list) == 0 and len(action_lists) == 0 and not is_waiting) else False
    return flag

  def _is_waiting_response(self) -> bool:
    action_lists = self._get_action_lists()
    is_waiting = self._get_flag_is_waiting()
    flag = True if (len(self.func_list) == 0 and len(self.action_list) == 0 and len(action_lists) == 0 and is_waiting) else False
    return flag

  def _is_executing_actions(self) -> bool:
    action_lists = self._get_action_lists()
    is_waiting = self._get_flag_is_waiting()
    flag = True if (len(self.func_list) != 0 or len(self.action_list) != 0 or len(action_lists) != 0) else False
    return flag

  def _get_flag_is_waiting(self):
    # return self.is_waiting
    with self.lock:
      return self.is_waiting

  def _get_action_lists(self):
    # return self.action_lists
    with self.lock:
      return self.action_lists

  def get_func(self, obs):  # 该函数需要将当前text-pysc2动作对应的下一个pysc2函数取出，确认函数和参数是合法的，然后交给到主智能体

    enable_no_op = False
    text_action = None
    text_func = None

    if len(self.func_list) == 0:
      action = self.action_list.pop(0)
      self.action_valid_check_1 = True
      action = llm_action.add_func_for_select_workers(self, obs, action)
      action = llm_action.add_func_for_train_and_research(self, obs, action)
      action = llm_action.add_func_for_easy_build(self, obs, action)
      action = llm_action.add_func_for_easy_control(self, obs, action)
      action = llm_action.add_func_for_easy_warp(self, obs, action)
      action = llm_action.add_func_for_build(self, obs, action)
      self.func_list = action['func']
      # self.func_list_standard = llm_a.get_text_action(self.name, action['name'])
      self.curr_action_name = action['name']
      self.curr_action_args = action['arg']
      self.curr_action_valid = True

      # text_action_args = ''
      # for i in range(len(action['arg'])):
      #   arg = action['arg'][i]
      #   text_action_args += str(arg)
      #   if i != len(action['arg']) - 1:
      #     text_action_args += ', '
      if self.curr_action_name != 'No_Operation':
        text_action = f'<{self.curr_action_name}({self.curr_action_args})>'

      if 'Attack' in self.curr_action_name and 'Ability' not in self.curr_action_name:
        queued, source_unit_tag = '', None
        for func_triple in self.func_list:
          func_id, func, llm_pysc2_args = func_triple
          for arg in llm_pysc2_args:
            queued = arg if (func_id == 12 and (arg == 'queued' or arg == 'now')) else queued   # attack
            source_unit_tag = arg if (func_id == 3 and isinstance(arg, int)) else source_unit_tag    # select rect
        self.action_valid_check_1 = llm_action.check_weapon_state(obs, queued, source_unit_tag, strict=True)

    # for i in range(len(self.func_list)):
    # logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}, get_func(): self.func_list[{i}] = {self.func_list[i]}")
    func_id, func, llm_pysc2_args = self.func_list.pop(0)
    func_call = None
    if func.name == "no_op" and self.curr_action_valid and self.action_valid_check_1:
      enable_no_op = True
    # func_id, func, llm_pysc2_arg_types = llm_a.get_action(self.name, )

    pysc2_args = []
    if func_id in obs.observation.available_actions:  # 函数合法性检验，非法动作直接跳出
      func_valid = True
      pysc2_args = []

      if len(llm_pysc2_args) == 0:
        func_call = func()
        # logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}, call func() = {func()}")

      if len(llm_pysc2_args) > 0:

        for i in range(len(llm_pysc2_args)):
          llm_pysc2_arg = llm_pysc2_args[i]
          # logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}, get_func(): llm_pysc2_arg= {llm_pysc2_arg}, type(llm_pysc2_arg) = {type(llm_pysc2_arg)}")
          if isinstance(llm_pysc2_arg, str):  # queued形式的flag
            func_valid = False if llm_pysc2_arg not in ['now', 'queued', 'select', 'add'] else True
            pysc2_arg = llm_pysc2_arg
            # if self.first_action and pysc2_arg in ['now', 'queued']:
            #   pysc2_arg = 'now'
          elif isinstance(llm_pysc2_arg, list) and len(llm_pysc2_arg) == 2:  # 坐标
            func_valid = False
            if func.args[i].name == 'minimap':  # 小地图坐标
              pysc2_arg, func_valid = llm_action.get_arg_minimap(obs, llm_pysc2_arg, self.size_minimap, self.curr_action_name)  # 小地图坐标合法性判断
            elif func.args[i].name == 'screen' and 'Build' in func.name:  # 建造
              pysc2_arg, func_valid = llm_action.get_arg_screen_build(obs, llm_pysc2_arg, self.size_screen, self.curr_action_name)  # 建筑的屏幕坐标合法性判断
            elif func.args[i].name == 'screen' and 'Build' not in func.name:  # 无限制
              pysc2_arg, func_valid = llm_action.get_arg_screen(obs, llm_pysc2_arg, self.size_screen, self.curr_action_name)  # 屏幕坐标合法性判断
            else:
              pysc2_arg = 'WrongType-Arg'  # 错误处理，接受func_valid = False，使用no_op代替该动作
          elif isinstance(llm_pysc2_arg, int):
            func_valid = False
            print(self.curr_action_name)
            print(i, func.args, func)
            if func.args[i].name == 'screen' and 'Build' in func.name:  # 建造  and self.config.ENABLE_EASY_BUILD
              pysc2_arg, func_valid = llm_action.get_arg_screen_tag_build(
                obs, llm_pysc2_arg, self.size_screen, self.curr_action_name)  # 建筑的屏幕坐标合法性判断
            elif func_id == 573 and ('Build_Nexus_' in self.curr_action_name or 'Lock_Nexus_' in self.curr_action_name):
              pysc2_arg, func_valid = llm_action.get_arg_world_tag_base_building(
                obs, llm_pysc2_arg, self.world_x_offset, self.world_y_offset, self.world_range)
            elif func_id == 573:
              pysc2_arg, func_valid = llm_action.get_arg_world_tag(
                obs, llm_pysc2_arg, self.world_x_offset, self.world_y_offset, self.world_range)  # tag转全局坐标
            elif func.name == 'select_rect':  # 单选单位
              pysc2_arg, func_valid = llm_action.get_arg_screen_tag_sclect_rect(
                obs, llm_pysc2_arg, self.size_screen, func.args[i].name)  # tag转屏幕坐标
            elif func.name == 'select_point':  # 该动作用于代替no_op,当作悬空动作，用于确保带后摇的攻击成功释放
              pysc2_arg, func_valid = llm_action.get_arg_screen_tag(
                obs, llm_pysc2_arg, self.size_screen, self.curr_action_name)  # tag转屏幕坐标
            elif func.args[i].name == 'screen' and 'Recall' in func.name:  # 召回，临近单位群的中心
              pysc2_arg, func_valid = llm_action.get_arg_screen_tag_recall(
                obs, llm_pysc2_arg, self.size_screen, self.curr_action_name)  # tag转屏幕坐标
            elif func.args[i].name == 'screen' and 'TrainWarp' in func.name:  # 折跃，水晶塔/棱镜力场附近
              pysc2_arg, func_valid = llm_action.get_arg_screen_tag_warp(
                obs, llm_pysc2_arg, self.size_screen, self.curr_action_name)  # tag转屏幕坐标
            elif func.args[i].name == 'screen' and func_id in [65, 70]:  # 建造主矿/水晶塔封矿
              pysc2_arg, func_valid = llm_action.get_arg_screen_tag_base_building(
                obs, llm_pysc2_arg, self.size_screen, self.curr_action_name)  # tag转屏幕坐标
            elif func.args[i].name == 'screen' and func_id in [40]:  # 建造气站/封对面气
              pysc2_arg, func_valid = llm_action.get_arg_screen_tag_gas_building(
                obs, llm_pysc2_arg, self.size_screen, self.curr_action_name)  # tag转屏幕坐标
            elif func.args[i].name == 'screen':  # 无限制
              pysc2_arg, func_valid = llm_action.get_arg_screen_tag(
                obs, llm_pysc2_arg, self.size_screen, self.curr_action_name)  # tag转屏幕坐标
            else:
              func_valid = False
              pysc2_arg = 'WrongType-Arg'  # 错误处理
          else:
            func_valid = False
            pysc2_arg = 'WrongType-Arg'

          if not func_valid:
            self.curr_action_valid = False
            if self.curr_action_name not in self.action_errors:
              self.action_errors[self.curr_action_name] = []
            if pysc2_arg not in self.action_errors[self.curr_action_name]:
              self.action_errors[self.curr_action_name].append(pysc2_arg)
          pysc2_args.append(pysc2_arg)

        if func_valid is True and 'error' not in pysc2_args:
          logger.info(
            f"[ID {self.log_id}] LLMAgent {self.name}, get_func(): func avaliable, func {func} pysc2_args {pysc2_args}")
          if len(pysc2_args) == 3:
            func_call = func(pysc2_args[0], pysc2_args[1], pysc2_args[2])
          elif len(pysc2_args) == 2:
            func_call = func(pysc2_args[0], pysc2_args[1])
          elif len(pysc2_args) == 1:
            func_call = func(pysc2_args[0])
          else:
            text = f"{self.name};   loop{self.main_loop_step};   step{self.num_step};   [Invalid Args]  {func.name} {pysc2_args}"
            utils.write_to_file(text, self.history_func_path)
            logger.warning(f"[ID {self.log_id}] LLMAgent {self.name} get_func() Error type 1: Arg quantity invalid: ({pysc2_args})! Replace with no_op().")
            func_id, func_call = (0, actions.FUNCTIONS.no_op())
        else:
          text = f"{self.name};   loop{self.main_loop_step};   step{self.num_step};   [Invalid Args]  {func.name} {pysc2_args} "
          utils.write_to_file(text, self.history_func_path)
          logger.warning(f"[ID {self.log_id}] LLMAgent {self.name} get_func() Error type 2: Func {func} Arg invalid: {pysc2_args}! Replace with no_op()")
          func_id, func_call = (0, actions.FUNCTIONS.no_op())

    else:
      enable_no_op = False
      error_info = f'Function Invalid'
      self.action_errors[self.curr_action_name] = [error_info]
      text = f"{self.name};   loop{self.main_loop_step};   step{self.num_step};   [Invalid Func]  {func.name} {error_info}"
      utils.write_to_file(text, self.history_func_path)
      logger.warning(f"[ID {self.log_id}] LLMAgent {self.name} get_func() Error type 3: Func invalid: {func}! Replace with no_op()")
      func_id, func_call = (0, actions.FUNCTIONS.no_op())

    if not self.action_valid_check_1 and func_id not in [12, 3, 4]:
      enable_no_op = False
      error_info = f'All weapons waiting for cooling down, unable to attack'
      self.action_errors[self.curr_action_name] = [error_info]
      text = f"{self.name};   loop{self.main_loop_step};   step{self.num_step};   [Invalid Func]  {func.name} {error_info}"
      utils.write_to_file(text, self.history_func_path)
      logger.warning(f"[ID {self.log_id}] LLMAgent {self.name} get_func() Error type 4: All weapons waiting for cooling down, unable to attack, but still redirect attack target")
      func_id, func_call = (0, actions.FUNCTIONS.no_op())


    # 保存动作信息
    if func_id != 0 or enable_no_op:
      text = f"{self.name};   loop{self.main_loop_step};   step{self.num_step};   [   Success  ]  {func_call}"
      utils.write_to_file(text, self.history_func_path)

    # if self.first_action and 'now' in pysc2_args:
    #   self.first_action = False
    # if len(self.action_list) == 0:
    #   self.first_action = True  # 本小队最后一个动作已经执行完毕

    logger.info(f"[ID {self.log_id}] LLMAgent {self.name} get_func(): Get Func {func_id}, {func_call}")
    return func_id, func_call, enable_no_op, text_action


# 用户定制智能体
class Customized_LLMAgent(LLMAgent):

  def __init__(self, name: str, log_id: int, start_time: str, config: "AgentConfig"=ProtossAgentConfig()):
    super(Customized_LLMAgent, self).__init__(name, log_id, start_time, config)

    # TODO: code here to redefine system prompt, example input prompt and example output prompt
    basic_prompt = self.config.AGENTS[name]['llm']['basic_prompt']  # edit it to change basic prompt
    translator_o = self.config.AGENTS[name]['llm']['translator_o']  # edit it to change obs translator
    translator_a = self.config.AGENTS[name]['llm']['translator_a']  # edit it to change action translator, not recommended
    communicator = self.config.communicator  # edit it to change communicator, not recommended

    self.api_key = self.config.AGENTS[name]['llm']['api_key']
    self.api_base = self.config.AGENTS[name]['llm']['api_base']
    self.model_name = self.config.AGENTS[name]['llm']['model_name']

    self.basic_prompt = llm_prompt.FACTORY[self.race][basic_prompt](name, log_id, config)
    self.translator_a = llm_action.FACTORY[self.race][translator_a](name, log_id, config)
    self.translator_o = llm_observation.FACTORY[self.race][translator_o](name, log_id, config)
    self.communicator = llm_communicate.FACTORY[self.race][communicator](name, log_id, config)

    self.client = llm_client.FACTORY[self.model_name](name, log_id, config)
    self.client.system_prompt = self.basic_prompt.sp
    self.client.example_i_prompt = self.basic_prompt.eip
    self.client.example_o_prompt = self.basic_prompt.eop

  # 如需修改Agent与LLM的交互方式，重定义接口函数query即可
  def query(self, obs) -> None:
    while self.is_waiting is False:
      with self.lock:
        self.is_waiting = True
    logger.success(f"[ID {self.log_id}] LLMAgent {self.name}: Start waiting for response")

    # TODO: code here to redefine how to interact with LLM
    self.get_text_c_inp()
    text_o = self.get_text_o(obs)
    if self.config.AGENTS[self.name]['llm']['img_rgb']:
      base64_image = llm_observation.get_img_obs_rgb(self, obs)
      raw_text_a = self.get_text_a(text_o, base64_image=base64_image)
    elif self.config.AGENTS[self.name]['llm']['img_fea']:
      base64_image = llm_observation.get_img_obs_fea(self, obs)
      raw_text_a = self.get_text_a(text_o, base64_image=base64_image)
    else:
      raw_text_a = self.get_text_a(text_o)
    action_lists, action_list_dict = self.get_func_a(raw_text_a)
    self.get_info_c_out(raw_text_a)

    logger.success(f"[ID {self.log_id}] LLMAgent {self.name}: Get response ")
    utils.write_to_file('--' * 50, self.history_func_path)

    self.first_action = True
    while self.is_waiting is True:
      with self.lock:
        self.is_waiting = False
        self.action_lists = action_lists
