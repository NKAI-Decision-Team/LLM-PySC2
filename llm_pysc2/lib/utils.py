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
import random

from pysc2.lib import units, upgrades, buffs, actions, features
import numpy as np
import math
import os


# Do not modify this variable
SCREEN_WORLD_GRID = 24

def get_tag_list(unit_list: list) -> list:
  tag_list = []
  for unit in unit_list:
    tag_list.append(unit.tag)
  return tag_list

def get_raw_unit_list_of_tags(obs, tags: "int or list") -> list:
  raw_unit_list = []
  for unit in obs.observation.raw_units:
    if ((not isinstance(tags, list)) and unit.tag == tags) or (isinstance(tags, list) and unit.tag in tags):
      raw_unit_list.append(unit)
  return raw_unit_list

def get_feature_unit_list_of_tags(obs, tags: "int or list") -> list:
  feature_unit_list = []
  for unit in obs.observation.feature_units:
    if ((not isinstance(tags, list)) and unit.tag == tags) or (isinstance(tags, list) and unit.tag in tags):
      feature_unit_list.append(unit)
  return feature_unit_list

def get_nearby_tag_list(center_unit, from_unit_list: list, dist: int = 15) -> list:
  tag_list = []
  center_unit_x = center_unit.x
  center_unit_y = center_unit.y
  for unit in from_unit_list:
    if math.sqrt((unit.x - center_unit_x) ** 2 + (unit.y - center_unit_y) ** 2) <= dist:
      tag_list.append(unit.tag)
  return tag_list

def get_nearby_unit_list(center_unit, from_unit_list: list, dist: int = 15) -> list:
  unit_list = []
  center_unit_x = center_unit.x
  center_unit_y = center_unit.y
  for unit in from_unit_list:
    if math.sqrt((unit.x - center_unit_x) ** 2 + (unit.y - center_unit_y) ** 2) <= dist:
      unit_list.append(unit)
  return unit_list

def get_dist(unit, unit_):
  return math.sqrt((unit.x - unit_.x) ** 2 + (unit.y - unit_.y) ** 2)

def get_cos(unit1, unit2, unit3):
  d1 = np.array([unit2.x - unit1.x, unit2.y - unit1.y])
  d2 = np.array([unit3.x - unit2.x, unit3.y - unit2.y])
  # result = float((d1[0] * d2[0] + d1[1] * d2[1]) / (np.linalg.norm(d1) * np.linalg.norm(d2)))
  result = np.dot(d1, d2) / (np.linalg.norm(d1) * np.linalg.norm(d2))
  return result

def get_relevant_team_dist(relevant_team_list, obs, curr_unit):
  relevant_team_dist = []
  for team in relevant_team_list:
    if len(team['unit_tags']) == 0:
      relevant_team_dist.append(99999)
    else:
      unit_r = None
      for unit in obs.observation.raw_units:
        if unit.tag == team['unit_tags'][0]:
          unit_r = unit
      if unit_r is None:
        relevant_team_dist.append(99999)
      else:
        relevant_team_dist.append(get_dist(unit_r, curr_unit))
  return relevant_team_dist

def write_to_file(text, path):
  if not os.path.exists(path):
    with open(path, "w") as f:
      text_ =  text + '\n' if text != '' else text
      f.write(text)
  else:
    with open(path, "a", newline='\n') as f:
      print(text, file=f)

BUFF_TO_TARGET_TYPE = {
  buffs.Buffs.GravitonBeam: 'air'
}

# TODO: Add Zerg and Terran buildings
BASE_BUILDING_NAMES = ['Nexus', 'Hatchery', 'Hive', 'Lair', 'CommandCenter', 'OrbitalCommand', 'PlanetaryFortress']
GAS_BUILDING_NAMES = ['Assimilator', 'AssimilatorRich', 'Extractor', 'ExtractorRich', 'Refinery', 'RefineryRich']

CREEP_BUILDING_NAMES = ['BanelingNest', 'CreepTumor', 'EvolutionChamber', 'Extractor', 'GreaterSpire', 'HydraliskDen',
                        'InfestationPit', 'LurkerDen', 'NydusNetwork', 'NydusCanal', 'RoachWarren', 'SpawningPool',
                        'SpineCrawler', 'Spire', 'SporeCrawler', 'UltraliskCavern']
POWER_BUILDING_NAMES = ['Gateway', 'Stargate', 'RoboticsFacility', 'CyberneticsCore', 'Forge', 'TwilightCouncil',
                        'FleetBeacon', 'RoboticsBay', 'TemplarArchive', 'DarkShrine', 'PhotonCannon', 'ShieldBattery']

SIZE5_BUILDING_NAMES = ['Nexus', 'Hatchery', 'Hive', 'Lair', 'CommandCenter', 'OrbitalCommand', 'PlanetaryFortress']
# + [str(units.Protoss.Nexus), str(units.Zerg.Hatchery), str(units.Zerg.Hive), str(units.Zerg.Lair)] + \
# [str(units.Terran.CommandCenter), str(units.Terran.OrbitalCommand), str(units.Terran.PlanetaryFortress)]
SIZE3_BUILDING_NAMES = ['Gateway', 'WarpGate', 'Stargate', 'RoboticsFacility', 'CyberneticsCore', 'Forge', 'TwilightCouncil',
                        'FleetBeacon', 'RoboticsBay', 'TemplarArchive', 'Assimilator', 'AssimilatorRich'] + \
                       [] + \
                       []
SIZE2_BUILDING_NAMES = ['Pylon', 'DarkShrine', 'PhotonCannon', 'ShieldBattery'] + \
                       [] + \
                       []
SIZE1_BUILDING_NAMES = ['StasisTrap'] + \
                       ['CreepTumor'] + \
                       ['SensorTower']

PROTOSS_BUILDING_TYPE = [
  units.Protoss.Nexus, units.Protoss.Assimilator, units.Protoss.AssimilatorRich, units.Protoss.Pylon,
  units.Protoss.CyberneticsCore, units.Protoss.Forge, units.Protoss.Gateway, units.Protoss.WarpGate,
  units.Protoss.ShieldBattery, units.Protoss.PhotonCannon,
  units.Protoss.TwilightCouncil, units.Protoss.Stargate, units.Protoss.RoboticsBay,
  units.Protoss.TemplarArchive, units.Protoss.FleetBeacon, units.Protoss.RoboticsFacility,
  units.Protoss.DarkShrine, units.Protoss.StasisTrap
]
ZERG_BUILDING_TYPE = [
  units.Zerg.Hatchery, units.Zerg.Lair, units.Zerg.Hive, units.Zerg.Extractor, units.Zerg.ExtractorRich,
  units.Zerg.SpawningPool, units.Zerg.EvolutionChamber, units.Zerg.HydraliskDen,
  units.Zerg.Spire, units.Zerg.GreaterSpire, units.Zerg.BanelingNest,
  units.Zerg.InfestationPit, units.Zerg.NydusNetwork, units.Zerg.NydusCanal,
  units.Zerg.UltraliskCavern, units.Zerg.RoachWarren, units.Zerg.LurkerDen,
  units.Zerg.SpineCrawler, units.Zerg.SpineCrawlerUprooted,
  units.Zerg.SporeCrawler, units.Zerg.SporeCrawlerUprooted,
]
TERRAN_BUILDING_TYPE = [
  units.Terran.CommandCenter, units.Terran.OrbitalCommand, units.Terran.PlanetaryFortress,
  units.Terran.Barracks, units.Terran.Bunker, units.Terran.Factory, units.Terran.Starport,
  units.Terran.EngineeringBay, units.Terran.MissileTurret, units.Terran.SensorTower,
  units.Terran.SupplyDepot, units.Terran.Refinery, units.Terran.GhostAcademy,
  units.Terran.Armory, units.Terran.FusionCore, units.Terran.Reactor, units.Terran.TechLab,
  units.Terran.BarracksTechLab, units.Terran.FactoryTechLab, units.Terran.StarportTechLab,
]
BUILDING_TYPE = PROTOSS_BUILDING_TYPE + ZERG_BUILDING_TYPE + TERRAN_BUILDING_TYPE

BUILDING_TYPE_MILITARY = [  # TODO: ADD MORE
  units.Protoss.Gateway, units.Protoss.WarpGate, units.Protoss.Stargate, units.Protoss.RoboticsFacility
]
BUILDING_TYPE_RESEARCH = [  # TODO: ADD MORE
  units.Protoss.CyberneticsCore, units.Protoss.Forge, units.Protoss.TwilightCouncil,
  units.Protoss.TemplarArchive, units.Protoss.FleetBeacon, units.Protoss.RoboticsBay, units.Protoss.DarkShrine
]
BUILDING_TYPE_DEFENSE = [  # TODO: ADD MORE
  units.Protoss.ShieldBattery, units.Protoss.PhotonCannon,
  units.Zerg.SpineCrawler, units.Zerg.SporeCrawler,
  units.Terran.Bunker
]


BASE_BUILDING_TYPE = [
  units.Protoss.Nexus,
  units.Terran.CommandCenter, units.Terran.OrbitalCommand, units.Terran.PlanetaryFortress,
  units.Zerg.Hatchery, units.Zerg.Lair, units.Zerg.Hive
]
BUILDER_TYPE = [
  units.Protoss.Probe,
  units.Terran.SCV,
  units.Zerg.Drone
]
WORKER_TYPE = [
  units.Protoss.Probe,
  units.Terran.SCV, units.Terran.MULE,  # 注意 MULE不能采集瓦斯
  units.Zerg.Drone
]
MINERAL_TYPE = [
  units.Neutral.MineralField, units.Neutral.MineralField750, units.Neutral.MineralField450,
  units.Neutral.RichMineralField, units.Neutral.RichMineralField750,
  units.Neutral.PurifierRichMineralField, units.Neutral.PurifierRichMineralField750,
  units.Neutral.BattleStationMineralField, units.Neutral.BattleStationMineralField750,
  units.Neutral.PurifierMineralField, units.Neutral.PurifierMineralField750,
  units.Neutral.PurifierRichMineralField, units.Neutral.PurifierRichMineralField750,
  units.Neutral.LabMineralField, units.Neutral.LabMineralField750
]
GAS_TYPE = [
  units.Neutral.VespeneGeyser, units.Neutral.RichVespeneGeyser, units.Neutral.ProtossVespeneGeyser,
  units.Neutral.PurifierVespeneGeyser, units.Neutral.ShakurasVespeneGeyser]
GAS_BUILDING_TYPE = [
  units.Protoss.Assimilator, units.Protoss.AssimilatorRich,
  units.Terran.Refinery, units.Terran.RefineryRich,
  units.Zerg.Extractor, units.Zerg.ExtractorRich
]
TRANSPORTER_TYPE = [
  units.Protoss.WarpPrism, units.Protoss.WarpPrismPhasing,
  units.Zerg.OverlordTransport, units.Zerg.NydusCanal, units.Zerg.NydusNetwork,
  units.Terran.Medivac,
]
OTHER_ACCESSBLE_UNIT_TYPE = [  # 不计gas_building
  units.Terran.Bunker # +人族基地？
]
ACCESSBLE_UNIT_TYPE = TRANSPORTER_TYPE + GAS_BUILDING_TYPE + OTHER_ACCESSBLE_UNIT_TYPE

BOOSTABLE_TYPE = [
  units.Protoss.Nexus, units.Protoss.Gateway, units.Protoss.CyberneticsCore, units.Protoss.Forge,
  units.Protoss.TwilightCouncil, units.Protoss.TemplarArchive, units.Protoss.DarkShrine,
  units.Protoss.Stargate, units.Protoss.FleetBeacon, units.Protoss.RoboticsBay, units.Protoss.RoboticsFacility,
]
# used in llm_observation
UNIT_DONOT_NEED_TAG = \
  [units.Protoss.Interceptor,
   units.Zerg.Broodling, units.Zerg.Locust, units.Zerg.LocustFlying, units.Zerg.Larva]
UNIT_DONOT_NEED_DIS = \
  [units.Protoss.Interceptor,
   units.Zerg.Broodling, units.Zerg.Locust, units.Zerg.LocustFlying, units.Zerg.Larva,
   units.Zerg.Zergling, units.Zerg.Baneling]
# used in locked_func1
UNIT_DONOT_NEED_GATHER = \
  [units.Protoss.Interceptor, units.Protoss.AdeptPhaseShift, units.Protoss.DisruptorPhased,
   units.Zerg.Broodling, units.Zerg.Locust, units.Zerg.LocustFlying, units.Zerg.Larva]

# zerg_tech_upgrades = {
#   'Melee Attacks': [
#     upgrades.Upgrades.ZergMeleeWeaponsLevel1,
#     upgrades.Upgrades.ZergMeleeWeaponsLevel2,
#     upgrades.Upgrades.ZergMeleeWeaponsLevel3
#   ],
#   'Missile Attacks': [
#     upgrades.Upgrades.ZergMissileWeaponsLevel1,
#     upgrades.Upgrades.ZergMissileWeaponsLevel2,
#     upgrades.Upgrades.ZergMissileWeaponsLevel3
#   ],
#   'Flyer Attacks': [
#     upgrades.Upgrades.ZergFlyerWeaponsLevel1,
#     upgrades.Upgrades.ZergFlyerWeaponsLevel2,
#     upgrades.Upgrades.ZergFlyerWeaponsLevel3
#   ],
#   'Ground Carapace': [
#     upgrades.Upgrades.ZergGroundArmorsLevel1,
#     upgrades.Upgrades.ZergGroundArmorsLevel2,
#     upgrades.Upgrades.ZergGroundArmorsLevel3
#   ],
#   'Flyer Carapace': [
#     upgrades.Upgrades.ZergFlyerArmorsLevel1,
#     upgrades.Upgrades.ZergFlyerArmorsLevel2, upgrades.Upgrades.ZergFlyerArmorsLevel3
#   ],
#   'Burrow': [upgrades.Upgrades.Burrow],
#   'Centrifugal Hooks': [upgrades.Upgrades.CentrificalHooks],
#   'Adrenal Glands': [upgrades.Upgrades.AdrenalGlands],
#   'Adaptive Talons': [upgrades.Upgrades.AdaptiveTalons],
#   'Anabolic Synthesis': [upgrades.Upgrades.AnabolicSynthesis],
#   'Chitinous Plating': [upgrades.Upgrades.ChitinousPlating],
#   'Glial Reconstitution': [upgrades.Upgrades.GlialReconstitution],
#   'Grooved Spines': [upgrades.Upgrades.GroovedSpines],
#   'Metabolic Boost': [upgrades.Upgrades.MetabolicBoost],
#   'Muscular Augments': [upgrades.Upgrades.MuscularAugments],
#   'Neural Parasite': [upgrades.Upgrades.NeuralParasite],
#   'Pathogen Glands': [upgrades.Upgrades.PathogenGlands],
#   'Pneumatized Carapace': [upgrades.Upgrades.PneumatizedCarapace],
#   'Tunneling Claws': [upgrades.Upgrades.TunnelingClaws]
# }
#
# # Protoss重要升级和建筑ID
# protoss_tech_upgrades = {
#   'Ground Weapons': [upgrades.Upgrades.ProtossGroundWeaponsLevel1,
#                      upgrades.Upgrades.ProtossGroundWeaponsLevel2,
#                      upgrades.Upgrades.ProtossGroundWeaponsLevel3],
#   'Ground Armors': [upgrades.Upgrades.ProtossGroundArmorsLevel1,
#                     upgrades.Upgrades.ProtossGroundArmorsLevel2,
#                     upgrades.Upgrades.ProtossGroundArmorsLevel3],
#   'Air Weapons': [upgrades.Upgrades.ProtossAirWeaponsLevel1,
#                   upgrades.Upgrades.ProtossAirWeaponsLevel2,
#                   upgrades.Upgrades.ProtossAirWeaponsLevel3],
#   'Air Armors': [upgrades.Upgrades.ProtossAirArmorsLevel1,
#                  upgrades.Upgrades.ProtossAirArmorsLevel2,
#                  upgrades.Upgrades.ProtossAirArmorsLevel3],
#   'Shields': [upgrades.Upgrades.ProtossShieldsLevel1,
#               upgrades.Upgrades.ProtossShieldsLevel2,
#               upgrades.Upgrades.ProtossShieldsLevel3],
#   'Blink': [upgrades.Upgrades.Blink],
#   'Charge': [upgrades.Upgrades.Charge],
#   'Extended Thermal Lance': [upgrades.Upgrades.ExtendedThermalLance],
#   'Gravitic Booster': [upgrades.Upgrades.GraviticBooster],
#   'Gravitic Drive': [upgrades.Upgrades.GraviticDrive],
#   'Graviton Catapult': [upgrades.Upgrades.GravitonCatapult],
#   'Psi Storm': [upgrades.Upgrades.PsiStorm],
#   'Resonating Glaives': [upgrades.Upgrades.ResonatingGlaives],
#   'Shadow Strike': [upgrades.Upgrades.ShadowStrike],
#   'Warp Gate Research': [upgrades.Upgrades.WarpGateResearch]
# }


def get_dis_pos_poses1(pos, pos1_list, flag='min'):
  if len(pos1_list) == 0:
    return (0, None)
  x, y, d_min = pos[0] + 0.01 * random.random(), pos[1] + 0.01 * random.random(), 999
  arr_pos1 = np.array(pos1_list).T
  arr_x1, arr_y1 = arr_pos1[0], arr_pos1[1]
  arr_x0, arr_y0 = np.zeros_like(arr_x1) + x, np.zeros_like(arr_x1) + y
  d_square = np.square(arr_x1 - arr_x0) + np.square(arr_y1 - arr_y0)
  d_min, index_min = math.sqrt(np.min(d_square)), np.unravel_index(np.argmin(d_square), d_square.shape)[0]
  d_max, index_max = math.sqrt(np.max(d_square)), np.unravel_index(np.argmax(d_square), d_square.shape)[0]
  return (d_min, index_min) if flag == 'min' else (d_max, index_max)


def get_dis_pos_poses1_manhattan(pos, pos1_list, flag='min', axis='none'):
  if len(pos1_list) == 0:
    return (0, None)
  x, y, d_min = pos[0], pos[1], 999
  arr_pos1 = np.array(pos1_list).T
  arr_x1, arr_y1 = arr_pos1[0], arr_pos1[1]
  arr_x0, arr_y0 = np.zeros_like(arr_x1) + x, np.zeros_like(arr_x1) + y
  dx = np.abs(arr_x1 - arr_x0)
  dy = np.abs(arr_y1 - arr_y0)
  if axis == 'x':
    d = dx
    d_min, index_min = np.min(d), np.unravel_index(np.argmin(d), d.shape)[0]
    d_max, index_max = np.max(d), np.unravel_index(np.argmax(d), d.shape)[0]
  elif axis == 'y':
    d = dy
    d_min, index_min = np.min(d), np.unravel_index(np.argmin(d), d.shape)[0]
    d_max, index_max = np.max(d), np.unravel_index(np.argmax(d), d.shape)[0]
  elif axis == 'xy':
    dx_min, dx_index_min = np.min(dx), np.unravel_index(np.argmin(dx), dx.shape)[0]
    dx_max, dx_index_max = np.max(dx), np.unravel_index(np.argmax(dx), dx.shape)[0]
    dy_min, dy_index_min = np.min(dy), np.unravel_index(np.argmin(dy), dy.shape)[0]
    dy_max, dy_index_max = np.max(dy), np.unravel_index(np.argmax(dy), dy.shape)[0]
    d_min, index_min = (dx_min, dx_index_min) if dx_min < dy_min else (dy_min, dy_index_min)
    d_max, index_max = (dx_max, dx_index_max) if dx_max > dy_max else (dy_max, dy_index_max)
  elif axis == 'xy_max':
    d = np.array([max(dx[i], dy[i]) for i in range(len(pos1_list))])
    d_min, index_min = np.min(d), np.unravel_index(np.argmin(d), d.shape)[0]
    d_max, index_max = np.max(d), np.unravel_index(np.argmax(d), d.shape)[0]
  else:
    d = arr_x1 - arr_x0 + arr_y1 - arr_y0
    d_min, index_min = np.min(d), np.unravel_index(np.argmin(d), d.shape)[0]
    d_max, index_max = np.max(d), np.unravel_index(np.argmax(d), d.shape)[0]
  return (d_min, index_min) if flag == 'min' else (d_max, index_max)


def get_dis_posse1_poses2(pos1_list, pos2_list, flag='min'):
  len1, len2 = len(pos1_list), len(pos2_list)
  if not (len1 > 0 and len2 > 0):
    return (0, None)
  mat_x1, mat_y1 = np.zeros((len1, len2)), np.zeros((len1, len2))
  mat_x2, mat_y2 = np.zeros((len1, len2)), np.zeros((len1, len2))
  arr_pos1 = np.array(pos1_list).T
  arr_pos2 = np.array(pos2_list).T
  arr_x1, arr_y1 = arr_pos1[0], arr_pos1[1]
  arr_x2, arr_y2 = arr_pos2[0], arr_pos2[1]
  mat_x1 = mat_x1 + np.array([arr_x1]).T
  mat_y1 = mat_y1 + np.array([arr_y1]).T
  mat_x2 = mat_x2 + np.array([arr_x2])
  mat_y2 = mat_y2 + np.array([arr_y2])
  mat_dx, mat_dy = mat_x1 - mat_x2, mat_y1 - mat_y2
  mat_d_square = np.square(mat_dx) + np.square(mat_dy)
  d_min, indexes_min = math.sqrt(np.min(mat_d_square)), np.unravel_index(np.argmin(mat_d_square), mat_d_square.shape)
  d_max, indexes_max = math.sqrt(np.max(mat_d_square)), np.unravel_index(np.argmax(mat_d_square), mat_d_square.shape)
  return (d_min, indexes_min) if flag=='min' else (d_max, indexes_max)


def get_nearby_unit_num_of_unit(pos1_list, pos2_list, r=3, flag='min'):  # pos1_list more, index for pos2_list
  len1, len2 = len(pos1_list), len(pos2_list)
  if not (len1 > 0 and len2 > 0):
    return (0, None)
  mat_x1, mat_y1 = np.zeros((len1, len2)), np.zeros((len1, len2))
  mat_x2, mat_y2 = np.zeros((len1, len2)), np.zeros((len1, len2))
  arr_pos1 = np.array(pos1_list).T
  arr_pos2 = np.array(pos2_list).T
  arr_x1, arr_y1 = arr_pos1[0], arr_pos1[1]
  arr_x2, arr_y2 = arr_pos2[0], arr_pos2[1]
  mat_x1 = mat_x1 + np.array([arr_x1]).T
  mat_y1 = mat_y1 + np.array([arr_y1]).T
  mat_x2 = mat_x2 + np.array([arr_x2])
  mat_y2 = mat_y2 + np.array([arr_y2])
  mat_dx, mat_dy = mat_x1 - mat_x2, mat_y1 - mat_y2
  mat_d = np.sqrt(np.square(mat_dx) + np.square(mat_dy))
  mat_r = np.zeros_like(mat_d) + r
  mat_r_min_d = mat_r - mat_d
  mat_none_zero_for_inner = (mat_r_min_d - abs(mat_r_min_d)).T
  counts = len(pos1_list) -  np.count_nonzero(mat_none_zero_for_inner, axis=1)
  counts_min, index_min = np.min(counts), np.argmin(counts)
  counts_max, index_max = np.max(counts), np.argmax(counts)
  return (counts_min, index_min) if flag == 'min' else (counts_max, index_max)


def get_ves_for_base_and_gas_building(obs):
  ves_all = []
  ves_near, ves_near_tags = [], []
  ves_new_base, ves_new_base_tags = [], []
  base_build, base_build_tags = [], []
  base_built, base_built_tags = [], []

  for unit in obs.observation.raw_units:
    if unit.unit_type in GAS_TYPE:
      ves_all.append(unit)
  for unit in obs.observation.raw_units:
    if unit.unit_type in BASE_BUILDING_TYPE and unit.alliance == features.PlayerRelative.SELF:
      if unit.build_progress == 100:
        base_built.append(unit)
        base_built_tags.append(unit.tag)
      else:
        base_build.append(unit)
        base_build_tags.append(unit.tag)
  base_all = base_build + base_built

  # 保留距离最近的
  for ves_unit in ves_all:
    d_min = 99
    for base_unit in base_built:
      d = get_dist(ves_unit, base_unit)
      d_min = d if d < d_min else d_min
    if d_min < 10:
      ves_near.append(ves_unit)
      ves_near_tags.append(ves_unit.tag)
    elif d_min < 35:
      ves_new_base.append(ves_unit)
      # ves_new_base_tags.append(ves_unit.tag)

  # 去重，2气对应1矿，保留一个气的tag即可
  ves_new_base_ = []
  for ves_unit in ves_new_base:
    d_min = 99
    for ves_unit_ in ves_new_base_:
      d = get_dist(ves_unit, ves_unit_)
      d_min = d if d < d_min else d_min
    if d_min >= 10 or len(ves_new_base_) == 0:
      ves_new_base_.append(ves_unit)
      ves_new_base_tags.append(ves_unit.tag)

  # 去除半场外的
  if 4 * len(base_all) >= len(ves_all):
    ves_new_base_ = []
    ves_new_base_tags = []

  return ves_new_base_, ves_near, ves_new_base_tags, ves_near_tags


# # print(str(units.Zerg.Lair).split('.')[-1])
# a = [[12, 14], [15, 12], [14, 14]]
# b = [13.5, 13]
# d, i = get_dis_pos_poses1_manhattan(b, a, 'min', 'xy_max')
# print(d, i, a[i])