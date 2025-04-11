

from llm_pysc2.lib.action import space as action_space
from llm_pysc2.lib.knowledge import knowledge_dict, unit_dict, protoss, terran, zerg
from llm_pysc2.lib.utils import *

from loguru import logger


def get_condition_elements(agent, obs=None) -> tuple:
  obs = agent.team_unit_obs_list[0] if obs is None else obs
  rc, tc, bc = {}, {}, {}
  rc.update(protoss.protoss_research_conditions)
  rc.update(terran.terran_research_conditions)
  rc.update(zerg.zerg_research_conditions)
  tc.update(protoss.protoss_train_conditions)
  tc.update(terran.terran_train_conditions)
  tc.update(zerg.zerg_train_conditions)
  bc.update(protoss.protoss_build_conditions)
  bc.update(terran.terran_build_conditions)
  bc.update(zerg.zerg_build_conditions)

  easy_build = agent.config.ENABLE_EASY_BUILD

  if agent.race == 'protoss':
    research_actions, train_actions = action_space.PROTOSS_ACTION_RESEARCH, action_space.PROTOSS_ACTION_TRAIN
    build_actions = action_space.PROTOSS_ACTION_BUILD if not easy_build else action_space.PROTOSS_ACTION_EASY_BUILD
  elif agent.race == 'terran':
    research_actions, train_actions = [], []
    build_actions = []
  elif agent.race == 'zerg':
    research_actions, train_actions = [], []
    build_actions = []
  else:
    research_actions, train_actions = action_space.PROTOSS_ACTION_RESEARCH, action_space.PROTOSS_ACTION_TRAIN
    build_actions = action_space.PROTOSS_ACTION_BUILD if not easy_build else action_space.PROTOSS_ACTION_EASY_BUILD
    logger.error(f"[ID {agent.log_id}] unknown agent.race: {agent.race}")

  player = obs.observation.player
  m = player.minerals  # mineral
  g = player.vespene  # gas
  s = player.food_cap - player.food_used  # supply
  u = obs.observation.upgrades  # upgrade
  b = []  # building

  obs = agent.team_unit_obs_list[0]
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100 and unit.active == 0 and \
        unit.unit_type in BUILDING_TYPE and unit.unit_type not in b:
      b.append(unit.unit_type)

  ra, ta, = research_actions, train_actions
  ba = build_actions + action_space.PROTOSS_BASIC_ACTION_2 if agent.name == 'Builder' else build_actions
  return ra, ta, ba, rc, tc, bc, m, g, s, u, b


def map_research_quick_to_level(func_id, u) -> int:
  global_map = {}
  global_map.update(protoss.protoss_map_research_quick_to_level)
  global_map.update(terran.terran_map_research_quick_to_level)
  global_map.update(zerg.zerg_map_research_quick_to_level)
  if func_id in global_map.keys():
    func_id_level_low_to_up = global_map[func_id]
    for func_id_ in func_id_level_low_to_up:
      if func_id_ not in u:
        return func_id_
    return -1
  else:
    return func_id


def all_building_condition_reached(conditions_building_types, curr_building_types):
  for building_type in conditions_building_types:
    if building_type not in curr_building_types:
      return False
  return True