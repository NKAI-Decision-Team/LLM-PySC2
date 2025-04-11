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

from pysc2.lib import features
import numpy as np
import math


def get_info(obs):
  # for time condition
  game_loop = obs.observation.game_loop
  game_s = int(game_loop / 22 % 60)  # SC2 runs at 22.4 game loops per second
  game_m = int(game_loop / 22 // 60)  # SC2 runs at 22.4 game loops per second
  # for position condition
  idx = np.nonzero(obs.observation['feature_minimap']['camera'])
  minimap_x, minimap_y = int(idx[:][1].mean()), int(idx[:][0].mean())
  return minimap_x, minimap_y, game_m, game_s


def get_dist(x1, y1, x2, y2):
  dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
  return dist


def task_harass(agent):
  task_dict = {}
  for team in agent.teams:
    if len(team['obs']) == 0:
      continue
    if 'task' not in team.keys():
      team['task'] = ''
    x, y, m, s = get_info(team['obs'][0])
    if team['name'] in ['Oracle-1', 'Adept-1', 'Phoenix-1']:
      d1 = 2 if team['name'] == 'Adept-1' else 6  # flying unit +2
      d2 = 10

      # define tasks
      task1 = "Go to minimap coordinate [52, 32] as quick as possible."
      task2 = "Kill as much as enemy **Drones** as possible until all units dead."
      task3 = "Go back to minimap coordinate [52, 32], continuing killing **Drones** until all units dead."
      # task0 -> task1, or continue task1
      if (team['task'] == '' and get_dist(x, y, 52, 32) > d1) or \
          (team['task'] == task1 and get_dist(x, y, 52, 32) > d1):
        team['task'] = task1
      # task1 -> task2, task3 -> task2, or continue task2
      if (team['task'] == task1 and get_dist(x, y, 52, 32) <= d1) or \
          (team['task'] == task3 and get_dist(x, y, 52, 32) <= d2) or \
          (team['task'] == task2 and get_dist(x, y, 52, 32) <= d2):
        team['task'] = task2
      # task2 -> task3, task3 -> task2, or continue task3
      if (team['task'] == task3 and get_dist(x, y, 52, 32) > d2) or \
          (team['task'] == task2 and get_dist(x, y, 52, 32) > d2):
        team['task'] = task3

    if team['name'] == 'AdeptPhase-1':
      # define tasks
      task1 = "Assist the team Adept-1 to sneak into enemy territory, reposition during combat, or retreat."
      team['task'] = task1  # always task1

    task_dict[team['name']] = team['task']
  return task_dict


def task_defend(agent):
  task_dict = {}
  for team in agent.teams:
    if len(team['obs']) == 0:
      continue
    if 'task' not in team.keys():
      team['task'] = ''
    x, y, m, s = get_info(team['obs'][0])
    task1 = "Protect our nexus and probes from enemy airdrops. At Game time 0:00, 2 airdrops detected from minimap [24, 32] and [12, 24] to [16, 32]"
    task2 = "Protect our nexus and probes from enemy airdrops. At Game time 0:10, 2 airdrops detected from minimap [20, 24] and [20, 40] to [16, 32]"
    task3 = "Protect our nexus and probes from enemy airdrops. At Game time 0:20, 2 airdrops detected from minimap [24, 32] and [12, 40] to [16, 32]"
    task4 = "Protect our nexus and probes from enemy airdrops. At Game time 0:30, 2 airdrops detected from minimap [24, 32] and [10, 32] to [16, 32]"
    if s < 10:
      team['task'] = task1
    if 10 <= s < 20:
      team['task'] = task2
    if 20 <= s < 30:
      team['task'] = task3
    if 30 <= s < 40:
      team['task'] = task4
    task_dict[team['name']] = team['task']
  return task_dict


def task_combat(agent):
  task_dict = {}
  for team in agent.teams:
    if len(team['obs']) == 0:
      continue
    if 'task' not in team.keys():
      team['task'] = ''
    x, y, m, s = get_info(team['obs'][0])
    task1 = "Go to minimap coordinate [32, 32]."
    task2 = "Kill as much as enemy units as possible. If no enemy found, hold the position."

    if team['name'] == 'Commander':
      team['task'] = "Organize frontline commanders to collaborate in defeating enemy troops, you should reach the goal and finish the battle before game time 1:30."
    else:
      if s < 10 or get_dist(x, y, 32, 32) > 4:
        team['task'] = task1
      else:
        team['task'] = task2

    task_dict[team['name']] = team['task']
  return task_dict


def task_combat_small(agent):
  task_dict = {}
  for team in agent.teams:
    if len(team['obs']) == 0:
      continue
    if 'task' not in team.keys():
      team['task'] = ''
    x, y, m, s = get_info(team['obs'][0])
    task1 = "Go to minimap coordinate [32, 32]."
    task2 = "Kill as much as enemy units as possible. If no enemy found, hold the position."

    if team['name'] == 'Commander':
      team['task'] = "Organize frontline commanders to collaborate in defeating enemy troops, you should reach the goal and finish the battle before game time 1:30."
    else:
      if s < 5 and get_dist(x, y, 32, 32) > 4:
        team['task'] = task1
      else:
        team['task'] = task2

    task_dict[team['name']] = team['task']
  return task_dict


def task_multi_attack(agent):
  task_dict = {}
  for team in agent.teams:
    if len(team['obs']) == 0:
      continue
    if 'task' not in team.keys():
      team['task'] = ''
    x, y, m, s = get_info(team['obs'][0])
    if team['name'] == 'Commander':
      team['task'] = "Organize a multiline combat to defeat enemy troops and kill their workers, you should reach all the goals and finish the battle before game time 1:30."
    task_dict[team['name']] = team['task']
  return task_dict


def task_smac(agent):
  task_dict = {}
  for team in agent.teams:  # agent.config.AGENTS[agent.name]['team'].values()
    if len(team['obs']) == 0:
      continue
    if 'task' not in team.keys():
      team['task'] = ''
    x, y, m, s = get_info(team['obs'][0])

    enemy_on_screen = False
    if len(team['obs']) > 0:
      obs = team['obs'][0]
      for unit_f in obs.observation.feature_units:
        if unit_f.alliance == features.PlayerRelative.ENEMY and unit_f.is_on_screen:
          enemy_on_screen = True

    if s < 2:
      team['task'] = "Hold position and concentrate all teams fire on the incoming melee enemies(such as Zealot)."
      task_dict[team['name']] = team['task']
    elif enemy_on_screen:
      team['task'] = "Kill as much as enemy units as possible and avoid losing unit."
      task_dict[team['name']] = team['task']
    else:
      team['task'] = "Search for enemy units and ready for fight."
      task_dict[team['name']] = team['task']

  return task_dict


def task_smac_2s_vs_1sc(agent):
  task_dict = {}
  for team in agent.teams:  # agent.config.AGENTS[agent.name]['team'].values()
    if len(team['obs']) == 0:
      continue
    if 'task' not in team.keys():
      team['task'] = ''
    x, y, m, s = get_info(team['obs'][0])

    enemy_on_screen = False
    if len(team['obs']) > 0:
      obs = team['obs'][0]
      for unit_f in obs.observation.feature_units:
        if unit_f.alliance == features.PlayerRelative.ENEMY and unit_f.is_on_screen:
          enemy_on_screen = True

    if enemy_on_screen:
      team['task'] = "Kill as much as enemy units as possible and avoid losing unit. If unit heavily damaged, retreat to upside (y getting bigger) for healing."
      task_dict[team['name']] = team['task']
    else:
      team['task'] = "Search for enemy units and ready for fight. If heavily damaged, hold position and waiting for healing before searching for enemy."
      task_dict[team['name']] = team['task']

    return task_dict

def task_default(agent):
  task_dict = {}
  for team in agent.teams:  # agent.config.AGENTS[agent.name]['team'].values()
    if len(team['obs']) == 0:
      continue
    if 'task' not in team.keys():
      team['task'] = 'Complete the tasks assigned by the Commander'
    x, y, m, s = get_info(team['obs'][0])

    if team['name'] == 'Empty':
      if agent.name == 'Commander':
        team['task'] = 'Organize other agents through communication to win the game'
      if agent.name == 'Developer':
        team['task'] = "Develop economy, technology, train units to win the game. organize the agent 'Builder' to build buildings."

    if agent.name == 'Builder':
      team['task'] = "Build buildings only, according to the tasks assigned by the Developer or Commander, or based on your own judgment."

  return task_dict


# search task function by map name, obs.observation.map_name
FACTORY = {
  'default': task_default,

  '2a_harass_level1': task_harass,
  '3ph_harass_level1': task_harass,
  '4s_blink_vs_4r': task_combat_small,
  '4s_blink_vs_5r': task_combat_small,
  "4s_blink_vs_6r": task_combat_small,
  "4s_blink_vs_1R3r": task_combat_small,
  "4s_blink_vs_1R4r": task_combat_small,

  'pvz_task1_level1': task_harass,
  'pvz_task1_level2': task_harass,
  'pvz_task1_level3': task_harass,
  'pvz_task2_level1': task_harass,
  'pvz_task2_level2': task_harass,
  'pvz_task2_level3': task_harass,

  '2s_vs_1sc': task_smac,  # _2s_vs_1sc
  '3s_vs_3z': task_smac,
  '3s_vs_4z': task_smac,
  '3s_vs_5z': task_smac,
  '3s5z': task_smac,
  '2s3z': task_smac,
}

