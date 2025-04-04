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


class DataRecorder():
  def __init__(self, save_dir, save_level=0):
    """
    Args:
      save_dir:
        MainAgent.log_dir_path
      save_level:
        0 for only first and last step,
        1 for important steps that unit changes,
        2 add obs that action may be important,
        3 for all obs
    """
    self.obs_list = []
    self.save_dir = save_dir
    # save_level:
    self.save_level = save_level
    self.last_step_unit_tags = []
    if not os.path.exists(self.save_dir):
      os.mkdir(self.save_dir)

  def _save_temp(self, obs, num_episode, num_step):
    self.obs_list.append(obs)
    save_dir_temp = f"{self.save_dir}/obs{num_episode}"
    obs_save_path = f"{save_dir_temp}/step{num_step}.pkl"
    if not os.path.exists(save_dir_temp):
      os.mkdir(save_dir_temp)
    with open(obs_save_path, 'wb') as f:
        pickle.dump(obs, f)

  def _save_all(self, obs, num_episode):
    result = ''

    if obs.step_type == environment.StepType.LAST:
      if obs.reward == 1 and obs.discount == 0:
        result = '-win'
      if obs.reward == 0 and obs.discount == 0:
        result = '-tie'
      if obs.reward == -1 and obs.discount == 0:
        result = '-lose'
    obs_save_path = f"{self.save_dir}/obs-list-episode{num_episode}{result}.pkl"
    with open(obs_save_path, 'wb') as f:
      pickle.dump(self.obs_list, f)
      print(f"Successfully save episode obs in {obs_save_path}")
    try:  # To avoid errors caused by insufficient permissions
      save_dir_temp = f"{self.save_dir}/obs{num_episode}"
      shutil.rmtree(save_dir_temp)
      print(f"Successfully delete temp obs directory")
    except:
      pass

  def _is_unit_appear_or_disappear(self, obs):
    step_unit_tags = []
    unit_appear_or_disappear = False
    for unit in obs.observation.raw_units:
      step_unit_tags.append(unit.tag)
      if unit.tag not in self.last_step_unit_tags:
        unit_appear_or_disappear = True
    if len(step_unit_tags) != len(self.last_step_unit_tags):
      unit_appear_or_disappear = True
    self.last_step_unit_tags = step_unit_tags
    return unit_appear_or_disappear

  def step(self, obs, num_episode, num_step):
    if obs.step_type == environment.StepType.MID:
      if self.save_level >= 0:
        pass
      if self.save_level >= 1 and self._is_unit_appear_or_disappear(obs):
        self._save_temp(obs, num_episode, num_step)
      if self.save_level >= 2 and 9 < obs.observation.last_actions[0] < 573:
        self._save_temp(obs, num_episode, num_step)
      if self.save_level >= 3:
        self._save_temp(obs, num_episode, num_step)
    if obs.step_type == environment.StepType.FIRST:
      self.obs_list = []
      self._save_temp(obs, num_episode, num_step)
    if obs.step_type == environment.StepType.LAST:
      self._save_temp(obs, num_episode, num_step)
      self._save_all(obs, num_episode)
