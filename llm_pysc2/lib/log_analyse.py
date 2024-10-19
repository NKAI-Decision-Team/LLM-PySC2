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

import os
import pickle

# import matplotlib.pyplot as plt
import numpy as np
from llm_pysc2.lib.knowledge import DATA_ZERG, DATA_PROTOSS, DATA_TERRAN
from pysc2.lib import units, features
from pysc2.env import environment


def analyse_all(start_time: int, end_time=0):
  num_experiments = 0
  total_enemy_lost = 0
  total_self_lost = 0
  total_win = 0
  total_tie = 0
  total_lose = 0
  log_folder_names = os.listdir(os.path.dirname(os.path.abspath(__file__)))
  for folder_name in log_folder_names:
    if '-' in folder_name and start_time <= int(folder_name.split('-')[0]) <= max(end_time, start_time + 1):
      experiment_folder = f'./{folder_name}'
      print("--" * 50)
      print(f"start analyse {experiment_folder}")
      print("--" * 25)
      enemy_lost, self_lost, win, tie, lose = analyse(experiment_folder)
      num_experiments = num_experiments + win + tie + lose
      total_enemy_lost += enemy_lost
      total_self_lost += self_lost
      total_win += win
      total_tie += tie
      total_lose += lose

  if num_experiments > 0:
    rate_win = 100 * total_win / num_experiments
    rate_tie = 100 * total_tie / num_experiments
    rate_lose = 100 * total_lose / num_experiments
    ave_enemy_lost = total_enemy_lost / num_experiments
    ave_self_lost = total_self_lost / num_experiments
    ave_ratio = ave_enemy_lost / ave_self_lost if ave_self_lost != 0 else 999999
    return ave_enemy_lost, ave_self_lost, ave_ratio, rate_win, rate_tie, rate_lose
  else:
    print(f"\033[1;31m Error num_experiments == 0! \033[0m")
    return 0, 0, 0, 0, 0, 0



def analyse(experiment_folder):
  win, tie, lose = 0, 0, 0
  self_total_resource_lost = 0
  enemy_total_resource_lost = 0
  obs_lists = []  # 1 experiment with several episodes
  obs_list = []

  # find saved obs
  obs_folder_paths = []
  obs_list_pkl_paths = []
  for file_or_dir_name in os.listdir(experiment_folder):
    file_or_dir_path = os.path.join(experiment_folder, f"{file_or_dir_name}")
    if 'obs' in file_or_dir_name and os.path.isdir(file_or_dir_path):
      obs_folder_paths.append(file_or_dir_path)
    if 'obs-list-episode' in file_or_dir_name and '.pkl' in file_or_dir_name:
      obs_list_pkl_paths.append(file_or_dir_path)

  # load saved obs
  if len(obs_list_pkl_paths) > 0:
    print(f"Start reading obs list")
    for obs_list_pkl_path in obs_list_pkl_paths:
      f = open(obs_list_pkl_path, 'rb')
      obs_list = pickle.load(f)
      obs_lists.append(obs_list)
      print(f"Successfully read obs list from [{obs_list_pkl_path}]", '\n' + "--" * 25)
  elif len(obs_list_pkl_paths) == 0 and len(obs_folder_paths) > 0:
    print(f"Start reading obs list from obs folder")
    for obs_folder_path in obs_folder_paths:
      for obs_pkl_name in os.listdir(obs_folder_path):
        obs_pkl_path = os.path.join(obs_folder_path, obs_pkl_name)
        with open(obs_pkl_path, 'rb') as f:
          obs = pickle.load(f)
        obs_list.append(obs)
      print(f"Successfully read obs list from obs folder [{obs_folder_path}]", '\n' + "--" * 25)
      obs_lists.append(obs_list)
      obs_list = []
  else:
    print(f"\033[1;31m No saved obs found! \033[0m", '\n' + "--" * 25)

  # analyse
  for obs_list in obs_lists:
    raw_units_list = []
    for obs in obs_list:
      raw_units = obs.observation.raw_units
      if obs.step_type == environment.StepType.LAST:
        if obs.reward == 1 and obs.discount == 0:
          win += 1
        if obs.reward == 0 and obs.discount == 0:
          tie += 1
        if obs.reward == -1 and obs.discount == 0:
          lose += 1
      raw_units_list.append(raw_units)

    # Generate unit matrix
    episode_all_unit_tags = []
    for raw_units in raw_units_list:
      for unit in raw_units:
        if unit.tag not in episode_all_unit_tags:
          episode_all_unit_tags.append(unit.tag)
    unit_mat = np.zeros((len(episode_all_unit_tags), len(obs_list)))
    for i in range(len(obs_list)):
      raw_units = raw_units_list[i]
      for unit in raw_units:
        tag = unit.tag
        index = episode_all_unit_tags.index(tag)
        unit_mat[index][i] = 1

    # plt.imshow(unit_mat, aspect='equal', cmap='gray')
    # plt.xlabel('Step')
    # plt.ylabel('Unit Index')
    # plt.show()

    lost_units = []
    self_lost_units = []
    enemy_lost_units = []
    self_lost_gas = []
    self_lost_minerals = []
    enemy_lost_gas = []
    enemy_lost_minerals = []

    self_gas_lost = 0
    self_minerals_lost = 0
    enemy_gas_lost = 0
    enemy_minerals_lost = 0

    for index in range(1, len(raw_units_list)):
      obs = raw_units_list[index]
      last_obs = raw_units_list[index - 1]
      tags = [unit.tag for unit in obs]
      for last_unit in last_obs:
        if last_unit.tag not in tags:
          for i in range(index + 1, len(raw_units_list)):
            if last_unit.tag in (d.tag for d in raw_units_list[i]):
              break
          else:
            lost_units.append(last_unit)
            if last_unit.alliance == features.PlayerRelative.SELF:
              print(f"\033[1;31m {units.get_unit_type(last_unit.unit_type).name} lost at step {index} \033[0m")
              self_lost_units.append(last_unit)
              for race in (DATA_PROTOSS, DATA_TERRAN, DATA_ZERG):
                try:
                  self_gas_lost += race[last_unit.unit_type]['produce_cost_gas']
                  self_minerals_lost += race[last_unit.unit_type]['produce_cost_mineral']
                except KeyError:
                  pass
            elif last_unit.alliance == features.PlayerRelative.ENEMY:
              print(f"\033[1;32m {units.get_unit_type(last_unit.unit_type).name} lost at step {index} \033[0m")
              enemy_lost_units.append(last_unit)
              for race in (DATA_PROTOSS, DATA_TERRAN, DATA_ZERG):
                try:
                  enemy_gas_lost += race[last_unit.unit_type]['produce_cost_gas']
                  enemy_minerals_lost += race[last_unit.unit_type]['produce_cost_mineral']
                except KeyError:
                  pass
        self_lost_gas.append(self_gas_lost)
        self_lost_minerals.append(self_minerals_lost)
        enemy_lost_gas.append(enemy_gas_lost)
        enemy_lost_minerals.append(enemy_minerals_lost)

    enemy_total_resource_lost += enemy_gas_lost * 2 + enemy_minerals_lost
    self_total_resource_lost += self_gas_lost * 2 + self_minerals_lost
    # ratio = enemy_resource_lost / self_resource_lost

  return enemy_total_resource_lost, self_total_resource_lost, win, tie, lose


# # print(self_lost_minerals)
#
# plt.subplot(2, 2, 1)
# plt.plot(self_lost_gas, label='Self Gas')
# plt.title('Self Gas Lost')
# plt.xlabel('Step')
# plt.ylabel('Gas')
# plt.legend()
#
# plt.subplot(2, 2, 2)
# plt.plot(self_lost_minerals, label='Self Minerals')
# plt.title('Self Minerals Lost')
# plt.xlabel('Step')
# plt.ylabel('Minerals')
# plt.legend()
#
# plt.subplot(2, 2, 3)
# plt.plot(enemy_lost_gas, label='Enemy Gas')
# plt.title('Enemy Gas Lost')
# plt.xlabel('Step')
# plt.ylabel('Gas')
# plt.legend()
#
# plt.subplot(2, 2, 4)
# plt.plot(enemy_lost_minerals, label='Enemy Minerals')
# plt.title('Enemy Minerals Lost')
# plt.xlabel('Step')
# plt.ylabel('Minerals')
# plt.legend()
#
# plt.tight_layout()
# plt.show()

# print("--" * 50)
# print(f"Self total gas lost: {self_total_gas_lost}")
# print(f"Self total minerals lost: {self_total_minerals_lost}")
# print(f"Enemy total gas lost: {enemy_total_gas_lost}")
# print(f"Enemy total minerals lost: {enemy_total_minerals_lost}")
# print("--" * 50)
# if self_total_gas_lost != 0:
#   print(f"Gas lost ratio: {enemy_total_gas_lost / self_total_gas_lost}")
# if self_total_minerals_lost != 0:
#   print(f"Minerals lost ratio: {enemy_total_minerals_lost / self_total_minerals_lost}")
# print("--" * 50)
# enemy_resource_lost = enemy_total_gas_lost / 4 + enemy_total_minerals_lost / 7
# self_resource_lost = self_total_gas_lost / 4 + self_total_minerals_lost / 7
# print(f"resource lost ratio: {enemy_resource_lost / self_resource_lost}")

start_time = 20240000000000
end_time   = 20250000000000
ave_enemy_lost, ave_self_lost, ave_ratio, rate_win, rate_tie, rate_lose = analyse_all(start_time, end_time)

print("--" * 50)
print(f"ave_enemy_resource_lost = {ave_enemy_lost:.2f} (1 gas for 2 mineral)")
print(f"ave_self_resource_lost = {ave_self_lost:.2f} (1 gas for 2 mineral)")
print(f"ave_ratio = {ave_ratio:.2f}")

print(f"winning_rate = {rate_win:.2f}% (win {rate_win:.2f}% tie {rate_tie:.2f}%, lose {rate_lose:.2f}%)")