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
import math

import numpy as np

from pysc2.lib.actions import FUNCTIONS as F
from pysc2.lib import features

from llm_pysc2.lib.utils import *
from llm_pysc2.lib.knowledge import *

from loguru import logger
import random
import re

# standard action object
AN_ACTION = {'name': '', 'arg': [], 'func': []}

HOLD_POSITION = {
  'name': 'Hold_Position', 'arg': [], 'func': [(274, F.HoldPosition_quick, ('queued'))]}
HOLD_POSITION_NO_OP = {
  'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]}

MOVE_SCREEN = {
  'name': 'Move_Screen', 'arg': ['screen'],
  'func': [(331, F.Move_screen, ('queued', 'screen')), (331, F.Move_screen, ('now', 'screen'))]}
MOVE_MINIMAP = {
  'name': 'Move_Minimap', 'arg': ['minimap'],
  'func': [(332, F.Move_minimap, ('queued', 'minimap')), (332, F.Move_minimap, ('now', 'minimap'))]}
SU_MOVE_SCREEN = {
  'name': 'Select_Unit_Move_Screen', 'arg': ['tag', 'screen'],
  'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
           (331, F.Move_screen, ('now', 'screen')),
           (331, F.Move_screen, ('queued', 'screen'))]}
SU_MOVE_MINIMAP = {
  'name': 'Select_Unit_Move_Minimap', 'arg': ['tag', 'minimap'],
  'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
           (332, F.Move_minimap, ('now', 'minimap')),
           (332, F.Move_minimap, ('queued', 'minimap'))]}

ATTACK_00S = {
  'name': 'Attack_Unit', 'arg': ['tag'],
  'func': [(12, F.Attack_screen, ('queued', 'screen_tag'))]}
ATTACK_02S = {
  'name': 'Attack_Unit', 'arg': ['tag'],
  'func': [(12, F.Attack_screen, ('queued', 'screen_tag')),
           (0, F.no_op, ()), (0, F.no_op, ()), (0, F.no_op, ()),
           (0, F.no_op, ()), (0, F.no_op, ())]}
SU_ATTACK_00S = {
  'name': 'Select_Unit_Attack_Unit', 'arg': ['tag', 'tag'],
  'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
           (12, F.Attack_screen, ('queued', 'screen_tag2'))]}
SU_ATTACK_02S = {
  'name': 'Select_Unit_Attack_Unit', 'arg': ['tag', 'tag'],
  'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
           (12, F.Attack_screen, ('queued', 'screen_tag2')),
           (0, F.no_op, ()), (0, F.no_op, ()), (0, F.no_op, ()),
           (0, F.no_op, ()), (0, F.no_op, ())]}

# actions for smac tasks, ACTION_SMAC for tasks that attack is enough
SMAC_ACTION_ZEALOT = [ATTACK_00S]
SMAC_ACTION_STALKER = [ATTACK_02S, MOVE_SCREEN]  # ,SU_MOVE_SCREEN
SMAC_ACTION_COLOSSUS = [ATTACK_00S, MOVE_SCREEN, SU_MOVE_SCREEN]

STOP_BUILDING_ACTION = {
  'name': 'Stop_Building_Unit', 'arg': ['tag'],
  'func': [(573, F.llm_pysc2_move_camera, ('world_tag')),
           (2, F.select_point, ('select', 'screen_tag')),
           (454, F.Stop_Building_quick, ('queued'))]}

# actions for sc2 unit, 1 for buildings
PROTOSS_BASIC_ACTION_1 = [
  # {'name': 'Stop', 'arg': [], 'func': [(453, F.Stop_quick, ('now'))]},
  # {'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]},
  # {'name': 'Stop_Building', 'arg': [], 'func': [(454, F.Stop_Building_quick, ('queued'))]},
  # {'name': 'Stop_Building_Unit',  'arg': ['tag'],
  #  'func': [(573, F.llm_pysc2_move_camera, ('world_tag')),
  #           (3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
  #           (454, F.Stop_Building_quick, ('queued'))]},
]
# actions for sc2 unit, 2 for units capable of launching attacks
PROTOSS_BASIC_ACTION_2 = [
  # {'name': 'Stop', 'arg': [], 'func': [(453, F.Stop_quick, ('now'))]},
  # {'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]},
  # {'name': 'Hold_Position',   'arg': [],  'func': [(274, F.HoldPosition_quick, ('queued'))]},
  {'name': 'Move_Minimap', 'arg': ['minimap'], 'func': [(332, F.Move_minimap, ('queued', 'minimap'))]},
  {'name': 'Move_Screen', 'arg': ['screen'], 'func': [(331, F.Move_screen, ('queued', 'screen'))]},
  {'name': 'Attack_Unit', 'arg': ['tag'], 'func': [(12, F.Attack_screen, ('queued', 'screen_tag'))]},
  {'name': 'Select_Unit_Attack_Unit', 'arg': ['tag', 'tag'],  # single unit control
   'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
            (12, F.Attack_screen, ('queued', 'screen_tag2'))]},
  {'name': 'Select_Unit_Move_Screen', 'arg': ['tag', 'screen'],  # single unit control
   'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
            (331, F.Move_screen, ('queued', 'screen'))]},
  # {'name': 'Select_Unit_Move_Minimap', 'arg': ['tag', 'minimap'],  # single unit control
  #  'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
  #           (332, F.Move_minimap, ('queued', 'minimap'))]},
  # {'name': 'Attack_Screen',   'arg': ['screen'],  'func': [(12, F.Attack_screen, ('queued', 'screen'))]},
  # {'name': 'Board_WarpPrism', 'arg': ['screen'],  'func': [(331, F.Move_screen, ('queued', 'screen_tag'))]},
]
# actions for sc2 unit, 3 for those unable to attack
PROTOSS_BASIC_ACTION_3 = [
  # {'name': 'Stop', 'arg': [], 'func': [(453, F.Stop_quick, ('now'))]},
  # {'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]},
  # {'name': 'Hold_Position',   'arg': [],  'func': [(274, F.HoldPosition_quick, ('queued'))]},
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
            (510, F.TrainWarp_Zealot_screen, ('queued', 'screen_tag')), ]},  # tag for WarpprismPhasing/Pylon
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
PROTOSS_ACTION_EASY_WARPTRAIN = [
  {'name': 'Warp_Adept', 'arg': [],
   'func': [(505, F.TrainWarp_Adept_screen, ('queued', 'auto'))]},  # tag for WarpprismPhasing/Pylon
  {'name': 'Warp_DarkTemplar', 'arg': [],
   'func': [(506, F.TrainWarp_DarkTemplar_screen, ('queued', 'auto'))]},  # tag for WarpprismPhasing/Pylon
  {'name': 'Warp_HighTemplar', 'arg': [],
   'func': [(507, F.TrainWarp_HighTemplar_screen, ('queued', 'auto'))]},  # tag for WarpprismPhasing/Pylon
  {'name': 'Warp_Sentry', 'arg': [],
   'func': [(508, F.TrainWarp_Sentry_screen, ('queued', 'auto'))]},  # tag for WarpprismPhasing/Pylon
  {'name': 'Warp_Stalker', 'arg': [],
   'func': [(509, F.TrainWarp_Stalker_screen, ('queued', 'auto'))]},  # tag for WarpprismPhasing/Pylon
  {'name': 'Warp_Zealot', 'arg': [],
   'func': [(510, F.TrainWarp_Zealot_screen, ('queued', 'auto')), ]},  # tag for WarpprismPhasing/Pylon
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
   'func': [(573, F.llm_pysc2_move_camera, ('world_tag')), (573, F.llm_pysc2_move_camera, ('world_tag')),
            (65, F.Build_Nexus_screen, ('queued', 'screen_tag'))]},
  # tag for Vespene Geyser
  {'name': 'Build_Assimilator_Near', 'arg': ['tag'],
   'func': [(573, F.llm_pysc2_move_camera, ('world_tag')), (573, F.llm_pysc2_move_camera, ('world_tag')),
            (40, F.Build_Assimilator_screen, ('queued', 'screen_tag'))]},
  # {'name': 'Build_Nexus_Screen', 'arg': ['screen'],
  #  'func': [(65, F.Build_Nexus_screen, ('queued', 'screen'))]},
  # {'name': 'Build_Assimilator_Screen', 'arg': ['screen'],
  #  'func': [(40, F.Build_Assimilator_screen, ('queued', 'screen'))]},
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
  {'name': 'Build_Nexus', 'arg': [],
   'func': [(65, F.Build_Nexus_screen, ('queued', 'screen_tag'))]},
  # tag for Vespene Geyser
  {'name': 'Build_Assimilator', 'arg': [],
   'func': [(40, F.Build_Assimilator_screen, ('queued', 'screen_tag'))]},
  # tag for WarpprismPhasing/Pylon
  {'name': 'Build_Pylon', 'arg': [],
   'func': [(70, F.Build_Pylon_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_Gateway', 'arg': [],
   'func': [(57, F.Build_Gateway_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_CyberneticsCore', 'arg': [],
   'func': [(48, F.Build_CyberneticsCore_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_Forge', 'arg': [],
   'func': [(55, F.Build_Forge_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_PhotonCannon', 'arg': [],
   'func': [(69, F.Build_PhotonCannon_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_ShieldBattery', 'arg': [],
   'func': [(525, F.Build_ShieldBattery_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_TwilightCouncil', 'arg': [],
   'func': [(101, F.Build_TwilightCouncil_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_TemplarArchive', 'arg': [],
   'func': [(100, F.Build_TemplarArchive_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_DarkShrine', 'arg': [],
   'func': [(49, F.Build_DarkShrine_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_Stargate', 'arg': [],
   'func': [(88, F.Build_Stargate_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_FleetBeacon', 'arg': [],
   'func': [(54, F.Build_FleetBeacon_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_RoboticsBay', 'arg': [],
   'func': [(81, F.Build_RoboticsBay_screen, ('queued', 'screen_tag'))]},
  {'name': 'Build_RoboticsFacility', 'arg': [],
   'func': [(82, F.Build_RoboticsFacility_screen, ('queued', 'screen_tag'))]},
]
PROTOSS_ACTION_EASY_CONTROL = [
  {'name': 'All_Units_Attack', 'arg': [], 'func': [(0, F.no_op, ())]},
  {'name': 'All_Units_Concentrate', 'arg': [], 'func': [(0, F.no_op, ())]},
  {'name': 'All_Units_Retreat', 'arg': [], 'func': [(0, F.no_op, ())]},
  {'name': 'Worker_Scan', 'arg': [], 'func': [(0, F.no_op, ())]},
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
   'func': [(573, F.llm_pysc2_move_camera, ('world_tag')),
            (527, F.Effect_ChronoBoostEnergyCost_screen, ('queued', 'screen_tag'))]},
  {'name': 'Ability_NexusMassRecall_Near', 'arg': ['tag'],
   'func': [(573, F.llm_pysc2_move_camera, ('world_tag')),
            (529, F.Effect_MassRecall_Nexus_screen, ('queued', 'screen_tag'))]},
  {'name': 'Ability_MothershipMassRecall_Near', 'arg': ['tag'],
   'func': [(573, F.llm_pysc2_move_camera, ('world_tag')),
            (208, F.Effect_MassRecall_screen, ('queued', 'screen_tag'))]},
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

STANDARD_ACTION_STALKER = PROTOSS_BASIC_ACTION_2 + [
  {'name': 'Ability_Blink_Screen', 'arg': ['screen'],
   'func': [(180, F.Effect_Blink_screen, ('now', 'screen'))]},
  {'name': 'Select_Unit_Blink_Screen', 'arg': ['tag', 'screen'],
   'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
            (180, F.Effect_Blink_screen, ('now', 'screen'))]},
]
SCANNING_ACTION_PROBE = PROTOSS_BASIC_ACTION_2 + [
  {'name': 'Lock_Nexus_Near', 'arg': ['tag'],
   'func': [(70, F.Build_Pylon_screen, ('queued', 'screen_tag'))]},
  {'name': 'Lock_Assimilator_Near', 'arg': ['tag'],
   'func': [(40, F.Build_Assimilator_screen, ('queued', 'screen_tag'))]},
]
STANDARD_ACTION_OBSERVER1 = [
  {'name': 'Move_Minimap', 'arg': ['minimap'], 'func': [(332, F.Move_minimap, ('queued', 'minimap'))]},
  {'name': 'Move_Screen', 'arg': ['screen'], 'func': [(331, F.Move_screen, ('queued', 'screen'))]},
  {'name': 'Morph_SurveillanceMode', 'arg': [], 'func': [(538, F.Morph_SurveillanceMode_quick, ('queued'))]},
]
STANDARD_ACTION_OBSERVER2 = [
  {'name': 'Continuously_Monitor_Here', 'arg': [], 'func': [(0, F.no_op, ())]},
  {'name': 'Morph_ObserverMode', 'arg': [], 'func': [(535, F.Morph_ObserverMode_quick, ('queued'))]},
]
STANDARD_ACTION_HIGHTEMPLAR = PROTOSS_BASIC_ACTION_2 + [
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
]
STANDARD_ACTION_DISRUPTOR = PROTOSS_BASIC_ACTION_3 + [
  {'name': 'Ability_PurificationNova_Attack_Unit', 'arg': ['tag'],
   'func': [(219, F.Effect_PurificationNova_screen, ('queued', 'screen_tag'))]},
]
STANDARD_ACTION_SENTRY = PROTOSS_BASIC_ACTION_2 + [
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
]
STANDARD_ACTION_MOTHERSHIP = PROTOSS_BASIC_ACTION_3 + [
  # Ability_CloakingField not supported in pysc2
  # Ability_MothershipMassRecall not neccessary in simple combat tasks
  # {'name': 'Ability_MothershipMassRecall_Near', 'arg': ['tag'],
  #  'func': [(573, F.llm_pysc2_move_camera, ('world_tag')), (208, F.Effect_MassRecall_screen, ('queued', 'screen_tag'))]},
  {'name': 'Ability_TimeWarp_Attack', 'arg': ['tag'],
   'func': [(241, F.Effect_TimeWarp_screen, ('queued', 'screen_tag'))]},
  {'name': 'Ability_TimeWarp_Screen', 'arg': ['screen'],
   'func': [(241, F.Effect_TimeWarp_screen, ('queued', 'screen'))]},
]
STANDARD_ACTION_DARKTEMPLAR = PROTOSS_BASIC_ACTION_2 + [
  {'name': 'Ability_ShadowStride_Unit', 'arg': ['tag'],
   'func': [(182, F.Effect_ShadowStride_screen, ('queued', 'screen_tag'))]},
  {'name': 'Morph_Archon', 'arg': [],
   'func': [(296, F.Morph_Archon_quick, ('queued'))]},
  {'name': 'Select_Two_Unit_Morph_Archon', 'arg': ['tag', 'tag'],
   'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
            (3, F.select_rect, ('add', 'screen1_tag2', 'screen2_tag2')),  # screen1/2_tag2 not realized yet
            (296, F.Morph_Archon_quick, ('queued'))]},
]
STANDARD_ACTION_ADEPT = PROTOSS_BASIC_ACTION_2 + [
  # {'name': 'Ability_AdeptPhaseShift_Screen', 'arg': ['screen'],
  #  'func': [(177, F.Effect_AdeptPhaseShift_screen, ('now', 'screen'))]},
  {'name': 'Ability_AdeptPhaseShift_Minimap', 'arg': ['minimap'],
   'func': [(547, F.Effect_AdeptPhaseShift_minimap, ('now', 'minimap'))]},
  {'name': 'Ability_CancelPhaseShift', 'arg': [], 'func': [(141, F.Cancel_AdeptPhaseShift_quick, ('now'))]},
]
STANDARD_ACTION_ORACLE = PROTOSS_BASIC_ACTION_2 + [
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
]
STANDARD_ACTION_PHOENIX = PROTOSS_BASIC_ACTION_2 + [
  # {'name': 'Ability_GravitonBeam_Unit', 'arg': ['tag'],
  #  'func': [(196, F.Effect_GravitonBeam_screen, ('queued', 'screen_tag'))]},
  {'name': 'Select_Phoenix_Ability_GravitonBeam_Unit', 'arg': ['tag', 'tag'],
   'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
            (196, F.Effect_GravitonBeam_screen, ('queued', 'screen_tag2'))]},
  {'name': 'Cancel_GravitonBeam_For_Phoenix', 'arg': ['tag'],
   'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
            (140, F.Cancel_quick, ('now'))]},
]
STANDARD_ACTION_WARPPRISM = PROTOSS_BASIC_ACTION_3 + [
  {'name': 'Morph_WarpPrismPhasingMode', 'arg': [],
   'func': [(329, F.Morph_WarpPrismPhasingMode_quick, ('queued'))]},
  {'name': 'Load_Unit', 'arg': ['tag'], 'func': [(287, F.Load_screen, ('queued', 'screen_tag'))]},
  {'name': 'Unload_Screen', 'arg': ['screen'],
   'func': [(516, F.UnloadAllAt_screen, ('queued', 'screen'))]},
]
STANDARD_ACTION_WARPPRISMPHASING = [
  {'name': 'Wait_For_Unit_Warp', 'arg': [], 'func': [(0, F.no_op, ())]},
  {'name': 'Morph_WarpPrismTransportMode', 'arg': [],
   'func': [(330, F.Morph_WarpPrismTransportMode_quick, ('queued'))]},
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


def check_weapon_state(obs, queued, source_unit_tag, strict=False):
  weapon_ready_unit_tags = []
  cooldown_time_limit = 0 if strict else 0.5
  if queued == 'queued':
    return True
  else:
    for unit in obs.observation.feature_units:
      if unit.is_selected and unit.weapon_cooldown <= cooldown_time_limit:
        weapon_ready_unit_tags.append(unit.tag)
    if (source_unit_tag is not None and source_unit_tag in weapon_ready_unit_tags) or \
        (source_unit_tag is None and len(weapon_ready_unit_tags) > 0):
      return True
    return False


def is_valid_screen_range(obs, screen, size_screen) -> (int, int, int, int):
  arr = obs.observation.feature_screen.buildable
  arr_t = arr.T
  edge_l, edge_r = 0, size_screen - 1
  edge_b, edge_u = size_screen - 1, 0  # y++ from up to down
  for i in range(size_screen):
    x1, y1 = i, i
    x2, y2 = size_screen - 1 - i, size_screen - 1 - i
    if x1 >= x2:
      break
    edge_u = y1 if (edge_u == y1 - 1 and sum(arr[y1][:]) == 0) else edge_u
    edge_b = y2 if (edge_b == y2 + 1 and sum(arr[y2][:]) == 0) else edge_b
    edge_l = x1 if (edge_l == x1 - 1 and sum(arr_t[x1][:]) == 0) else edge_l
    edge_r = x2 if (edge_r == x2 + 1 and sum(arr_t[x2][:]) == 0) else edge_r
  edge_b = edge_b if edge_b == size_screen - 1 else edge_b - int(size_screen / 8)  # /8 3s_vs_3z
  edge_u = edge_u if edge_u == 0 else edge_u + int(size_screen / 8)
  edge_l = edge_l if edge_l == 0 else edge_l + int(size_screen / 8)
  edge_r = edge_r if edge_r == size_screen - 1 else edge_r - int(size_screen / 8)
  return edge_l, edge_r, edge_u, edge_b


# Parameter verification
def get_arg_minimap(obs, minimap: list, size_minimap, action_name) -> (tuple, bool):  # 小地图坐标，校验范围
  if isinstance(minimap, list) and len(minimap) == 2 and isinstance(minimap[0], (int, float)) and isinstance(minimap[1],
                                                                                                             (int,
                                                                                                              float)):
    x = int(min(max(0, minimap[0]), size_minimap))
    y = int(min(max(0, minimap[1]), size_minimap))
    if 'Attack' in action_name and obs.observation.feature_minimap.player_relative[x][y] in [1, 2]:
      return f'minimap ({x}, {y}) is alliance, can not attack alliance', False
    if 'Load' in action_name and obs.observation.feature_minimap.player_relative[x][y] not in [1, 2]:
      return f'minimap ({x}, {y}) is not alliance, can not load the target', False
    if 'Follow' in action_name and obs.observation.feature_minimap.player_relative[x][y] not in [1, 2]:
      return f'minimap ({x}, {y}) is not alliance, can not follow the target', False
    # there is no need for Move_Minimap action due to pretreatment
    return (x, y), True
  return f'input arg error: minimap={minimap}', False


# Parameter verification
def get_arg_screen(obs, screen: list, size_screen, action_name) -> (tuple, bool):  # 屏幕坐标，校验范围
  if isinstance(screen, list) and len(screen) == 2 and isinstance(screen[0], (int, float)) and isinstance(screen[1],
                                                                                                          (int, float)):
    x = int(min(max(0, screen[0]), size_screen))
    y = int(min(max(0, screen[1]), size_screen))
    ratio = size_screen / SCREEN_WORLD_GRID
    if 'Attack' in action_name and obs.observation.feature_screen.player_relative[x][y] in [1, 2]:
      return f'screen ({x}, {y}) is alliance, can not attack alliance', False
    if 'Load' in action_name and obs.observation.feature_screen.player_relative[x][y] not in [1, 2]:
      return f'screen ({x}, {y}) is not alliance, can not load the target', False
    if 'Follow' in action_name and obs.observation.feature_screen.player_relative[x][y] not in [1, 2]:
      return f'screen ({x}, {y}) is not alliance, can not follow the target', False
    if 'Move' in action_name:
      x1, x2, y1, y2 = is_valid_screen_range(obs, [x, y], size_screen)
      if not ((x1 <= x <= x2) or (y1 <= y <= y2)):
        return f'Move failed! x({int(x / ratio)}) and y({int(y / ratio)}) coordinate exceeds the boundary, valid ranges are **{int(x1 / ratio)}<x<{int(x2 / ratio)}**, **{int(y1 / ratio)}<y<{int(y2 / ratio)}**', False
      if not (x1 <= x <= x2):
        return f"Move failed! x({int(x / ratio)}) exceeds the boundary, valid range is **{int(x1 / ratio)}<x<{int(x2 / ratio)}**", False
      if not (y1 <= y <= y2):
        return f"Move failed! y({int(y / ratio)}) exceeds the boundary, valid range is **{int(y1 / ratio)}<y<{int(y2 / ratio)}**", False
    return (x, y), True
  return f'input arg error: screen={screen}', False


# Parameter verification, for build
def get_arg_screen_build(obs, screen: list, size_screen, action_name, easy_build=False, tag=None, max_retry=600) -> (
tuple, bool):  # 标准建造，校验地点和建造条件
  pos00 = [0, 0]
  if easy_build:
    building_name = action_name.split('Build_')[1]
    building_size = find_building_size(building_name)
    for unit in obs.observation.raw_units:
      if tag is not None and unit.tag == tag:
        pos00 = [unit.x, unit.y]
  else:
    building_name = action_name.split('Build_')[1].split('_Screen')[0]
    building_size = find_building_size(building_name)

  if building_size == 0:
    return f'Do not find the building named as {building_name}, action_name: {action_name}', False

  if isinstance(screen, list) and len(screen) == 2 and isinstance(screen[0], (int, float)) and isinstance(screen[1],
                                                                                                          (int, float)):
    x00 = int(min(max(0.1 * size_screen, screen[0] + 0 * (random.randint(0, 10) - 5)), 0.9 * size_screen))
    y00 = int(min(max(0.1 * size_screen, screen[1] + 0 * (random.randint(0, 10) - 5)), 0.9 * size_screen))
    ratio = size_screen / SCREEN_WORLD_GRID
    pysc2_arg0, func_valid0 = 'unknown error in arg', False

    screen_m_pos, screen_g_pos, screen_base_pos, screen_pylon_pos, = [], [], [], []
    screen_building1_pos, screen_building2_pos, screen_building3_pos, screen_building5_pos = [], [], [], []
    pylon_in_construction = []
    unit_list = obs.observation.raw_units if easy_build else obs.observation.feature_units
    ratio_ = 1. if easy_build else ratio

    for unit in unit_list:
      if not unit.is_on_screen:
        continue
      if unit.unit_type in MINERAL_TYPE:
        screen_m_pos.append([unit.x / ratio_, unit.y / ratio_])
        screen_building2_pos.append([unit.x / ratio_, unit.y / ratio_])
      if (unit.unit_type in GAS_BUILDING_TYPE and unit.alliance in [1]) or unit.unit_type in GAS_TYPE:
        screen_g_pos.append([unit.x / ratio_, unit.y / ratio_])
        screen_building3_pos.append([unit.x / ratio_, unit.y / ratio_])
      if unit.unit_type in BASE_BUILDING_TYPE and unit.alliance in [1]:
        screen_base_pos.append([unit.x / ratio_, unit.y / ratio_])
      if unit.unit_type == units.Protoss.Pylon and unit.alliance in [1]:
        screen_pylon_pos.append([unit.x / ratio_, unit.y / ratio_])
        if unit.build_progress != 100:
          pylon_in_construction.append(unit)
      if unit.unit_type in BUILDING_TYPE:
        unit_name = str(units.get_unit_type(unit.unit_type)).split('.')[-1] if len(
          str(unit.unit_type).split('.')) > 0 else ''
        pos = [unit.x / ratio_, unit.y / ratio_]
        print(f"unit_name={unit_name} pos={pos}")
        if find_building_size(unit_name) == 1:
          screen_building1_pos.append(pos)
        if find_building_size(unit_name) == 2:
          screen_building2_pos.append(pos)
        if find_building_size(unit_name) == 3:
          screen_building3_pos.append(pos)
        if find_building_size(unit_name) == 5:
          screen_building5_pos.append(pos)

    for retry in range(max_retry):
      # r = 12 - retry // 12 - 3 * random.random() if building_name in ['Pylon']
      # rad = 2 * math.pi * random.random()  #  * random.random()  * ((retry % 20) / 20)
      # r = 11 - retry // n - 2 * random.random() if easy_build else retry // n
      # rad = ((retry % n) / n) * math.pi * 2
      if easy_build:
        length, r, rad = SCREEN_WORLD_GRID, 0, 0
        i0, j0 = (0, 0) if retry == 0 else (length * (random.random() - 0.5), length * (random.random() - 0.5))
        # n = max_retry // 10
        # r = 3 * random.random() + retry // n
        # rad = 2 * math.pi * random.random()
        # i0, j0 = (0, 0) if retry == 0 else (r * math.cos(rad), r * math.sin(rad))
        if building_name in ['Pylon']:
          r = 12 - retry // 12 - 3 * random.random()
          rad = 2 * math.pi * random.random()  # * random.random()  * ((retry % 20) / 20)
          i0, j0 = (0, 0) if retry == 0 else (r * math.cos(rad), r * math.sin(rad))
      else:
        n = max_retry // 10
        r = 1 * random.random() + retry // n
        rad = 2 * math.pi * random.random()
        i0, j0 = (0, 0) if retry == 0 else (r * math.cos(rad), r * math.sin(rad))

        # length, r, rad = SCREEN_WORLD_GRID, 0, 0
        # i0, j0 = (0, 0) if retry == 0 else (length * (random.random() - 0.5), length * (random.random() - 0.5))
        # if building_name in ['Pylon']:
        #   r = 12 - retry // 12 - 3 * random.random()
        #   rad = 2 * math.pi * random.random()  # * random.random()  * ((retry % 20) / 20)
        #   i0, j0 = (0, 0) if retry == 0 else (r * math.cos(rad), r * math.sin(rad))

      # x0 = int(min(max(0.1 * size_screen, x00 + ratio * i0), 0.9 * size_screen))
      # y0 = int(min(max(0.1 * size_screen, y00 + ratio * j0), 0.9 * size_screen))
      # x1_ = int(min(max(0.1 * size_screen, x0 - ratio * (1 + building_size / 2)), 0.9 * size_screen))
      # y1_ = int(min(max(0.1 * size_screen, y0 - ratio * (1 + building_size / 2)), 0.9 * size_screen))
      # x2_ = int(min(max(0.1 * size_screen, x0 + ratio * (1 + building_size / 2)), 0.9 * size_screen))
      # y2_ = int(min(max(0.1 * size_screen, y0 + ratio * (1 + building_size / 2)), 0.9 * size_screen))
      x0 = int(x00 + ratio * i0)
      y0 = int(y00 + ratio * j0)
      x1_ = int(x0 - ratio * (building_size // 2))
      y1_ = int(y0 - ratio * (building_size // 2))
      x2_ = int(x0 + ratio * (building_size // 2))
      y2_ = int(y0 + ratio * (building_size // 2))
      pysc2_arg, func_valid = (x0, y0), True
      down_bound, up_bound = (0, size_screen - 1) if building_size < 3 else (0.05 * size_screen, 0.95 * size_screen - 1)

      if not (down_bound < min(x0, y0, x1_, y1_, x2_, y2_) and max(x0, y0, x1_, y1_, x2_, y2_) < up_bound):
        pysc2_arg, func_valid = 'position out of boundary', False
        continue
      x1, x2, y1, y2 = is_valid_screen_range(obs, [x0, y0], size_screen)

      if building_name in POWER_BUILDING_NAMES and obs.observation.feature_screen.power[x0][y0] == 0:
        pysc2_arg, func_valid = f'Build failed! ({int(x0 / ratio)}, {int(y0 / ratio)}) is not in power field, you need to build Pylon first or build near an existing Pylon', False
      if building_name in CREEP_BUILDING_NAMES and obs.observation.feature_screen.creep[x0][y0] == 0:
        pysc2_arg, func_valid = f'Build failed! ({int(x0 / ratio)}, {int(y0 / ratio)}) is not in creep, you need to create creep tumor by Queen', False

      pos0 = [pos00[0] + i0, pos00[1] + j0] if easy_build else [x0 / ratio_, y0 / ratio_]
      d1, d2 = get_dis_pos_poses1(pos0, screen_base_pos, 'min')[0], get_dis_pos_poses1(pos0, screen_m_pos, 'min')[0]
      d3, d4 = get_dis_pos_poses1(pos0, screen_g_pos, 'min')[0], get_dis_pos_poses1(pos0, screen_pylon_pos, 'min')[0]
      db1 = get_dis_pos_poses1_manhattan(pos0, screen_building1_pos, flag='min', axis='xy_max')[0]
      db2 = get_dis_pos_poses1_manhattan(pos0, screen_building2_pos, flag='min', axis='xy_max')[0]
      db3 = get_dis_pos_poses1_manhattan(pos0, screen_building3_pos, flag='min', axis='xy_max')[0]
      db5 = get_dis_pos_poses1_manhattan(pos0, screen_building5_pos, flag='min', axis='xy_max')[0]
      db2_pylon = get_dis_pos_poses1_manhattan(pos0, screen_pylon_pos, flag='min', axis='xy_max')[0]

      if func_valid and 0 < db1 < (building_size + 1) / 2:
        pysc2_arg, func_valid = f"Build failed! Too close to another building", False
      if func_valid and 0 < db2 < (building_size + 2) / 2:
        pysc2_arg, func_valid = f"Build failed! Too close to another building", False
      if func_valid and 0 < db3 < (building_size + 3) / 2:
        pysc2_arg, func_valid = f"Build failed! Too close to another building", False
      if func_valid and 0 < db5 < (building_size + 5) / 2:
        pysc2_arg, func_valid = f"Build failed! Too close to another building", False
      if func_valid and (0 < d1 + d2 < 9):
        pysc2_arg, func_valid = f"Build failed! This location obstructs mining minerals", False
      if func_valid and (0 < d1 + d3 < 9):
        pysc2_arg, func_valid = f"Build failed! This location obstructs mining gas", False
      if func_valid and building_name in POWER_BUILDING_NAMES:
        if len(screen_pylon_pos) != 0 and not 2.5 < d4 < 5.5:  # 2.5 < d4 < 5.5
          pysc2_arg, func_valid = f"Build failed! Too far away from a Pylon", False
      # if func_valid and building_name in POWER_BUILDING_NAMES:
      #   if len(screen_pylon_pos) != 0 and not 0 < db2_pylon < 6:  # 2.5 < d4 < 5.5     0 < db2_pylon < 6
      #     pysc2_arg, func_valid = f"Build failed! Too far away from a Pylon", False
      if func_valid and building_name == 'Pylon':
        supply = 7 * len(pylon_in_construction) + obs.observation.player.food_cap - obs.observation.player.food_used
        if len(screen_pylon_pos) != 0 and 0 <= d4 < 6 and len(screen_pylon_pos) / len(
            screen_base_pos) < 6:  # len(screen_pylon_pos) / len(screen_base_pos) < 6
          pysc2_arg, func_valid = f"Build failed! Too close to another Pylon", False
        if 0 < obs.observation.player.food_cap <= 75 and supply > 20 and obs.observation.player.minerals < 300:
          pysc2_arg, func_valid = f"Build failed! Too Many Pylon", False
        if 75 < obs.observation.player.food_cap < 125 and supply > 25 and obs.observation.player.minerals < 500:
          pysc2_arg, func_valid = f"Build failed! Too Many Pylon", False
        if 125 <= obs.observation.player.food_cap < 200 and supply > 50 and obs.observation.player.minerals < 1000:
          pysc2_arg, func_valid = f"Build failed! Too Many Pylon", False
        if obs.observation.player.food_cap == 200 and len(screen_pylon_pos) / len(screen_base_pos) > 6:
          pysc2_arg, func_valid = f"Build failed! Too Many Pylon", False

      for i in range(building_size + 1):
        for j in range(building_size + 1):
          if not func_valid:
            continue
          x = int(x1_ + i * ratio)
          y = int(y1_ + j * ratio)
          # x = int(x0 + i * ratio)
          # y = int(y0 + j * ratio)
          # x = int(min(max(0, x), size_screen - 1))
          # y = int(min(max(0, y), size_screen - 1))

          down_bound, up_bound = (0.03 * size_screen, 0.97 * size_screen - 1) if building_size < 3 else (
          0.05 * size_screen, 0.95 * size_screen - 1)
          if func_valid and not (down_bound < x < up_bound and down_bound <= y < up_bound):
            pysc2_arg, func_valid = 'out of boundary', False
          # if not (x1 <= x <= x2 or y1 <= y <= y2):
          #   pysc2_arg, func_valid = f'Build failed! x({int(x / ratio)}) and y({int(y / ratio)}) coordinate exceeds the boundary, valid ranges are {int(x1 / ratio)} < x < {int(x2 / ratio)}, {int(y1 / ratio)} < y < {int(y2 / ratio)}', False
          # if not x1 <= x <= x2:
          #   pysc2_arg, func_valid = f"Build failed! x({int(x / ratio)}) exceeds the boundary, valid range is {int(x1 / ratio)} < x < {int(x2 / ratio)}", False
          # if not y1 <= y <= y2:
          #   pysc2_arg, func_valid = f"Build failed! y({int(y / ratio)}) exceeds the boundary, valid range is {int(y1 / ratio)} < y < {int(y2 / ratio)}", False
          if func_valid and obs.observation.feature_screen.buildable[x][y] != 1:
            pysc2_arg, func_valid = f'Build failed! Area near ({int(x0 / ratio)}, {int(y0 / ratio)}) not buildable', False
          if func_valid and obs.observation.feature_screen.pathable[x][y] != 1:
            pysc2_arg, func_valid = f'Build failed! Area near ({int(x0 / ratio)}, {int(y0 / ratio)}) not pathable', False
          if func_valid and obs.observation.feature_screen.player_relative[x][y] not in [0, 1]:
            pysc2_arg, func_valid = f'Build failed! Area near ({int(x0 / ratio)}, {int(y0 / ratio)}) blocked', False
          if func_valid and obs.observation.feature_screen.height_map[x][y] != \
              obs.observation.feature_screen.height_map[x00][y00]:
            pysc2_arg, func_valid = f'Build failed! Area ({int(x0 / ratio)}, {int(y0 / ratio)}) in different height', False
          if func_valid and obs.observation.feature_screen.placeholder[x][y] != 0:
            pysc2_arg, func_valid = f'Build failed! Area near ({int(x0 / ratio)}, {int(y0 / ratio)}) blocked by other building', False
      if func_valid or retry == 0:
        print(f"pos00, pos0, d1, d2, d3, d4 = {pos00}, {pos0}, {d1}, {d2}, {d3}, {d4}")
        print(f"db1, db2, db3, db5, n_pylon = {db1}, {db2}, {db3}, {db5} {screen_pylon_pos}")
        print(
          f"retry {retry}, r = {r}, rad = {rad}, deg = {math.degrees(rad)},  [x00, y00] = [{x00 / ratio}, {y00 / ratio}], [i0, j0] = [{i0}, {j0}], [x0, y0] = [{x0 / ratio}, {y0 / ratio}], pysc2_arg = {pysc2_arg}")
      if retry == 0:
        pysc2_arg0, func_valid0 = pysc2_arg, func_valid
      if not isinstance(pysc2_arg, str):
        return pysc2_arg, func_valid

    return pysc2_arg0, func_valid0
  return f'input arg error: screen={screen}', False


def get_arg_screen_tag_build(obs, tag: int, size_screen, action_name) -> (tuple, bool):
  if action_name == 'Build_Nexus' or action_name == 'Build_Hatchery' or action_name == 'Build_CommandCenter':
    pysc2_arg, func_valid = get_arg_screen_tag_base_building(obs, tag, size_screen, action_name)
  elif action_name == 'Build_Assimilator' or action_name == 'Build_Refinery' or action_name == 'Build_Extractor':
    pysc2_arg, func_valid = get_arg_screen_tag_gas_building(obs, tag, size_screen, action_name)
  else:
    screen, unit_type = None, None
    for unit in obs.observation.feature_units:
      if unit.tag == tag:
        screen = [float(unit.x), float(unit.y)]
        unit_type = unit.unit_type
    # this func only called in easy build mode
    pysc2_arg, func_valid = get_arg_screen_build(obs, screen, size_screen, action_name, easy_build=True, tag=tag)
  if func_valid:
    return pysc2_arg, func_valid
  else:
    return f"auto build position, " + pysc2_arg, func_valid


# Parameter verification, tag to world coordinate
def get_arg_world_tag(obs, tag: int, x_offset, y_offset, world_range) -> (tuple, bool):  # 获取指定tag单位的世界坐标
  for unit in obs.observation.raw_units:
    if unit.tag == tag:
      x = unit.x + x_offset
      y = max(0, world_range - unit.y + y_offset)
      return (x, y), True
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag}', False


def check_attack_target(obs, tag):
  source_unit_types = []
  target_unit_types = []
  available_target_types = []
  target_types = []
  target_unit = None
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.is_on_screen and unit.unit_type not in source_unit_types:
      source_unit_types.append(unit.unit_type)
    if unit.tag == tag and unit.unit_type not in target_unit_types:  # source_unit_types
      target_unit_types.append(unit.unit_type)
      target_unit = unit
  for unit_type in source_unit_types:
    if unit_type in DATA_SC2_UNITS.keys():
      unit_data = DATA_SC2_UNITS[unit_type]
      for available_target_type in unit_data['target']:
        if available_target_type not in available_target_types:
          available_target_types.append(available_target_type)
  for unit_type in target_unit_types:
    if unit_type in DATA_SC2_UNITS.keys():
      unit_data = DATA_SC2_UNITS[unit_type]
      for target_type in unit_data['target_self']:
        if target_type not in target_types:
          target_types.append(target_type)
  # print(available_target_types, target_types)
  if target_unit is not None:
    if target_unit.buff_id_0 in BUFF_TO_TARGET_TYPE.keys() and BUFF_TO_TARGET_TYPE[
      target_unit.buff_id_0] in available_target_types:
      return True, f''
    if target_unit.buff_id_1 in BUFF_TO_TARGET_TYPE.keys() and BUFF_TO_TARGET_TYPE[
      target_unit.buff_id_1] in available_target_types:
      return True, f''
  if 'ground' in target_types and 'air' not in target_types and 'ground' not in available_target_types:
    return False, f'Must target air unit'
  if 'air' in target_types and 'ground' not in target_types and 'air' not in available_target_types:
    return False, f'Must target ground unit'
  return True, f''
  # for target_type in target_types:
  #   if target_type in available_target_types:
  #     return True, available_target_types, target_types
  # return False, available_target_types, target_types


# Parameter verification, tag to screen coordinate
def get_arg_screen_tag(obs, tag: int, size_screen, action_name) -> (tuple, bool):  # 获取指定tag单位的屏幕坐标
  for unit in obs.observation.feature_units:
    if unit.tag == tag:
      unit_info = f'unit {hex(tag)}({str(units.get_unit_type(unit.unit_type))})'
      if 'Attack' in action_name:
        if unit.alliance in [1, 2]:
          return f'{unit_info} is alliance', False
        target_can_be_attack, error_info = check_attack_target(obs, tag)
        if not target_can_be_attack:
          return f'{error_info}: {unit_info}', False
      if 'Load' in action_name and unit.alliance not in [1]:
        return f'{unit_info} is not alliance', False
      if 'Follow' in action_name and unit.alliance not in [1, 2]:
        return f'{unit_info} is not alliance', False
      if 'MassRecall' in action_name and unit.alliance not in [1]:
        return f'{unit_info} is not alliance', False
      if 'Chrono_Boost' in action_name and (unit.alliance not in [1] or unit.unit_type not in BOOSTABLE_TYPE):
        return f'{unit_info} is not boostable', False
      if 'Board_' in action_name and (unit.alliance not in [1] or unit.unit_type not in TRANSPORTER_TYPE):
        return f'{unit_info} is not a transporter', False
      if unit.is_on_screen and (0 < unit.x < size_screen and 0 < unit.y < size_screen):
        return (unit.x, unit.y), True
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag} on screen', False


# Parameter verification, tag to rect screen coordinates
def get_arg_screen_tag_sclect_rect(obs, tag: int, size_screen, func_arg_name) -> (tuple, bool):  # 获取指定tag附近单位群的中心坐标
  for unit in obs.observation.feature_units:
    if unit.tag == tag:
      unit_info = f'unit {hex(tag)}({str(units.get_unit_type(unit.unit_type))})'
      if unit.alliance not in [1]:
        return f'{unit_info} is not alliance, can not select the unit', False
      if not (0 < unit.x < size_screen and 0 < unit.y < size_screen):
        return f'{unit_info} ({unit.x}, {unit.y})) not no screen', False
      if func_arg_name == 'screen' and unit.is_on_screen:
        x = max(0, min(int(unit.x - size_screen / 64), size_screen - 1))
        y = max(0, min(int(unit.y - size_screen / 64), size_screen - 1))
        return (x, y), True
      if func_arg_name == 'screen2' and unit.is_on_screen:
        x = max(0, min(int(unit.x + size_screen / 64), size_screen - 1))
        y = max(0, min(int(unit.y + size_screen / 64), size_screen - 1))
        return (x, y), True
  tag = hex(tag) if isinstance(tag, int) else tag
  return f'cannot find unit {tag} on screen', False


# Parameter verification, tag to screen coordinate, for recall
def get_arg_screen_tag_recall(obs, tag: int, size_screen, action_name) -> (tuple, bool):  # 获取指定tag附近单位群的中心坐标
  for unit in obs.observation.feature_units:
    if unit.tag == tag:
      unit_info = f'unit {hex(unit.tag)}({str(units.get_unit_type(unit.unit_type))})'
      if unit.alliance not in [1]:
        return f'{unit_info} is not alliance', False
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
      unit_info = f'unit {hex(unit.tag)}({str(units.get_unit_type(unit.unit_type))})'
      if unit.unit_type not in [units.Protoss.Pylon, units.Protoss.WarpPrismPhasing]:
        return f'{unit_info} is not Pylon(60) or WarpPrismPhasing(136)', False
      elif unit.alliance not in [1]:
        return f'{unit_info} is not alliance', False
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
      unit_info = f'unit {hex(unit.tag)}({str(units.get_unit_type(unit.unit_type))})'
      base_nearby = False
      for unit_ in obs.observation.raw_units:
        if unit_.alliance == features.PlayerRelative.SELF and unit_.unit_type in BASE_BUILDING_TYPE and \
            math.sqrt((unit_.x - unit_r.x) ** 2 + (unit_.y - unit_r.y) ** 2) < 10:
          base_nearby = True
      if not base_nearby:
        return f'{unit_info} is far away from our base building', False
      if unit.unit_type not in GAS_TYPE:
        return f'{unit_info} is not VespeneGeyser(342 344 608 880 881)', False
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
      unit_info = f'unit {hex(unit.tag)}({str(units.get_unit_type(unit.unit_type))})'
      if unit.unit_type not in GAS_TYPE + MINERAL_TYPE:
        return f'{unit_info} is not VespeneGeyser', False
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
      if not (isinstance(x0, float) and isinstance(y0, float)):
        tag = hex(tag) if isinstance(tag, int) else tag
        return f'unknown error in fing base_building position near unit {tag}', False
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
    mineral_r, mineral_m = 8 * ratio, 1
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
      if unit.unit_type in MINERAL_TYPE and not (7 * ratio < d < 9 * ratio):
        bad = True
      if bad:
        bad_n += 1
    return (x + fx / n), (y + fy / n), bad_n

  building_name = action_name.split('_Screen')[0].split('_')[1]  # Build/Lock
  building_size = find_building_size(building_name)
  for unit in obs.observation.feature_units:
    if unit.tag == tag or (unit.unit_type in GAS_TYPE + MINERAL_TYPE and unit.is_on_screen):
      unit_info = f'unit {hex(unit.tag)}({str(units.get_unit_type(unit.unit_type))})'
      if unit.unit_type not in GAS_TYPE + MINERAL_TYPE:
        return f'{unit_info} is not VespeneGeyser', False
      mineral_gas_list = find_nearby_screen_mg(unit)
      n, x0, y0 = 0, 0, 0
      for mineral in mineral_gas_list:
        n += 1
        x0 += mineral.x
        y0 += mineral.y
      x = x0 / n
      y = y0 / n
      bad_n = len(mineral_gas_list)
      for i in range(32):
        x, y, bad_n = artificial_force_field_iteration_screen(mineral_gas_list, x, y)
      if not (isinstance(x, float) and isinstance(y, float)):
        tag = hex(tag) if isinstance(tag, int) else tag
        return f'unknown error in fing base_building position near unit {tag}', False
      if not ((0 < x < size_screen) and (0 < y < size_screen)):
        return f'unknown error in fing base_building position near unit {tag}', False
      x, y = int(min(max(0., x), size_screen - 1)), int(min(max(0., y), size_screen - 1))
      if bad_n > 1:
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


def tag_for_easy_build_protoss(obs):  # 查找周围空间较大的pylon的screen坐标(先求tag再screen), 然后通过随机坐标甩到周围去
  all_building_list, all_resource_list, base_list, pylon_list = [], [], [], []
  all_building_pos_list, all_resource_pos_list, base_pos_list, pylon_pos_list = [], [], [], []
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF:  # and unit.build_progress == 100
      if unit.unit_type in MINERAL_TYPE + GAS_TYPE + GAS_BUILDING_TYPE:
        all_resource_list.append(unit)
        all_resource_pos_list.append([unit.x, unit.y])
      if unit.unit_type in BUILDING_TYPE:
        all_building_list.append(unit)
        all_building_pos_list.append([unit.x, unit.y])
      if unit.unit_type in BASE_BUILDING_TYPE:
        base_list.append(unit)
        base_pos_list.append([unit.x, unit.y])
      if unit.unit_type in [units.Protoss.Pylon]:
        pylon_list.append(unit)
        pylon_pos_list.append([unit.x, unit.y])

  counts, index = get_nearby_unit_num_of_unit(all_building_pos_list, base_pos_list, r=12, flag='min')
  tag = None if counts == 0 else base_list[index].tag

  if counts <= 8 and tag is not None:
    return tag
  if 8 < counts <= 16 and tag is not None:
    return base_list[random.randint(0, len(base_list) - 1)].tag
  if counts > 16 and tag is not None:
    unit_pos_list = all_resource_pos_list + all_resource_pos_list + all_building_pos_list
    counts, index = get_nearby_unit_num_of_unit(unit_pos_list, pylon_pos_list, r=7, flag='min')
    tag = None if counts == 0 else pylon_list[index].tag
    if 1 < counts < 4:
      return tag
    else:
      return base_list[random.randint(0, len(base_list) - 1)].tag


def tag_for_easy_build_pylon(obs):  # 查找周围空间较大的nexus的screen坐标(先求tag再screen), 然后通过随机坐标甩到周围去
  base_list, pylon_list = [], []
  base_pos_list, pylon_pos_list = [], []
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF:  # and unit.build_progress == 100
      if unit.unit_type in BASE_BUILDING_TYPE:
        base_list.append(unit)
        base_pos_list.append([unit.x, unit.y])
      if unit.unit_type in [units.Protoss.Pylon]:
        pylon_list.append(unit)
        pylon_pos_list.append([unit.x, unit.y])
  counts, index = get_nearby_unit_num_of_unit(base_pos_list + pylon_pos_list, base_pos_list, r=12, flag='min')
  tag_for_base = None if counts == 0 else base_list[index].tag
  return tag_for_base


def tag_for_easy_build_base(obs):  # 查找最近的nexus坐标，和obs中的函数一个原理
  ves_new_base, ves_near, _, _ = get_ves_for_base_and_gas_building(obs)
  tag_for_base = None if len(ves_new_base) == 0 else ves_new_base[0].tag
  return tag_for_base


def tag_for_easy_build_gas(obs):  # 查找最近的vespene坐标，和obs中的函数一个原理
  ves_new_base, ves_near, _, _ = get_ves_for_base_and_gas_building(obs)
  tag_for_ves = None if len(ves_near) == 0 else ves_near[0].tag
  return tag_for_ves


def tag_for_easy_warp(obs, first_ctrl_base_tag='', first_oppo_base_tag=''):  # 查找距离一矿次远的水晶塔的tag
  first_ctrl_base_pos, first_oppo_base_pos = None, None
  all_unit_list, base_list, pylon_list = [], [], []
  all_unit_tag_list, base_tag_list, pylon_tag_list = [], [], []
  all_unit_pos_list, base_pos_list, pylon_pos_list = [], [], []
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100:
      all_unit_list.append(unit)
      all_unit_tag_list.append(unit.tag)
      all_unit_pos_list.append([unit.x, unit.y])
      if unit.unit_type in BASE_BUILDING_TYPE:
        base_list.append(unit)
        base_tag_list.append(unit.tag)
        base_pos_list.append([unit.x, unit.y])
      if unit.unit_type in [units.Protoss.Pylon, units.Protoss.WarpPrismPhasing]:
        pylon_list.append(unit)
        pylon_tag_list.append(unit.tag)
        pylon_pos_list.append([unit.x, unit.y])
      # if unit.tag == first_ctrl_base_tag:
      #   first_ctrl_base_pos = [unit.x, unit.y]
      # if unit.tag == first_oppo_base_tag:
      #   first_oppo_base_pos = [unit.x, unit.y]

  tag_for_pylon = None
  if tag_for_pylon is None:
    counts, index = get_nearby_unit_num_of_unit(all_unit_pos_list, pylon_pos_list, r=7, flag='min')
    tag_for_pylon = None if counts == 0 else pylon_list[index].tag

  # if first_oppo_base_pos is not None:
  #   d_min, index_min = get_dis_pos_poses1(first_oppo_base_pos, base_pos_list, 'min')
  #   tag_for_pylon = None if d_min == 0 else pylon_list[index_min].tag

  return tag_for_pylon


def tag_for_closest_worker(obs, tag, mining_only=True):
  target_unit = None
  worker_list, worker_pos_list = [], []
  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100:
      if unit.unit_type in WORKER_TYPE:
        if mining_only and unit.order_id_0 in [356, 357, 358, 359, 102, 103, 154, 360, 361, 362]:
          worker_list.append(unit)
          worker_pos_list.append([unit.x, unit.y])
        if not mining_only:
          worker_list.append(unit)
          worker_pos_list.append([unit.x, unit.y])
  for unit in obs.observation.raw_units:
    if unit.tag == tag:
      target_unit = unit
  if target_unit is None or len(worker_list) == 0:
    return None
  pos = [target_unit.x, target_unit.y]
  d_min, index_min = get_dis_pos_poses1(pos, worker_pos_list, flag='min')
  tag_for_worker = None if d_min == 0 else worker_list[index_min].tag
  return tag_for_worker


def tag_for_closest_screen_worker(obs, screen, size_screen, mining_only=True):
  worker_list, worker_pos_list = [], []
  down_bound, up_bound = 0.1 * size_screen, 0.9 * size_screen
  for unit in obs.observation.feature_units:
    if not unit.is_on_screen or not (down_bound < unit.x < up_bound and down_bound < unit.y < up_bound):
      continue
    if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100:
      if unit.unit_type in WORKER_TYPE:
        if mining_only and unit.order_id_0 in [356, 357, 358, 359, 102, 103, 154, 360, 361, 362]:
          worker_list.append(unit)
          worker_pos_list.append([unit.x, unit.y])
        if not mining_only:
          worker_list.append(unit)
          worker_pos_list.append([unit.x, unit.y])

  d_min, index_min = get_dis_pos_poses1(screen, worker_pos_list, flag='min')
  tag_for_worker = None if d_min == 0 else worker_list[index_min].tag
  return tag_for_worker


def add_func_for_build(self, obs, action):
  action_name = action['name']
  action_arg = action['arg']
  action_func = action['func']
  if self.config.ENABLE_EASY_BUILD:
    return action
  if (not 'Build_' in action_name) or ('Near' not in action_name and 'Screen' not in action_name):
    return action
  if not (len(action['func'][0][2]) == 2 and len(action['func'][0][2][1]) == 2):
    print(f"add_func_for_build(): screen = action['func'][0][2][1] = {action['func'][0][2][1]}")
    return action
  print(self.size_screen)
  print(f"add_func_for_build(): screen = action['func'][0][2][1] = {action['func'][0][2][1]}")
  screen = action['func'][0][2][1]
  worker_tag = tag_for_closest_screen_worker(obs, screen, self.size_screen)

  if worker_tag is not None:
    full_shape_action = {'name': action_name, 'arg': [], 'func':
      [(3, F.select_rect, ['select', int(worker_tag), int(worker_tag)]),
       (action['func'][0][0], action['func'][0][1], action['func'][0][2])]}
  else:
    return action

  return full_shape_action


def add_func_for_easy_build(self, obs, action):
  action_name = action['name']
  action_arg = action['arg']
  action_func = action['func']
  if (not 'Build_' in action_name) or (
      'Near' in action_name or 'Screen' in action_name) or not self.config.ENABLE_EASY_BUILD:
    return action

  target_position_tag, worker_tag = None, None
  # print(action_name)
  if action_name == 'Build_Nexus' or action_name == 'Build_Hatchery' or action_name == 'Build_CommandCenter':
    target_position_tag = tag_for_easy_build_base(obs)
  elif action_name == 'Build_Assimilator' or action_name == 'Build_Refinery' or action_name == 'Build_Extractor':
    target_position_tag = tag_for_easy_build_gas(obs)
  elif action_name == 'Build_Pylon':
    target_position_tag = tag_for_easy_build_pylon(obs)
  elif self.race == 'protoss':
    target_position_tag = tag_for_easy_build_protoss(obs)
  elif self.race == 'terran':
    # TODO: ADD SUPPORT FOR TERRAN EASY BUILD
    logger.error(f"[ID {self.log_id}] Agent {self.name}, add func for terran EASY BUILD actions not realized")
  elif self.race == 'zerg':
    # TODO: ADD SUPPORT FOR ZERG EASY BUILD
    logger.error(f"[ID {self.log_id}] Agent {self.name}, add func for zerg EASY BUILD actions not realized")
  else:
    pass
  worker_tag = tag_for_closest_worker(obs, target_position_tag)

  l = self.size_screen
  dx = int(2 * (random.random() - 0.5) * 0.2 * l)
  dy = int(2 * (random.random() - 0.5) * 0.2 * l)
  # print(target_position_tag)
  # print(worker_tag)
  if target_position_tag is not None and worker_tag is not None:
    full_shape_action = {'name': action_name, 'arg': [], 'func':
      [(573, F.llm_pysc2_move_camera, [int(worker_tag)]),
       (573, F.llm_pysc2_move_camera, [int(worker_tag)]),
       (3, F.select_rect, ['select', int(worker_tag), int(worker_tag)]),
       (573, F.llm_pysc2_move_camera, [int(target_position_tag)]),
       (573, F.llm_pysc2_move_camera, [int(target_position_tag)]),
       (action['func'][0][0], action['func'][0][1], ['now', int(target_position_tag)])]}
  else:
    return action

  return full_shape_action


def add_func_for_easy_warp(self, obs, action):
  pylon_tag = tag_for_easy_warp(obs, self.first_ctrl_base_tag, self.first_oppo_base_tag)
  action_name = action['name']
  action_arg = action['arg']
  action_func = action['func']
  if not ('Warp_' in action_name and 'Near' not in action_name and self.config.ENABLE_EASY_WARP):
    return action

  if pylon_tag is not None:
    full_shape_action = {'name': action['name'], 'arg': [], 'func':
      [(8, F.select_warp_gates, ['select']),
       (573, F.llm_pysc2_move_camera, [int(pylon_tag)]),
       (action['func'][0][0], action['func'][0][1], ['now', int(pylon_tag)])]}
  else:
    full_shape_action = {'name': 'No_Operation', 'arg': [], 'func': [(0, actions.FUNCTIONS.no_op, {})]}

  return full_shape_action


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
    down_bound, up_bound = 0.1 * self.size_screen, 0.9 * self.size_screen
    if unit.alliance == features.PlayerRelative.SELF and unit.unit_type in WORKER_TYPE and \
        unit.is_on_screen and (down_bound < unit.x < up_bound and down_bound < unit.y < up_bound):
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

  # full_shape_action = None
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
       (573, actions.FUNCTIONS.llm_pysc2_move_camera, [int(source_unit_tag)]),
       (2, actions.FUNCTIONS.select_point, ['select', int(source_unit_tag)])] + action['func']}
  else:
    full_shape_action = {'name': 'No_Operation', 'arg': [], 'func':
      [(0, actions.FUNCTIONS.no_op, {})]}

  return full_shape_action


def add_func_for_easy_control(self, obs, action):  # goto enemy base
  action_name = action['name']
  action_arg = action['arg']
  action_func = action['func']
  if not ('All_Units_Attack' in action_name or 'Worker_Scan' in action_name or
          'All_Units_Retreat' in action_name or 'All_Units_Concentrate' in action_name or 'All_Units_Defend' in action_name):
    return action

  n_worker = 0
  for unit in obs.observation.raw_units:
    if unit.unit_type in WORKER_TYPE and unit.alliance == features.PlayerRelative.SELF:
      n_worker += 1

  first_ctrl_base_pos, first_oppo_base_pos = None, None
  target_tag = self.first_oppo_base_tag
  target_tag2 = None  # front line pylon
  all_pylon_list, all_pylon_pos_list = [], []
  all_base_list, all_base_pos_list = [], []
  all_ves_list, all_ves_pos_list = [], []
  for unit in obs.observation.raw_units:
    if unit.unit_type in BASE_BUILDING_TYPE and unit.alliance == features.PlayerRelative.SELF:
      all_base_list.append(unit)
      all_base_pos_list.append([unit.x, unit.y])
    if unit.unit_type == units.Protoss.Pylon and unit.alliance == features.PlayerRelative.SELF:
      all_pylon_list.append(unit)
      all_pylon_pos_list.append([unit.x, unit.y])
    if unit.unit_type in GAS_TYPE:
      all_ves_list.append(unit)
      all_ves_pos_list.append([unit.x, unit.y])
    if unit.tag == self.first_ctrl_base_tag:
      first_ctrl_base_pos = [unit.x, unit.y]
    if unit.tag == self.first_oppo_base_tag:
      first_oppo_base_pos = [unit.x, unit.y]

  if target_tag is None:
    logger.warning(
      f"[ID {self.log_id}] Agent {self.name}, add_func_for_easy_control(): Can not find enemy base, randomly choice a vespene as target for scan or attack")
    target_tag = all_ves_list[random.randint(0, len(all_ves_list) - 1)].tag

  worker_tag = tag_for_closest_worker(obs, target_tag, mining_only=False)

  # if first_ctrl_base_pos is not None:
  #   d_max, index_max = get_dis_pos_poses1(first_ctrl_base_pos, all_pylon_pos_list, flag='max')
  #   target_tag2 = all_pylon_list[index_max].tag if d_max != 0 else self.first_ctrl_base_tag
  if first_oppo_base_pos is not None:
    d_min, index_min = get_dis_pos_poses1(first_oppo_base_pos, all_pylon_pos_list, flag='min')  # front line pylon
    target_tag2 = all_pylon_list[index_min].tag if d_min != 0 else self.first_oppo_base_tag
  else:
    d_max, indexes_max = get_dis_posse1_poses2(all_base_pos_list, all_pylon_pos_list)
    target_tag2 = all_pylon_list[indexes_max[1]].tag if d_max != 0 else self.first_ctrl_base_tag

  full_shape_action = {'name': 'No_Operation', 'arg': [], 'func': [(0, actions.FUNCTIONS.no_op, {})]}
  if ('All_Units_Attack' in action_name):
    supply = obs.observation.player.food_cap - obs.observation.player.food_used
    print(target_tag, target_tag2, worker_tag)
    if target_tag is not None:  # and obs.observation.player.food_used - n_worker > 100 or supply < 10
      full_shape_action = {'name': action_name, 'arg': [], 'func': [
        (7, F.select_army, ['select']),
        (573, F.llm_pysc2_move_camera, [int(target_tag)]),
        (573, F.llm_pysc2_move_camera, [int(target_tag)]),
        (12, F.Attack_screen, ('now', int(target_tag)))]}
  elif ('Worker_Scan' in action_name):
    print(target_tag, target_tag2, worker_tag)
    if target_tag is not None and target_tag2 is not None and worker_tag is not None:
      full_shape_action = {'name': action_name, 'arg': [], 'func':
        [(573, F.llm_pysc2_move_camera, [int(worker_tag)]),
         (573, F.llm_pysc2_move_camera, [int(worker_tag)]),
         (2, F.select_point, ['select', int(worker_tag)]),
         (573, F.llm_pysc2_move_camera, [int(target_tag)]),
         (573, F.llm_pysc2_move_camera, [int(target_tag)]),
         (331, F.Move_screen, ('now', int(target_tag))),
         ]}
  elif (
      'All_Units_Retreat' in action_name or 'All_Units_Concentrate' in action_name or 'All_Units_Defend' in action_name):
    if target_tag2 is not None:
      full_shape_action = {'name': action_name, 'arg': [], 'func': [
        (7, F.select_army, ['select']),
        (573, F.llm_pysc2_move_camera, [int(target_tag2)]),
        (573, F.llm_pysc2_move_camera, [int(target_tag2)]),
        (331, F.Move_screen, ('now', int(target_tag2))),
      ]}
  else:
    full_shape_action = {'name': 'No_Operation', 'arg': [], 'func': [
      (0, actions.FUNCTIONS.no_op, [])]}
  return full_shape_action


# def add_func_for_build_base_and_ves(self, obs, action):
#   action_name = action['name']
#   action_arg = action['arg']
#   action_func = action['func']
#   if not 'Build_' in action_name and ('Nexus' in action_name or 'Assimilator' in action_name):
#     return action
#
#   if isinstance(action_arg, list) and len(action_arg) == 1:
#     full_shape_action = {'name': action_name, 'arg': action_arg, 'func':
#       [(573, actions.FUNCTIONS.llm_pysc2_move_camera, [action_arg[0]])] + action['func']}
#   else:
#     full_shape_action = action
#
#   return full_shape_action


class BaseTranslatorA:

  def __init__(self, name, log_id, config):
    self.name = name
    self.log_id = log_id
    self.config = config
    self.actions = []
    self.action = {}

    self.size_minimap = None
    self.size_screen = None

    # self.ACTION_SPACE = config.AGENTS[name]['action']
    # self.ACTION_SPACE_DICT = {}
    # for unit_type in self.ACTION_SPACE.keys():
    #   for action in self.ACTION_SPACE[unit_type]:
    #     self.ACTION_SPACE_DICT[action['name']] = action

  def translate(self, obs) -> "list of [(func_id, func_call)]":
    pass


# TODO: You can specialize your TranslatorA here


class DefaultTranslatorA(BaseTranslatorA):

  def __init__(self, name, log_id, config):
    super(DefaultTranslatorA, self).__init__(name, log_id, config)
    logger.info(f"[ID {self.log_id}] {name} DefaultTranslatorA initialized")

  # text actions recognition
  def translate(self, raw_text_a: str, obs=None):
    self.action = {'analysis': '', 'actions': ''}

    action_list_dict = {}
    action_lists, action_lists2 = [], []
    team_actions, team_actions2 = [], []
    processed_text_a, team_name, team_names = '', '', []
    self.curr_team_action_list = []
    self.curr_team_action_name_list = []

    lines = raw_text_a.splitlines()
    start_recognize = False
    first_function = True
    first_function_move = True
    first_action_attack = True
    first2_actions_attack = True
    # team_action_name_list = []

    for line in lines:
      line = line.replace('*', '')
      line = line.replace('`', '')
      line = line.replace('- ', '')
      # ACTION PART
      if ("Actions:" in line) or ("Action:" in line) or \
          ("actions:" in line) or ("action:" in line):
        processed_text_a = "Actions:"
        start_recognize = True

      # ANALYSIS PART
      if not start_recognize:
        if 'analysis' not in self.action.keys() and (("Analysis:" in line) or ("analysis:" in line)):
          self.action['analysis'] = line + '\n'
        elif 'analysis' in self.action.keys():
          self.action['analysis'] += line + '\n'
        else:
          pass

      # COMMUNICATION PART
      if ("Communications:" in line) or ("Communication:" in line) or \
          ("communications:" in line) or ("Communication:" in line):
        start_recognize = False

      # ACTION PART, TEAM ACTIONS
      if start_recognize:
        if ("Team" in line and ":" in line) or ("team" in line and ":" in line):

          team_name_old = team_name
          team_name = line.split("eam ")[-1].split(":")[0]  # Team/team xxxx:  -->  xxxx

          self.curr_team_config = {}
          if team_name in self.config.AGENTS[self.name]['team'].keys():
            self.curr_team_config = self.config.AGENTS[self.name]['team'][team_name]
          elif team_name[:-2] in self.config.AGENTS[self.name]['team'].keys():
            self.curr_team_config = self.config.AGENTS[self.name]['team'][team_name[:-2]]  # single select 类型

          if len(self.curr_team_config.keys()) > 0:
            self.curr_team_action_list = []
            self.curr_team_action_name_list = []
            for team_actions_ in self.curr_team_config['actions'].values():
              self.curr_team_action_list += team_actions_
            for team_action in self.curr_team_action_list:
              self.curr_team_action_name_list.append(team_action['name'])  # 可能重复，如同一个小队多个兵种时，可能有多个Move

          # print(self.config.AGENTS[self.name]['team'].keys())
          # print(f"self.curr_team_config = {self.curr_team_config}")
          # print(f"self.curr_team_action_list = {self.curr_team_action_list}")

          # else:
          #   teams_ = self.config.AGENTS[self.name]['team']
          #   teams_unit_types, action_space = [], []
          #   for team_ in teams_:
          #     if team_['name'] == team_name:
          #       teams_unit_types += team_['unit_type']
          #   for unit_type in teams_unit_types:
          #     if unit_type in self.config.AGENTS[self.name]['action']:
          #       action_space += self.config.AGENTS[self.name]['action'][unit_type]
          #   team_action_name_list = [action['name'] for action in action_space]

          processed_text_a += f"\n\tTeam {team_name}:"
          if len(team_actions) != 0:
            action_lists.append(team_actions)
            action_lists2.append(team_actions2)
            action_list_dict[team_name_old] = team_actions
            team_actions, team_actions2 = [], []
            if team_name not in team_names:
              first_function = True
              first_function_move = True
              first_action_attack = True
              first2_actions_attack = True

            team_names.append(team_name)

          # print(f"team_name={team_name}, self.curr_team_action_name_list={self.curr_team_action_name_list}")


        elif "<" in line and ">" in line and '(' in line and ')' in line:
          line.replace('tag=', '')
          line.replace('screen=', '')
          line.replace('minimap=', '')
          try:
            action_text = line.split("<")[1].split(">")[0]
            action_name = action_text.split("(")[0]
            action_args = action_text.split("(")[-1].split(")")[0]
            print(action_text)
          except Exception as e:
            logger.error(f"translator find invalid action in line: {line}")
            continue
          action_valid, tag, tag2, tag3, x, y = True, None, None, None, None, None
          action = {'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]}
          if action_name not in self.curr_team_action_name_list:
            logger.error(f"translator unable to find {action_name} in team_config {self.curr_team_action_list}")
            continue
          if action_name not in self.curr_team_action_name_list:
            logger.error(f"translator unable to find {action_name} in current team config: {self.curr_team_config}")
            continue
          # if not first_action_attack and "Attack" in action_name and \
          #     "Select_Unit" not in action_name and "Ability" not in action_name:
          #   continue
          if not first2_actions_attack and "Attack" in action_name and \
              "Select_Unit" not in action_name and "Ability" not in action_name:
            continue
          if "0x" in action_args:
            tag = int(re.findall(r'0x\w+', action_args)[0], 16)
            if len(re.findall(r'0x\w+', action_args)) > 1:
              tag2 = int(re.findall(r'0x\w+', action_args)[1], 16)
            if len(re.findall(r'0x\w+', action_args)) > 2:
              tag3 = int(re.findall(r'0x\w+', action_args)[2], 16)
          if "[" in action_args:
            ratio = 1 if "Minimap" in action_name else self.size_screen / SCREEN_WORLD_GRID
            try:
              x = float(re.findall(r'\[-?\d+\.?\d*e?-?\d*?', action_args)[0].split("[")[1]) * ratio
              y = float(re.findall(r'-?\d+\.?\d*e?-?\d*?\]', action_args)[0].split("]")[0]) * ratio
            except Exception as e:
              logger.error(f"translator find invalid action in line: {line}")
              continue

          for action_ in self.curr_team_action_list:
            if action_name == action_['name']:
              action = action_

          # # 在动作空间中查找action_name对应的action
          # if action_name in self.ACTION_SPACE_DICT.keys():
          #   action = self.ACTION_SPACE_DICT[action_name]
          # else:
          #   logger.error(f"translator unable to find {action_name}")
          #   action = {'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]}
          #   action_valid = False

          # 将识别出的动作参数填入函数参数元组中
          new_func_triples, new_func_triples2 = [], []
          new_func_triple, new_func_triple2, new_func_args = [], [], []
          for func_triple in action['func']:  # func_triple 形如 (0, F.no_op, ())
            new_func_triple, new_func_triple2, new_func_args = [], [], []
            func_args = func_triple[2]
            if len(list(func_args)) > 0:
              if not isinstance(func_args, tuple):
                func_args = [func_args]
              for arg in list(func_args):
                if arg == 'auto':
                  new_func_args.append('auto')
                if arg == "now":
                  if "Move" not in action_name:
                    new_func_args.append('now')
                  elif "Move" in action_name and (first_function_move or "Select_Unit" in action_name):
                    new_func_args.append('now')
                  else:
                    new_func_args.append('queued')
                if arg == "queued":
                  if first_function:
                    new_func_args.append('now')
                    # if "Build" in action_name or self.name == 'Builder':
                    #   new_func_args.append('queued')
                    #   first_function = False
                    # else:
                    #   new_func_args.append('now')
                  else:
                    new_func_args.append('queued')
                if arg == "select":
                  new_func_args.append('select')
                if arg in ["screen_tag", "minimap_tag", "world_tag", "screen1_tag", "screen2_tag"]:
                  if tag is not None:
                    new_func_args.append(tag)
                  elif 'Build' in action_name and self.config.ENABLE_EASY_BUILD:
                    new_func_args.append('auto')
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
            if 'error' not in new_func_args and first_function_move and 'now' in new_func_args and \
                "Move" in action_name and "Select_Unit" not in action_name:
              first_function_move = False
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

          if 'error' not in new_func_args and not first_action_attack and first2_actions_attack and \
              "Attack" in action_name and "Ability" not in action_name and "Select_Unit" not in action_name:
            first2_actions_attack = False
          if 'error' not in new_func_args and first_action_attack and \
              "Attack" in action_name and "Ability" not in action_name and "Select_Unit" not in action_name:
            first_action_attack = False

          if action_valid:

            team_actions.append({'name': action['name'], 'arg': action_args, 'func': new_func_triples})
            team_actions2.append({'name': action['name'], 'arg': action_args, 'func': new_func_triples2})
            processed_text_a += f"\n\t\t<{action_text}>"
          else:
            team_actions.append({'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]})
            team_actions2.append({'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]})
        else:
          pass

    self.action['actions'] = processed_text_a
    self.actions.append(self.action)

    if self.name == 'Builder':
      team_actions.append({'name': 'HoldPosition-Auto', 'arg': [], 'func': [(274, F.HoldPosition_quick, ('queued',))]})
    if self.name == 'Developer' and obs is not None:
      gateway_list, morph_action_list = [], []
      for unit in obs.observation.raw_units:
        if unit.unit_type == units.Protoss.Gateway and unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100 and unit.active == 0:
          gateway_list.append(unit)

      if upgrades.Upgrades.WarpGateResearch in obs.observation.upgrades and len(gateway_list) > 0:
        a1 = (573, F.llm_pysc2_move_camera, [int(gateway_list[0].tag)])
        a2 = (2, F.select_point, ['select_all_type', int(gateway_list[0].tag)])
        a3 = (328, F.Morph_WarpGate_quick, [])
        team_actions.append({'name': 'Auto_Morph_Warpgate', 'arg': [], 'func': [a1, a2, a3]})
        processed_text_a += '\n\t\t<Auto_Morph_Warpgate()>'

    if len(team_actions) != 0:
      action_lists.append(team_actions)
      action_lists2.append(team_actions2)
      action_list_dict[team_name] = team_actions

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
  from llm_pysc2.cfg import ConfigSmac_2s3z, ProtossAgentConfig

  config = ProtossAgentConfig()

  # ----------------- show action space -----------------
  # def show(config):
  #   for name in config.AGENTS.keys():
  #     # agent_actions = config.AGENTS[name]['action']
  #     agent_actions = {}
  #     for team_config in config.AGENTS[name]['team'].values():
  #       agent_actions[team_config['name']] = {}
  #       for unit_type in team_config['actions'].keys():
  #         agent_actions[team_config['name']][unit_type] = team_config['actions'][unit_type]
  #     print(name)
  #     for team_name in agent_actions.keys():
  #       print(f"\t{team_name}")
  #       for unit_type in agent_actions[team_name].keys():
  #         print(f"\t{str(units.get_unit_type(unit_type))}")
  #         for i in range(len(agent_actions[team_name][unit_type])):
  #           action = agent_actions[team_name][unit_type][i]
  #           if len(action['arg']) == 0:
  #             print(f"\t\t <{action['name']}()>")
  #         for i in range(len(agent_actions[team_name][unit_type])):
  #           action = agent_actions[team_name][unit_type][i]
  #           if len(action['arg']) == 1 and 'minimap' in action['arg']:
  #             print(f"\t\t <{action['name']}({action['arg'][0]})>")
  #         for i in range(len(agent_actions[team_name][unit_type])):
  #           action = agent_actions[team_name][unit_type][i]
  #           if len(action['arg']) == 1 and 'screen' in action['arg']:
  #             print(f"\t\t <{action['name']}({action['arg'][0]})>")
  #         for i in range(len(agent_actions[team_name][unit_type])):
  #           action = agent_actions[team_name][unit_type][i]
  #           if len(action['arg']) == 1 and 'tag' in action['arg']:
  #             print(f"\t\t <{action['name']}({action['arg'][0]})>")
  #         for i in range(len(agent_actions[team_name][unit_type])):
  #           action = agent_actions[team_name][unit_type][i]
  #           if len(action['arg']) == 2:
  #             print(f"\t\t <{action['name']}({action['arg'][0]}, {action['arg'][1]})>")
  # show(config)

  # ----------------- example of TranslatorA -----------------

  # translator = DefaultTranslatorA('CombatGroup0', log_id=0, config=config)
  translator = DefaultTranslatorA('Developer', log_id=0, config=config)
  # translator = DefaultTranslatorA('Builder', log_id=0, config=config)
  text = \
    """
    Analysis:
        We should do xxx and xxx.
    
    Actions:
        Builder-Probe-1:
            <Build_Nexus_Near(0x200ea0001)>
    
    Actions:
        **Team Zealot-1**:
            <Attack_Unit(0x200540001)> 
        Team Zealot-2:
            <Attack_Unit(0x200540001)>
            <Move_Minimap([24, 54])>                              # invalid in smac
        Team Stalker-1:
            <Ability_Blink_Screen([33, 96])>                      # invalid in smac
            <Select_Unit_Blink_Screen(0x1007c0001 ,[33, 96])>     # invalid in smac
            <Move_Screen([2, 9])>
        Team Builder-Probe-1:
            <Build_Pylon_Screen([8, 12])>  # Build the Pylon safely at a screen location, avoiding the Queens' range.
            <Build_Gateway_Screen([10, 12])>  # After the Pylon is completed, build the Gateway at a safe distance.
            <Build_Nexus_Near(0x200ea0001)>
        Team Protoss-Buildings-1:
            <Research_Charge()>
            <Research_Blink()>
            <Train_Stalker()>
            <Warp_Zealot()>
    """

  translator.size_screen = 128
  actions, action_list_dict, processed_text_a = translator.translate(text)

  print(f"\n\ntext to translator:{text}")
  print(f"detected action from translator:\n{actions}\n")
  print(f"action_list_dict from translator:\n{action_list_dict}\n")
  print(f"detected text_a from translator:\n{processed_text_a}\n")

