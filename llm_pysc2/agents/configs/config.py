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

from llm_pysc2.lib.llm_action import PROTOSS_ACTION_BUILD, \
  PROTOSS_BASIC_ACTION_1, PROTOSS_BASIC_ACTION_2, PROTOSS_BASIC_ACTION_3, \
  PROTOSS_ACTION_WARPTRAIN, PROTOSS_ACTION_TRAIN, PROTOSS_ACTION_RESEARCH, F
from llm_pysc2.lib.llm_client import vision_model_names  #, video_model_names

from pysc2.lib import units
from loguru import logger
import time


def wait(second, log_id, more_info=''):
  for i in range(5):
    logger.warning(f"[ID {log_id}] Experiment will start with UNSAFE settings in {5 - i} seconds. {more_info}")
    time.sleep(1)


class AgentConfig:

  def __init__(self):

    self.race = 'protoss'
    self.model_name = 'YOUR-MODEL-NAME'       # 'gpt-3.5-turbo'
    self.api_base = 'YOUR-API-BASE'           # 'https://hk.xty.app/v1'
    self.api_key = 'YOUR-API-KEY'             # 'xxxxxxxxxxxxxxxxxxxxxxxx....'
    self.temperature = 0.1

    self.basic_prompt = 'default'
    self.translator_o = 'default'
    self.translator_a = 'default'
    self.communicator = 'default'

    self.ENABLE_INIT_STEPS = True
    self.ENABLE_AUTO_WORKER_MANAGE = True
    self.ENABLE_AUTO_WORKER_TRAINING = True
    self.ENABLE_COMMUNICATION = False

    self.ENABLE_IMAGE_RGB = False
    self.ENABLE_IMAGE_FEATURE = False
    self.ENABLE_SAVE_IMAGES = True

    self.LLM_SIMULATION_TIME = 0
    self.MAX_LLM_QUERY_TIMES = 5
    self.MAX_LLM_WAITING_TIME = 15
    self.MAX_LLM_RUNTIME_ERROR_TIME = 45
    self.MAX_LLM_DECISION_FREQUENCY = 1
    self.MAX_NUM_ACTIONS = 3

    self.AGENTS = []
    self.AGENTS_ALWAYS_DISABLE = []

  def reset_llm(self, model_name=None, api_base=None, api_key=None, ENABLE_IMAGE_RGB=None, ENABLE_IMAGE_FEATURE=None):
    if model_name is not None and model_name != 'YOUR-MODEL-NAME':
      self.model_name = model_name
    if api_base is not None and api_base != 'YOUR-API-BASE':
      self.api_base = api_base
    if api_key is not None and api_key != 'YOUR-API-KEY':
      self.api_key = api_key
    if ENABLE_IMAGE_RGB is not None:
      self.ENABLE_IMAGE_RGB = ENABLE_IMAGE_RGB
    if ENABLE_IMAGE_FEATURE is not None:
      self.ENABLE_IMAGE_FEATURE = ENABLE_IMAGE_FEATURE
    if ENABLE_IMAGE_RGB is True and ENABLE_IMAGE_FEATURE is True:
      raise AssertionError("Do not support ENABLE_IMAGE_RGB and ENABLE_IMAGE_FEATURE at the same time, currently")
    for agent_name in self.AGENTS.keys():
      self.AGENTS[agent_name]['llm']['model_name'] = self.model_name
      self.AGENTS[agent_name]['llm']['api_base'] = self.api_base
      self.AGENTS[agent_name]['llm']['api_key'] = self.api_key
      if self.ENABLE_IMAGE_RGB:
        self.AGENTS[agent_name]['llm']['img_rgb'] = True
        self.AGENTS[agent_name]['llm']['img_fea'] = False
      elif self.ENABLE_IMAGE_FEATURE:
        self.AGENTS[agent_name]['llm']['img_rgb'] = False
        self.AGENTS[agent_name]['llm']['img_fea'] = True
      else:
        self.AGENTS[agent_name]['llm']['img_rgb'] = False
        self.AGENTS[agent_name]['llm']['img_fea'] = False

  def auto_check(self, log_id):
    if not isinstance(self.LLM_SIMULATION_TIME, (int, float)) or self.LLM_SIMULATION_TIME <= 0:
      error_in_llm_setting = False
      if self.model_name == '' or self.model_name == 'YOUR-MODEL-NAME':
        self.reset_llm(model_name='gpt-3.5-turbo')
        logger.error(f"[ID {log_id}] No model_name set, please specify model_name in the config.")
        self.LLM_SIMULATION_TIME = 5
        error_in_llm_setting = True
      if self.api_key == '' or self.api_key == 'YOUR-API-KEY':
        logger.error(f"[ID {log_id}] No api_key set, please specify your api_key in the config.")
        self.LLM_SIMULATION_TIME = 5
        error_in_llm_setting = True
      if self.model_name == '' or self.api_key == '':
        self.LLM_SIMULATION_TIME = 5
        error_in_llm_setting = True
      if error_in_llm_setting:
        wait(5, log_id, "(in LLM SIMULATION MODE)")

    if self.ENABLE_IMAGE_RGB or self.ENABLE_IMAGE_FEATURE:
      if self.ENABLE_IMAGE_RGB and self.ENABLE_IMAGE_FEATURE:
        logger.error(f"[ID {log_id}] can not enable config.ENABLE_IMAGE_RGB and config.ENABLE_IMAGE_FEATURE together.")
        AssertionError(f"config.ENABLE_IMAGE_RGB and config.ENABLE_IMAGE_FEATURE can not be True together")
      if self.model_name not in vision_model_names:
        logger.error(f"[ID {log_id}] config.ENABLE_IMAGE_RGB/FEATURE with large models that do not support images.")
        wait(5, log_id)
      if self.model_name in vision_model_names:
        logger.warning(f"[ID {log_id}] You are using a vision model with image obs, this may cost a lot, be cautious.")
        wait(5, log_id)
    else:
      if self.model_name in vision_model_names:
        logger.warning(f"[ID {log_id}] You are using a vision avaliable model without using any image obs.")
        wait(5, log_id)

class ProtossAgentConfig(AgentConfig):

  def __init__(self):
    super(ProtossAgentConfig, self).__init__()

    # Program control parameters in class AgentConfig (above)

    self.AGENTS_ALWAYS_DISABLE = []
    self.AGENTS = {
      'Airborne': {
        'describe': "Protoss airborne commander, controls units airborne/warptrain from WarpPrism. "
                    "Responsible for quick reinforcing nearby units or executing multiline combat.",
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
          {'name': 'Airborne-Zealot-1', 'unit_type': [units.Protoss.Zealot],
           'game_group': -1, 'select_type': 'select_all_type'},  # , 'max_unit_num': {units.Protoss.Zealot: -1}
        ],
        'action': {
          units.Protoss.Zealot: PROTOSS_BASIC_ACTION_2,
        },
      },

      'Builder': {
        'describe': "Protoss builder, controls several Probe. Responsible for build buildings",
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
          {'name': 'Builder-Probe-1', 'unit_type': [units.Protoss.Probe],
           'game_group': -1, 'select_type': 'select'},  # , 'max_unit_num': {units.Protoss.Probe: -1}
        ],
        'action': {
          units.Protoss.Probe: PROTOSS_BASIC_ACTION_2 + PROTOSS_ACTION_BUILD,
        },
      },

      'Commander': {
        'describe': "Protoss military supreme commander. "
                    "Responsible for making macro decision through communication, and controls nexus for massrecall "
                    "for tactical objectives. When make deployment, describe the time, location, and objectives of the "
                    "mission as clearly as possible",
        'llm': {
          'basic_prompt': self.basic_prompt,
          'translator_o': 'commander',
          'translator_a': self.translator_a,
          'img_fea': self.ENABLE_IMAGE_FEATURE,
          'img_rgb': self.ENABLE_IMAGE_RGB,
          'model_name': self.model_name,
          'api_base': self.api_base,
          'api_key': self.api_key,
        },
        'team': [
          {'name': 'Empty', 'unit_type': [],
           'game_group': -1, 'select_type': 'select'},
        ],
        'action': {
          'EmptyGroup': [],
        },
      },

      'Developer': {
        'describe': "Protoss logistics commander. "
                    "Responsible for unit trainning, unit warp trainning, technology upgrade and order the Builder "
                    "to build.",
        'llm': {
          'basic_prompt': self.basic_prompt,
          'translator_o': 'developer',
          'translator_a': self.translator_a,
          'img_fea': self.ENABLE_IMAGE_FEATURE,
          'img_rgb': self.ENABLE_IMAGE_RGB,
          'model_name': self.model_name,
          'api_base': self.api_base,
          'api_key': self.api_key,
        },
        'team': [
          {'name': 'WarpGate-1', 'unit_type': [units.Protoss.WarpGate],
           'game_group': -1, 'select_type': 'select_all_type'},  # , 'max_unit_num': {units.Protoss.WarpGate: -1}
          {'name': 'Empty', 'unit_type': [],
           'game_group': -1, 'select_type': 'select'},
        ],
        'action': {
          units.Protoss.WarpGate: PROTOSS_ACTION_WARPTRAIN,
          'EmptyGroup': PROTOSS_BASIC_ACTION_1 + PROTOSS_ACTION_RESEARCH + PROTOSS_ACTION_TRAIN + [
            {'name': 'Stop_Building_Unit', 'arg': ['tag'],
             'func': [(573, F.llm_pysc2_move_camera, ('world_tag')),
                      (3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
                      (454, F.Stop_Building_quick, ('queued'))]}
          ],
        },
      },

      'Defender': {
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
          # {'name': 'Nexus', 'unit_type': [units.Protoss.Nexus],
          #  'game_group': -1, 'select_type': 'select', 'max_unit_num': {units.Protoss.Nexus: 8}},
          {'name': 'Stalker-1', 'unit_type': [units.Protoss.Stalker],
           'game_group': 1, 'select_type': 'group'},  # , 'max_unit_num': {units.Protoss.Stalker: 8}
        ],
        'action': {
          # units.Protoss.Nexus: [
          #   {'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]},
          #   {'name': 'Select_Workers_Attack_Screen', 'arg': ['screen'],
          #    'func': [(12, F.Attack_screen, ('queued', 'screen'))]},
          #   {'name': 'Select_Workers_Move_Screen', 'arg': ['screen'],
          #    'func': [(331, F.Move_screen, ('queued', 'screen'))]},
          # ],
          units.Protoss.Stalker: PROTOSS_BASIC_ACTION_2 + [
            {'name': 'Ability_Blink_Screen', 'arg': ['screen'],
             'func': [(180, F.Effect_Blink_screen, ('queued', 'screen'))]},
            {'name': 'Select_Unit_Blink_Screen', 'arg': ['tag', 'screen'],
             'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
                      (180, F.Effect_Blink_screen, ('now', 'screen'))]},
          ]
        },
      },

      'CombatGroup0': {
        'describe': "Protoss frontline commander, controls several Zealots. "
                    "Responsible for providing cover for the main force and executing multi line combat.",
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
          {'name': 'Zealot-1', 'unit_type': [units.Protoss.Zealot],
           'game_group': 2, 'select_type': 'group'},  # , 'max_unit_num': {units.Protoss.Zealot: -1}, -1 for unlimited
          {'name': 'Zealot-2', 'unit_type': [units.Protoss.Zealot],
           'game_group': 3, 'select_type': 'group'},  # , 'max_unit_num': {units.Protoss.Zealot: -1}, -1 for unlimited
        ],
        'action': {
          units.Protoss.Zealot: PROTOSS_BASIC_ACTION_2,
        },
      },

      'CombatGroup1': {
        'describe': "Protoss frontline commander, controls several Stalkers. "
                    "Responsible for providing cover for the main force and restraining enemy forces.",
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
          {'name': 'Stalker-3', 'unit_type': [units.Protoss.Stalker],
           'game_group': 6, 'select_type': 'group'},
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

      'CombatGroup2': {
        'describe': "Protoss frontline commander, controls ground main force such as Immortal, Colossus and Archon. "
                    "Responsible for frontal combat.",
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
          {'name': 'Immortal-1', 'unit_type': [units.Protoss.Immortal],
           'game_group': -1, 'select_type': 'select_all_type'},
          # {'name': 'Immortal-2', 'unit_type': [units.Protoss.Immortal],
          #  'game_group': -1, 'select_type': 'select_all_type'},  # more than 1 select_all_type not currently supported
          {'name': 'Colossus-1', 'unit_type': [units.Protoss.Colossus],
           'game_group': -1, 'select_type': 'select_all_type'},
          # {'name': 'Colossus-2', 'unit_type': [units.Protoss.Colossus],
          #  'game_group': -1, 'select_type': 'select_all_type'},  # more than 1 select_all_type not currently supported
          {'name': 'Archon-1', 'unit_type': [units.Protoss.Archon],
           'game_group': -1, 'select_type': 'select_all_type'},
          # {'name': 'Archon-2', 'unit_type': [units.Protoss.Archon],
          #  'game_group': -1, 'select_type': 'select_all_type'},  # more than 1 select_all_type not currently supported
        ],
        'action': {
          units.Protoss.Immortal: PROTOSS_BASIC_ACTION_2,
          units.Protoss.Colossus: PROTOSS_BASIC_ACTION_2,
          units.Protoss.Archon: PROTOSS_BASIC_ACTION_2,
        },
      },

      'CombatGroup3': {
        'describe': "Protoss frontline commander, controls air main force such as VoidRay, Carrier and Tempest. "
                    "Responsible for frontal combat.",
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
          {'name': 'VoidRay-1', 'unit_type': [units.Protoss.VoidRay],
           'game_group': -1, 'select_type': 'select_all_type'},
          # {'name': 'VoidRay-2', 'unit_type': [units.Protoss.VoidRay],
          #  'game_group': -1, 'select_type': 'select_all_type'},  # more than 1 select_all_type not currently supported
          {'name': 'Carrier-1', 'unit_type': [units.Protoss.Carrier],
           'game_group': -1, 'select_type': 'select_all_type'},
          # {'name': 'Carrier-2', 'unit_type': [units.Protoss.Carrier],
          #  'game_group': -1, 'select_type': 'select_all_type'},  # more than 1 select_all_type not currently supported
          {'name': 'Tempest-1', 'unit_type': [units.Protoss.Tempest],
           'game_group': -1, 'select_type': 'select_all_type'},
          # {'name': 'Tempest-2', 'unit_type': [units.Protoss.Tempest],
          #  'game_group': -1, 'select_type': 'select_all_type'},  # more than 1 select_all_type not currently supported
        ],
        'action': {
          units.Protoss.Carrier: PROTOSS_BASIC_ACTION_2,
          units.Protoss.Tempest: PROTOSS_BASIC_ACTION_2,
          units.Protoss.VoidRay: PROTOSS_BASIC_ACTION_2 + [
            {'name': 'Ability_PrismaticAlignment', 'arg': [],
             'func': [(244, F.Effect_VoidRayPrismaticAlignment_quick, ('queued'))]},
          ],
        },
      },

      'CombatGroup4': {
        'describe': "Protoss reconnaissance commander, controls Observer and several Probe. "
                    "Responsible for providing reconnaissance infomation and detect cloak unit for main force",
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
          {'name': 'Probe', 'unit_type': [units.Protoss.Probe],
           'game_group': -1, 'select_type': 'select'},
          {'name': 'Observer', 'unit_type': [units.Protoss.Observer, units.Protoss.ObserverSurveillanceMode],
           'game_group': -1, 'select_type': 'select'},
        ],
        'action': {
          units.Protoss.Probe: PROTOSS_BASIC_ACTION_2 + [
            {'name': 'Lock_Nexus_Near', 'arg': ['tag'],
             'func': [(70, F.Build_Pylon_screen, ('queued', 'screen_tag'))]},
            {'name': 'Lock_Assimilator_Near', 'arg': ['tag'],
             'func': [(40, F.Build_Assimilator_screen, ('queued', 'screen_tag'))]},
          ],
          units.Protoss.Observer: PROTOSS_BASIC_ACTION_3 + [
            {'name': 'Morph_SurveillanceMode', 'arg': [],
             'func': [(538, F.Morph_SurveillanceMode_quick, ('queued'))]},
          ],
          units.Protoss.ObserverSurveillanceMode: [
            {'name': 'Continuously_Monitor_Here', 'arg': [],
             'func': [(0, F.no_op, ())]},
            {'name': 'Morph_ObserverMode', 'arg': [],
             'func': [(535, F.Morph_ObserverMode_quick, ('queued'))]},
          ],
        },
      },

      'CombatGroup5': {
        'describe': "Protoss AOE commander, controls HighTemplar and Disruptor. "
                    "Responsible for dealing high damage to clustered enemies",
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
          {'name': 'HighTemplar-1', 'unit_type': [units.Protoss.HighTemplar],
           'game_group': 7, 'select_type': 'group'},
          {'name': 'Disruptor-1', 'unit_type': [units.Protoss.Disruptor],
           'game_group': 8, 'select_type': 'group'},
        ],
        'action': {
          units.Protoss.HighTemplar: PROTOSS_BASIC_ACTION_2 + [
            {'name': 'Ability_PsiStorm_Screen', 'arg': ['screen'],
             'func': [(218, F.Effect_PsiStorm_screen, ('queued', 'screen'))]},
            {'name': 'Ability_PsiStorm_Attack_Unit', 'arg': ['tag'],
             'func': [(218, F.Effect_PsiStorm_screen, ('queued', 'screen_tag'))]},
            {'name': 'Morph_Archon', 'arg': [],
             'func': [(296, F.Morph_Archon_quick, ('queued'))]},
            {'name': 'Select_Two_Unit_Morph_Archon', 'arg': ['tag', 'tag'],
             'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
                      (3, F.select_rect, ('add', 'screen1_tag2', 'screen2_tag2')),
                      (296, F.Morph_Archon_quick, ('queued'))]},
          ],
          units.Protoss.Disruptor: PROTOSS_BASIC_ACTION_3 + [
            {'name': 'Ability_PurificationNova_Attack_Unit', 'arg': ['tag'],
             'func': [(219, F.Effect_PurificationNova_screen, ('queued', 'screen_tag'))]},
          ],
          # units.Protoss.DisruptorPhased: PROTOSS_BASIC_ACTION_2,
        },
      },

      'CombatGroup6': {
        'describe': "Protoss tactical support commander, controls Sentry and Mothership. "
                      "Responsible for providing tactical support by using skills",
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
          {'name': 'Sentry-1', 'unit_type': [units.Protoss.Sentry],
           'game_group': 9, 'select_type': 'group'},
          {'name': 'Mothership', 'unit_type': [units.Protoss.Mothership],
           'game_group': -1, 'select_type': 'select'}
        ],
        'action': {
          units.Protoss.Sentry: PROTOSS_BASIC_ACTION_2 + [
            {'name': 'Ability_ForceField_Screen', 'arg': ['screen'],
             'func': [(193, F.Effect_ForceField_screen, ('queued', 'screen'))]},
            {'name': 'Ability_GuardianShield', 'arg': [],
             'func': [(197, F.Effect_GuardianShield_quick, ('queued'))]},
            # # Hallucination not supported in pysc2
            # {'name': 'Hallucination_Adept',             'arg': [],
            #  'func': [(248, F.Hallucination_Adept_quick, ('queued'))]},
            # {'name': 'Hallucination_Archon',            'arg': [],
            #  'func': [(249, F.Hallucination_Archon_quick, ('queued'))]},
            # {'name': 'Hallucination_Colossus',          'arg': [],
            #  'func': [(250, F.Hallucination_Colossus_quick, ('queued'))]},
            # {'name': 'Hallucination_Disruptor',         'arg': [],
            #  'func': [(251, F.Hallucination_Disruptor_quick, ('queued'))]},
            # {'name': 'Hallucination_HighTemplar',       'arg': [],
            #  'func': [(252, F.Hallucination_HighTemplar_quick, ('queued'))]},
            # {'name': 'Hallucination_Immortal',          'arg': [],
            #  'func': [(253, F.Hallucination_Immortal_quick, ('queued'))]},
            # {'name': 'Hallucination_Oracle',            'arg': [],
            #  'func': [(254, F.Hallucination_Oracle_quick, ('queued'))]},
            # {'name': 'Hallucination_Phoenix',           'arg': [],
            #  'func': [(255, F.Hallucination_Phoenix_quick, ('queued'))]},
            # {'name': 'Hallucination_Probe',             'arg': [],
            #  'func': [(256, F.Hallucination_Probe_quick, ('queued'))]},
            # {'name': 'Hallucination_Stalker',           'arg': [],
            #  'func': [(257, F.Hallucination_Stalker_quick, ('queued'))]},
            # {'name': 'Hallucination_VoidRay',           'arg': [],
            #  'func': [(258, F.Hallucination_VoidRay_quick, ('queued'))]},
            # {'name': 'Hallucination_WarpPrism',         'arg': [],
            #  'func': [(259, F.Hallucination_WarpPrism_quick, ('queued'))]},
            # {'name': 'Hallucination_Zealot',            'arg': [],
            #  'func': [(260, F.Hallucination_Zealot_quick, ('queued'))]},
          ],
          units.Protoss.Mothership: PROTOSS_BASIC_ACTION_3 + [
            # Ability_CloakingField not supported in pysc2
            # Ability_MothershipMassRecall not neccessary in simple combat tasks
            # {'name': 'Ability_MothershipMassRecall_Near', 'arg': ['tag'],
            #  'func': [(573, F.llm_pysc2_move_camera, ('world_tag')), (208, F.Effect_MassRecall_screen, ('queued', 'screen_tag'))]},
            {'name': 'Ability_TimeWarp_Attack', 'arg': ['tag'],
             'func': [(241, F.Effect_TimeWarp_screen, ('queued', 'screen_tag'))]},
            {'name': 'Ability_TimeWarp_Screen', 'arg': ['screen'],
             'func': [(241, F.Effect_TimeWarp_screen, ('queued', 'screen'))]},
          ],
        },
      },

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
        'team': [
          {'name': 'Adept-1', 'unit_type': [units.Protoss.Adept],
           'game_group': -1, 'select_type': 'select_all_type'},
          {'name': 'AdeptPhase-1', 'unit_type': [units.Protoss.AdeptPhaseShift],
           'game_group': -1, 'select_type': 'select_all_type'},
          {'name': 'DarkTemplar-1', 'unit_type': [units.Protoss.DarkTemplar],
           'game_group': -1, 'select_type': 'select_all_type'},
          # {'name': 'DarkTemplar-2', 'unit_type': [units.Protoss.DarkTemplar],
          #  'game_group': -1, 'select_type': 'select_all_type'},  # more than one select_all_type not currently supported
        ],
        'action': {
          units.Protoss.AdeptPhaseShift: PROTOSS_BASIC_ACTION_3,
          units.Protoss.Adept: PROTOSS_BASIC_ACTION_2 + [
            {'name': 'Ability_AdeptPhaseShift_Screen', 'arg': ['screen'],
             'func': [(177, F.Effect_AdeptPhaseShift_screen, ('queued', 'screen'))]},
            {'name': 'Ability_AdeptPhaseShift_Minimap', 'arg': ['minimap'],
             'func': [(547, F.Effect_AdeptPhaseShift_minimap, ('queued', 'minimap'))]},
            {'name': 'Ability_CancelPhaseShift', 'arg': [], 'func': [(141, F.Cancel_AdeptPhaseShift_quick, ('queued'))]},
          ],
          units.Protoss.DarkTemplar: PROTOSS_BASIC_ACTION_2 + [
            {'name': 'Ability_ShadowStride_Unit', 'arg': ['tag'],
             'func': [(182, F.Effect_ShadowStride_screen, ('queued', 'screen_tag'))]},
            {'name': 'Morph_Archon', 'arg': [],
             'func': [(296, F.Morph_Archon_quick, ('queued'))]},
            {'name': 'Select_Two_Unit_Morph_Archon', 'arg': ['tag', 'tag'],
             'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
                      (3, F.select_rect, ('add', 'screen1_tag2', 'screen2_tag2')),  # screen1/2_tag2 not realized yet
                      (296, F.Morph_Archon_quick, ('queued'))]},
          ],
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
        'team': [
          {'name': 'Oracle-1', 'unit_type': [units.Protoss.Oracle],
           'game_group': -1, 'select_type': 'select_all_type'},
          {'name': 'Phoenix-1', 'unit_type': [units.Protoss.Phoenix],
           'game_group': -1, 'select_type': 'select_all_type'},
        ],
        'action': {
          units.Protoss.Oracle: PROTOSS_BASIC_ACTION_2 + [
            {'name': 'Ability_PulsarBeamOn', 'arg': [],
             'func': [(38, F.Behavior_PulsarBeamOn_quick, ('queued'))]},
            {'name': 'Ability_OracleRevelation_Screen', 'arg': ['screen'],
             'func': [(214, F.Effect_OracleRevelation_screen, ('queued', 'screen'))]},
            {'name': 'Build_StasisTrap_Screen', 'arg': ['screen'],
             'func': [(90, F.Build_StasisTrap_screen, ('queued', 'screen'))]},
            {'name': 'Select_Unit_Ability_PulsarBeamOn', 'arg': ['tag'],
             'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
                      (38, F.Behavior_PulsarBeamOn_quick, ('queued'))]},
            {'name': 'Select_Unit_OracleRevelation_Screen', 'arg': ['tag', 'screen'],
             'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
                      (214, F.Effect_OracleRevelation_screen, ('queued', 'screen'))]},
            {'name': 'Select_Unit_Build_StasisTrap_Screen', 'arg': ['tag', 'screen'],
             'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
                      (90, F.Build_StasisTrap_screen, ('queued', 'screen'))]},
          ],
          units.Protoss.Phoenix: PROTOSS_BASIC_ACTION_2 + [
            {'name': 'Ability_GravitonBeam_Unit', 'arg': ['tag'],
             'func': [(196, F.Effect_GravitonBeam_screen, ('queued', 'screen_tag'))]},
            {'name': 'Select_Unit_Ability_GravitonBeam_Unit', 'arg': ['tag', 'tag'],
             'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
                      (196, F.Effect_GravitonBeam_screen, ('queued', 'screen_tag2'))]},
          ],
        },
      },

      'CombatGroup9': {
        'describe': "Protoss airborne commander, controls WarpPrism and airborne units like Zealots, Stalkers."
                    "Responsible for supplement troops on the front line, or executing multi line combat. "
                    "Keep stability as much as possible in WarpRismPhashing mode to provide stable power field for "
                    "unit warpping.",
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
          {'name': 'WarpPrism', 'unit_type': [units.Protoss.WarpPrism, units.Protoss.WarpPrismPhasing],
           'game_group': -1, 'select_type': 'select'},
        ],
        'action': {
          units.Protoss.WarpPrism: PROTOSS_BASIC_ACTION_3 + [
            {'name': 'Morph_WarpPrismPhasingMode', 'arg': [],
             'func': [(329, F.Morph_WarpPrismPhasingMode_quick, ('queued'))]},
            {'name': 'Load_Unit', 'arg': ['tag'], 'func': [(287, F.Load_screen, ('queued', 'screen_tag'))]},
            {'name': 'Unload_Screen', 'arg': ['screen'],
             'func': [(516, F.UnloadAllAt_screen, ('queued', 'screen'))]},
          ],
          units.Protoss.WarpPrismPhasing: [
            {'name': 'Wait_For_Unit_Warp', 'arg': [], 'func': [(0, F.no_op, ())]},
            {'name': 'Morph_WarpPrismTransportMode', 'arg': [],
             'func': [(330, F.Morph_WarpPrismTransportMode_quick, ('queued'))]},
          ],
        },
      },
    }


# TerranAgentConfig part undergoing
class TerranAgentConfig(AgentConfig):
  def __init__(self):
    super(TerranAgentConfig, self).__init__()


# ZergAgentConfig part undergoing
class ZergAgentConfig(AgentConfig):
  def __init__(self):
    super(ZergAgentConfig, self).__init__()
