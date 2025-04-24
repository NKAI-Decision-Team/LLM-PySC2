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


from llm_pysc2.lib.action.check import check_develop_action_validity, check_scan_action_validity, check_weapon_state
from llm_pysc2.lib.action.complete import *
from llm_pysc2.lib.action.arg_build import *
from llm_pysc2.lib.action.arg import *
from llm_pysc2.lib import utils

from pysc2.lib import units, actions, features, buffs, upgrades
from pysc2.lib.actions import FUNCTIONS as F

from loguru import logger
import numpy as np
import random
import math
import re


def get_func(agent, obs):  # 该函数需要将当前text-pysc2动作对应的下一个pysc2函数取出，确认函数和参数是合法的，然后交给到主智能体

  enable_no_op = False
  text_action = None
  text_func = None

  if len(agent.func_list) == 0:
    action = agent.action_list.pop(0)
    agent.action_valid_check_1 = True
    agent.curr_action_name = action['name']
    agent.curr_action_args = action['arg']
    action = add_func_for_select_workers(agent, obs, action)
    action = add_func_for_train_and_research(agent, obs, action)
    action = add_func_for_chrono_boost(agent, obs, action)
    action = add_func_for_easy_build(agent, obs, action)
    action = add_func_for_easy_control(agent, obs, action)
    action = add_func_for_easy_warp(agent, obs, action)
    action = add_func_for_build(agent, obs, action)
    agent.func_list = action['func']
    agent.curr_action_valid = True
    text_action = f'<{agent.curr_action_name}({agent.curr_action_args})>'

    valid = check_develop_action_validity(agent, obs, agent.curr_action_name)
    valid = valid and check_scan_action_validity(agent, obs, agent.curr_action_name)
    if not valid:
      agent.func_list = []
      text = f"{agent.name};   loop{agent.main_loop_step};   step{agent.num_step};   [Invalid Action]  {agent.curr_action_name}"
      utils.write_to_file(text, agent.history_func_path)
      func_id, func_call = (0, F.no_op())
      return func_id, func_call, enable_no_op, None

    if agent.curr_action_name != 'No_Operation':
      text = f"{agent.name};   loop{agent.main_loop_step};   step{agent.num_step};   [   Success  ]  Action Detected: {text_action}"
      utils.write_to_file(text, agent.history_func_path)

    if 'Attack' in agent.curr_action_name and 'Ability' not in agent.curr_action_name and 'All_Unit_' not in agent.curr_action_name:
      queued, source_unit_tag = '', None
      for func_triple in agent.func_list:
        func_id, func, llm_pysc2_args = func_triple
        for arg in llm_pysc2_args:
          queued = arg if (func_id == 12 and (arg == 'queued' or arg == 'now')) else queued  # attack
          source_unit_tag = arg if (func_id == 3 and isinstance(arg, int)) else source_unit_tag  # select rect
      agent.action_valid_check_1 = check_weapon_state(obs, queued, source_unit_tag, strict=True)

  # for i in range(len(agent.func_list)):
  # logger.debug(f"[ID {agent.log_id}] LLMAgent {agent.name}, get_func(): agent.func_list[{i}] = {agent.func_list[i]}")
  func_id, func, llm_pysc2_args = agent.func_list.pop(0)
  func_call = None
  if func.name == "no_op" and agent.curr_action_valid and agent.action_valid_check_1:
    enable_no_op = True
  # func_id, func, llm_pysc2_arg_types = llm_a.get_action(agent.name, )

  pysc2_args = []
  if func_id in obs.observation.available_actions:  # 函数合法性检验，非法动作直接跳出
    func_valid = True
    pysc2_args = []

    if len(llm_pysc2_args) == 0:
      func_call = func()
      # logger.debug(f"[ID {agent.log_id}] LLMAgent {agent.name}, call func() = {func()}")

    if len(llm_pysc2_args) > 0:

      for i in range(len(llm_pysc2_args)):
        llm_pysc2_arg = llm_pysc2_args[i]
        # logger.debug(f"[ID {agent.log_id}] LLMAgent {agent.name}, get_func(): llm_pysc2_arg= {llm_pysc2_arg}, type(llm_pysc2_arg) = {type(llm_pysc2_arg)}")
        if isinstance(llm_pysc2_arg, str):  # queued形式的flag
          func_valid = False if llm_pysc2_arg not in ['now', 'queued', 'select', 'add'] else True
          pysc2_arg = llm_pysc2_arg
          if func.args[i].name == 'minimap' and llm_pysc2_arg == 'here':
            pysc2_arg, func_valid = get_arg_minimap_here(obs, agent.size_minimap, agent.curr_action_name)
          # if agent.first_action and pysc2_arg in ['now', 'queued']:
          #   pysc2_arg = 'now'
        elif isinstance(llm_pysc2_arg, list) and len(llm_pysc2_arg) == 2:  # 坐标
          func_valid = False
          if func.args[i].name == 'minimap':  # 小地图坐标
            pysc2_arg, func_valid = get_arg_minimap(obs, llm_pysc2_arg, agent.size_minimap, agent.curr_action_name)  # 小地图坐标合法性判断
          elif func.args[i].name == 'screen' and 'Build' in func.name:  # 建造
            pysc2_arg, func_valid = get_arg_screen_build(obs, llm_pysc2_arg, agent.size_screen, agent.curr_action_name)  # 建筑的屏幕坐标合法性判断
          elif func.args[i].name == 'screen' and 'Build' not in func.name:  # 无限制
            pysc2_arg, func_valid = get_arg_screen(obs, llm_pysc2_arg, agent.size_screen, agent.curr_action_name)  # 屏幕坐标合法性判断
          elif func_id == 573:
            pysc2_arg, func_valid = get_arg_world(obs, llm_pysc2_arg, agent.world_x_offset, agent.world_y_offset, agent.world_range)  # tag转全局坐标
          else:
            pysc2_arg = 'WrongType-Arg'  # 错误处理，接受func_valid = False，使用no_op代替该动作
        elif isinstance(llm_pysc2_arg, int):
          func_valid = False
          # print(agent.curr_action_name)
          # print(i, func.args, func)
          builder_selected, is_builder_tag = False, False
          if 'Build_' in agent.curr_action_name or 'Lock_' in agent.curr_action_name:
            for unit in obs.observation.raw_units:
              if unit.unit_type in BUILDER_TYPE and unit.alliance == features.PlayerRelative.SELF and unit.is_selected == 1:
                builder_selected = True
              if unit.unit_type in BUILDER_TYPE and unit.alliance == features.PlayerRelative.SELF and unit.tag == llm_pysc2_arg:
                is_builder_tag = True
          # print(f"xxx conditions = {func_id, agent.curr_action_name, agent.curr_action_name.split('_')[1], builder_selected}")
          if func.args[i].name == 'screen' and 'Build' in func.name:  # 建造  and agent.config.ENABLE_EASY_BUILD
            pysc2_arg, func_valid = get_arg_screen_tag_build(
              obs, llm_pysc2_arg, agent.size_screen, agent.curr_action_name, agent.config.ENABLE_EASY_BUILD)  # 建筑的屏幕坐标合法性判断
          elif func_id == 573 and ('Build_' in agent.curr_action_name or 'Lock_' in agent.curr_action_name) and \
              agent.curr_action_name.split('_')[1] in BASE_BUILDING_NAMES and builder_selected and not is_builder_tag:
            pysc2_arg, func_valid = get_arg_world_tag_base_building(
              obs, llm_pysc2_arg, agent.world_x_offset, agent.world_y_offset, agent.world_range)
          elif func_id == 573:
            pysc2_arg, func_valid = get_arg_world_tag(
              obs, llm_pysc2_arg, agent.world_x_offset, agent.world_y_offset, agent.world_range)  # tag转全局坐标
          elif func.name == 'select_rect':  # 单选单位
            pysc2_arg, func_valid = get_arg_screen_tag_sclect_rect(
              obs, llm_pysc2_arg, agent.size_screen, func.args[i].name)  # tag转屏幕坐标
          elif func.name == 'select_point':  # 该动作用于代替no_op,当作悬空动作，用于确保带后摇的攻击成功释放
            pysc2_arg, func_valid = get_arg_screen_tag(
              obs, llm_pysc2_arg, agent.size_screen, agent.curr_action_name)  # tag转屏幕坐标
          elif func.args[i].name == 'screen' and 'Recall' in func.name:  # 召回，临近单位群的中心
            pysc2_arg, func_valid = get_arg_screen_tag_recall(
              obs, llm_pysc2_arg, agent.size_screen, agent.curr_action_name)  # tag转屏幕坐标
          elif func.args[i].name == 'screen' and 'TrainWarp' in func.name:  # 折跃，水晶塔/棱镜力场附近
            pysc2_arg, func_valid = get_arg_screen_tag_warp(
              obs, llm_pysc2_arg, agent.size_screen, agent.curr_action_name)  # tag转屏幕坐标
          elif func.args[i].name == 'screen' and func_id in [65, 70]:  # 建造主矿/水晶塔封矿
            pysc2_arg, func_valid = get_arg_screen_tag_base_building(
              obs, llm_pysc2_arg, agent.size_screen, agent.curr_action_name)  # tag转屏幕坐标
          elif func.args[i].name == 'screen' and func_id in [40]:  # 建造气站/封对面气
            pysc2_arg, func_valid = get_arg_screen_tag_gas_building(
              obs, llm_pysc2_arg, agent.size_screen, agent.curr_action_name)  # tag转屏幕坐标
          elif func.args[i].name == 'screen':  # 无限制
            pysc2_arg, func_valid = get_arg_screen_tag(
              obs, llm_pysc2_arg, agent.size_screen, agent.curr_action_name)  # tag转屏幕坐标
          else:
            func_valid = False
            pysc2_arg = 'WrongType-Arg'  # 错误处理
        else:
          func_valid = False
          pysc2_arg = 'WrongType-Arg'

        if not func_valid:
          agent.curr_action_valid = False
          if agent.curr_action_name not in agent.action_errors:
            agent.action_errors[agent.curr_action_name] = []
          if pysc2_arg not in agent.action_errors[agent.curr_action_name]:
            agent.action_errors[agent.curr_action_name].append(pysc2_arg)
        pysc2_args.append(pysc2_arg)

      if func_valid is True and 'error' not in pysc2_args:
        logger.info(
          f"[ID {agent.log_id}] LLMAgent {agent.name}, get_func(): func avaliable, func {func} pysc2_args {pysc2_args}")
        if len(pysc2_args) == 3:
          func_call = func(pysc2_args[0], pysc2_args[1], pysc2_args[2])
        elif len(pysc2_args) == 2:
          func_call = func(pysc2_args[0], pysc2_args[1])
        elif len(pysc2_args) == 1:
          func_call = func(pysc2_args[0])
        else:
          text = f"{agent.name};   loop{agent.main_loop_step};   step{agent.num_step};   [Invalid Args]  {func.name} {pysc2_args}"
          utils.write_to_file(text, agent.history_func_path)
          logger.warning(
            f"[ID {agent.log_id}] LLMAgent {agent.name} get_func() Error type 1: Arg quantity invalid: ({pysc2_args})! Replace with no_op().")
          func_id, func_call = (0, F.no_op())
      else:
        text = f"{agent.name};   loop{agent.main_loop_step};   step{agent.num_step};   [Invalid Args]  {func.name} {pysc2_args} "
        utils.write_to_file(text, agent.history_func_path)
        logger.warning(
          f"[ID {agent.log_id}] LLMAgent {agent.name} get_func() Error type 2: Func {func} Arg invalid: {pysc2_args}! Replace with no_op()")
        func_id, func_call = (0, F.no_op())

  else:
    enable_no_op = False
    error_info = f'Function Invalid'
    agent.action_errors[agent.curr_action_name] = [error_info]
    text = f"{agent.name};   loop{agent.main_loop_step};   step{agent.num_step};   [Invalid Func]  {func.name} {error_info}"
    utils.write_to_file(text, agent.history_func_path)
    logger.warning(
      f"[ID {agent.log_id}] LLMAgent {agent.name} get_func() Error type 3: Func invalid: {func}! Replace with no_op()")
    for unit in obs.observation.raw_units:
      if unit.is_selected == 1:
        unit_info = f'unit {hex(unit.tag)}({str(units.get_unit_type(unit.unit_type))}) {unit.is_on_screen} {unit.is_selected} {unit.x, unit.y}'
        logger.debug(f"[ID {agent.log_id}] LLMAgent {agent.name}, get_func() selected_unit_info = {unit_info}")
    func_id, func_call = (0, F.no_op())

  if not agent.action_valid_check_1 and func_id not in [12, 3, 4]:
    enable_no_op = False
    error_info = f'All weapons waiting for cooling down, unable to attack'
    agent.action_errors[agent.curr_action_name] = [error_info]
    text = f"{agent.name};   loop{agent.main_loop_step};   step{agent.num_step};   [Invalid Func]  {func.name} {error_info}"
    utils.write_to_file(text, agent.history_func_path)
    logger.warning(
      f"[ID {agent.log_id}] LLMAgent {agent.name} get_func() Error type 4: All weapons waiting for cooling down, unable to attack, but still redirect attack target")
    func_id, func_call = (0, F.no_op())

  # 保存动作信息
  if func_id != 0 or enable_no_op:
    text = f"{agent.name};   loop{agent.main_loop_step};   step{agent.num_step};   [   Success  ]  {func_call}"
    utils.write_to_file(text, agent.history_func_path)

  # if agent.first_action and 'now' in pysc2_args:
  #   agent.first_action = False
  # if len(agent.action_list) == 0:
  #   agent.first_action = True  # 本小队最后一个动作已经执行完毕

  logger.info(f"[ID {agent.log_id}] LLMAgent {agent.name} get_func(): Get Func {func_id}, {func_call}")
  return func_id, func_call, enable_no_op, text_action