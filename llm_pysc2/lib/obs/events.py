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


from pysc2.lib import features, units, buffs


def get_unit_in_unit_dict(tag, unit_dict):
  for unit_tag in unit_dict.keys():
    if unit_tag == tag:
      return unit_dict[unit_tag]


def get_events(agent, t, n, i_list: list):
  # TODO: s_{t-n}, a_{t-n}, s_{t-n+i1}, s_{t-n+i2}, s_{t-n+i3} ...
  #  n 往前n步， i从t-n往后i步

  event_dicts = {}

  i_list.sort(reverse=False)
  teams_history = agent.teams_history
  teams_history_keys = teams_history.keys()

  for i in i_list:

    teams_t_n = teams_history[t - n] if t - n in teams_history_keys else None
    teams_t_n_i = teams_history[t - n + i] if t - n + i in teams_history_keys else None
    teams_t1, teams_t2 = (teams_t_n, teams_t_n_i) if (i > 0) else (teams_t_n_i, teams_t_n)

    event_dict = get_event(agent, teams_t1, teams_t2)
    event_dicts[str(i)] = event_dict
    # print(f"event_dict[{event_name}] = {event_dict}")

  return event_dicts

def get_event(agent, teams_t1=None, teams_t2=None):
  # team in agent.teams, usually, one team only have one obs
  event_dict = {}
  if teams_t1 is None or teams_t2 is None:
    return event_dict

  # for team in agent.teams:
  #   if len(team['obs']) == len(team['obs_last']):
  #     team_name = team['name']
  #     event_dict[team_name] = {}
  #     for i in range(len(team['obs'])):
  #       obs1 = team['obs_last'][i]
  #       obs2 = team['obs'][i]

  for team_t1 in teams_t1:
    team_name = team_t1['name']
    event_dict[team_name] = {}
    team_t2 = None
    for team in teams_t2:
      if team['name'] == team_name:
        team_t2 = team

    team_event_dict = {'ctrl': {}, 'ally': {}, 'enemy': {}}
    if len(team_t1['obs']) == 0 or len(team_t2['obs']) == 0:
      if len(team_t1['obs']) == 0:
        team_event_dict = {'ctrl': {}, 'ally': {}, 'enemy': {}}  # team enable
      if len(team_t2['obs']) == 0:
        team_event_dict = {'ctrl': {}, 'ally': {}, 'enemy': {}}  # team disable, all units dead

    total_life = 0
    if len(team_t1['obs']) == len(team_t2['obs']) and (len(team_t1['obs']) != 0 and len(team_t2['obs']) != 0):
      # for i in range(len(team_t1['obs'])):
      obs1 = team_t1['obs'][0]
      obs2 = team_t2['obs'][0]
      unit_ctrl_state_dict1 = {}
      unit_ally_state_dict1 = {}
      unit_enemy_state_dict1 = {}
      unit_ctrl_state_dict2 = {}
      unit_ally_state_dict2 = {}
      unit_enemy_state_dict2 = {}
      unit_ctrl_state_dict3 = {}
      unit_ally_state_dict3 = {}
      unit_enemy_state_dict3 = {}
      team_event_dict = {'ctrl': {}, 'ally': {}, 'enemy': {}}

      if 'raw_units' not in obs1.observation.keys():
        print(obs1.observation.__dir__())
        print(obs1.observation.keys())
      if 'raw_units' not in obs2.observation.keys():
        print(obs2.observation.__dir__())
        print(obs2.observation.keys())
      if 'raw_units' not in obs1.observation.keys() or 'raw_units' not in obs2.observation.keys():
        continue
      for unit_r in obs2.observation['raw_units']:
        if unit_r.tag in team_t2['unit_tags']:
          total_life += unit_r.health + unit_r.shield

      for unit in obs1.observation['raw_units']:
        # controlled/ally/enemy units
        if unit.is_on_screen and unit.alliance in [1] and unit.tag in agent.unit_tag_list_history:
          unit_ctrl_state_dict1[unit.tag] = unit
        if unit.is_on_screen and unit.alliance in [1, 2] and unit.tag not in agent.unit_tag_list_history:
          unit_ally_state_dict1[unit.tag] = unit
        if unit.is_on_screen and unit.alliance in [4]:
          unit_enemy_state_dict1[unit.tag] = unit

      for unit in obs2.observation['raw_units']:
        # controlled/ally/enemy units
        if unit.alliance in [1] and unit.tag in agent.unit_tag_list_history:
          unit_ctrl_state_dict2[unit.tag] = unit
        if unit.alliance in [1, 2] and unit.tag not in agent.unit_tag_list_history:
          unit_ally_state_dict2[unit.tag] = unit
        if unit.alliance in [4]:
          unit_enemy_state_dict2[unit.tag] = unit

      for unit in obs2.observation['raw_units']:
        # controlled/ally/enemy units
        if unit.is_on_screen and unit.alliance in [1] and unit.tag in agent.unit_tag_list_history:
          unit_ctrl_state_dict3[unit.tag] = unit
        if unit.is_on_screen and unit.alliance in [1, 2] and unit.tag not in agent.unit_tag_list_history:
          unit_ally_state_dict3[unit.tag] = unit
        if unit.is_on_screen and unit.alliance in [4]:
          unit_enemy_state_dict3[unit.tag] = unit

      for tag in unit_ctrl_state_dict1.keys():
        unit1 = unit_ctrl_state_dict1[tag]
        unit_info = f"{hex(tag)}({str(units.get_unit_type(unit1.unit_type))})"
        if unit1.tag in unit_ctrl_state_dict2.keys():
          unit2 = get_unit_in_unit_dict(unit1.tag, unit_ctrl_state_dict2)
          delta_health = (unit2.health + unit2.shield) - (unit1.health + unit1.shield)
          if delta_health > 0:
            team_event_dict['ctrl'][int(unit1.tag)] = f'unit {unit_info} is healing, health +{abs(delta_health)}'
          if delta_health < 0:
            team_event_dict['ctrl'][int(unit1.tag)] = f'unit {unit_info} is attacked, health -{abs(delta_health)}'
          unit_ctrl_state_dict3[int(unit1.tag)] = None
        if unit1.tag not in unit_ctrl_state_dict2.keys():
          team_event_dict['ctrl'][int(unit1.tag)] = f'unit {unit_info} dead, lost the final {unit1.health + unit1.shield} health'

      for tag in unit_ally_state_dict1.keys():
        unit1 = unit_ally_state_dict1[tag]
        unit_info = f"{hex(tag)}({str(units.get_unit_type(unit1.unit_type))})"
        if unit1.tag in unit_ally_state_dict2.keys():
          unit2 = get_unit_in_unit_dict(unit1.tag, unit_ally_state_dict2)
          delta_health = (unit2.health + unit2.shield) - (unit1.health + unit1.shield)
          if delta_health > 0 and unit2.build_progress == 100:
            team_event_dict['ally'][int(unit1.tag)] = f'unit {unit_info} is healing, health +{abs(delta_health)}%'
          if delta_health < 0 and unit2.build_progress == 100:
            team_event_dict['ally'][int(unit1.tag)] = f'unit {unit_info} is attacked, health -{abs(delta_health)}%'
          if unit2.build_progress < 100:
            delta_building_process = unit2.build_progress - unit1.build_progress
            team_event_dict['ally'][int(unit1.tag)] = f'unit {unit_info} is training/building, process +{abs(delta_building_process)}%  (current process {unit2.build_progress}%)'
          unit_ally_state_dict3[int(unit1.tag)] = None
        if unit1.tag not in unit_ally_state_dict2.keys():
          team_event_dict['ally'][int(unit1.tag)] = f'unit {unit_info} dead, lost the final {unit1.health + unit1.shield} health'

      for tag in unit_enemy_state_dict1.keys():
        unit1 = unit_enemy_state_dict1[tag]
        unit_info = f"{hex(tag)}({str(units.get_unit_type(unit1.unit_type))})"
        if unit1.tag in unit_enemy_state_dict2.keys():
          unit2 = get_unit_in_unit_dict(unit1.tag, unit_enemy_state_dict2)
          delta_health = (unit2.health + unit2.shield) - (unit1.health + unit1.shield)
          if delta_health > 0:
            team_event_dict['enemy'][int(unit1.tag)] = f'unit {unit_info} is healing, health +{abs(delta_health)}'
          if delta_health < 0:
            team_event_dict['enemy'][int(unit1.tag)] = f'unit {unit_info} is attacked, health -{abs(delta_health)}'
          unit_enemy_state_dict3[int(unit1.tag)] = None
        if unit1.tag not in unit_enemy_state_dict2.keys():
          team_event_dict['enemy'][int(unit1.tag)] = f'unit {unit_info} dead, lost the final {unit1.health + unit1.shield} health'

      # event_dict[team_name][i] = team_event_dict

      for tag in unit_ctrl_state_dict3.keys():
        unit3 = unit_ctrl_state_dict3[tag]
        if unit3 is not None:
          unit_info = f"{hex(tag)}({str(units.get_unit_type(unit3.unit_type))})"
          team_event_dict['ctrl'][int(tag)] = f'unit {unit_info} joint the team {team_name}'
      for tag in unit_ally_state_dict3.keys():
        unit3 = unit_ally_state_dict3[tag]
        if unit3 is not None:
          unit_info = f"{hex(tag)}({str(units.get_unit_type(unit3.unit_type))})"
          team_event_dict['ally'][int(tag)] = f'unit {unit_info} ally unit enter sight'
      for tag in unit_enemy_state_dict3.keys():
        unit3 = unit_enemy_state_dict3[tag]
        if unit3 is not None:
          unit_info = f"{hex(tag)}({str(units.get_unit_type(unit3.unit_type))})"
          team_event_dict['enemy'][int(tag)] = f'unit {unit_info} enemy unit enter sight'

      event_dict[team_name] = team_event_dict
      if total_life < 10:
        event_dict[team_name]['ally'] = {}
        event_dict[team_name]['enemy'] = {}

  return event_dict