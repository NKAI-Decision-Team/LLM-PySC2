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

from llm_pysc2.cfg.config import ProtossAgentConfig
from llm_pysc2.lib.action.space import *
from pysc2.lib import units


class ConfigPysc2_Harass(ProtossAgentConfig):

  def __init__(self):
    super(ConfigPysc2_Harass, self).__init__()
    self.AGENTS_ALWAYS_DISABLE = [
      'Airborne', 'Builder', 'Commander', 'Developer', 'Defender', 'CombatGroup4',
    ]
    self.ENABLE_INIT_STEPS = False
    self.ENABLE_AUTO_WORKER_MANAGE = False
    self.ENABLE_AUTO_WORKER_TRAINING = False

    # self.LLM_SIMULATION_TIME = 0
    # self.MAX_LLM_QUERY_TIMES = 5
    # self.MAX_LLM_WAITING_TIME = 10
    # self.MAX_LLM_RUNTIME_ERROR_TIME = 30
    # self.MAX_LLM_DECISION_FREQUENCY = 2
    # self.MAX_NUM_ACTIONS = 3

    self.AGENTS = {
      'CombatGroup7': {
        'describe': "Protoss special force commander, controls Adept and DarkTemplar. "
                    "Responsible for infiltrating the enemy's rear and disrupt economic production, sometimes "
                    "collecting reconnaissance infomation, participating in frontline combat.",
        'llm': {
          'basic_prompt': self.basic_prompt,
          'translator_o': self.translator_o,
          'translator_a': self.translator_a,
          'img_fea': self.ENABLE_IMAGE_FEATURE,
          'img_rgb': self.ENABLE_IMAGE_RGB,
          'model_name': self.model_name,
          'api_base': self.api_base,
          'api_key': self.api_key,
        },
        'team': {
          'Adept-1': {
            'name': 'Adept-1', 'unit_type': [units.Protoss.Adept], 'game_group': 1, 'select_type': 'group',
            'actions': {units.Protoss.Adept: STANDARD_ACTION_ADEPT}},
          'AdeptPhase-1': {
            'name': 'AdeptPhase-1', 'unit_type': [units.Protoss.AdeptPhaseShift], 'game_group': 2, 'select_type': 'select_all_type',
            'actions': {units.Protoss.AdeptPhaseShift: PROTOSS_BASIC_ACTION_3}},
          'DarkTemplar-1': {
            'name': 'DarkTemplar-1', 'unit_type': [units.Protoss.DarkTemplar], 'game_group': -1, 'select_type': 'select_all_type',
            'actions': {units.Protoss.DarkTemplar: STANDARD_ACTION_DARKTEMPLAR}},
        },
      },

      'CombatGroup8': {
        'describe': "Protoss air special force commander, controls Oracle and Phoenix. "
                    "Responsible for infiltrating the enemy's rear and disrupt economic production, sometimes "
                    "collecting reconnaissance infomation, participating in frontline combat, or build StasisTrap "
                    "to block the enemy's main force.",
        'llm': {
          'basic_prompt': self.basic_prompt,
          'translator_o': self.translator_o,
          'translator_a': self.translator_a,
          'img_fea': self.ENABLE_IMAGE_FEATURE,
          'img_rgb': self.ENABLE_IMAGE_RGB,
          'model_name': self.model_name,
          'api_base': self.api_base,
          'api_key': self.api_key,
        },
        'team': {
          'Oracle-1': {
            'name': 'Oracle-1', 'unit_type': [units.Protoss.Oracle], 'game_group': 3, 'select_type': 'group',
            'actions': {units.Protoss.Oracle: STANDARD_ACTION_ORACLE}},
          'Phoenix-1': {
            'name': 'Phoenix-1', 'unit_type': [units.Protoss.Phoenix], 'game_group': 4, 'select_type': 'group',
            'actions': {units.Protoss.Phoenix: STANDARD_ACTION_PHOENIX}},
        },
      }
    }