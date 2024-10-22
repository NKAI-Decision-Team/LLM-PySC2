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
import shutil

from pysc2.env import environment

# analyse one experiment folder
def analyse(experiment_folder, delete_unfinished):
  win, tie, lose = 0, 0, 0
  score_cumulative = None
  score_by_category = None
  score_by_vital = None
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

    if len(obs_list) > 0 and obs_list[-1].step_type != environment.StepType.LAST:  # unfinished experiment
      print("Possible unfinished experiment")
      if delete_unfinished:
        shutil.rmtree(experiment_folder)
      continue

    for obs in obs_list:
      raw_units = obs.observation.raw_units
      raw_units_list.append(raw_units)
      if obs.step_type == environment.StepType.LAST:
        if obs.reward == 1 and obs.discount == 0:
          win += 1
        if obs.reward == 0 and obs.discount == 0:
          tie += 1
        if obs.reward == -1 and obs.discount == 0:
          lose += 1
        score_c = obs.observation.score_cumulative
        score_bc = obs.observation.score_by_category
        score_bv = obs.observation.score_by_vital
        score_cumulative = score_c if score_cumulative is None else score_cumulative + score_c
        score_by_category = score_bc if score_by_category is None else score_by_category + score_bc
        score_by_vital = score_bv if score_by_vital is None else score_by_vital + score_bv

  return score_cumulative, score_by_category, score_by_vital, win, tie, lose


# analyse all experiment folder in llm_log
def analyse_all(start_time: int, end_time=0, delete_unfinished=False):
  num_experiments = 0
  total_score_cumulative, total_score_by_category, total_score_by_vital = None, None, None
  total_damage_dealt, total_damage_taken, total_healed = 0, 0, 0
  total_killed_minerals, total_killed_vespene = 0, 0
  total_lost_minerals, total_lost_vespene = 0, 0
  total_win, total_tie, total_lose = 0, 0, 0

  log_folder_names = os.listdir(os.path.dirname(os.path.abspath(__file__)))
  for folder_name in log_folder_names:

    if '-' in folder_name and start_time <= int(folder_name.split('-')[0]) <= max(end_time, start_time + 1):
      experiment_folder = f'./{folder_name}'
      score_cumulative, score_by_category, score_by_vital, win, tie, lose = analyse(experiment_folder, delete_unfinished)

      if total_score_cumulative is None:
        total_score_cumulative = score_cumulative
        total_score_by_category = score_by_category
        total_score_by_vital = score_by_vital
      elif (score_cumulative is not None) and (score_by_category is not None) and (score_by_vital is not None):
        total_score_cumulative += score_cumulative
        total_score_by_category += score_by_category
        total_score_by_vital += score_by_vital
      else:
        continue
      num_experiments = num_experiments + win + tie + lose
      total_win += win
      total_tie += tie
      total_lose += lose

  if num_experiments > 0:
    print(f"num_experiments={num_experiments}")
    print("--" * 25)

    total_damage_dealt = total_score_by_vital[0][0] + total_score_by_vital[0][1]
    total_damage_taken = total_score_by_vital[1][0] + total_score_by_vital[1][1]
    total_healed = total_score_by_vital[2][0] + total_score_by_vital[2][1]

    total_killed_minerals = total_score_by_category.killed_minerals.army + total_score_by_category.killed_minerals.economy
    total_killed_vespene = total_score_by_category.killed_vespene.army + total_score_by_category.killed_vespene.economy
    total_lost_minerals = total_score_by_category.lost_minerals.army + total_score_by_category.lost_minerals.economy
    total_lost_vespene = total_score_by_category.lost_vespene.army + total_score_by_category.lost_vespene.economy

    total_killed_resource = total_killed_minerals + 2 * total_killed_vespene
    total_lost_resource = total_lost_minerals + 2 * total_lost_vespene

    rate_win = 100 * total_win / num_experiments
    rate_tie = 100 * total_tie / num_experiments
    rate_lose = 100 * total_lose / num_experiments
    ave_damage_dealt = total_damage_dealt / num_experiments
    ave_damage_taken = total_damage_taken / num_experiments
    ave_healed = total_healed / num_experiments
    ave_killed_resource = total_killed_resource / num_experiments
    ave_lost_resource = total_lost_resource / num_experiments
    ave_kill_death_ratio = ave_killed_resource / ave_lost_resource if ave_lost_resource != 0 else None

    result = {
      'rate_win': rate_win,
      'rate_tie': rate_tie,
      'rate_lose': rate_lose,
      'ave_damage_dealt': ave_damage_dealt,
      'ave_damage_taken': ave_damage_taken,
      'ave_healed': ave_healed,
      'ave_killed_resource': ave_killed_resource,
      'ave_lost_resource': ave_lost_resource,
      'ave_kill_death_ratio': ave_kill_death_ratio,
    }

    return result
  else:
    print(f"\033[1;31m Error num_experiments == 0! \033[0m")
    return None


start_time = 20240000000000
end_time   = 20250000000000
result = analyse_all(start_time, end_time)

from pprint import pprint
pprint(result)