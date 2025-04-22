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


from llm_pysc2.lib.obs.info import *
from loguru import logger


class BaseTranslatorO:

  def __init__(self, name, log_id, config):
    self.agent_name = name
    self.log_id = log_id
    self.config = config
    self.loop_step = -1
    self.states = []
    self.state = {}
    self.size_screen = None
    self.size_minimap = None
    self.final_prompt = ''

  def obs_list_safe(self, agent):
    obs_list = agent.team_unit_obs_list
    return False if not isinstance(obs_list, list) or len(obs_list) < 1 else True

  def translate(self, agent) -> str:
    if not self.obs_list_safe(agent):
      return f"obs_list error, no obs found"

    self.state = {
      'game_info': get_game_info(agent),
      'units_info': get_teams_info(agent),
      'event_info': get_event_info(agent),
      'knowledge_info': get_relevant_knowledge(agent),
      'valid_actions': get_valid_actions(agent),
      'valid_args_explanation': get_valid_action_args_explanation(agent),
      'last_action_info': get_last_action_info(agent),
      'last_action_error_info': get_action_error_info(agent),
      'upgrades_info': get_upgrades_info(agent),
      'task_info': get_task_info(agent),
      'final_prompt': self.final_prompt,
    }

    if agent.config.ENABLE_COMMUNICATION:
      # self.state['communication_info'] = get_communication_info(agent)
      self.state['communication_input'] = agent.last_text_c_inp
      self.state['communication_target'] = agent.last_text_c_tar + '\n\n'
    else:
      self.state['communication_input'] = ''
      self.state['communication_target'] = ''

    if self.loop_step != agent.main_loop_step:
      self.loop_step = agent.main_loop_step
      self.states.append(self.state)

    return ''


class CombatGroupTranslatorO(BaseTranslatorO):

  def __init__(self, name, log_id, config):
    super(CombatGroupTranslatorO, self).__init__(name, log_id, config)
    if config.ENABLE_COMMUNICATION:
      self.final_prompt = f"Give each team no more than {config.MAX_NUM_ACTIONS} actions, " \
                          f"these actions will be executed in the following {round(1 / config.MAX_LLM_DECISION_FREQUENCY, 2)} seconds, " \
                          f"among which activity release should usually before attack and move." \
                          f"\nNow, start generating your analysis, strategy, actions and communication:"
    else:
      self.final_prompt = f"Give each team no more than {config.MAX_NUM_ACTIONS} actions, " \
                          f"these actions will be executed in the following {round(1 / config.MAX_LLM_DECISION_FREQUENCY, 2)} seconds, " \
                          f"among which activity release should usually before attack and move." \
                          f"\nNow, start generating your analysis, strategy and actions:"
    logger.info(f"[ID {log_id}] {name} CombatGroupTranslatorO initialized")

  def translate(self, agent) -> str:
    super(CombatGroupTranslatorO, self).translate(agent)
    if not self.obs_list_safe(agent):
      return f"obs_list error, no obs found"

    # observation and relevant info
    self.text_obs = self.state['game_info'] + self.state['units_info'] + self.state['event_info'] + \
                    self.state['valid_actions'] + self.state['valid_args_explanation'] + self.state['last_action_info']
                    # self.state['last_action_error_info']  #  + self.state['knowledge_info']
    self.text_task = self.state['communication_input'] + self.state['communication_target'] + self.state['task_info']
    self.text_prompt = self.text_obs + self.text_task + self.final_prompt

    text_o = self.text_prompt
    return text_o


class CommanderTranslatorO(BaseTranslatorO):

  def __init__(self, name, log_id, config):
    super(CommanderTranslatorO, self).__init__(name, log_id, config)
    if config.ENABLE_COMMUNICATION:
      self.final_prompt = f"As the supreme military commander, you should not directly give actions, " \
                          f"instead, tell your subordinates what to do through communication." \
                          f"\nNow, start analysis, making macro decisions in military deployments by sending message to other agents:"
    else:
      logger.warning(f"[ID {self.log_id}] {self.agent_name} CommanderTranslatorO: Commander can not communicate with other agents due to agent.config.ENABLE_COMMUNICATION=False")
      self.final_prompt = f"As the supreme military commander, you should not directly give actions, " \
                          f"instead, tell your subordinates what to do through communication." \
                          f"\nNow, start analysis, making macro decisions in military deployments by sending message to other agents:"
    logger.info(f"[ID {log_id}] {name} CommanderTranslatorO initialized")

  def translate(self, agent) -> str:
    super(CommanderTranslatorO, self).translate(agent)
    if not self.obs_list_safe(agent):
      return f"obs_list error, no obs found"
    self.states[-1]['unit_count_info'] = get_unit_count_info(agent, return_type=1)
    self.states[-1]['other_agents_info'] = '' if self.config.ENABLE_EASY_CONTROL else get_other_agents_info(agent)
    self.states[-1]['valid_actions'] = get_valid_actions_commander(agent)

    # observation
    self.text_obs = self.state['game_info'] + self.states[-1]['unit_count_info'] + self.states[-1]['valid_actions'] + self.state['last_action_info']
    self.text_task =  self.states[-1]['other_agents_info'] + self.state['communication_input'] + self.state['communication_target'] + self.state['task_info']
    self.text_prompt = self.text_obs + self.text_task + self.final_prompt
    text_o = self.text_prompt

    if not agent.config.ENABLE_COMMUNICATION:
      logger.warning(f"[ID {self.log_id}] {self.agent_name} CommanderTranslatorO: Commander can not communicate with other agents due to agent.config.ENABLE_COMMUNICATION=False")
    return text_o


class DeveloperTranslatorO(BaseTranslatorO):

  def __init__(self, name, log_id, config):
    super(DeveloperTranslatorO, self).__init__(name, log_id, config)
    if config.ENABLE_COMMUNICATION:
      self.final_prompt = f"As a senior commander, the max number of your actions is not limited, " \
                          f"when you warp units, try to use all the WarpGate as much as possible, " \
                          f"and warp all units near a single WarpTrain Field Provider." \
                          f"\nNow, start generating your analysis, actions and communication:"
    else:
      self.final_prompt = f"As a senior commander, the max number of your actions is not limited, " \
                          f"when you warp units, try to use all the WarpGate as much as possible, " \
                          f"and warp all units near a single WarpTrain Field Provider." \
                          f"\nNow, start generating your analysis and actions:"
    logger.info(f"[ID {log_id}] {name} DeveloperTranslatorO initialized")

  def translate(self, agent) -> str:
    super(DeveloperTranslatorO, self).translate(agent)
    if not self.obs_list_safe(agent):
      return f"obs_list error, no obs found"
    self.states[-1]['unit_count_info'] = get_unit_count_info(agent, return_type=2)
    if agent.config.ENABLE_EASY_BUILD:
      self.states[-1]['valid_actions'] = get_valid_actions_developer(agent)
    else:
      self.states[-1]['valid_actions'] = get_valid_actions_developer(agent) + get_valid_actions_builder(agent)

    self.states[-1]['warp_info'] = get_warp_info(agent)
    warp_info = '' if agent.config.ENABLE_EASY_WARP else self.states[-1]['warp_info']
    action_args_explanation = '' if agent.config.ENABLE_EASY_WARP else self.state['valid_args_explanation']

    # observation
    self.text_obs = self.state['game_info'] + self.states[-1]['unit_count_info'] + \
               self.states[-1]['valid_actions'] + action_args_explanation + warp_info  #  + self.state['last_action_info']

    self.text_task = self.state['communication_input'] + self.state['communication_target'] + self.state['task_info']
    self.text_prompt = self.text_obs + self.text_task + self.final_prompt

    if not agent.config.ENABLE_COMMUNICATION:
      logger.warning(f"[ID {self.log_id}] {self.agent_name} DeveloperTranslatorO: Developer can not communicate with other agents due to agent.config.ENABLE_COMMUNICATION=False")
    text_o = self.text_prompt
    return text_o


class BuilderTranslatorO(BaseTranslatorO):
  def __init__(self, name, log_id, config):
    super(BuilderTranslatorO, self).__init__(name, log_id, config)
    if config.ENABLE_COMMUNICATION:
      self.final_prompt = f"As a builder, you need to move the worker to an open location (not far away from a base building such as protoss' Nexus), and complete the construction of the building." \
                          f"If you have enough supply (such as more than 10), build base building / gas building / unit training buildings or research building" \
                          f"You can build more than one building at the same time. It is suggest to build before move to next building position" \
                          f"\nNow, start generating your analysis, actions and communication:"
    else:
      self.final_prompt = f"As a builder, you need to move the worker to an open location (not far away from a base building such as protoss' Nexus), and complete the construction of the building." \
                          f"If you have enough supply (such as more than 10), build base building / gas building / unit training buildings or research building" \
                          f"You can build more than one building at the same time. It is suggest to build before move to next building position" \
                          f"\nNow, start generating your analysis, actions:"
    logger.info(f"[ID {log_id}] {name} DeveloperTranslatorO initialized")

  def translate(self, agent) -> str:
    super(BuilderTranslatorO, self).translate(agent)
    if not self.obs_list_safe(agent):
      return f"obs_list error, no obs found"
    self.states[-1]['unit_count_info'] = get_unit_count_info(agent, return_type=3)
    self.states[-1]['new_base_and_ves_info'] = get_ves_and_base_info(agent)
    self.states[-1]['valid_actions'] = get_valid_actions_builder(agent)

    # observation
    self.text_obs = self.state['game_info'] + self.state['units_info'] + self.states[-1]['unit_count_info'] + self.state['event_info'] + \
               self.states[-1]['valid_actions'] + self.state['valid_args_explanation'] + self.state['last_action_info'] + \
               self.state['last_action_error_info'] + self.states[-1]['new_base_and_ves_info']
    self.text_task = self.state['communication_input'] + self.state['communication_target'] + self.state['task_info']
    self.text_prompt = self.text_obs + self.text_task + self.final_prompt

    if not agent.config.ENABLE_COMMUNICATION:
      logger.warning(f"[ID {self.log_id}] {self.agent_name} DeveloperTranslatorO: Developer can not communicate with other agents due to agent.config.ENABLE_COMMUNICATION=False")
    text_o = self.text_prompt
    return text_o

# TODO: You can specialize your TranslatorO here


PROTOSS_FACTORY = {
  'default': CombatGroupTranslatorO,  # CombatGroup Observation
  'combatgroup': CombatGroupTranslatorO,  # CombatGroup Observation
  'commander': CommanderTranslatorO,  # only information relevant to macro decision, military
  'developer': DeveloperTranslatorO,  # only information relevant to macro decision, development
  'builder': BuilderTranslatorO,
}
TERRAN_FACTORY = {}
ZERG_FACTORY = {}

FACTORY = {
  'protoss': PROTOSS_FACTORY,
  'terran': TERRAN_FACTORY,
  'zerg': ZERG_FACTORY,
}
