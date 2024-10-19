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

from llm_pysc2.agents.configs import AgentConfig, ProtossAgentConfig
from llm_pysc2.lib import llm_client, llm_observation, llm_action, llm_prompt, llm_communicate

from pysc2.lib import actions

from shutil import copyfile
from loguru import logger
import threading
import time
import json
import math
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
    for team in self.config.AGENTS[self.name]['team']:
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
    self.flag_enable_empty_unit_group = False
    self.teams = self.config.AGENTS[self.name]['team']
    for team in self.teams:
      team['unit_tags'] = []
      team['unit_tags_selected'] = []
      team['obs'] = []  # collected observation
      team['pos'] = []  # camera coordinate
      team['minimap_pos'] = []  # for commander, get global deployment info
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

    # enable agent if it has unit
    if self.enable is False and len(self.unit_tag_list) > 0:
      self.enable = True
      self.query_llm_times = self.main_loop_step
      self.executing_times = self.main_loop_step
    if len(self.unit_tag_list) == 0 and 'CombatGroup' in self.name:
      self.enable = False
    if self.name in self.config.AGENTS_ALWAYS_DISABLE:
      self.enable = False

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
        with open(self.log_dir_path + f"/{self.name}/o.txt", "w") as f:
          f.write('')
      if not os.path.exists(self.log_dir_path + f"/{self.name}/a_his.txt"):
        with open(self.log_dir_path + f"/{self.name}/a_his.txt", "w") as f:
          f.write('')
      if not os.path.exists(self.log_dir_path + f"/{self.name}/a_raw.txt"):
        with open(self.log_dir_path + f"/{self.name}/a_raw.txt", "w") as f:
          f.write('')
      if not os.path.exists(self.log_dir_path + f"/{self.name}/a_pro.txt"):
        with open(self.log_dir_path + f"/{self.name}/a_pro.txt", "w") as f:
          f.write('')
      if not os.path.exists(self.log_dir_path + f"/{self.name}/a_inp.txt") and self.config.LLM_SIMULATION_TIME > 0:
        with open(self.log_dir_path + f"/{self.name}/a_inp.txt", "w") as f:
          f.write('')
      if not os.path.exists(self.log_dir_path + f"/{self.name}/c_inp.txt") and self.config.ENABLE_COMMUNICATION:
        with open(self.log_dir_path + f"/{self.name}/c_inp.txt", "w") as f:
          f.write('')
      if not os.path.exists(self.log_dir_path + f"/{self.name}/c_out.txt") and self.config.ENABLE_COMMUNICATION:
        with open(self.log_dir_path + f"/{self.name}/c_out.txt", "w") as f:
          f.write('')
      if not os.path.exists(self.log_dir_path + f"/{self.name}/cost.txt"):
        with open(self.log_dir_path + f"/{self.name}/cost.txt", "w") as f:
          f.write('')
      if not os.path.exists(self.log_dir_path + f"/{self.name}/prompt.txt"):
        with open(self.log_dir_path + f"/{self.name}/prompt.txt", "w") as f:
          f.write(self.basic_prompt.sp)
        with open(self.log_dir_path + f"/{self.name}/prompt.txt", "a") as f:
          f.write('--' * 25 + " example input prompt " + '--' * 25)
          f.write(self.basic_prompt.eip)
          f.write('--' * 25 + " example output prompt " + '--' * 25)
          f.write(self.basic_prompt.eop)


  # Main API Func, receive obs and get actions
  def query(self, obs) -> None:
    while self.is_waiting is False:
      with self.lock:
        self.is_waiting = True
    logger.success(f"[ID {self.log_id}] LLMAgent {self.name}: Start waiting for response")

    self.get_text_c_inp()
    text_o = self.get_text_o(obs)

    # raw_text_a = self.get_text_a(text_o)
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
    self.first_action = True
    logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: Listen to {self.communication_message_i}")
    logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: Send info to {self.communication_message_o}")
    with open(self.history_func_path, "a") as f:
      print('--' * 50, file=f)
    while self.is_waiting is True:
      with self.lock:
        self.is_waiting = False
        self.action_lists = action_lists

  # query step1: all teams' pysc2 obs to a llm obs text (or multimodal llm text)
  def get_text_o(self, obs) -> str:

    text_o = ''
    # try:
    #     text_o = self.translator_o.translate(self)
    # except Exception as e:
    #     logger.error(f"[ID {self.log_id}] Error in {self.name} get_text_o(): {e}")
    text_o = self.translator_o.translate(self)

    if self.name not in self.config.AGENTS_ALWAYS_DISABLE and self.enable:
      with open(self.log_dir_path + f"/{self.name}/o.txt", "a", newline='\n') as f:
        print(json.dumps({self.main_loop_step: text_o}), file=f)

    self.last_text_o = text_o
    return text_o

  # query step2: communicate with llm and get text actions
  def get_text_a(self, text_o: str, base64_image=None) -> str:
    text_a = ''

    if self.config.LLM_SIMULATION_TIME > 0:
      logger.warning(f"[ID {self.log_id}] LLM SIMULATION MODE, no remote llm involved")
      time.sleep(self.config.LLM_SIMULATION_TIME)  # simulate llm response, for debug
      if self.name not in self.config.AGENTS_ALWAYS_DISABLE and self.enable:
        with open(self.log_dir_path + f"/{self.name}/a_inp.txt", "r") as f:
          text_a = f.read()  # simulate llm response by reading text in a_inp.txt
    else:
      if base64_image is None:
        text_a = self.client.query(text_o)  # Communicate with LLM
        logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: No image provided to LLM.")
      else:
        text_a = self.client.query(text_o, base64_image=base64_image)  # Communicate with VLLM
        logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}: Image provided to LLM.")

    self.last_text_a_raw = text_a
    return text_a

  # query step3: text action to pysc2 functions
  def get_func_a(self, raw_text_a) -> (list, dict):
    new_action_lists = []
    action_list_dict = {}
    processed_text_a = ''

    try:
        new_action_lists, action_list_dict, processed_text_a = self.translator_a.translate(raw_text_a)
    except Exception as e:
        logger.error(f"[ID {self.log_id}] Error in {self.name} get_func_a(): {e}")
    # new_action_lists, processed_text_a = self.translator_a.translate(raw_text_a)
    self.last_text_a_pro = processed_text_a

    if self.name not in self.config.AGENTS_ALWAYS_DISABLE and self.enable:
      with open(self.log_dir_path + f"/{self.name}/a_raw.txt", "a", newline='\n') as f:
        print(json.dumps({self.main_loop_step: raw_text_a}), file=f)

    if self.name not in self.config.AGENTS_ALWAYS_DISABLE and self.enable:
      with open(self.log_dir_path + f"/{self.name}/a_pro.txt", "a", newline='\n') as f:
        print(json.dumps({self.main_loop_step: processed_text_a}), file=f)

    if self.name not in self.config.AGENTS_ALWAYS_DISABLE and self.enable:
      with open(self.log_dir_path + f"/{self.name}/cost.txt", "a", newline='\n') as f:
        c = self.client
        client_cost = f"time={c.query_time:.2f}, ave_time={c.ave_query_time:.2f}, " \
                      f"token_in={c.query_token_in}, ave_token_in={c.ave_query_token_in:.2f}, " \
                      f"token_out={c.query_token_out}, ave_token_out = {c.ave_query_token_out:.2f}"
        print(json.dumps({self.main_loop_step: client_cost}), file=f)

    return new_action_lists, action_list_dict

  # get text shaped communication
  def get_text_c_inp(self) -> None:
    if self.name not in self.config.AGENTS_ALWAYS_DISABLE and self.enable and self.config.ENABLE_COMMUNICATION:
      with open(self.log_dir_path + f"/{self.name}/c_inp.txt", "a", newline='\n') as f:
        print(json.dumps({self.main_loop_step: self.last_text_c_inp}), file=f)

  # get channel listen to and sort information to sent out
  def get_info_c_out(self, raw_text_a) -> None:
    self.communication_message_i, self.communication_message_o, self.last_text_c_out = self.communicator.send(raw_text_a)
    if self.name not in self.config.AGENTS_ALWAYS_DISABLE and self.enable and self.config.ENABLE_COMMUNICATION:
      with open(self.log_dir_path + f"/{self.name}/c_out.txt", "a", newline='\n') as f:
        print(json.dumps({self.main_loop_step: self.last_text_c_out}), file=f)

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

    if len(self.func_list) == 0:
      action = self.action_list.pop(0)
      action = llm_action.add_func_for_select_workers(self, obs, action)
      action = llm_action.add_func_for_train_and_research(self, obs, action)
      self.func_list = action['func']
      # self.func_list_standard = llm_a.get_text_action(self.name, action['name'])
      self.curr_action_name = action['name']
      self.curr_action_args = action['arg']

    # for i in range(len(self.func_list)):
    # logger.debug(f"[ID {self.log_id}] LLMAgent {self.name}, get_func(): self.func_list[{i}] = {self.func_list[i]}")
    func_id, func, llm_pysc2_args = self.func_list.pop(0)
    func_call = None
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
            if self.first_action and pysc2_arg in ['now', 'queued']:
              pysc2_arg = 'now'
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
            if func_id == 573 and ('Build_Nexus_' in self.curr_action_name or 'Lock_Nexus_' in self.curr_action_name):
              pysc2_arg, func_valid = llm_action.get_arg_world_tag_base_building(
                obs, llm_pysc2_arg, self.world_x_offset, self.world_y_offset, self.world_range)
            elif func_id == 573:
              pysc2_arg, func_valid = llm_action.get_arg_world_tag(
                obs, llm_pysc2_arg, self.world_x_offset, self.world_y_offset, self.world_range)  # tag转全局坐标
            elif func.name == 'select_rect':  # 单选单位
              pysc2_arg, func_valid = llm_action.get_arg_screen_tag_sclect_rect(
                obs, llm_pysc2_arg, self.size_screen, func.args[i].name)  # tag转屏幕坐标
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
            with open(self.history_func_path, "a") as f:  # 打开文件
              print(f"{self.name};   loop{self.main_loop_step};   step{self.num_step};   [Invalid Args]  {func.name} {pysc2_args}", file=f)
            logger.warning(f"[ID {self.log_id}] LLMAgent {self.name} get_func() Error type 1: Arg quantity invalid: ({pysc2_args})! Replace with no_op().")
            func_id, func_call = (0, actions.FUNCTIONS.no_op())
        else:
          with open(self.history_func_path, "a") as f:  # 打开文件
            print(f"{self.name};   loop{self.main_loop_step};   step{self.num_step};   [Invalid Args]  {func.name} {pysc2_args} ", file=f)
          logger.warning(f"[ID {self.log_id}] LLMAgent {self.name} get_func() Error type 2: Func {func} Arg invalid: {pysc2_args}! Replace with no_op()")
          func_id, func_call = (0, actions.FUNCTIONS.no_op())
    else:
      with open(self.history_func_path, "a") as f:  # 打开文件
        print(f"{self.name};   loop{self.main_loop_step};   step{self.num_step};   [Invalid Func]  {func.name} ", file=f)
      logger.warning(f"[ID {self.log_id}] LLMAgent {self.name} get_func() Error type 3: Func invalid: {func}! Replace with no_op()")
      func_id, func_call = (0, actions.FUNCTIONS.no_op())

    # 保存动作信息
    with open(self.history_func_path, "a") as f:  # 打开文件
      if func_id != 0:
        print(f"{self.name};   loop{self.main_loop_step};   step{self.num_step};   [   Success  ]  {func_call}", file=f)
    if self.first_action and 'now' in pysc2_args:
      self.first_action = False
    if len(self.action_list) == 0:
      self.first_action = True  # 本小队最后一个动作已经执行完毕
    logger.info(f"[ID {self.log_id}] LLMAgent {self.name} get_func(): Get Func {func_id}, {func_call}")
    return func_id, func_call


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

  # 如需修改Agent与LLM的交互方式，重定义接口函数act即可
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
    self.first_action = True
    with open(self.history_func_path, "a") as f:
      print('--' * 50, file=f)
    while self.is_waiting is True:
      with self.lock:
        self.is_waiting = False
        self.action_lists = action_lists
