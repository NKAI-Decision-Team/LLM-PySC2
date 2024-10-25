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

from pysc2.lib import units, upgrades, buffs, actions
import numpy as np
import math


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

# TODO: Add Zerg and Terran buildings
BASE_BUILDING_NAMES = ['Nexus', 'Hatchery', 'Hive', 'Lair', 'CommandCenter', 'OrbitalCommand', 'PlanetaryFortress']
GAS_BUILDING_NAMES = ['Assimilator', 'AssimilatorRich', 'Extractor', 'ExtractorRich', 'Refinery', 'RefineryRich']

CREEP_BUILDING_NAMES = ['BanelingNest', 'CreepTumor', 'EvolutionChamber', 'Extractor', 'GreaterSpire', 'HydraliskDen',
                        'InfestationPit', 'LurkerDen', 'NydusNetwork', 'NydusCanal', 'RoachWarren', 'SpawningPool',
                        'SpineCrawler', 'Spire', 'SporeCrawler', 'UltraliskCavern']
POWER_BUILDING_NAMES = ['Gateway', 'Stargate', 'RoboticsFacility', 'CyberneticsCore', 'Forge', 'TwilightCouncil',
                        'FleetBeacon', 'RoboticsBay', 'TemplarArchive', 'DarkShrine', 'PhotonCannon', 'ShieldBattery']

SIZE5_BUILDING_NAMES = ['Nexus', 'Hatchery', 'Hive', 'Lair', 'CommandCenter', 'OrbitalCommand', 'PlanetaryFortress']
SIZE3_BUILDING_NAMES = ['Gateway', 'Stargate', 'RoboticsFacility', 'CyberneticsCore', 'Forge', 'TwilightCouncil',
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
  units.Zerg.SporeCrawler, units.Zerg.SporeCrawlerUprooted
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


BASE_BUILDING_TYPE = [
  units.Protoss.Nexus,
  units.Terran.CommandCenter, units.Terran.OrbitalCommand, units.Terran.PlanetaryFortress,
  units.Zerg.Hatchery, units.Zerg.Lair, units.Zerg.Hive
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
  units.Zerg.Hatchery, units.Zerg.Lair, units.Zerg.Hive,
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
