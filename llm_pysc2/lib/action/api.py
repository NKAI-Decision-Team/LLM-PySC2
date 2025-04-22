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


from llm_pysc2.lib.utils import SCREEN_WORLD_GRID

from pysc2.lib import units, actions, features, buffs, upgrades
from pysc2.lib.actions import FUNCTIONS as F

from loguru import logger
import numpy as np
import random
import math
import re



class BaseTranslatorA:

  def __init__(self, name, log_id, config):
    self.name = name
    self.log_id = log_id
    self.config = config
    self.actions = []
    self.action = {}

    self.size_minimap = None
    self.size_screen = None

    # self.ACTION_SPACE = config.AGENTS[name]['action']
    # self.ACTION_SPACE_DICT = {}
    # for unit_type in self.ACTION_SPACE.keys():
    #   for action in self.ACTION_SPACE[unit_type]:
    #     self.ACTION_SPACE_DICT[action['name']] = action

  def translate(self, obs) -> "list of [(func_id, func_call)]":
    pass


# TODO: You can specialize your TranslatorA here


class DefaultTranslatorA(BaseTranslatorA):

  def __init__(self, name, log_id, config):
    super(DefaultTranslatorA, self).__init__(name, log_id, config)
    logger.info(f"[ID {self.log_id}] {name} DefaultTranslatorA initialized")

  # text actions recognition
  def translate(self, raw_text_a: str, obs=None):
    self.action = {'analysis': '', 'actions': ''}

    action_list_dict = {}
    action_lists, action_lists2 = [], []
    team_actions, team_actions2 = [], []
    processed_text_a, team_name, team_names = '', '', []
    self.curr_team_action_list = []
    self.curr_team_action_name_list = []

    lines = raw_text_a.splitlines()
    start_recognize = False
    first_function = True
    first_function_move = True
    first_action_attack = True
    first2_actions_attack = True
    # team_action_name_list = []

    for line in lines:
      line = line.replace('*', '')
      line = line.replace('`', '')
      line = line.replace('- ', '')
      # ACTION PART
      if ("Actions:" in line) or ("Action:" in line) or \
          ("actions:" in line) or ("action:" in line):
        processed_text_a = "Actions:"
        start_recognize = True

      # ANALYSIS PART
      if not start_recognize:
        if 'analysis' not in self.action.keys() and (("Analysis:" in line) or ("analysis:" in line)):
          self.action['analysis'] = line + '\n'
        elif 'analysis' in self.action.keys():
          self.action['analysis'] += line + '\n'
        else:
          pass

      # COMMUNICATION PART
      if ("Communications:" in line) or ("Communication:" in line) or \
          ("communications:" in line) or ("Communication:" in line):
        start_recognize = False

      # ACTION PART, TEAM ACTIONS
      if start_recognize:
        if ("Team" in line and ":" in line) or ("team" in line and ":" in line):

          team_name_old = team_name
          team_name = line.split("eam ")[-1].split(":")[0]  # Team/team xxxx:  -->  xxxx
          if 'eam' in team_name:
            team_name = team_name.replace('Team-', '')
            team_name = team_name.replace('team-', '')
            team_name = team_name.replace('Team', '')
            team_name = team_name.replace('team', '')

          self.curr_team_config = {}
          if team_name in self.config.AGENTS[self.name]['team'].keys():
            self.curr_team_config = self.config.AGENTS[self.name]['team'][team_name]
          elif team_name[:-2] in self.config.AGENTS[self.name]['team'].keys():
            self.curr_team_config = self.config.AGENTS[self.name]['team'][team_name[:-2]]  # single select 类型

          if len(self.curr_team_config.keys()) > 0:
            self.curr_team_action_list = []
            self.curr_team_action_name_list = []
            for team_actions_ in self.curr_team_config['actions'].values():
              self.curr_team_action_list += team_actions_
            for team_action in self.curr_team_action_list:
              self.curr_team_action_name_list.append(team_action['name'])  # 可能重复，如同一个小队多个兵种时，可能有多个Move

          # print(self.config.AGENTS[self.name]['team'].keys())
          # print(f"self.curr_team_config = {self.curr_team_config}")
          # print(f"self.curr_team_action_list = {self.curr_team_action_list}")

          # else:
          #   teams_ = self.config.AGENTS[self.name]['team']
          #   teams_unit_types, action_space = [], []
          #   for team_ in teams_:
          #     if team_['name'] == team_name:
          #       teams_unit_types += team_['unit_type']
          #   for unit_type in teams_unit_types:
          #     if unit_type in self.config.AGENTS[self.name]['action']:
          #       action_space += self.config.AGENTS[self.name]['action'][unit_type]
          #   team_action_name_list = [action['name'] for action in action_space]

          processed_text_a += f"\n\tTeam {team_name}:"
          if len(team_actions) != 0:
            action_lists.append(team_actions)
            action_lists2.append(team_actions2)
            action_list_dict[team_name_old] = team_actions
            team_actions, team_actions2 = [], []
            if team_name not in team_names:
              first_function = True
              first_function_move = True
              first_action_attack = True
              first2_actions_attack = True

            team_names.append(team_name)

          # print(f"team_name={team_name}, self.curr_team_action_name_list={self.curr_team_action_name_list}")


        elif "<" in line and ">" in line and '(' in line and ')' in line:
          line.replace('tag=', '')
          line.replace('screen=', '')
          line.replace('minimap=', '')
          try:
            action_text = line.split("<")[1].split(">")[0]
            action_name = action_text.split("(")[0]
            action_args = action_text.split("(")[-1].split(")")[0]
            print(action_text)
          except Exception as e:
            logger.error(f"translator find invalid action in line: {line}")
            continue
          action_valid, tag, tag2, tag3, x, y = True, None, None, None, None, None
          action = {'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]}
          if action_name not in self.curr_team_action_name_list:
            logger.error(f"translator unable to find {action_name} in team_config {self.curr_team_action_list}")
            continue
          if action_name not in self.curr_team_action_name_list:
            logger.error(f"translator unable to find {action_name} in current team config: {self.curr_team_config}")
            continue
          # if not first_action_attack and "Attack" in action_name and \
          #     "Select_Unit" not in action_name and "Ability" not in action_name:
          #   continue
          if not first2_actions_attack and "Attack" in action_name and \
              "Select_Unit" not in action_name and "Ability" not in action_name:
            continue
          if "0x" in action_args:
            tag = int(re.findall(r'0x\w+', action_args)[0], 16)
            if len(re.findall(r'0x\w+', action_args)) > 1:
              tag2 = int(re.findall(r'0x\w+', action_args)[1], 16)
            if len(re.findall(r'0x\w+', action_args)) > 2:
              tag3 = int(re.findall(r'0x\w+', action_args)[2], 16)
          if "[" in action_args:
            ratio = 1 if "Minimap" in action_name else self.size_screen / SCREEN_WORLD_GRID
            try:
              x = float(re.findall(r'\[-?\d+\.?\d*e?-?\d*?', action_args)[0].split("[")[1]) * ratio
              y = float(re.findall(r'-?\d+\.?\d*e?-?\d*?\]', action_args)[0].split("]")[0]) * ratio
            except Exception as e:
              logger.error(f"translator find invalid action in line: {line}")
              continue

          for action_ in self.curr_team_action_list:
            if action_name == action_['name']:
              action = action_

          # # 在动作空间中查找action_name对应的action
          # if action_name in self.ACTION_SPACE_DICT.keys():
          #   action = self.ACTION_SPACE_DICT[action_name]
          # else:
          #   logger.error(f"translator unable to find {action_name}")
          #   action = {'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]}
          #   action_valid = False

          # 将识别出的动作参数填入函数参数元组中
          new_func_triples, new_func_triples2 = [], []
          new_func_triple, new_func_triple2, new_func_args = [], [], []
          for func_triple in action['func']:  # func_triple 形如 (0, F.no_op, ())
            new_func_triple, new_func_triple2, new_func_args = [], [], []
            func_args = func_triple[2]
            if len(list(func_args)) > 0:
              if not isinstance(func_args, tuple):
                func_args = [func_args]
              for arg in list(func_args):
                if arg == 'auto':
                  new_func_args.append('auto')
                if arg == "now":
                  if "Move" not in action_name:
                    new_func_args.append('now')
                  elif "Move" in action_name and (first_function_move or "Select_Unit" in action_name):
                    new_func_args.append('now')
                  else:
                    new_func_args.append('queued')
                if arg == "queued":
                  if first_function:
                    new_func_args.append('now')
                    # if "Build" in action_name or self.name == 'Builder':
                    #   new_func_args.append('queued')
                    #   first_function = False
                    # else:
                    #   new_func_args.append('now')
                  else:
                    new_func_args.append('queued')
                if arg == "select":
                  new_func_args.append('select')
                if arg in ["screen_tag", "minimap_tag", "world_tag", "screen1_tag", "screen2_tag"]:
                  if tag is not None:
                    new_func_args.append(tag)
                  elif 'Build' in action_name and self.config.ENABLE_EASY_BUILD:
                    new_func_args.append('auto')
                  else:
                    new_func_args.append('error')
                if arg in ["screen_tag2", "minimap_tag2", "world_tag2", "screen1_tag2", "screen2_tag2"]:
                  if tag2 is not None:
                    new_func_args.append(tag2)
                  else:
                    new_func_args.append('error')
                if arg in ["screen", "minimap"]:
                  if (x is not None) and (y is not None):
                    new_func_args.append([x, y])
                  else:
                    new_func_args.append('error')
                # if arg in ["screen1_tag", "screen2_tag"]:
                #   if tag is not None:
                #     new_func_args.append(tag)
                #   else:
                #     new_func_args.append('error')
                # if arg in ["screen1_tag2", "screen2_tag2"]:
                #   if tag2 is not None:
                #     new_func_args.append(tag2)
                #   else:
                #     new_func_args.append('error')
            if 'error' not in new_func_args and first_function and 'now' in new_func_args:
              first_function = False
            if 'error' not in new_func_args and first_function_move and 'now' in new_func_args and \
                "Move" in action_name and "Select_Unit" not in action_name:
              first_function_move = False
            if 'error' in new_func_args:
              action_valid = False
            new_func_triple.append(func_triple[0])
            new_func_triple.append(func_triple[1])
            new_func_triple.append(tuple(new_func_args))
            new_func_triples.append(tuple(new_func_triple))

            new_func_triple2.append(func_triple[0])
            new_func_triple2.append(func_triple[1].name)
            new_func_triple2.append(tuple(new_func_args))
            new_func_triples2.append(tuple(new_func_triple2))

          if 'error' not in new_func_args and not first_action_attack and first2_actions_attack and \
              "Attack" in action_name and "Ability" not in action_name and "Select_Unit" not in action_name:
            first2_actions_attack = False
          if 'error' not in new_func_args and first_action_attack and \
              "Attack" in action_name and "Ability" not in action_name and "Select_Unit" not in action_name:
            first_action_attack = False

          if action_valid:

            team_actions.append({'name': action['name'], 'arg': action_args, 'func': new_func_triples})
            team_actions2.append({'name': action['name'], 'arg': action_args, 'func': new_func_triples2})
            processed_text_a += f"\n\t\t<{action_text}>"
          else:
            team_actions.append({'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]})
            team_actions2.append({'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]})
        else:
          pass

    self.action['actions'] = processed_text_a
    self.actions.append(self.action)

    # if self.name == 'Builder':
    #   team_actions.append({'name': 'HoldPosition-Auto', 'arg': [], 'func': [(274, F.HoldPosition_quick, ('queued',))]})
    # if self.name == 'Commander' and len(team_actions) == 0:
    #   team_actions.append({'name': 'All_Units_Defend-Auto', 'arg': [], 'func': [(0, F.no_op, ())]})
    if self.name == 'Developer' and obs is not None:
      gateway_list, morph_action_list = [], []
      for unit in obs.observation.raw_units:
        if unit.unit_type == units.Protoss.Gateway and unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100 and unit.active == 0:
          gateway_list.append(unit)

      if upgrades.Upgrades.WarpGateResearch in obs.observation.upgrades and len(gateway_list) > 0:
        a1 = (573, F.llm_pysc2_move_camera, [int(gateway_list[0].tag)])
        a2 = (2, F.select_point, ['select_all_type', int(gateway_list[0].tag)])
        a3 = (328, F.Morph_WarpGate_quick, [])
        team_actions.append({'name': 'Auto_Morph_Warpgate', 'arg': [], 'func': [a1, a2, a3]})
        processed_text_a += '\n\t\t<Auto_Morph_Warpgate()>'

    if len(team_actions) != 0:
      action_lists.append(team_actions)
      action_lists2.append(team_actions2)
      action_list_dict[team_name] = team_actions

    return action_lists, action_list_dict, processed_text_a


PROTOSS_FACTORY = {'default': DefaultTranslatorA}
TERRAN_FACTORY = {}
ZERG_FACTORY = {}

FACTORY = {
  'protoss': PROTOSS_FACTORY,
  'terran': TERRAN_FACTORY,
  'zerg': ZERG_FACTORY,
}


if __name__ == "__main__":
  from llm_pysc2.cfg import ConfigSmac_2s3z, ProtossAgentConfig

  config = ProtossAgentConfig()

  # ----------------- show action space -----------------
  # def show(config):
  #   for name in config.AGENTS.keys():
  #     # agent_actions = config.AGENTS[name]['action']
  #     agent_actions = {}
  #     for team_config in config.AGENTS[name]['team'].values():
  #       agent_actions[team_config['name']] = {}
  #       for unit_type in team_config['actions'].keys():
  #         agent_actions[team_config['name']][unit_type] = team_config['actions'][unit_type]
  #     print(name)
  #     for team_name in agent_actions.keys():
  #       print(f"\t{team_name}")
  #       for unit_type in agent_actions[team_name].keys():
  #         print(f"\t{str(units.get_unit_type(unit_type))}")
  #         for i in range(len(agent_actions[team_name][unit_type])):
  #           action = agent_actions[team_name][unit_type][i]
  #           if len(action['arg']) == 0:
  #             print(f"\t\t <{action['name']}()>")
  #         for i in range(len(agent_actions[team_name][unit_type])):
  #           action = agent_actions[team_name][unit_type][i]
  #           if len(action['arg']) == 1 and 'minimap' in action['arg']:
  #             print(f"\t\t <{action['name']}({action['arg'][0]})>")
  #         for i in range(len(agent_actions[team_name][unit_type])):
  #           action = agent_actions[team_name][unit_type][i]
  #           if len(action['arg']) == 1 and 'screen' in action['arg']:
  #             print(f"\t\t <{action['name']}({action['arg'][0]})>")
  #         for i in range(len(agent_actions[team_name][unit_type])):
  #           action = agent_actions[team_name][unit_type][i]
  #           if len(action['arg']) == 1 and 'tag' in action['arg']:
  #             print(f"\t\t <{action['name']}({action['arg'][0]})>")
  #         for i in range(len(agent_actions[team_name][unit_type])):
  #           action = agent_actions[team_name][unit_type][i]
  #           if len(action['arg']) == 2:
  #             print(f"\t\t <{action['name']}({action['arg'][0]}, {action['arg'][1]})>")
  # show(config)

  # ----------------- example of TranslatorA -----------------

  # translator = DefaultTranslatorA('CombatGroup0', log_id=0, config=config)
  translator = DefaultTranslatorA('Developer', log_id=0, config=config)
  # translator = DefaultTranslatorA('Builder', log_id=0, config=config)
  text = \
    """
    Analysis:
        We should do xxx and xxx.
    
    Actions:
        Builder-Probe-1:
            <Build_Nexus_Near(0x200ea0001)>
    
    Actions:
        **Team Zealot-1**:
            <Attack_Unit(0x200540001)> 
        Team Zealot-2:
            <Attack_Unit(0x200540001)>
            <Move_Minimap([24, 54])>                              # invalid in smac
        Team Stalker-1:
            <Ability_Blink_Screen([33, 96])>                      # invalid in smac
            <Select_Unit_Blink_Screen(0x1007c0001 ,[33, 96])>     # invalid in smac
            <Move_Screen([2, 9])>
        Team Builder-Probe-1:
            <Build_Pylon_Screen([8, 12])>  # Build the Pylon safely at a screen location, avoiding the Queens' range.
            <Build_Gateway_Screen([10, 12])>  # After the Pylon is completed, build the Gateway at a safe distance.
            <Build_Nexus_Near(0x200ea0001)>
        Team Protoss-Buildings-1:
            <Research_Charge()>
            <Research_Blink()>
            <Train_Stalker()>
            <Warp_Zealot()>
    """

  translator.size_screen = 128
  actions, action_list_dict, processed_text_a = translator.translate(text)

  print(f"\n\ntext to translator:{text}")
  print(f"detected action from translator:\n{actions}\n")
  print(f"action_list_dict from translator:\n{action_list_dict}\n")
  print(f"detected text_a from translator:\n{processed_text_a}\n")

