

from llm_pysc2.lib.utils import SIZE5_BUILDING_NAMES, SIZE3_BUILDING_NAMES, SIZE2_BUILDING_NAMES, SIZE1_BUILDING_NAMES

from pysc2.lib import units


def find_unit_type_the_func_belongs_to(func_id, race):
  if race == 'protoss':
    if func_id in [541, 485]:
      return units.Protoss.Nexus
    if func_id in [457, 465, 471, 491, 493, 503]:
      return units.Protoss.Gateway
    if func_id in [482, 484, 500, 495, 461]:
      return units.Protoss.Stargate
    if func_id in [481, 501, 473, 462, 466]:
      return units.Protoss.RoboticsFacility
    if func_id in [381, 385, 428]:
      return units.Protoss.CyberneticsCore
    if func_id in [389, 393, 397]:
      return units.Protoss.Forge
    if func_id in [359, 356, 351]:
      return units.Protoss.TwilightCouncil
    if func_id in [379]:  # 缺失两个升级选项
      return units.Protoss.FleetBeacon
    if func_id in [364, 366, 367]:
      return units.Protoss.RoboticsBay
    if func_id in [401]:
      return units.Protoss.TemplarArchive
    if func_id in [404]:
      return units.Protoss.DarkShrine
  if race == 'zerg':
    pass  # Support for Zerg is undergoing
  if race == 'terran':
    pass  # Support for Terran is undergoing
  return None


def find_building_size(build_name: str) -> int:
  if build_name in SIZE5_BUILDING_NAMES:  # Support for Terran/Zerg is undergoing
    return 5
  elif build_name in SIZE3_BUILDING_NAMES:  # Support for Terran/Zerg is undergoing
    return 3
  elif build_name in SIZE2_BUILDING_NAMES:  # Support for Terran/Zerg is undergoing
    return 2
  elif build_name in SIZE1_BUILDING_NAMES:  # Support for Terran/Zerg is undergoing
    return 1
  else:
    return 0
