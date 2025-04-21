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


from llm_pysc2.lib.action.space.basic import *
from pysc2.lib.actions import FUNCTIONS as F


# actions for smac tasks, ACTION_SMAC for tasks that attack is enough
SMAC_ACTION_ZEALOT = [ATTACK_00S]
SMAC_ACTION_STALKER = [ATTACK_02S, MOVE_SCREEN]  #  ,SU_MOVE_SCREEN
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
   'func': [(573, F.llm_pysc2_move_camera, ('world_tag')), (573, F.llm_pysc2_move_camera, ('world_tag')), (65, F.Build_Nexus_screen, ('queued', 'screen_tag'))]},
  # tag for Vespene Geyser
  {'name': 'Build_Assimilator_Near', 'arg': ['tag'],
   'func': [(573, F.llm_pysc2_move_camera, ('world_tag')), (573, F.llm_pysc2_move_camera, ('world_tag')), (40, F.Build_Assimilator_screen, ('queued', 'screen_tag'))]},
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
  # {'name': 'Lock_Nexus_Near', 'arg': ['tag'],
  #  'func': [(70, F.Build_Pylon_screen, ('queued', 'screen_tag'))]},
  # {'name': 'Lock_Assimilator_Near', 'arg': ['tag'],
  #  'func': [(40, F.Build_Assimilator_screen, ('queued', 'screen_tag'))]},
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
  # {'name': 'Lock_Nexus_Near', 'arg': ['tag'],
  #  'func': [(70, F.Build_Pylon_screen, ('queued', 'screen_tag'))]},
  # {'name': 'Lock_Assimilator_Near', 'arg': ['tag'],
  #  'func': [(40, F.Build_Assimilator_screen, ('queued', 'screen_tag'))]},
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