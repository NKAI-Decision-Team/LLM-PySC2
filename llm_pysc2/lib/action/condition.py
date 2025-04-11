
from pysc2.lib import units, actions, upgrades

a = actions.FUNCTIONS
u = upgrades.Upgrades


protoss_map_research_quick_to_level = {
  actions.FUNCTIONS.Research_ProtossAirArmor_quick.id: [382, 383, 384],
  actions.FUNCTIONS.Research_ProtossAirWeapons_quick.id: [386, 387, 388],
  actions.FUNCTIONS.Research_ProtossGroundArmor_quick.id: [390, 391, 392],
  actions.FUNCTIONS.Research_ProtossGroundWeapons_quick.id: [394, 395, 396],
  actions.FUNCTIONS.Research_ProtossShields_quick.id: [398, 399, 400],
}
# minerals gas building upgrade time
protoss_research_conditions = {
  # CyberneticsCore BY
  actions.FUNCTIONS.Research_ProtossAirArmorLevel1_quick.id:
    {'m': 100, 'g': 100, 'b': [units.Protoss.CyberneticsCore], 't': 180},  # map from Research_ProtossAirArmor_quick
  actions.FUNCTIONS.Research_ProtossAirWeaponsLevel1_quick.id:
    {'m': 100, 'g': 100, 'b': [units.Protoss.CyberneticsCore], 't': 180},  # map from Research_ProtossAirWeapons_quick
  actions.FUNCTIONS.Research_ProtossAirArmorLevel2_quick.id:
    {'m': 175, 'g': 175, 'b': [units.Protoss.CyberneticsCore, units.Protoss.FleetBeacon], 'u': u.ProtossAirArmorsLevel1, 't': 215},
  actions.FUNCTIONS.Research_ProtossAirWeaponsLevel2_quick.id:
    {'m': 175, 'g': 175, 'b': [units.Protoss.CyberneticsCore, units.Protoss.FleetBeacon], 'u': u.ProtossAirWeaponsLevel1, 't': 215},
  actions.FUNCTIONS.Research_ProtossAirArmorLevel3_quick.id:
    {'m': 250, 'g': 250, 'b': [units.Protoss.CyberneticsCore, units.Protoss.FleetBeacon], 'u': u.ProtossAirArmorsLevel2, 't': 250},
  actions.FUNCTIONS.Research_ProtossAirWeaponsLevel3_quick.id:
    {'m': 250, 'g': 250, 'b': [units.Protoss.CyberneticsCore, units.Protoss.FleetBeacon], 'u': u.ProtossAirWeaponsLevel2, 't': 250},
  actions.FUNCTIONS.Research_WarpGate_quick.id:
    {'m': 50, 'g': 50, 'b': [units.Protoss.CyberneticsCore], 't': 140},
  # Forge BF
  actions.FUNCTIONS.Research_ProtossGroundArmorLevel1_quick.id:
    {'m': 100, 'g': 100, 'b': [units.Protoss.Forge], 't': 170},  # map from Research_ProtossGroundArmor_quick
  actions.FUNCTIONS.Research_ProtossGroundWeaponsLevel1_quick.id:
    {'m': 100, 'g': 100, 'b': [units.Protoss.Forge], 't': 170},  # map from Research_ProtossGroundWeapon_quick
  actions.FUNCTIONS.Research_ProtossShieldsLevel1_quick.id:
    {'m': 150, 'g': 150, 'b': [units.Protoss.Forge], 't': 170},  # map from Research_ProtossShield_quick
  actions.FUNCTIONS.Research_ProtossGroundArmorLevel2_quick.id:
    {'m': 150, 'g': 150, 'b': [units.Protoss.Forge, units.Protoss.TwilightCouncil], 'u': u.ProtossGroundArmorsLevel1, 't': 203},
  actions.FUNCTIONS.Research_ProtossGroundWeaponsLevel2_quick.id:
    {'m': 150, 'g': 150, 'b': [units.Protoss.Forge, units.Protoss.TwilightCouncil], 'u': u.ProtossGroundWeaponsLevel1, 't': 203},
  actions.FUNCTIONS.Research_ProtossShieldsLevel2_quick.id:
    {'m': 200, 'g': 200, 'b': [units.Protoss.Forge, units.Protoss.TwilightCouncil], 'u': u.ProtossShieldsLevel1, 't': 203},
  actions.FUNCTIONS.Research_ProtossGroundArmorLevel3_quick.id:
    {'m': 200, 'g': 200, 'b': [units.Protoss.Forge, units.Protoss.TwilightCouncil], 'u': u.ProtossGroundArmorsLevel2, 't': 235},
  actions.FUNCTIONS.Research_ProtossGroundWeaponsLevel3_quick.id:
    {'m': 200, 'g': 200, 'b': [units.Protoss.Forge, units.Protoss.TwilightCouncil], 'u': u.ProtossGroundWeaponsLevel2, 't': 235},
  actions.FUNCTIONS.Research_ProtossShieldsLevel3_quick.id:
    {'m': 250, 'g': 250, 'b': [units.Protoss.Forge, units.Protoss.TwilightCouncil], 'u': u.ProtossShieldsLevel2, 't': 235},
  # TwilightCouncil VC
  actions.FUNCTIONS.Research_AdeptResonatingGlaives_quick.id:
    {'m': 100,'g': 100, 'b':[units.Protoss.TwilightCouncil], 't': 140},
  actions.FUNCTIONS.Research_Blink_quick.id:
    {'m': 150,'g': 150, 'b':[units.Protoss.TwilightCouncil], 't': 170},
  actions.FUNCTIONS.Research_Charge_quick.id:
    {'m': 100, 'g': 100, 'b': [units.Protoss.TwilightCouncil], 't': 140},
  # FleetBeacon VF
  actions.FUNCTIONS.Research_PhoenixAnionPulseCrystals_quick.id:
    {'m': 150, 'g': 150, 'b': [units.Protoss.FleetBeacon], 't': 90},
  # actions.FUNCTIONS.Research_VoidRayFluxVanes_quick.id:
  #   {'m': 100, 'g': 100, 'b': units.Protoss.FleetBeacon, 't': 80},  # Do not realised in pysc2
  # actions.FUNCTIONS.Research_TempestTectonicDestabilizers_quick.id:
  #   {'m': 150, 'g': 150, 'b': units.Protoss.FleetBeacon, 't': 140},  # Do not realised in pysc2
  # RoboticsBay VB
  actions.FUNCTIONS.Research_ExtendedThermalLance_quick.id:
    {'m': 150, 'g': 150, 'b': [units.Protoss.RoboticsBay], 't': 140},
  actions.FUNCTIONS.Research_GraviticBooster_quick.id:
    {'m': 100, 'g': 100, 'b': [units.Protoss.RoboticsBay], 't': 80},
  actions.FUNCTIONS.Research_GraviticDrive_quick.id:
    {'m': 100, 'g': 100, 'b': [units.Protoss.RoboticsBay], 't': 80},
  # TemplarArchive VT
  actions.FUNCTIONS.Research_PsiStorm_quick.id:
    {'m': 200, 'g': 200, 'b': [units.Protoss.TemplarArchive], 't': 110},
  # DarkShrine VD
  actions.FUNCTIONS.Research_ShadowStrike_quick.id:
    {'m': 100, 'g': 100, 'b': [units.Protoss.DarkShrine], 't': 140},
}
# minerals gas building time supply
protoss_train_conditions = {
  # Nexus, BN
  actions.FUNCTIONS.Train_Mothership_quick.id:
    {'m': 300, 'g': 300, 'b': [units.Protoss.Nexus, units.Protoss.FleetBeacon], 't': 125, 's': 6},
  # Gateway, BG
  actions.FUNCTIONS.Train_Zealot_quick.id:
    {'m': 100, 'g': 0, 'b': [units.Protoss.Gateway], 't': 38, 's': 2},
  actions.FUNCTIONS.Train_Stalker_quick.id:
    {'m': 125, 'g': 50, 'b': [units.Protoss.Gateway, units.Protoss.CyberneticsCore], 't': 42, 's': 2},
  actions.FUNCTIONS.Train_Adept_quick.id:
    {'m': 100, 'g': 25, 'b': [units.Protoss.Gateway, units.Protoss.CyberneticsCore], 't': 42, 's': 2},
  actions.FUNCTIONS.Train_Sentry_quick.id:
    {'m': 50, 'g': 100, 'b': [units.Protoss.Gateway, units.Protoss.CyberneticsCore], 't': 32, 's': 2},
  actions.FUNCTIONS.Train_HighTemplar_quick.id:
    {'m': 50, 'g': 150, 'b': [units.Protoss.Gateway, units.Protoss.TwilightCouncil], 't': 55, 's': 2},
  actions.FUNCTIONS.Train_DarkTemplar_quick.id:
    {'m': 125, 'g': 125, 'b': [units.Protoss.Gateway, units.Protoss.TwilightCouncil], 't': 55, 's': 2},
  # Stargate, VS
  actions.FUNCTIONS.Train_Oracle_quick.id:
    {'m': 150, 'g': 150, 'b': [units.Protoss.Stargate], 't': 52, 's': 3},
  actions.FUNCTIONS.Train_Phoenix_quick.id:
    {'m': 150, 'g': 100, 'b': [units.Protoss.Stargate], 't': 35, 's': 2},
  actions.FUNCTIONS.Train_VoidRay_quick.id:
    {'m': 250, 'g': 150, 'b': [units.Protoss.Stargate], 't': 60, 's': 4},
  actions.FUNCTIONS.Train_Tempest_quick.id:
    {'m': 250, 'g': 175, 'b': [units.Protoss.Stargate, units.Protoss.FleetBeacon], 't': 60, 's': 5},
  actions.FUNCTIONS.Train_Carrier_quick.id:
    {'m': 350, 'g': 250, 'b': [units.Protoss.Stargate, units.Protoss.FleetBeacon], 't': 90, 's': 6},
  # RoboticsFacility, VB
  actions.FUNCTIONS.Train_Observer_quick.id:
    {'m': 25, 'g': 75, 'b': [units.Protoss.RoboticsFacility], 't': 25, 's': 1},
  actions.FUNCTIONS.Train_WarpPrism_quick.id:
    {'m': 250, 'g': 0, 'b': [units.Protoss.RoboticsFacility], 't': 50, 's': 2},
  actions.FUNCTIONS.Train_Immortal_quick.id:
    {'m': 275, 'g': 100, 'b': [units.Protoss.RoboticsFacility], 't': 55, 's': 4},
  actions.FUNCTIONS.Train_Colossus_quick.id:
    {'m': 300, 'g': 200, 'b': [units.Protoss.RoboticsFacility, units.Protoss.RoboticsBay], 't': 75, 's': 6},
  actions.FUNCTIONS.Train_Disruptor_quick.id:
    {'m': 150, 'g': 150, 'b': [units.Protoss.RoboticsFacility, units.Protoss.RoboticsBay], 't': 50, 's': 4},
}
# minerals gas building time length
protoss_build_conditions = {
  actions.FUNCTIONS.Build_Nexus_screen.id:
    {'m': 400, 'g': 0, 'b': [], 't': 100},
  actions.FUNCTIONS.Build_Pylon_screen.id:
    {'m': 100, 'g': 0, 'b': [units.Protoss.Nexus], 't': 25},
  actions.FUNCTIONS.Build_Assimilator_screen.id:
    {'m': 75, 'g': 0, 'b': [units.Protoss.Pylon], 't': 30},
  actions.FUNCTIONS.Build_Gateway_screen.id:
    {'m': 150, 'g': 0, 'b': [units.Protoss.Pylon], 't': 65},
  actions.FUNCTIONS.Build_CyberneticsCore_screen.id:
    {'m': 150, 'g': 0, 'b': [units.Protoss.Gateway], 't': 50},
  actions.FUNCTIONS.Build_Forge_screen.id:
    {'m': 150, 'g': 0, 'b': [], 't': 45, 'l': 3},
  actions.FUNCTIONS.Build_PhotonCannon_screen.id:
    {'m': 150, 'g': 0, 'b': [units.Protoss.Forge], 't': 40},
  actions.FUNCTIONS.Build_ShieldBattery_screen.id:
    {'m': 100, 'g': 0, 'b': [units.Protoss.CyberneticsCore], 't': 40},
  actions.FUNCTIONS.Build_TwilightCouncil_screen.id:
    {'m': 150, 'g': 100, 'b': [units.Protoss.CyberneticsCore], 't': 50},
  actions.FUNCTIONS.Build_TemplarArchive_screen.id:
    {'m': 150, 'g': 200, 'b': [units.Protoss.TwilightCouncil], 't': 50},
  actions.FUNCTIONS.Build_DarkShrine_screen.id:
    {'m': 150, 'g': 150, 'b': [units.Protoss.TwilightCouncil], 't': 100},
  actions.FUNCTIONS.Build_Stargate_screen.id:
    {'m': 150, 'g': 150, 'b': [units.Protoss.CyberneticsCore], 't': 60},
  actions.FUNCTIONS.Build_FleetBeacon_screen.id:
    {'m': 300, 'g': 200, 'b': [units.Protoss.Stargate], 't': 60},
  actions.FUNCTIONS.Build_RoboticsFacility_screen.id:
    {'m': 150, 'g': 100, 'b': [units.Protoss.CyberneticsCore], 't': 65},
  actions.FUNCTIONS.Build_RoboticsBay_screen.id:
    {'m': 150, 'g': 150, 'b': [units.Protoss.RoboticsFacility], 't': 30},
}


terran_map_research_quick_to_level = {}
terran_research_conditions = {}
terran_train_conditions = {}
terran_build_conditions = {}


zerg_map_research_quick_to_level = {}
zerg_research_conditions = {}
zerg_train_conditions = {}
zerg_build_conditions = {}