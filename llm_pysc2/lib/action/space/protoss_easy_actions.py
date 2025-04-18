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


from pysc2.lib.actions import FUNCTIONS as F


# Simplified control actions
PROTOSS_ACTION_EASY_CONTROL = [
  {'name': 'All_Units_Attack', 'arg': [], 'func': [(0, F.no_op, ())]},
  {'name': 'All_Units_Defend', 'arg': [], 'func': [(0, F.no_op, ())]},
  {'name': 'All_Units_Retreat', 'arg': [], 'func': [(0, F.no_op, ())]},
  {'name': 'Observer_Scan', 'arg': [], 'func': [(0, F.no_op, ())]},
  {'name': 'Worker_Scan', 'arg': [], 'func': [(0, F.no_op, ())]},
  {'name': 'Zealot_Scan', 'arg': [], 'func': [(0, F.no_op, ())]},
  {'name': 'Adept_Scan', 'arg': [], 'func': [(0, F.no_op, ())]},
]

PROTOSS_ACTION_EASY_CHRONO_BOOST = [
  {'name': 'ChronoBoost_Economy', 'arg': [], 'func': [(0, F.no_op, ())]},
  {'name': 'ChronoBoost_Military', 'arg': [], 'func': [(0, F.no_op, ())]},
  {'name': 'ChronoBoost_Research', 'arg': [], 'func': [(0, F.no_op, ())]},
]

# Simplified warp train actions
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
   'func': [(510, F.TrainWarp_Zealot_screen, ('queued', 'auto'))]},  # tag for WarpprismPhasing/Pylon
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
