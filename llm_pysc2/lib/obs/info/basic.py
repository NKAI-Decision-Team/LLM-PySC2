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


from pysc2.lib import upgrades
from llm_pysc2.lib.obs import events

import numpy as np
from loguru import logger


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


def get_task_info(agent) -> str:
  task_info = ''
  for team in agent.config.AGENTS[agent.name]['team'].values():
    if len(team['obs']) == 0:
      continue
    if isinstance(team['task'], str):
      task_info += f"\n\tTeam {team['name']}' task: {team['task']}"
  if task_info != '':
    task_info = f"Tasks:" + task_info
    task_info += "\nPlease note that **Tasks** are the most important information, all your decisions must aimed at completing the tasks.\n\n"
  return task_info


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





from llm_pysc2.lib.utils import *
from pysc2.lib import units


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
  # unit_info = f'unit {hex(unit.tag)}({str(units.get_unit_type(unit.unit_type)).split('.')[-1]})'

  def add_to_dict(my_dict, key, value):
    if key in my_dict.keys():
      my_dict[key].append(value)
    else:
      my_dict[key] = [value]

  obs = agent.team_unit_obs_list[0]
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.ENEMY:
      add_to_dict(unit_oppo, str(units.get_unit_type(unit.unit_type)).split('.')[-1], unit)
    if unit.alliance == features.PlayerRelative.SELF:
      if unit.build_progress == 100 and unit.unit_type in BUILDING_TYPE:
        add_to_dict(unit_self_building, str(units.get_unit_type(unit.unit_type)).split('.')[-1], unit)
      if unit.build_progress == 100 and unit.unit_type not in BUILDING_TYPE:
        add_to_dict(unit_self_other, str(units.get_unit_type(unit.unit_type)).split('.')[-1], unit)
      if unit.build_progress != 100 and unit.unit_type in BUILDING_TYPE:
        add_to_dict(build_process_building, str(units.get_unit_type(unit.unit_type)).split('.')[-1], unit)
      if unit.build_progress != 100 and unit.unit_type not in BUILDING_TYPE:
        add_to_dict(build_process_other, str(units.get_unit_type(unit.unit_type)).split('.')[-1], unit)

      if unit.unit_type in BUILDING_TYPE_MILITARY and unit.build_progress == 100:
        add_to_dict(unit_count['building_military'], str(units.get_unit_type(unit.unit_type)).split('.')[-1], unit)
        if unit.active == 0:
          add_to_dict(unit_count['building_military_idle'], str(units.get_unit_type(unit.unit_type)).split('.')[-1], unit)
        else:
          add_to_dict(unit_count['building_military_working'], str(units.get_unit_type(unit.unit_type)).split('.')[-1], unit)
      if unit.unit_type in BUILDING_TYPE_RESEARCH and unit.build_progress == 100:
        add_to_dict(unit_count['building_research'], str(units.get_unit_type(unit.unit_type)).split('.')[-1], unit)
        if unit.active == 0:
          add_to_dict(unit_count['building_research_idle'], str(units.get_unit_type(unit.unit_type)).split('.')[-1], unit)
        else:
          add_to_dict(unit_count['building_research_working'], str(units.get_unit_type(unit.unit_type)).split('.')[-1], unit)

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