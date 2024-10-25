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


class ConfigPysc2_Defend(ProtossAgentConfig):

  def __init__(self):
    super(ConfigPysc2_Defend, self).__init__()
    self.AGENTS_ALWAYS_DISABLE = [
      'Airborne', 'Builder', 'Commander', 'Developer', 'Defender',
      'CombatGroup0', '            ', 'CombatGroup2', 'CombatGroup3', 'CombatGroup4',
      'CombatGroup5', 'CombatGroup6', 'CombatGroup7', 'CombatGroup8', 'CombatGroup9'
    ]  # CombatGroup1
    self.ENABLE_INIT_STEPS = False
    self.ENABLE_AUTO_WORKER_MANAGE = False
    self.ENABLE_AUTO_WORKER_TRAINING = False

    # self.LLM_SIMULATION_TIME = 0
    # self.MAX_LLM_QUERY_TIMES = 5
    # self.MAX_LLM_WAITING_TIME = 10
    # self.MAX_LLM_RUNTIME_ERROR_TIME = 30
    # self.MAX_LLM_DECISION_FREQUENCY = 1
    # self.MAX_NUM_ACTIONS = 3

    self.AGENTS = {
      'CombatGroup1': {
        'describe': "Protoss garrison troops commander, controls several Stalkers. "
                    "Responsible for intercepting enemy infiltrating forces.",
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
        ],
        'action': {
          units.Protoss.Stalker: PROTOSS_BASIC_ACTION_2 + [
            {'name': 'Ability_Blink_Screen', 'arg': ['screen'],
             'func': [(180, F.Effect_Blink_screen, ('queued', 'screen'))]},
            {'name': 'Select_Unit_Blink_Screen', 'arg': ['tag', 'screen'],
             'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
                      (180, F.Effect_Blink_screen, ('now', 'screen'))]},
          ]
        },
      },
    }
