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

from llm_pysc2.agents.configs.config import ProtossAgentConfig
from llm_pysc2.lib.llm_action import *


class ConfigSmac_2s(ProtossAgentConfig):

  def __init__(self):
    super(ConfigSmac_2s, self).__init__()
    self.ENABLE_INIT_STEPS = False
    self.ENABLE_AUTO_WORKER_MANAGE = False
    self.ENABLE_AUTO_WORKER_TRAINING = False

    # self.LLM_SIMULATION_TIME = 0
    # self.MAX_LLM_QUERY_TIMES = 5
    # self.MAX_LLM_WAITING_TIME = 10
    # self.MAX_LLM_RUNTIME_ERROR_TIME = 30
    # self.MAX_LLM_DECISION_FREQUENCY = 1
    # self.MAX_NUM_ACTIONS = 3

    self.AGENTS_ALWAYS_DISABLE = []
    self.AGENTS = {
      'CombatGroupSmac': {
        'describe': "Protoss military commander, controls units to fight against enemy. ",
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
        'team': [
          {'name': 'Stalker-1', 'unit_type': [units.Protoss.Stalker],
           'game_group': 4, 'select_type': 'group'},
          {'name': 'Stalker-2', 'unit_type': [units.Protoss.Stalker],
           'game_group': 5, 'select_type': 'group'},
        ],
        'action': {
          units.Protoss.Stalker: PROTOSS_BASIC_ACTION_SMAC2,
        },
      },
    }
