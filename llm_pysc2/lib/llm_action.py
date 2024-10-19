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

from pysc2.lib.actions import FUNCTIONS as F
from pysc2.lib import features

from llm_pysc2.lib.utils import *

from loguru import logger
import random
import re

# standard action object
AN_ACTION = {'name': '', 'arg': [], 'func': []}

# actions for smac tasks, ACTION_SMAC for tasks that attack is enough
PROTOSS_BASIC_ACTION_SMAC = [
  {'name': 'Attack_Unit', 'arg': ['tag'],
   'func': [(12, F.Attack_screen, ('queued', 'screen_tag'))]},
  # {'name': 'Select_Unit_Attack_Unit', 'arg': ['tag', 'tag'],  # single unit control
  #  'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
  #           (12, F.Attack_screen, ('queued', 'screen_tag2'))]},
]
# actions for smac tasks, ACTION_SMAC2 for those moving is indispensable
PROTOSS_BASIC_ACTION_SMAC2 = [
  {'name': 'Attack_Unit', 'arg': ['tag'],
   'func': [(12, F.Attack_screen, ('queued', 'screen_tag'))]},
  {'name': 'Move_Screen', 'arg': ['screen'],
   'func': [(331, F.Move_screen, ('queued', 'screen'))]},
  # {'name': 'Select_Unit_Attack_Unit', 'arg': ['tag', 'tag'],  # single unit control
  #  'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
  #           (12, F.Attack_screen, ('queued', 'screen_tag2'))]},
  # {'name': 'Select_Unit_Move_Screen', 'arg': ['tag', 'screen'],  # single unit control
  #  'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
  #           (331, F.Move_screen, ('queued', 'screen'))]},
]
# actions for sc2 unit, 1 for buildings
PROTOSS_BASIC_ACTION_1 = [
  {'name': 'Stop', 'arg': [], 'func': [(453, F.Stop_quick, ('now'))]},
  {'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]},
  {'name': 'Stop_Building', 'arg': [], 'func': [(454, F.Stop_Building_quick, ('queued'))]},
  # {'name': 'Stop_Building_Unit',  'arg': ['tag'],
  #  'func': [(573, F.llm_pysc2_move_camera, ('world_tag')),
  #           (3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
  #           (454, F.Stop_Building_quick, ('queued'))]},
]
# actions for sc2 unit, 2 for units capable of launching attacks
PROTOSS_BASIC_ACTION_2 = [
  {'name': 'Stop', 'arg': [], 'func': [(453, F.Stop_quick, ('now'))]},
  {'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]},
  {'name': 'Hold_Position',   'arg': [],  'func': [(274, F.HoldPosition_quick, ('queued'))]},
  {'name': 'Move_Minimap', 'arg': ['minimap'], 'func': [(332, F.Move_minimap, ('queued', 'minimap'))]},
  {'name': 'Move_Screen', 'arg': ['screen'], 'func': [(331, F.Move_screen, ('queued', 'screen'))]},
  {'name': 'Attack_Unit', 'arg': ['tag'], 'func': [(12, F.Attack_screen, ('queued', 'screen_tag'))]},
  # {'name': 'Attack_Screen',   'arg': ['screen'],  'func': [(12, F.Attack_screen, ('queued', 'screen'))]},
  # {'name': 'Board_WarpPrism', 'arg': ['screen'],  'func': [(331, F.Move_screen, ('queued', 'screen_tag'))]},
]
# actions for sc2 unit, 3 for those unable to attack
PROTOSS_BASIC_ACTION_3 = [
  {'name': 'Stop', 'arg': [], 'func': [(453, F.Stop_quick, ('now'))]},
  {'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]},
  {'name': 'Hold_Position',   'arg': [],  'func': [(274, F.HoldPosition_quick, ('queued'))]},
  {'name': 'Move_Minimap', 'arg': ['minimap'], 'func': [(332, F.Move_minimap, ('queued', 'minimap'))]},
  {'name': 'Move_Screen', 'arg': ['screen'], 'func': [(331, F.Move_screen, ('queued', 'screen'))]},
  # {'name': 'Board_WarpPrism', 'arg': ['screen'],  'func': [(331, F.Move_screen, ('queued', 'screen_tag'))]},
]
# WarpTrain of protoss WarpGates
PROTOSS_ACTION_WARPTRAIN = [
  {'name': 'Warp_Adept_Near', 'arg': ['tag'],
   'func': [(8, F.select_warp_gates, ('select')), (573, F.llm_pysc2_move_camera, ('world_tag')),
            (505, F.TrainWarp_Adept_screen, ('queued', 'screen_tag'))]},  # tag for WarpprismPhasing/Pylon
  {'name': 'Warp_DarkTemplar_Near', 'arg': ['tag'],
   'func': [(8, F.select_warp_gates, ('select')), (573, F.llm_pysc2_move_camera, ('world_tag')),
            (506, F.TrainWarp_DarkTemplar_screen, ('queued', 'screen_tag'))]},  # tag for WarpprismPhasing/Pylon
  {'name': 'Warp_HighTemplar_Near', 'arg': ['tag'],
   'func': [(8, F.select_warp_gates, ('select')), (573, F.llm_pysc2_move_camera, ('world_tag')),
            (507, F.TrainWarp_HighTemplar_screen, ('queued', 'screen_tag'))]},  # tag for WarpprismPhasing/Pylon
  {'name': 'Warp_Sentry_Near', 'arg': ['tag'],
   'func': [(8, F.select_warp_gates, ('select')), (573, F.llm_pysc2_move_camera, ('world_tag')),
            (508, F.TrainWarp_Sentry_screen, ('queued', 'screen_tag'))]},  # tag for WarpprismPhasing/Pylon
  {'name': 'Warp_Stalker_Near', 'arg': ['tag'],
   'func': [(8, F.select_warp_gates, ('select')), (573, F.llm_pysc2_move_camera, ('world_tag')),
            (509, F.TrainWarp_Stalker_screen, ('queued', 'screen_tag'))]},  # tag for WarpprismPhasing/Pylon
  {'name': 'Warp_Zealot_Near', 'arg': ['tag'],
   'func': [(8, F.select_warp_gates, ('select')), (573, F.llm_pysc2_move_camera, ('world_tag')),
            (510, F.TrainWarp_Zealot_screen, ('queued', 'screen_tag')),
            (510, F.TrainWarp_Zealot_screen, ('queued', 'screen_tag')),
            (510, F.TrainWarp_Zealot_screen, ('queued', 'screen_tag')),
            (510, F.TrainWarp_Zealot_screen, ('queued', 'screen_tag')),]},  # tag for WarpprismPhasing/Pylon
  # {'name': 'Warp_One_Adept_Screen', 'arg': ['screen'],
  #  'func': [(8, F.select_warp_gates, ('select')), (505, F.TrainWarp_Adept_screen, ('queued', 'screen'))]},
  # {'name': 'Warp_One_DarkTemplar_Screen', 'arg': ['screen'],
  #  'func': [(8, F.select_warp_gates, ('select')), (506, F.TrainWarp_DarkTemplar_screen, ('queued', 'screen'))]},
  # {'name': 'Warp_One_HighTemplar_Screen', 'arg': ['screen'],
  #  'func': [(8, F.select_warp_gates, ('select')), (507, F.TrainWarp_HighTemplar_screen, ('queued', 'screen'))]},
  # {'name': 'Warp_One_Sentry_Screen', 'arg': ['screen'],
  #  'func': [(8, F.select_warp_gates, ('select')), (508, F.TrainWarp_Sentry_screen, ('queued', 'screen'))]},
  # {'name': 'Warp_One_Stalker_Screen', 'arg': ['screen'],
  #  'func': [(8, F.select_warp_gates, ('select')), (509, F.TrainWarp_Stalker_screen, ('queued', 'screen'))]},
  # {'name': 'Warp_One_Zealot_Screen', 'arg': ['screen'],
  #  'func': [(8, F.select_warp_gates, ('select')), (510, F.TrainWarp_Zealot_screen, ('queued', 'screen'))]},
]
# Idle production buildings will be automatically selected by LLMAgent._add_func_for_train_and_research()
PROTOSS_ACTION_TRAIN = [
  # Nexus, BN
  {'name': 'Train_Mothership', 'arg': [], 'func': [(541, F.Train_Mothership_quick, ('queued'))]},
  # GateWay BG
  {'name': 'Train_Adept', 'arg': [], 'func': [(457, F.Train_Adept_quick, ('queued'))]},
  {'name': 'Train_DarkTemplar', 'arg': [], 'func': [(465, F.Train_DarkTemplar_quick, ('queued'))]},
  {'name': 'Train_HighTemplar', 'arg': [], 'func': [(471, F.Train_HighTemplar_quick, ('queued'))]},
  {'name': 'Train_Sentry', 'arg': [], 'func': [(491, F.Train_Sentry_quick, ('queued'))]},
  {'name': 'Train_Stalker', 'arg': [], 'func': [(493, F.Train_Stalker_quick, ('queued'))]},
  {'name': 'Train_Zealot', 'arg': [], 'func': [(503, F.Train_Zealot_quick, ('queued'))]},
  # StarGate VS
  {'name': 'Train_Oracle', 'arg': [], 'func': [(482, F.Train_Oracle_quick, ('queued'))]},
  {'name': 'Train_Phoenix', 'arg': [], 'func': [(484, F.Train_Phoenix_quick, ('queued'))]},
  {'name': 'Train_VoidRay', 'arg': [], 'func': [(500, F.Train_VoidRay_quick, ('queued'))]},
  {'name': 'Train_Tempest', 'arg': [], 'func': [(495, F.Train_Tempest_quick, ('queued'))]},
  {'name': 'Train_Carrier', 'arg': [], 'func': [(461, F.Train_Carrier_quick, ('queued'))]},
  # RoboticFacility VR
  {'name': 'Train_Observer', 'arg': [], 'func': [(481, F.Train_Observer_quick, ('queued'))]},
  {'name': 'Train_WarpPrism', 'arg': [], 'func': [(501, F.Train_WarpPrism_quick, ('queued'))]},
  {'name': 'Train_Immortal', 'arg': [], 'func': [(473, F.Train_Immortal_quick, ('queued'))]},
  {'name': 'Train_Colossus', 'arg': [], 'func': [(462, F.Train_Colossus_quick, ('queued'))]},
  {'name': 'Train_Disruptor', 'arg': [], 'func': [(466, F.Train_Disruptor_quick, ('queued'))]},
]
# Idle technology buildings will be automatically selected by LLMAgent._add_func_for_train_and_research()
PROTOSS_ACTION_RESEARCH = [
  # CyberneticsCore BY
  {'name': 'Research_ProtossAirArmor', 'arg': [],
   'func': [(381, F.Research_ProtossAirArmor_quick, ('queued'))]},
  {'name': 'Research_ProtossAirWeapons', 'arg': [],
   'func': [(385, F.Research_ProtossAirWeapons_quick, ('queued'))]},
  {'name': 'Research_WarpGate', 'arg': [],
   'func': [(428, F.Research_WarpGate_quick, ('queued'))]},
  # Forge BF
  {'name': 'Research_ProtossGroundArmor', 'arg': [],
   'func': [(389, F.Research_ProtossGroundArmor_quick, ('queued'))]},
  {'name': 'Research_ProtossGroundWeapons', 'arg': [],
   'func': [(393, F.Research_ProtossGroundWeapons_quick, ('queued'))]},
  {'name': 'Research_ProtossShields', 'arg': [],
   'func': [(397, F.Research_ProtossShields_quick, ('queued'))]},
  # TwilightCouncil VC
  {'name': 'Research_Charge', 'arg': [],
   'func': [(359, F.Research_Charge_quick, ('queued'))]},
  {'name': 'Research_Blink', 'arg': [],
   'func': [(356, F.Research_Blink_quick, ('queued'))]},
  {'name': 'Research_AdeptResonatingGlaives', 'arg': [],
   'func': [(351, F.Research_AdeptResonatingGlaives_quick, ('queued'))]},
  # FleetBeacon VF (Void ray upgrade and Tempest upgrade are not realised in pysc2)
  {'name': 'Research_PhoenixAnionPulseCrystals', 'arg': [],
   'func': [(379, F.Research_PhoenixAnionPulseCrystals_quick, ('queued'))]},
  # RoboticsBay VB
  {'name': 'Research_ExtendedThermalLance', 'arg': [],
   'func': [(364, F.Research_ExtendedThermalLance_quick, ('queued'))]},
  {'name': 'Research_GraviticBooster', 'arg': [],
   'func': [(366, F.Research_GraviticBooster_quick, ('queued'))]},
  {'name': 'Research_GraviticDrive', 'arg': [],
   'func': [(367, F.Research_GraviticDrive_quick, ('queued'))]},
  # TemplarArchive VT
  {'name': 'Research_PsiStorm', 'arg': [],
   'func': [(401, F.Research_PsiStorm_quick, ('queued'))]},
  # DarkShrine VD
  {'name': 'Research_ShadowStrike', 'arg': [],
   'func': [(404, F.Research_ShadowStrike_quick, ('queued'))]},
]
# Standard build actions
PROTOSS_ACTION_BUILD = [
  # tag for Vespene Geyser
  {'name': 'Build_Nexus_Near', 'arg': ['tag'],
   'func': [(573, F.llm_pysc2_move_camera, ('world_tag')), (65, F.Build_Nexus_screen, ('queued', 'screen_tag'))]},
  # tag for Vespene Geyser
  {'name': 'Build_Assimilator_Near', 'arg': ['tag'],
   'func': [(40, F.Build_Assimilator_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_Nexus_Screen', 'arg': ['screen'],
   'func': [(65, F.Build_Nexus_screen, ('queued', 'screen'))]},
  {'name': 'Build_Assimilator_Screen', 'arg': ['screen'],
   'func': [(40, F.Build_Assimilator_screen, ('queued', 'screen'))]},
  {'name': 'Build_Pylon_Screen', 'arg': ['screen'],
   'func': [(70, F.Build_Pylon_screen, ('queued', 'screen'))]},
  {'name': 'Build_Gateway_Screen', 'arg': ['screen'],
   'func': [(57, F.Build_Gateway_screen, ('queued', 'screen'))]},
  {'name': 'Build_CyberneticsCore_Screen', 'arg': ['screen'],
   'func': [(48, F.Build_CyberneticsCore_screen, ('queued', 'screen'))]},
  {'name': 'Build_Forge_Screen', 'arg': ['screen'],
   'func': [(55, F.Build_Forge_screen, ('queued', 'screen'))]},
  {'name': 'Build_PhotonCannon_Screen', 'arg': ['screen'],
   'func': [(69, F.Build_PhotonCannon_screen, ('queued', 'screen'))]},
  {'name': 'Build_ShieldBattery_Screen', 'arg': ['screen'],
   'func': [(525, F.Build_ShieldBattery_screen, ('queued', 'screen'))]},
  {'name': 'Build_TwilightCouncil_Screen', 'arg': ['screen'],
   'func': [(101, F.Build_TwilightCouncil_screen, ('queued', 'screen'))]},
  {'name': 'Build_TemplarArchive_Screen', 'arg': ['screen'],
   'func': [(100, F.Build_TemplarArchive_screen, ('queued', 'screen'))]},
  {'name': 'Build_DarkShrine_Screen', 'arg': ['screen'],
   'func': [(49, F.Build_DarkShrine_screen, ('queued', 'screen'))]},
  {'name': 'Build_Stargate_Screen', 'arg': ['screen'],
   'func': [(88, F.Build_Stargate_screen, ('queued', 'screen'))]},
  {'name': 'Build_FleetBeacon_Screen', 'arg': ['screen'],
   'func': [(54, F.Build_FleetBeacon_screen, ('queued', 'screen'))]},
  {'name': 'Build_RoboticsBay_Screen', 'arg': ['screen'],
   'func': [(81, F.Build_RoboticsBay_screen, ('queued', 'screen'))]},
  {'name': 'Build_RoboticsFacility_Screen', 'arg': ['screen'],
   'func': [(82, F.Build_RoboticsFacility_screen, ('queued', 'screen'))]},
]
# Simplified build actions
PROTOSS_ACTION_EASY_BUILD = [
  # tag for Vespene Geyser
  {'name': 'Build_Nexus_Near', 'arg': ['tag'],
   'func': [(65, F.Build_Nexus_screen, ('queued', 'screen_tag'))]},
  # tag for Vespene Geyser
  {'name': 'Build_Assimilator_Near', 'arg': ['tag'],
   'func': [(40, F.Build_Assimilator_screen, ('queued', 'screen_tag'))]},
  # tag for WarpprismPhasing/Pylon
  {'name': 'Build_Pylon_Near', 'arg': ['tag'],
   'func': [(70, F.Build_Pylon_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_Gateway_Near', 'arg': ['tag'],
   'func': [(57, F.Build_Gateway_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_CyberneticsCore_Near', 'arg': ['tag'],
   'func': [(48, F.Build_CyberneticsCore_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_Forge_Near', 'arg': ['tag'],
   'func': [(55, F.Build_Forge_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_PhotonCannon_Near', 'arg': ['tag'],
   'func': [(69, F.Build_PhotonCannon_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_ShieldBattery_Near', 'arg': ['tag'],
   'func': [(525, F.Build_ShieldBattery_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_TwilightCouncil_Near', 'arg': ['tag'],
   'func': [(101, F.Build_TwilightCouncil_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_TemplarArchive_Near', 'arg': ['tag'],
   'func': [(100, F.Build_TemplarArchive_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_DarkShrine_Near', 'arg': ['tag'],
   'func': [(49, F.Build_DarkShrine_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_Stargate_Near', 'arg': ['tag'],
   'func': [(88, F.Build_Stargate_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_FleetBeacon_Near', 'arg': ['tag'],
   'func': [(54, F.Build_FleetBeacon_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_RoboticsBay_Near', 'arg': ['tag'],
   'func': [(81, F.Build_RoboticsBay_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_RoboticsFacility_Near', 'arg': ['tag'],
   'func': [(82, F.Build_RoboticsFacility_screen, ('queued', 'screen_tag'))]},
]
# Unit Abilities
PROTOSS_ACTION_ABILITY = [
  {'name': 'Morph_WarpPrismPhasingMode', 'arg': [],
   'func': [(329, F.Morph_WarpPrismPhasingMode_quick, ('queued'))]},
  {'name': 'Morph_WarpPrismTransportMode', 'arg': [],
   'func': [(330, F.Morph_WarpPrismTransportMode_quick, ('queued'))]},
  {'name': 'Morph_SurveillanceMode', 'arg': [],
   'func': [(538, F.Morph_SurveillanceMode_quick, ('queued'))]},
  {'name': 'Morph_ObserverMode', 'arg': [],
   'func': [(535, F.Morph_ObserverMode_quick, ('queued'))]},
  {'name': 'Morph_Archon', 'arg': [],
   'func': [(296, F.Morph_Archon_quick, ('queued'))]},
  {'name': 'Ability_PrismaticAlignment', 'arg': [],
   'func': [(244, F.Effect_VoidRayPrismaticAlignment_quick, ('queued'))]},
  {'name': 'Ability_CancelPhaseShift', 'arg': [],
   'func': [(453, F.Stop_quick, ('queued'))]},
  {'name': 'Ability_GuardianShield', 'arg': [],
   'func': [(197, F.Effect_GuardianShield_quick, ('queued'))]},
  {'name': 'Ability_PulsarBeamOn', 'arg': [],
   'func': [(38, F.Behavior_PulsarBeamOn_quick, ('queued'))]},
  {'name': 'Ability_ChronoBoost_Unit', 'arg': ['tag'],
   'func': [(573, F.llm_pysc2_move_camera, ('world_tag')), (527, F.Effect_ChronoBoostEnergyCost_screen, ('queued', 'screen_tag'))]},
  {'name': 'Ability_NexusMassRecall_Near', 'arg': ['tag'],
   'func': [(573, F.llm_pysc2_move_camera, ('world_tag')), (529, F.Effect_MassRecall_Nexus_screen, ('queued', 'screen_tag'))]},
  {'name': 'Ability_MothershipMassRecall_Near', 'arg': ['tag'],
   'func': [(573, F.llm_pysc2_move_camera, ('world_tag')), (208, F.Effect_MassRecall_screen, ('queued', 'screen_tag'))]},
  {'name': 'Ability_ShadowStride_Unit', 'arg': ['tag'],
   'func': [(182, F.Effect_ShadowStride_screen, ('queued', 'screen_tag'))]},
  {'name': 'Ability_GravitonBeam_Unit', 'arg': ['tag'],
   'func': [(196, F.Effect_GravitonBeam_screen, ('queued', 'screen_tag'))]},
  {'name': 'Ability_Blink_Screen', 'arg': ['screen'],
   'func': [(180, F.Effect_Blink_screen, ('queued', 'screen'))]},
  {'name': 'Ability_AdeptPhaseShift_Screen', 'arg': ['screen'],
   'func': [(177, F.Effect_AdeptPhaseShift_screen, ('queued', 'screen'))]},
  {'name': 'Ability_PsiStorm_Screen', 'arg': ['screen'],
   'func': [(218, F.Effect_PsiStorm_screen, ('queued', 'screen'))]},
  {'name': 'Ability_PurificationNova_Screen', 'arg': ['screen'],
   'func': [(219, F.Effect_PurificationNova_screen, ('queued', 'screen'))]},
  {'name': 'Ability_ForceField_Screen', 'arg': ['screen'],
   'func': [(193, F.Effect_ForceField_screen, ('queued', 'screen'))]},
  {'name': 'Ability_TimeWarp_Screen', 'arg': ['screen'],
   'func': [(241, F.Effect_TimeWarp_screen, ('queued', 'screen'))]},
  {'name': 'Ability_OracleRevelation_Screen', 'arg': ['screen'],
   'func': [(214, F.Effect_OracleRevelation_screen, ('queued', 'screen'))]},
  {'name': 'Ability_StasisTrap_Screen', 'arg': ['screen'],
   'func': [(90, F.Build_StasisTrap_screen, ('queued', 'screen'))]},
  {'name': 'Load_Unit', 'arg': ['tag'],
   'func': [(287, F.Load_screen, ('queued', 'screen_tag'))]},
  {'name': 'Unload_Screen', 'arg': ['screen'],
   'func': [(516, F.UnloadAllAt_screen, ('queued', 'screen'))]},
  {'name': 'Lock_Nexus_Near', 'arg': ['tag'],
   'func': [(70, F.Build_Pylon_screen, ('queued', 'screen_tag'))]},
  {'name': 'Lock_Assimilator_Near', 'arg': ['tag'],
   'func': [(40, F.Build_Assimilator_screen, ('queued', 'screen_tag'))]},
  {'name': 'Select_Unit_Blink_Screen', 'arg': ['tag', 'screen'],
   'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
            (180, F.Effect_Blink_screen, ('queued', 'screen'))]},
]


# 目标类型查询函数，获取Research和Train所需的源单位类型
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


# Find idle unit tag, conditions: ours + reigh-type + already-built + not-active
def find_idle_unit_tag(obs, unit_type, queued_source_unit_tag_list):
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100 and unit.active == 0 \
        and unit_type is not None and unit.unit_type == unit_type and unit.tag not in queued_source_unit_tag_list:
      return unit.tag
  return None


# Parameter verification
def get_arg_minimap(obs, minimap: list, size_minimap, action_name) -> (tuple, bool):  # 小地图坐标，校验范围
  if isinstance(minimap, list) and len(minimap) == 2 and isinstance(minimap[0], (int, float)) and isinstance(minimap[1], (int, float)):
    x = min(max(0, minimap[0]), size_minimap)
    y = min(max(0, minimap[1]), size_minimap)
    if 'Attack' in action_name and obs.observation.feature_minimap.player_relative[x][y] in [1, 2]:
      return f'({x}, {y}) is alliance', False
    if 'Load' in action_name and obs.observation.feature_minimap.player_relative[x][y] not in [1, 2]:
      return f'({x}, {y}) is not alliance', False
    if 'Follow' in action_name and obs.observation.feature_minimap.player_relative[x][y] not in [1, 2]:
      return f'({x}, {y}) is not alliance', False
    return (x, y), True
  return f'minimap={minimap}, unknown error', False


# Parameter verification
def get_arg_screen(obs, screen: list, size_screen, action_name) -> (tuple, bool):  # 屏幕坐标，校验范围
  if isinstance(screen, list) and len(screen) == 2 and isinstance(screen[0], (int, float)) and isinstance(screen[1], (int, float)):
    x = int(min(max(0, screen[0]), size_screen))
    y = int(min(max(0, screen[1]), size_screen))
    if 'Attack' in action_name and obs.observation.feature_screen.player_relative[x][y] in [1, 2]:
      return f'({x}, {y}) is alliance', False
    if 'Load' in action_name and obs.observation.feature_screen.player_relative[x][y] not in [1, 2]:
      return f'({x}, {y}) is not alliance', False
    if 'Follow' in action_name and obs.observation.feature_screen.player_relative[x][y] not in [1, 2]:
      return f'({x}, {y}) is not alliance', False
    return (x, y), True
  return f'input arg {screen} error', False


# Parameter verification, for build
def get_arg_screen_build(obs, screen: list, size_screen, action_name) -> (tuple, bool):  # 标准建造，校验地点和建造条件
  building_name = action_name.split('Build_')[1].split('_Screen')[0]
  building_size = find_building_size(building_name)
  if isinstance(screen, list) and len(screen) == 2 and isinstance(screen[0], (int, float)) and isinstance(screen[1], (
  int, float)) and building_size != 0:
    ratio = int(size_screen / SCREEN_WORLD_GRID)
    x0 = int(min(max(0, screen[0]), size_screen))
    y0 = int(min(max(0, screen[1]), size_screen))
    x1 = int(min(max(0, screen[0]), size_screen) - ratio * (building_size - 1) / 2)
    y1 = int(min(max(0, screen[1]), size_screen) - ratio * (building_size - 1) / 2)
    if building_name in POWER_BUILDING_NAMES and obs.observation.feature_screen.power[x0][y0] == 0:
      return f'({x0}, {y0}) need power', False
    if building_name in CREEP_BUILDING_NAMES and obs.observation.feature_screen.creep[x0][y0] == 0:
      return f'({x0}, {y0}) need creep', False
    for i in range(building_size):
      for j in range(building_size):
        x = int(x1 + i * ratio)
        y = int(y1 + j * ratio)
        if not (0 < x < size_screen and 0 < y < size_screen):
          return f'({x0}, {y0}) too close to screen edge', False
        if obs.observation.feature_screen.buildable[x][y] != 1:
          return f'area near ({x0}, {y0}) not buildable', False
        if obs.observation.feature_screen.pathable[x][y] != 1:
          return f'area near ({x0}, {y0}) not pathable', False
        if obs.observation.feature_screen.player_relative[x][y] not in [0, 1]:
          return f'area near ({x0}, {y0}) not blocked', False
    return (x0, y0), True
  return f'input arg {screen} error', False


# Parameter verification, tag to world coordinate
def get_arg_world_tag(obs, tag: int, x_offset, y_offset, world_range) -> (tuple, bool):  # 获取指定tag单位的世界坐标
  for unit in obs.observation.raw_units:
    if unit.tag == tag:
      x = unit.x + x_offset
      y = max(0, world_range - unit.y + y_offset)
      return (x, y), True
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag}', False


# Parameter verification, tag to screen coordinate
def get_arg_screen_tag(obs, tag: int, size_screen, action_name) -> (tuple, bool):  # 获取指定tag单位的屏幕坐标
  for unit in obs.observation.feature_units:
    if unit.tag == tag:
      x, y = unit.x, unit.y
      if 'Attack' in action_name and unit.alliance in [1, 2]:
        return f'({x}, {y}) is alliance', False
      if 'Load' in action_name and unit.alliance not in [1]:
        return f'({x}, {y}) is not alliance', False
      if 'Follow' in action_name and unit.alliance not in [1, 2]:
        return f'({x}, {y}) is not alliance', False
      if 'MassRecall' in action_name and unit.alliance not in [1]:
        return f'({x}, {y}) is not alliance', False
      if 'Chrono_Boost' in action_name and (unit.alliance not in [1] or unit.unit_type not in BOOSTABLE_TYPE):
        return f'({x}, {y}) is not boostable', False
      if 'Board_' in action_name and (unit.alliance not in [1] or unit.unit_type not in TRANSPORTER_TYPE):
        return f'({x}, {y}) is not a transporter', False
      if unit.is_on_screen and (0 < unit.x < size_screen and 0 < unit.y < size_screen):
        return (unit.x, unit.y), True
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag} on screen', False


# Parameter verification, tag to rect screen coordinates
def get_arg_screen_tag_sclect_rect(obs, tag: int, size_screen, func_arg_name) -> (tuple, bool):  # 获取指定tag附近单位群的中心坐标
  for unit in obs.observation.feature_units:
    if unit.tag == tag:
      if unit.alliance not in [1]:
        return f'({unit.y}, {unit.y}) is not alliance', False
      if not (0 < unit.x < size_screen and 0 < unit.y < size_screen):
        return f'unit {tag} ({unit.x}, {unit.y}) not no screen', False
      if func_arg_name == 'screen' and unit.is_on_screen:
        x = max(0, min(int(unit.x - size_screen / 64), size_screen))
        y = max(0, min(int(unit.y - size_screen / 64), size_screen))
        return (x, y), True
      if func_arg_name == 'screen2' and unit.is_on_screen:
        x = max(0, min(int(unit.x + size_screen / 64), size_screen))
        y = max(0, min(int(unit.y + size_screen / 64), size_screen))
        return (x, y), True
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag} on screen', False


# Parameter verification, tag to screen coordinate, for recall
def get_arg_screen_tag_recall(obs, tag: int, size_screen, action_name) -> (tuple, bool):  # 获取指定tag附近单位群的中心坐标
  for unit in obs.observation.feature_units:
    if unit.tag == tag:
      x, y = unit.x, unit.y
      if unit.alliance not in [1]:
        return f'({x}, {y}) is not alliance', False
      if unit.is_on_screen and (0 < unit.x < size_screen and 0 < unit.y < size_screen):
        return (unit.x, unit.y), True
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag} on screen', False


# Parameter verification, tag to screen coordinate, for warp
def get_arg_screen_tag_warp(obs, tag: int, size_screen, action_name) -> (tuple, bool):  # 获取指定tag附近可折跃单位的坐标
  n = 0
  for unit in obs.observation.feature_units:
    max_try = 72
    if unit.tag == tag:
      if unit.unit_type not in [units.Protoss.Pylon, units.Protoss.WarpPrismPhasing]:
        return f'tag {unit.tag}({unit.unit_type}) is not Pylon(60) or WarpPrismPhasing(136)', False
      else:
        radius = [2, 3, 4, 5, 6] if unit.unit_type == units.Protoss.Pylon else [1, 2, 3]
        angles = [0, 45, 90, 135, 180, 225, 270, 315]
        while n < max_try:
          r = radius[random.randint(0, len(radius) - 1)]
          a = angles[random.randint(0, len(angles) - 1)]
          x = int(unit.x + r * (size_screen / SCREEN_WORLD_GRID) * math.cos(math.radians(a)))
          y = int(unit.y + r * (size_screen / SCREEN_WORLD_GRID) * math.sin(math.radians(a)))
          if (0 < x < size_screen and 0 < y < size_screen) and \
              obs.observation.feature_screen.power[x][y] == 1 and \
              obs.observation.feature_screen.pathable[x][y] == 1 and \
              obs.observation.feature_screen.unit_type[x][y] == 0 and \
              obs.observation.feature_screen.build_progress[x][y] == 0 and \
              obs.observation.feature_screen.unit_shields[x][y] == 0:
            return (x, y), True
          else:
            n = n + 1
  if n == 36:
    return f'cannot find valid position to warp unit', False
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag} on screen', False


# Parameter verification, tag to screen coordinate, for gas building
def get_arg_screen_tag_gas_building(obs, tag: int, size_screen, action_name) -> (tuple, bool):

  # find vesoene gesyer raw_unit
  unit_r = None
  for unit in obs.observation.raw_units:
    if unit.tag == tag:
      unit_r = unit
  if unit_r is None:
    tag = hex(tag) if isinstance(tag, int) else tag
    return f'cannot find unit {tag}', False
  # confirm if is possible to construct
  for unit in obs.observation.feature_units:
    if unit.tag == tag:
      base_nearby = False
      for unit_ in obs.observation.raw_units:
        if unit_.alliance == features.PlayerRelative.SELF and unit_.unit_type in BASE_BUILDING_TYPE and \
            math.sqrt((unit_.x - unit_r.x) ** 2 + (unit_.y - unit_r.y) ** 2) < 10:
          base_nearby = True
      if not base_nearby:
        return f'tag {unit.tag}({unit.unit_type}) is far away from our base building', False
      if unit.unit_type not in GAS_TYPE:
        return f'tag {unit.tag}({unit.unit_type}) is not VespeneGeyser(342 344 608 880 881)', False
      if unit.is_on_screen and (0 < unit.x < size_screen and 0 < unit.y < size_screen):
        return (unit.x, unit.y), True
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag} on screen', False


# Parameter verification, tag to screen coordinate, for base building
def get_arg_world_tag_base_building(obs, tag: int, x_offset, y_offset, world_range) -> (tuple, bool):

  def find_nearby_raw_mg(unit_g):
    nearby_resource_unit_dict = {}
    for unit in obs.observation.raw_units:
      if unit.unit_type in MINERAL_TYPE:
        dist = math.sqrt((unit.x - unit_g.x) ** 2 + (unit.y - unit_g.y) ** 2)
        if dist < 16:
          nearby_resource_unit_dict[dist] = unit
      if unit.unit_type in GAS_TYPE:
        dist = math.sqrt((unit.x - unit_g.x) ** 2 + (unit.y - unit_g.y) ** 2)
        if dist < 16:
          nearby_resource_unit_dict[dist] = unit
    return nearby_resource_unit_dict.values()

  def artificial_force_field_iteration_world(unit_list, x, y):
    k, r, m = 0.5, 7, 1
    vespene_r, vespene_m = 8, 1
    mineral_r, mineral_m = 7, 1
    n, bad_n, fx, fy = 0, 0, 0, 0
    for unit in unit_list:
      bad = False
      if unit.unit_type in GAS_TYPE:
        r, m = vespene_r, vespene_m
      if unit.unit_type in MINERAL_TYPE:
        r, m = mineral_r, mineral_m
      d = math.sqrt((unit.x - x) ** 2 + (unit.y - y) ** 2)
      f = k * (r - d) * m
      fx += f * (x - unit.x) / d
      fy += f * (y - unit.y) / d
      n += 1
      if unit.unit_type in GAS_TYPE and not (7 < d < 10):
        bad = True
      if unit.unit_type in MINERAL_TYPE and not (6 < d < 9):
        bad = True
      if bad:
        bad_n += 1
    return (x + fx / n), (y + fy / n), bad_n

  for unit in obs.observation.raw_units:
    if unit.tag == tag:
      if unit.unit_type not in GAS_TYPE + MINERAL_TYPE:
        return f'tag {unit.tag}({unit.unit_type}) is not VespeneGaser', False
      mineral_list = find_nearby_raw_mg(unit)
      n, x0, y0 = 0, 0, 0
      for mineral in mineral_list:
        n += 1
        x0 += mineral.x
        y0 += mineral.y
      x0 = x0 / n
      y0 = y0 / n
      for i in range(16):
        x0, y0, bad_n = artificial_force_field_iteration_world(mineral_list, x0, y0)
      x = int(x0 + x_offset)
      y = int(max(0, world_range - y0 + y_offset))
      return (x, y), True
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag} on screen', False


# Parameter verification, tag to screen coordinate, for base building
def get_arg_screen_tag_base_building(obs, tag: int, size_screen, action_name) -> (tuple, bool):
  def find_nearby_screen_mg(unit_g):
    ratio = size_screen / SCREEN_WORLD_GRID
    nearby_resource_unit_dict = {}
    for unit in obs.observation.feature_units:
      if unit.unit_type in MINERAL_TYPE:
        dist = math.sqrt((unit.x - unit_g.x) ** 2 + (unit.y - unit_g.y) ** 2)
        if dist < 16 * ratio:
          nearby_resource_unit_dict[dist] = unit
      if unit.unit_type in GAS_TYPE:
        dist = math.sqrt((unit.x - unit_g.x) ** 2 + (unit.y - unit_g.y) ** 2)
        if dist < 16 * ratio:
          nearby_resource_unit_dict[dist] = unit
    return nearby_resource_unit_dict.values()

  def artificial_force_field_iteration_screen(unit_list, x, y):
    ratio = size_screen / SCREEN_WORLD_GRID
    k, r, m = 0.5, 7 * ratio, 1
    vespene_r, vespene_m = 8 * ratio, 1
    mineral_r, mineral_m = 7 * ratio, 1
    n, bad_n, fx, fy = 0, 0, 0, 0
    for unit in unit_list:
      bad = False
      if unit.unit_type in GAS_TYPE:
        r, m = vespene_r, vespene_m
      if unit.unit_type in MINERAL_TYPE:
        r, m = mineral_r, mineral_m
      d = math.sqrt((unit.x - x) ** 2 + (unit.y - y) ** 2)
      f = k * (r - d) * m
      fx += f * (x - unit.x) / d
      fy += f * (y - unit.y) / d
      n += 1
      if unit.unit_type in GAS_TYPE and not (7 * ratio < d < 10 * ratio):
        bad = True
      if unit.unit_type in MINERAL_TYPE and not (6 * ratio < d < 9 * ratio):
        bad = True
      if bad:
        bad_n += 1
    return (x + fx / n), (y + fy / n), bad_n

  building_name = action_name.split('_Screen')[0].split('_')[1]  # Build/Lock
  building_size = find_building_size(building_name)
  for unit in obs.observation.feature_units:
    if unit.tag == tag or (unit.unit_type in GAS_TYPE + MINERAL_TYPE and unit.is_on_screen):
      if unit.unit_type not in GAS_TYPE + MINERAL_TYPE:
        return f'tag {unit.tag}({unit.unit_type}) is not VespeneGaser', False
      mineral_gas_list = find_nearby_screen_mg(unit)
      n, x0, y0 = 0, 0, 0
      for mineral in mineral_gas_list:
        n += 1
        x0 += mineral.x
        y0 += mineral.y
      x = x0 / n
      y = y0 / n
      bad_n = len(mineral_gas_list)
      for i in range(16):
        x, y, bad_n = artificial_force_field_iteration_screen(mineral_gas_list, x, y)
      x, y = int(x), int(y)
      if bad_n > 3:
        return f'({x}, {y}) may be a bad position for base building', False
      if not (0 < x < size_screen and 0 < y < size_screen):
        return f'({x}, {y}) too close to screen edge', False
      if obs.observation.feature_screen.buildable[x][y] != 1:
        return f'area near ({x}, {y}) not buildable', False
      if obs.observation.feature_screen.pathable[x][y] != 1:
        return f'area near ({x}, {y}) not pathable', False
      if obs.observation.feature_screen.player_relative[x][y] not in [0, 1]:
        return f'area near ({x}, {y}) not blocked', False
      if unit.is_on_screen and (0 < x < size_screen and 0 < y < size_screen):
        return (x, y), True
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag} on screen', False


# 补齐拖农民的前置函数
def add_func_for_select_workers(self, obs, action):

  action_name = action['name']
  action_arg = action['arg']
  action_func = action['func']
  if not ('Select_Workers_' in action_name):
    return action

  full_shape_action = None
  logger.debug(self.action_list)

  func_id, func, arg_type = action_func[0]
  source_unit_tag = None
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.unit_type in WORKER_TYPE and \
        unit.is_on_screen and (0 < unit.x < self.size_screen and 0 < unit.y < self.size_screen):
      source_unit_tag = unit.tag
  if source_unit_tag is None:
    logger.error(
      f"[ID {self.log_id}] Agent {self.name}, Can not find source unit type for func {actions.FUNCTIONS[func_id].name}")
  else:
    logger.debug(f"[ID {self.log_id}] Agent {self.name}, find source unit worker {source_unit_tag}")

  if source_unit_tag is not None:
    full_shape_action = {'name': action_name, 'arg': [], 'func':
      [(2, actions.FUNCTIONS.select_point, ['select_all_type', int(source_unit_tag)])] + action['func']}
  else:
    full_shape_action = {'name': 'No_Operation', 'arg': [], 'func':
      [(0, actions.FUNCTIONS.no_op, {})]}

  return full_shape_action


# 补齐训练和升级的前置函数，移动相机到闲置建筑，并选择该建筑
def add_func_for_train_and_research(self, obs, action):
  # 该函数将train/research动作需要的move_camera和select动作补齐，
  #  补到self.text_func_list中，将它从单一的F.Train_xxx_quick/F.Research_xxx_quick变成三个动作

  action_name = action['name']
  action_arg = action['arg']
  action_func = action['func']
  if not ('Train_' in action_name or 'Research_' in action_name):
    return action

  full_shape_action = None
  queued_source_unit_tag_list = []  # 已经准备训练/升级单位的建筑，用于避免重复选中
  logger.debug(self.action_list)

  func_id, func, arg_type = action_func[0]
  source_unit_type = find_unit_type_the_func_belongs_to(func_id, self.race)
  source_unit_tag = find_idle_unit_tag(obs, source_unit_type, queued_source_unit_tag_list)

  if source_unit_type is None:
    logger.error(
      f"[ID {self.log_id}] Agent {self.name}, Can not find source unit type for func {actions.FUNCTIONS[func_id].name}")
  elif source_unit_tag is None:
    logger.error(
      f"[ID {self.log_id}] Agent {self.name}, Can not find source unit of {str(units.get_unit_type(source_unit_type))} type")
  else:
    queued_source_unit_tag_list.append(source_unit_tag)

  if source_unit_tag is not None:
    full_shape_action = {'name': action_name, 'arg': [], 'func':
      [(573, actions.FUNCTIONS.llm_pysc2_move_camera, [int(source_unit_tag)]),
       (2, actions.FUNCTIONS.select_point, ['select', int(source_unit_tag)])] + action['func']}
  else:
    full_shape_action = {'name': 'No_Operation', 'arg': [], 'func':
      [(0, actions.FUNCTIONS.no_op, {})]}

  return full_shape_action


class BaseTranslatorA:

  def __init__(self):
    pass

  def translate(self, obs) -> "list of [(func_id, func_call)]":
    pass


# TODO: You can specialize your TranslatorA here


class DefaultTranslatorA(BaseTranslatorA):

  def __init__(self, name, log_id, config):
    super(DefaultTranslatorA, self).__init__()
    self.agent_name = name
    self.ACTION_SPACE = config.AGENTS[name]['action']
    self.ACTION_SPACE_DICT = {}
    for unit_type in self.ACTION_SPACE.keys():
      for action in self.ACTION_SPACE[unit_type]:
        self.ACTION_SPACE_DICT[action['name']] = action
    self.log_id = log_id
    logger.info(f"[ID {self.log_id}] {name} DefaultTranslatorA initialized")

  # text actions recognition
  def translate(self, raw_text_a: str):
    action_list_dict = {}
    action_lists, action_lists2 = [], []
    team_actions, team_actions2 = [], []
    processed_text_a, team_name = '', ''
    lines = raw_text_a.splitlines()
    start_recognize = False
    first_function = True
    for line in lines:
      if ("Actions:" in line) or ("Action:" in line) or \
          ("actions:" in line) or ("action:" in line):
        processed_text_a = "Actions:"
        start_recognize = True
      if ("Communications:" in line) or ("Communication:" in line) or \
          ("communications:" in line) or ("Communication:" in line):
        start_recognize = False
      if start_recognize:
        if ("Team" in line and ":" in line) or ("team" in line and ":" in line):
          team_name = line.split("eam ")[1].split(":")[0]  # Team/team xxxx:  -->  xxxx
          processed_text_a += f"\n\tTeam {team_name}:"
          if len(team_actions) != 0:
            action_lists.append(team_actions)
            action_lists2.append(team_actions2)
            action_list_dict[team_name] = team_actions
            first_function = True
            team_actions, team_actions2 = [], []
        elif "<" in line and ">" in line:
          action_text = line.split("<")[1].split(">")[0]
          action_name = action_text.split("(")[0]
          action_args = action_text.split("(")[1].split(")")[0]
          action_valid, tag, tag2, tag3, x, y = True, None, None, None, None, None
          if "0x" in action_args:
            tag = int(re.findall(r'0x\w+', action_args)[0], 16)
            if len(re.findall(r'0x\w+', action_args)) > 1:
              tag2 = int(re.findall(r'0x\w+', action_args)[1], 16)
            if len(re.findall(r'0x\w+', action_args)) > 2:
              tag3 = int(re.findall(r'0x\w+', action_args)[2], 16)
          if "[" in action_args:
            x = float(re.findall(r'\[-?\d+\.?\d*e?-?\d*?', action_args)[0].split("[")[1])
            y = float(re.findall(r'-?\d+\.?\d*e?-?\d*?\]', action_args)[0].split("]")[0])

          # 在动作空间中查找action_name对应的action
          if action_name in self.ACTION_SPACE_DICT.keys():
            action = self.ACTION_SPACE_DICT[action_name]
          else:
            logger.error(f"translator unable to find {action_name}")
            action = {'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]}
            action_valid = False

          # 将识别出的动作参数填入函数参数元组中
          new_func_triples, new_func_triples2 = [], []
          for func_triple in action['func']:  # func_triple 形如 (0, F.no_op, ())
            new_func_triple, new_func_triple2, new_func_args = [], [], []
            func_args = func_triple[2]
            if len(list(func_args)) > 0:
              if not isinstance(func_args, tuple):
                func_args = [func_args]
              for arg in list(func_args):
                if arg == "now":
                  new_func_args.append('now')
                if arg == "queued":
                  if first_function:
                    new_func_args.append('now')
                  else:
                    new_func_args.append('queued')
                if arg == "select":
                  new_func_args.append('select')
                if arg in ["screen_tag", "minimap_tag", "world_tag", "screen1_tag", "screen2_tag"]:
                  if tag is not None:
                    new_func_args.append(tag)
                  else:
                    new_func_args.append('error')
                if arg in ["screen_tag2", "minimap_tag2", "world_tag2", "screen1_tag2", "screen2_tag2"]:
                  if tag2 is not None:
                    new_func_args.append(tag2)
                  else:
                    new_func_args.append('error')
                if arg in ["screen", "minimap"]:
                  if (x is not None) and (y is not None):
                    new_func_args.append([x, y])
                  else:
                    new_func_args.append('error')
                # if arg in ["screen1_tag", "screen2_tag"]:
                #   if tag is not None:
                #     new_func_args.append(tag)
                #   else:
                #     new_func_args.append('error')
                # if arg in ["screen1_tag2", "screen2_tag2"]:
                #   if tag2 is not None:
                #     new_func_args.append(tag2)
                #   else:
                #     new_func_args.append('error')
            if 'error' not in new_func_args and first_function and 'now' in new_func_args:
              first_function = False
            if 'error' in new_func_args:
                action_valid = False
            new_func_triple.append(func_triple[0])
            new_func_triple.append(func_triple[1])
            new_func_triple.append(tuple(new_func_args))
            new_func_triples.append(tuple(new_func_triple))

            new_func_triple2.append(func_triple[0])
            new_func_triple2.append(func_triple[1].name)
            new_func_triple2.append(tuple(new_func_args))
            new_func_triples2.append(tuple(new_func_triple2))

          if action_valid:
            team_actions.append({'name': action['name'], 'arg': action['arg'], 'func': new_func_triples})
            team_actions2.append({'name': action['name'], 'arg': action['arg'], 'func': new_func_triples2})
            processed_text_a += f"\n\t\t<{action_text}>"
          else:
            team_actions.append({'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]})
            team_actions2.append({'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]})
        else:
          pass

    if len(team_actions) != 0:
      action_lists.append(team_actions)
      action_lists2.append(team_actions2)
      action_list_dict[team_name] = team_actions
      first_function = True
      team_actions, team_actions2 = [], []

    return action_lists, action_list_dict, processed_text_a


PROTOSS_FACTORY = {'default': DefaultTranslatorA}
TERRAN_FACTORY = {}
ZERG_FACTORY = {}

FACTORY = {
  'protoss': PROTOSS_FACTORY,
  'terran': TERRAN_FACTORY,
  'zerg': ZERG_FACTORY,
}


if __name__ == "__main__":
  from llm_pysc2.agents.configs.config import ProtossAgentConfig
  config = ProtossAgentConfig()

  # ----------------- show action space -----------------
  def show(config):
    for name in config.AGENTS.keys():
      agent_actions = config.AGENTS[name]['action']
      print(name)
      for unit_type in agent_actions.keys():
        print(f"\t{str(units.get_unit_type(unit_type))}")
        for i in range(len(agent_actions[unit_type])):
          action = agent_actions[unit_type][i]
          if len(action['arg']) == 0:
            print(f"\t\t <{action['name']}()>")
        for i in range(len(agent_actions[unit_type])):
          action = agent_actions[unit_type][i]
          if len(action['arg']) == 1 and 'minimap' in action['arg']:
            print(f"\t\t <{action['name']}({action['arg'][0]})>")
        for i in range(len(agent_actions[unit_type])):
          action = agent_actions[unit_type][i]
          if len(action['arg']) == 1 and 'screen' in action['arg']:
            print(f"\t\t <{action['name']}({action['arg'][0]})>")
        for i in range(len(agent_actions[unit_type])):
          action = agent_actions[unit_type][i]
          if len(action['arg']) == 1 and 'tag' in action['arg']:
            print(f"\t\t <{action['name']}({action['arg'][0]})>")
        for i in range(len(agent_actions[unit_type])):
          action = agent_actions[unit_type][i]
          if len(action['arg']) == 2:
            print(f"\t\t <{action['name']}({action['arg'][0]}, {action['arg'][1]})>")
  show(config)

  # ----------------- example of TranslatorA -----------------

  translator = DefaultTranslatorA('CombatGroup1', 0, config)
  text = \
"""
Analysis:
    We should do xxx and xxx.

Actions:
    Team Stalker-1:
        <Move_Screen([2, 9])>
        <Attack_Unit(0x200540001)>
    Team Stalker-2:
        <Ability_Blink_Screen([33, 96])>
        <Move_Minimap([24, 54])>
    Team Stalker-3:
        <Select_Unit_Blink_Screen(0x1007c0001 ,[33, 96])>
        <Hold_Position()>
"""

  actions, processed_text_a, _ = translator.translate(text)
  print(f"\n\ntext to translator:{text}")
  print(f"detected action from translator:\n{actions}\n")
  print(f"detected text_a from translator:\n{processed_text_a}\n")
  print(f"agent {translator.agent_name} action names: {translator.ACTION_SPACE_DICT.keys()}")
  print(f"agent {translator.agent_name} action num: {len(translator.ACTION_SPACE_DICT.keys())}")
