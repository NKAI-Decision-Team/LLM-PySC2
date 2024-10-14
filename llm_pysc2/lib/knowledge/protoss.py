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

from pysc2.lib import units, actions

# minerals gas building time
protoss_research_conditions = {
  # CyberneticsCore BY
  actions.FUNCTIONS.Research_ProtossAirArmorLevel1_quick.id:
    {'m': 100, 'g': 100, 'b': units.Protoss.CyberneticsCore, 't': 180},  # map from Research_ProtossAirArmor_quick
  actions.FUNCTIONS.Research_ProtossAirWeaponsLevel1_quick.id:
    {'m': 100, 'g': 100, 'b': units.Protoss.CyberneticsCore, 't': 180},  # map from Research_ProtossAirWeapons_quick
  actions.FUNCTIONS.Research_ProtossAirArmorLevel2_quick.id:
    {'m': 175, 'g': 175, 'b': units.Protoss.CyberneticsCore, 't': 215},
  actions.FUNCTIONS.Research_ProtossAirWeaponsLevel2_quick.id:
    {'m': 175, 'g': 175, 'b': units.Protoss.CyberneticsCore, 't': 215},
  actions.FUNCTIONS.Research_ProtossAirArmorLevel3_quick.id:
    {'m': 250, 'g': 250, 'b': units.Protoss.CyberneticsCore, 't': 250},
  actions.FUNCTIONS.Research_ProtossAirWeaponsLevel3_quick.id:
    {'m': 250, 'g': 250, 'b': units.Protoss.CyberneticsCore, 't': 250},
  actions.FUNCTIONS.Research_WarpGate_quick.id:
    {'m': 50, 'g': 50, 'b': units.Protoss.CyberneticsCore, 't': 140},
  # Forge BF
  actions.FUNCTIONS.Research_ProtossGroundArmorLevel1_quick.id:
    {'m': 100, 'g': 100, 'b': units.Protoss.Forge, 't': 170},  # map from Research_ProtossGroundArmor_quick
  actions.FUNCTIONS.Research_ProtossGroundWeaponsLevel1_quick.id:
    {'m': 100, 'g': 100, 'b': units.Protoss.Forge, 't': 170},  # map from Research_ProtossGroundWeapon_quick
  actions.FUNCTIONS.Research_ProtossShieldsLevel1_quick.id:
    {'m': 150, 'g': 150, 'b': units.Protoss.Forge, 't': 170},  # map from Research_ProtossShield_quick
  actions.FUNCTIONS.Research_ProtossGroundArmorLevel2_quick.id:
    {'m': 150, 'g': 150, 'b': units.Protoss.Forge, 't': 203},
  actions.FUNCTIONS.Research_ProtossGroundWeaponsLevel2_quick.id:
    {'m': 150, 'g': 150, 'b': units.Protoss.Forge, 't': 203},
  actions.FUNCTIONS.Research_ProtossShieldsLevel2_quick.id:
    {'m': 200, 'g': 200, 'b': units.Protoss.Forge, 't': 203},
  actions.FUNCTIONS.Research_ProtossGroundArmorLevel3_quick.id:
    {'m': 200, 'g': 200, 'b': units.Protoss.Forge, 't': 235},
  actions.FUNCTIONS.Research_ProtossGroundWeaponsLevel3_quick.id:
    {'m': 200, 'g': 200, 'b': units.Protoss.Forge, 't': 235},
  actions.FUNCTIONS.Research_ProtossShieldsLevel3_quick.id:
    {'m': 250, 'g': 250, 'b': units.Protoss.Forge, 't': 235},
  # TwilightCouncil VC
  actions.FUNCTIONS.Research_AdeptResonatingGlaives_quick.id:
    {'m': 100,'g': 100, 'b':units.Protoss.TwilightCouncil, 't': 140},
  actions.FUNCTIONS.Research_Blink_quick.id:
    {'m': 150,'g': 150, 'b':units.Protoss.TwilightCouncil, 't': 170},
  actions.FUNCTIONS.Research_Charge_quick.id:
    {'m': 100, 'g': 100, 'b': units.Protoss.TwilightCouncil, 't': 140},
  # FleetBeacon VF
  actions.FUNCTIONS.Research_PhoenixAnionPulseCrystals_quick.id:
    {'m': 150, 'g': 150, 'b': units.Protoss.FleetBeacon, 't': 90},
  # actions.FUNCTIONS.Research_VoidRayFluxVanes_quick.id:
  #   {'m': 100, 'g': 100, 'b': units.Protoss.FleetBeacon, 't': 80},  # Do not realised in pysc2
  # actions.FUNCTIONS.Research_TempestTectonicDestabilizers_quick.id:
  #   {'m': 150, 'g': 150, 'b': units.Protoss.FleetBeacon, 't': 140},  # Do not realised in pysc2
  # RoboticsBay VB
  actions.FUNCTIONS.Research_ExtendedThermalLance_quick.id:
    {'m': 150, 'g': 150, 'b': units.Protoss.RoboticsBay, 't': 140},
  actions.FUNCTIONS.Research_GraviticBooster_quick.id:
    {'m': 100, 'g': 100, 'b': units.Protoss.RoboticsBay, 't': 80},
  actions.FUNCTIONS.Research_GraviticDrive_quick.id:
    {'m': 100, 'g': 100, 'b': units.Protoss.RoboticsBay, 't': 80},
  # TemplarArchive VT
  actions.FUNCTIONS.Research_PsiStorm_quick.id:
    {'m': 200, 'g': 200, 'b': units.Protoss.TemplarArchive, 't': 110},
  # DarkShrine VD
  actions.FUNCTIONS.Research_ShadowStrike_quick.id:
    {'m': 100, 'g': 100, 'b': units.Protoss.DarkShrine, 't': 140},
}

# minerals gas building time supply
protoss_train_conditions = {
  # Nexus, BN
  actions.FUNCTIONS.Train_Mothership_quick.id:
    {'m': 300, 'g': 300, 'b': units.Protoss.Nexus, 't': 125, 's': 6},
  # Gateway, BG
  actions.FUNCTIONS.Train_Zealot_quick.id:
    {'m': 100, 'g': 0, 'b': units.Protoss.Gateway, 't': 38, 's': 2},
  actions.FUNCTIONS.Train_Stalker_quick.id:
    {'m': 125, 'g': 50, 'b': units.Protoss.Gateway, 't': 42, 's': 2},
  actions.FUNCTIONS.Train_Adept_quick.id:
    {'m': 100, 'g': 25, 'b': units.Protoss.Gateway, 't': 42, 's': 2},
  actions.FUNCTIONS.Train_Sentry_quick.id:
    {'m': 50, 'g': 100, 'b': units.Protoss.Gateway, 't': 32, 's': 2},
  actions.FUNCTIONS.Train_HighTemplar_quick.id:
    {'m': 50, 'g': 150, 'b': units.Protoss.Gateway, 't': 55, 's': 2},
  actions.FUNCTIONS.Train_DarkTemplar_quick.id:
    {'m': 125, 'g': 125, 'b': units.Protoss.Gateway, 't': 55, 's': 2},
  # Stargate, VS
  actions.FUNCTIONS.Train_Oracle_quick.id:
    {'m': 150, 'g': 150, 'b': units.Protoss.Stargate, 't': 52, 's': 3},
  actions.FUNCTIONS.Train_Phoenix_quick.id:
    {'m': 150, 'g': 100, 'b': units.Protoss.Stargate, 't': 35, 's': 2},
  actions.FUNCTIONS.Train_VoidRay_quick.id:
    {'m': 250, 'g': 150, 'b': units.Protoss.Stargate, 't': 60, 's': 4},
  actions.FUNCTIONS.Train_Tempest_quick.id:
    {'m': 250, 'g': 175, 'b': units.Protoss.Stargate, 't': 60, 's': 5},
  actions.FUNCTIONS.Train_Carrier_quick.id:
    {'m': 350, 'g': 250, 'b': units.Protoss.Stargate, 't': 90, 's': 6},
  # RoboticsFacility, VB
  actions.FUNCTIONS.Train_Observer_quick.id:
    {'m': 25, 'g': 75, 'b': units.Protoss.RoboticsFacility, 't': 25, 's': 1},
  actions.FUNCTIONS.Train_WarpPrism_quick.id:
    {'m': 250, 'g': 0, 'b': units.Protoss.RoboticsFacility, 't': 50, 's': 2},
  actions.FUNCTIONS.Train_Immortal_quick.id:
    {'m': 275, 'g': 100, 'b': units.Protoss.RoboticsFacility, 't': 55, 's': 4},
  actions.FUNCTIONS.Train_Colossus_quick.id:
    {'m': 300, 'g': 200, 'b': units.Protoss.RoboticsFacility, 't': 75, 's': 6},
  actions.FUNCTIONS.Train_Disruptor_quick.id:
    {'m': 150, 'g': 150, 'b': units.Protoss.RoboticsFacility, 't': 50, 's': 4},
}

# minerals gas building time length
protoss_build_conditions = {
  actions.FUNCTIONS.Build_Nexus_screen.id:
    {'m': 400, 'g': 0, 'b': None, 't': 100, 'l': 5},
  actions.FUNCTIONS.Build_Assimilator_screen.id:
    {'m': 75, 'g': 0, 'b': None, 't': 30, 'l': 3},
  actions.FUNCTIONS.Build_Pylon_screen.id:
    {'m': 100, 'g': 0, 'b': None, 't': 25, 'l': 2},
  actions.FUNCTIONS.Build_Gateway_screen.id:
    {'m': 150, 'g': 0, 'b': None, 't': 65, 'l': 3},
  actions.FUNCTIONS.Build_CyberneticsCore_screen.id:
    {'m': 150, 'g': 0, 'b': units.Protoss.Gateway, 't': 50, 'l': 3},
  actions.FUNCTIONS.Build_Forge_screen.id:
    {'m': 150, 'g': 0, 'b': units.Protoss.Gateway, 't': 45, 'l': 3},
  actions.FUNCTIONS.Build_PhotonCannon_screen.id:
    {'m': 150, 'g': 0, 'b': units.Protoss.Forge, 't': 40, 'l': 2},
  actions.FUNCTIONS.Build_ShieldBattery_screen.id:
    {'m': 100, 'g': 0, 'b': units.Protoss.CyberneticsCore, 't': 40, 'l': 2},
  actions.FUNCTIONS.Build_TwilightCouncil_screen.id:
    {'m': 150, 'g': 100, 'b': units.Protoss.CyberneticsCore, 't': 50, 'l': 3},
  actions.FUNCTIONS.Build_TemplarArchive_screen.id:
    {'m': 150, 'g': 200, 'b': units.Protoss.TwilightCouncil, 't': 50, 'l': 3},
  actions.FUNCTIONS.Build_DarkShrine_screen.id:
    {'m': 150, 'g': 150, 'b': units.Protoss.TwilightCouncil, 't': 100, 'l': 2},
  actions.FUNCTIONS.Build_Stargate_screen.id:
    {'m': 150, 'g': 150, 'b': units.Protoss.CyberneticsCore, 't': 60, 'l': 3},
  actions.FUNCTIONS.Build_FleetBeacon_screen.id:
    {'m': 300, 'g': 200, 'b': units.Protoss.Stargate, 't': 60, 'l': 3},
  actions.FUNCTIONS.Build_RoboticsFacility_screen.id:
    {'m': 150, 'g': 100, 'b': units.Protoss.CyberneticsCore, 't': 65, 'l': 3},
  actions.FUNCTIONS.Build_RoboticsBay_screen.id:
    {'m': 150, 'g': 150, 'b': units.Protoss.RoboticsFacility, 't': 30, 'l': 3},
}


DATA_PROTOSS = {

    units.Protoss.Adept: {
        # wiki英文 Unit
        'name': 'Adept',
        'name_cn': '使徒',
        # wiki英文 Details
        'description': 'Ground-only ranged attack unit, armed with psionic transfer ability to teleport to '
                       'nearby locations for harassment.',
        # 可以对什么对象造成伤害，ground/air
        'target': ['ground'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['light', 'biological'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['light'],

        # 生存
        'health': 70,  # wiki中文 基本信息/生命值
        'shield': 70,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.5,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['ground'],
        'weapon1_type_anti': ['light'],
        'weapon1_attack': 10,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 12,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 4,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 2.25,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 28,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 42,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 25,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'train from GateWay or warp from WarpGate.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade
            'Research_ResonatingGlaives': 'Increase the attack speed of the Adept by 45%.'
                                          'Cost 100 mineral, 100 gas and 100 seconds. In DarkShrine.',
        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Effect_PsionicTransfer': 'Active skill.Always avaliable. Cooldowm 11 seconds.'
                                      'Projects an invulnerable psionic image that can move but not attack.'
                                      ' After 7 seconds, the adept teleports to the images location. '
                                      'The shade may be canceled at any time, and the adept would not teleport. '
                                      'The shade has a sight radius of 2.',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway/WarpGate , have Cybernetics Core',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },

    units.Protoss.Archon: {
        # wiki英文 Unit
        'name': 'Archon',
        'name_cn': '执政官',
        # wiki英文 Details
        'description': 'Created by merging two templar units, the archon is a powerful melee unit with a very durable '
                       'force shield and a strong energy-based attack.',
        # 可以对什么对象造成伤害，ground/air
        'target': ['ground', 'air'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['psionic', 'massive'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['biological'],

        # 生存
        'health': 10,  # wiki中文 基本信息/生命值
        'shield': 350,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.8125,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['ground', 'air'],
        'weapon1_type_anti': ['biological'],
        'weapon1_attack': 25,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 10,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 3,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 3,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1.754,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 4,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 12,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 4,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'train from GateWay or warp from WarpGate.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway/WarpGate, have CyberneticsCore, have TwilightCouncil, '
                            'have TemplarArchives/DarkShrine',
        'require_tech': '',
        'require_unit': 'sacrifice 2 templars',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },

    units.Protoss.Carrier: {
        # wiki英文 Unit
        'name': 'Carrier',
        'name_cn': '航母',
        # wiki英文 Details
        'description': 'A powerful air unit. Carriers do not have their own attacks but '
                       'create interceptors to fight for them.',
        # 可以对什么对象造成伤害，ground/air
        'target': ['ground', 'air'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'massive', 'mechanical'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 300,  # wiki中文 基本信息/生命值
        'shield': 150,  # wiki中文 基本信息/护盾
        'health_armor': 2,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 1.875,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['ground', 'air'],
        'weapon1_type_anti': [],
        'weapon1_attack': 5,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 8,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 16,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 3.14,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 6,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 90,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 350,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 250,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Stargate.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'BuildInterceptor': 'Passive ability. Always available. The Carrier is produced with four interceptors. '
                                'Carriers may produce up to eight interceptors as an auto-cast ability. '
                                'Cost: 15 minerals per interceptor, 9 seconds each.',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway/WarpGate, have Stargate, have Cybernetics Core, have FleetBeacon',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Protoss.Colossus: {
        # wiki英文 Unit
        'name': 'Colossus',
        'name_cn': '巨像',
        # wiki英文 Details
        'description': 'The large quad-legged vehicle fires lasers in a splash pattern well-suited to '
                       'destroying swarms of weaker units. This unit can also traverse differences in terrain height '
                       'due to its long legs, and will appear to step over ledges and other obstacles '
                       'due to the inverse kinematics system.',
        # 可以对什么对象造成伤害，ground/air
        'target': ['ground'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground', 'air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'massive', 'mechanical'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['light'],

        # 生存
        'health': 200,  # wiki中文 基本信息/生命值
        'shield': 150,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.25,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['ground'],
        'weapon1_type_anti': ['light'],
        'weapon1_attack': 10,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 5,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 7,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 2,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1.5,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 6,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 75,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 300,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 200,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Robotics Facility.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade
            'ExtendedThermalLance': 'Increases the range of the colossus attack from 7 to 9. '
                                    'Cost: 150 minerals, 150 gas, 100 seconds. Requires Robotics Bay.',
        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway/WarpGate, have Cybernetics Core, have Robotics Facility, have Robotics Bay',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Protoss.DarkTemplar: {
        # wiki英文 Unit
        'name': 'DarkTemplar',
        'name_cn': '黑暗圣堂武士',
        # wiki英文 Details
        'description': 'A permanently cloaked stealth warrior.',
        # 可以对什么对象造成伤害，ground/air
        'target': ['ground'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['light', 'biological', 'psionic'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 40,  # wiki中文 基本信息/生命值
        'shield': 80,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.8125,  # wiki中文 基本信息/移动速度

        # 作战
        'attack': 45,  # wiki中文 作战/武器/伤害，基础伤害
        'attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'attack_upgrade_base_damage_offset': 5,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'attack_range': 1,  # wiki中文 作战/武器/射程，近战为1
        'attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'cooldown': 1.7694,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 45,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 55,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 125,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 123,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'train from GateWay or warp from WarpGate.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade
            'Research_ShadowStrike': 'Enable ShadowStride ability.'
                                     'Cost 100 mineral, 100 gas and 100 seconds. In DarkShrine.',
        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'ArchonWarp': 'Always available. Any combination of two high templar/dark templar can '
                          'sacrifice themselves, transforming into an archon.',
            'ShadowStride': 'Available after Research_ShadowStrike. Cooldown 14 seconds.'
                            'Teleports the Dark Templar to a nearby target location. Has a 0.71 attack delay after use.'
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway/WarpGate, have Cybernetics Core, have TwilightCouncil, have DarkShrine',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': 'Archon',

    },

    units.Protoss.Disruptor: {
        # wiki英文 Unit
        'name': 'Disruptor',
        'name_cn': '干扰者',
        # wiki英文 Details
        'description': 'Light ground mechanized support unit, '
                       'armed with energy spikes to wreak havoc against swaths of ground forces.',
        'target': ['ground'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'mechanical'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 100,  # wiki中文 基本信息/生命值
        'shield': 100,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.25,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['ground'],
        'weapon1_type_anti': ['shield'],
        'weapon1_attack': 145,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 55,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 9,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 21,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 4,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 50,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 150,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Robotics Facility',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {

        },
        'ability': {
            'PurificationNova': 'Always available. Active skill. Shoots a ball of energy at a target point that can be '
                                'controlled and lasts 2 seconds. After two seconds, the energy ball explodes, '
                                'dealing 155 (+55 vs shields) damage to nearby enemies in a 1.3575 radius. '
                                'Has a 0.7 second charge time after being dropped from a transport. '
                                'Cooldown: 14.3 seconds.',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway, have Cybernetics Core, have Robotics Facility, have Robotics Bay',
        'require_tech': '',
        'require_unit': '',
        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Protoss.HighTemplar: {
        # wiki英文 Unit
        'name': 'Hightemplar',
        'name_cn': '高阶圣堂武士',
        # wiki英文 Details
        'description': 'A physically fragile unit with strong psychic abilities.',
        # 可以对什么对象造成伤害，ground/air
        'target': ['ground'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['light', 'biological', 'psionic'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 40,  # wiki中文 基本信息/生命值
        'shield': 40,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.0156,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['ground'],
        'weapon1_type_anti': [],
        'weapon1_attack': 4,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 6,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1.754,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 45,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 55,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 50,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 150,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Gateway/WarpGate.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 200,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # High Templar 的升级，不记录公共升级如 ground_weapon_upgrade
            'PsionicStorm': 'Deals 80 damage in the target area in small packets over 2.85 seconds. '
                            'Cost: 200 minerals, 200 gas, 79 seconds. Requires Templar Archives.',
        },
        'ability': {  # High Templar 的主动技能
            'PsionicStorm': 'Available after Psionic Storm upgrade in Templar Archives. Deals 80 damage in the target '
                            'area in small packets over 2.85 seconds. Hits both air and ground units. '
                            'Cost: 75 energy, Range: 9, Duration: 2.85 seconds, Cooldown: 1.43 seconds.',
            'Feedback': 'Always available. Drains all energy from a target unit, '
                        'dealing damage equal to half of the energy drained. Cost: 50 energy, Range: 10.',
            'ArchonWarp': 'Always available. Any combination of two High Templar/Dark Templar can sacrifice '
                          'themselves, transforming into an Archon. Cost: 9 seconds.'
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway/WarpGate, have Cybernetics Core, have Twilight Council, '
                            'have Templar Archives',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': 'Archon',
    },

    units.Protoss.Immortal: {
        # wiki英文 Unit
        'name': 'Immortal',
        'name_cn': '不朽者',
        # wiki英文 Details
        'description': 'Dragoon-like walker with a strong defense against powerful attacks, '
                       'but vulnerable to weaker attacks.',
        # 可以对什么对象造成伤害，ground/air
        'target': ['ground'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'mechanical'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['armored'],

        # 生存
        'health': 200,  # wiki中文 基本信息/生命值
        'shield': 100,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.25,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['ground'],
        'weapon1_type_anti': ['armored'],
        'weapon1_attack': 20,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 30,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 2,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 3,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 6,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1.45,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 4,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 55,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 275,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Robotics Facility.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {
        },
        'ability': {
            'Barrier': 'Passive Ability.The immortal gains a barrier which absorbs 100 damage before falling, '
                       'and blocks the first instance of damage that activates the barrier. Lasts 2 seconds. '
                       'Automatically activates upon taking damage to shields or health. '
                       'Duration 2 seconds, Cooldown 32 seconds'
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway/WarpGate, have Cybernetics Core, have Robotics Facility',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Protoss.Mothership: {
        # wiki英文 Unit
        'name': 'Mothership',
        'name_cn': '母舰',
        # wiki英文 Details
        'description': 'A powerful flying unit that consumes a high amount of resources to produce. '
                       'It has powerful special abilities.',
        # 可以对什么对象造成伤害，ground/air
        'target': ['ground', 'air'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'mechanical', 'psionic', 'massive', 'heroic'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 250,  # wiki中文 基本信息/生命值
        'shield': 250,  # wiki中文 基本信息/护盾
        'health_armor': 2,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.0156,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['ground', 'air'],
        'weapon1_type_anti': [],
        'weapon1_attack': 6,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 7,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 6,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 2.21,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 6,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 125,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 300,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 300,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Nexus.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'CloakingField': 'Always available. Cloaks nearby friendly units and buildings within a range of '
                             '5 for 20 seconds. Duration: 20 seconds, Cooldown: 50 seconds.',
            'MassRecall': 'Always available. Summons all units in target area (5) owned by the mothership\'s player '
                          'to the mothership\'s location. Does not share a cooldown with the Nexus Strategic Recall. '
                          'Duration: 2 seconds, Cooldown: 89 seconds.',
            'TimeWarp': 'Always available. After a 0.71-second delay, warps spacetime within the target area of 3.75 '
                        'for 7 seconds. Enemy ground units, air units, and structures within the field are slowed and '
                        'have their attack speed reduced by 40%. Duration: 11 seconds, Cooldown: 60 seconds.',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway/WarpGate, have Stargate, have Cybernetics Core, have FleetBeacon',
        'require_tech': '',
        'require_unit': 'Not have Carrier',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Protoss.MothershipCore: {
        # wiki英文 Unit
        'name': 'Mothershipcore',
        'name_cn': '母舰核心',
        # wiki英文 Details
        'description': 'A base defense unit that can overcharge structures, recall allies and slow enemies. '
                       'Can be upgraded into the mothership.',
        'target': ['ground'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['Armored', 'mechanical', 'psionic'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['massive', 'structure'],

        # 生存
        'health': 130,  # wiki中文 基本信息/生命值
        'shield': 60,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 1.88,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['ground'],
        'weapon1_type_anti': ['massive'],
        'weapon1_attack': 8,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 5,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0.85,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 30,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Nexus.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 50,  # 默认值为0
        'upgrade': {
            'Upgrade to Mothership': 'Transforms the Mothership Core into a Mothership. '
                                     'Costs 300 minerals, 300 gas, 100 seconds and 6 additional supplies.'
        },
        'ability': {
            'Photon Overcharge': 'Always available. Costs 100 energy. Causes the targeted Nexus to gain a '
                                 'long-range attack for 60 seconds, dealing 20 damage per hit with a range of 13.',
            'Mass Recall': 'Always available. Costs 100 energy. Warps the Mothership Core and nearby units '
                           'to the targeted Nexus.',
            'Time Warp': 'Always available. Costs 75 energy. Creates a field for 30 seconds that slows ground unit '
                         'movement by 50% in the affected area.',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Nexus, have Cybernetics Core',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': 'Mothership',
    },

    units.Protoss.Observer: {
        # wiki英文 Unit
        'name': 'Observer',
        'name_cn': '侦测器',
        # wiki英文 Details
        'description': 'A cloaking air unit that functions as a detector.',
        # 可以对什么对象造成伤害，ground/air
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['light', 'mechanical'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 40,  # wiki中文 基本信息/生命值
        'shield': 30,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.0156,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 1,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 25,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 25,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 75,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Robotics Facility.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {  # Observer的升级，不记录公共升级如 ground_weapon_upgrade
            'GraviticBoosters': 'Increases observer movement speed by 1.31. '
                                'Cost: 100 minerals, 100 gas, 57 seconds. Requires Robotics Bay.',
        },
        'ability': {  # Observer的主动技能
            'SurveillanceMode': 'Always available. The observer can switch to Surveillance Mode, becoming immobile and '
                                'gaining 50% increased sight radius. Can switch back to Observer Mode to move again. '
                                'Cost: 3 second.',
            'Detector': 'Passive ability. This unit or structure can detect cloaked, burrowed, '
                        'duplicated and hallucination enemies.',
            'Permanent Cloaking': 'Passive ability. This unit is permanently cloaked. They cannot be seen or directly '
                                  'attacked by enemy forces, unless they have detector support.',
        },
        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway/WarpGate, have Cybernetics Core, have Robotics Facility',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Protoss.Oracle: {
        # wiki英文 Unit
        'name': 'Oracle',
        'name_cn': '先知',
        # wiki英文 Details
        'description': 'A light, psionic, support and harassment ship. '
                       'Can grant vision and harass light units and workers with its pulsar beam.'
                       '(Cannot attack ground units before activating Pulsar Beam)',
        'target': ['ground'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'mechanical', 'psionic'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['light'],

        # 生存
        'health': 100,  # wiki中文 基本信息/生命值
        'shield': 60,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 4,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['ground'],
        'weapon1_type_anti': ['light'],
        'weapon1_attack': 15,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 7,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 4,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0.86,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 3,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 52,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 150,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Stargate.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 200,  # 默认值为0
        'upgrade': {
        },
        'ability': {
            'Revelation': 'Always available. Active skill. Cost: 25 energy. '
                          'Reveals enemy units and structures in an area, granting vision for 20 seconds. '
                          'Also reveals cloaked or burrowed units or structures.',
            'Pulsar Beam': 'Always available. Active skill. Cost: 25 energy (+1.96 energy per second). '
                           'Enables the Oracle to attack ground units with high damage, '
                           'particularly effective against light units.',
            'Stasis Ward': 'Always available. Active skill. Cost: 50 energy. '
                           'Places a cloaked stasis ward on the ground that traps enemy units in stasis '
                           'for 21 seconds upon activation.',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway, have Cybernetics Core, have Stargate',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Protoss.Phoenix: {
        # wiki英文 Unit
        'name': 'Phoenix',
        'name_cn': '凤凰',
        # wiki英文 Details
        'description': 'An aerial fighter with an anti-gravity ability that lifts ground units into the air.',
        # 可以对什么对象造成伤害，ground/air
        'target': ['ground', 'air'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['light', 'mechanical'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['light'],

        # 生存
        'health': 120,  # wiki中文 基本信息/生命值
        'shield': 60,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 4.25,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['air'],
        'weapon1_type_anti': ['light'],
        'weapon1_attack': 5,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 5,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 5,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 2,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1.1,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 35,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Stargate.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 200,  # 默认值为0
        'upgrade': {  # Phoenix的升级，不记录公共升级如 ground_weapon_upgrade
            'AnionPulseCrystals': 'Increases Phoenix attack range by 2. '
                                  'Cost: 150 minerals, 150 gas, 64 seconds. Requires Fleet Beacon.',
        },
        'ability': {  # Phoenix的主动技能
            'GravitonBeam': 'Always available. Lifts target unit into the air, preventing it from moving, attacking, '
                            'or using abilities. While using this ability the Phoenix cannot move or attack. '
                            'Cost: 50 energy, Duration: 7 seconds.',
        },
        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway/WarpGate, have Cybernetics Core, have Stargate',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Protoss.Probe: {
        # wiki英文 Unit
        'name': 'Probe',
        'name_cn': '探机',
        # wiki英文 Details
        'description': 'The builder of the protoss race. Gathers gas and minerals.',
        'target': ['ground'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['light', 'mechanical'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 20,  # wiki中文 基本信息/生命值
        'shield': 20,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.8125,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['ground'],
        'weapon1_type_anti': [],
        'weapon1_attack': 5,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0.2,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1.5,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 1,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 17,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 50,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Nexus.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {  # Probe的升级，不记录公共升级如 ground_weapon_upgrade
            # 探机没有专属升级
        },
        'ability': {  # Probe的主动技能
            'WorkerAbilities': 'Always available. The probe warps in structures and harvests minerals and vespene gas.',
        },
        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Nexus',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Protoss.Sentry: {
        # wiki英文 Unit
        'name': 'Sentry',
        'name_cn': '机械哨兵',
        # wiki英文 Details
        'description': 'Previously known as the disruptor, and the nullifier before that. A ground support unit.',
        'target': ['ground', 'air'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['psionic', 'mechanical'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['shield'],

        # 生存
        'health': 40,  # wiki中文 基本信息/生命值
        'shield': 40,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.5,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['ground', 'air'],
        'weapon1_type_anti': ['shield'],
        'weapon1_attack': 6,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 4,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 5,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 32,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 32,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 50,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'train from GateWay or warp from WarpGate.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 200,  # 默认值为0
        'upgrade': {  # Sentry的升级，不记录公共升级如 ground_weapon_upgrade
            # 哨兵没有专属升级
        },
        'ability': {  # Sentry的主动技能
            # 'Hallucination': 'Always available. Sentries produce false copies of units to distract opponents. '
            #                  'Cost: 75 energy, Duration: 43 seconds.',
            'ForceField': 'Always available. Creates a wall of energy at target point, '
                          'pushing nearby units away and making the terrain impassable. '
                          'Cost: 50 energy, Duration: 11 seconds, Cooldown: 11 seconds.',
            'GuardianShield': 'Always available. Sentries create a radius 4.5 aura which reduces incoming ranged '
                              'damage to friendly units by 2. '
                              'Cost: 75 energy, Duration: 12.86 seconds, Cooldown: 12.86 seconds.',
        },
        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway/WarpGate, have Cybernetics Core',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Protoss.Stalker: {
        # wiki英文 Unit
        'name': 'Stalker',
        'name_cn': '追猎者',
        # wiki英文 Details
        'description': 'A dragoon-like Nerazim unit, able to blink (short-range teleport) and deliver ranged attacks '
                       'against air and ground units.',
        'target': ['ground', 'air'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'mechanical'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['armored'],

        # 生存
        'health': 80,  # wiki中文 基本信息/生命值
        'shield': 80,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.9531,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['ground', 'air'],
        'weapon1_type_anti': ['armored'],
        'weapon1_attack': 13,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 5,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 6,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1.87,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 32,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 42,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 125,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 50,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'train from GateWay or warp from WarpGate.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {  # Stalker的升级，不记录公共升级如 ground_weapon_upgrade
            'Blink': 'Allows Stalkers to instantly teleport over short distances. '
                     'Cost: 100 minerals, 100 gas, 121 seconds. Requires Twilight Council.',
        },
        'ability': {  # Stalker的主动技能
            'Blink': 'Available after Blink upgrade in Twilight Council. Stalkers instantly teleport over short '
                     'distances, Commonly used to pursue the enemy when in an advantageous position or to stay away '
                     'from the enemy when in a disadvantageous position, or for individual retreat.'
                     'Range: 8, Cooldown: 7 seconds.',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway/WarpGate, have Cybernetics Core',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Protoss.StasisTrap: {
        # wiki英文 Unit
        'name': 'Stasisward',
        'name_cn': '静滞结界',
        # wiki英文 Details
        'description': 'Cloaked structure created by the Oracle. Used to freeze incoming units.'
                       'Permanent Cloaking:This unit is permanently cloaked. They cannot be seen or directly attacked '
                       'by enemy forces, unless they have detector support.',
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['ligth', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 30,  # wiki中文 基本信息/生命值
        'shield': 30,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 5,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 50,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Probe.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {

        },
        'ability': {
            'StasisTrap': 'Always available. Active skill. Traps nearby enemies in stasis for 21 seconds. '
                          'Trapped units cannot be attacked or affected by abilities.',
        },
        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway, have Cybernetics Core, have Stargate',
        'require_tech': '',
        'require_unit': 'have Oracle',
        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Protoss.Tempest: {
        # wiki英文 Unit
        'name': 'Tempest',
        'name_cn': '风暴战舰',
        # wiki英文 Details
        'description': 'A long-range capital ship that excels at taking down massive units.',
        'target': ['ground', 'air'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'mechanical', 'massive'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['massive', 'structure'],

        # 生存
        'health': 200,  # wiki中文 基本信息/生命值
        'shield': 100,  # wiki中文 基本信息/护盾
        'health_armor': 2,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.25,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['air'],
        'weapon1_type_anti': ['massive'],
        'weapon1_attack': 30,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 22,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 3,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 2,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 14,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 3.3,  # wiki中文 作战/武器/攻击间隔
        # 作战 weapon2
        'weapon2_target': ['ground'],
        'weapon2_type_anti': ['structure'],
        'weapon2_attack': 40,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon2_attack_bonus': 40,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 4,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 10,  # wiki中文 作战/武器/射程，近战为1
        'weapon2_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon2_cooldown': 3.3,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 5,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 60,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 250,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 175,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Stargate.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {
            'TectonicDestabilizers': 'Improves the Tempest\'s Resonance Coil to deal +40 damage vs structures. '
                                     'Cost: 150 minerals, 150 gas, 100 seconds. Requires Fleet Beacon.',
        },
        'ability': {

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway, have Cybernetics Core, have Stargate, have Fleet Beacon',
        'require_tech': '',
        'require_unit': '',
        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Protoss.VoidRay: {
        # wiki英文 Unit
        'name': 'VoidRay',
        'name_cn': '虚空辉光舰',
        # wiki英文 Details
        'description': 'Formerly known as the warp ray, this flying unit deals damage with a blue energy beam '
                       'that does more damage as it focuses on the same target. Good versus heavily armored targets '
                       'like buildings, weak against small arms fire.',
        'target': ['ground', 'air'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'mechanical'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['armored'],

        # 生存
        'health': 150,  # wiki中文 基本信息/生命值
        'shield': 100,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.75,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['ground', 'air'],
        'weapon1_type_anti': ['armored'],
        'weapon1_attack': 6,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 4,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 6,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0.5,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 4,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 60,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 250,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 150,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Stargate.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {
            'Flux Vanes': 'Increases the Void Ray\'s movement speed to 4.65 and acceleration to 3.76. '
                          'Cost: 100 minerals, 100 gas, 57 seconds. Purchased from Fleet Beacon.',
        },
        'ability': {
            'Prismatic Alignment': 'Always available. The Void Ray gains +6 damage against Armored enemies. '
                                   'Slows the Void Ray by 25%. Cost: 0, Duration: 14.3 seconds, Cooldown: 43 seconds.',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Stargate, have Cybernetics Core, have Nexus',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': 'have Gateway/WarpGate, have Cybernetics Core, have Stargate',
        'activate_tech': '',
        'activate_unit': ''
    },

    units.Protoss.WarpPrism: {
        # wiki英文 Unit
        'name': 'Warpprism',
        'name_cn': '折跃棱镜',
        # wiki英文 Details
        'description': 'Formerly known as the phase prism, the warp prism is a dual-purpose unit, '
                       'able to transport units or to create a warp matrix field like the pylon.'
                       'Warp Conduit:Passive ability. Increases the speed of warp in for units warped '
                       'into the power field to 4 seconds ',
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'mechanical', 'psionic'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 80,  # wiki中文 基本信息/生命值
        'shield': 100,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.9531,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 50,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 1.5,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 250,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Robotics Facility.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {
            'Gravitic Drive': 'Increases the movement speed of warp prisms from Normal (2.953) to Fast (3.375). '
                              'Cost: 100 minerals, 100 gas, 57 seconds. Purchased from Robotics Bay.',
        },
        'ability': {
            'Phase Mode/Transport Mode': 'Always available. The warp prism can transform to project a power field, '
                                         'allowing the warping in of units and powering Protoss structures. '
                                         'In Phase Mode, the warp prism is immobile. '
                                         'Cost: 0.75 seconds for both transformations.',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Robotics Facility, have Cybernetics Core, have Gateway',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': 'have Gateway/WarpGate, have Cybernetics Core, have Robotics Facility',
        'activate_tech': '',
        'activate_unit': ''
    },

    units.Protoss.Zealot: {
        # wiki英文 Unit
        'name': 'Zealot',
        'name_cn': '狂热者',
        # wiki英文 Details
        'description': 'Melee unit with the ability to charge, allowing it to quickly close the distance between '
                       'itself and an enemy unit.',
        'target': ['ground'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['light', 'biological'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 100,  # wiki中文 基本信息/生命值
        'shield': 50,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.25,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['ground'],
        'weapon1_type_anti': [],
        'weapon1_attack': 8,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 1,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 2,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1.2,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 28,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 38,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'train from GateWay or warp from WarpGate.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {

        },
        'ability': {
            'Charge': 'Passive ability. Available after Charge upgrade in Twilight Council. '
                      'The zealot charges towards a target enemy unit or structure, boosting its speed to 8.47 '
                      'for the duration. The zealot must have clear ground pathing to their target to reach it. '
                      'Range: 4, Duration: 2.5 seconds, Cooldown: 7 seconds.'
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': ''
    },

    # ---------------------- buildings ---------------------- #

    units.Protoss.Assimilator: {
        # wiki英文 Unit
        'name': 'Assimilator',
        'name_cn': '吸纳舱',
        # wiki英文 Details
        'description': 'Allows probes to harvest vespene gas from geysers.',
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 300,  # wiki中文 基本信息/生命值
        'shield': 300,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 30,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 75,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Probe.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {

        },
        'ability': {

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Nexus',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': ''
    },

    units.Protoss.CyberneticsCore: {
        # wiki英文 Unit
        'name': 'CyberneticsCore',
        'name_cn': '控制核心',
        # wiki英文 Details
        'description': 'Allows for the warping in of stalkers and sentries. '
                       'Also allows research of weapon and armor upgrades for air units.',
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 550,  # wiki中文 基本信息/生命值
        'shield': 550,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 50,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Probe.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {
            'WarpGateTransformation': 'Enables gateways to transform into warp gates. '
                                      'Cost: 50 minerals, 50 gas, 100 seconds. Requires Cybernetics Core.',
        },
        'ability': {

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': 'Robotics Facility, Stargate, Twilight Council, Shield Battery',
        'activate_tech': 'Air Weapons, Air Armor, WarpGate Transformation,, Hallucination',
        'activate_unit': 'Sentry, Stalker, Adept',
    },

    units.Protoss.DarkShrine: {
        # wiki英文 Unit
        'name': 'DarkShrine',
        'name_cn': '黑暗圣坛',
        # wiki英文 Details
        'description': 'Formerly known as the dark obelisk, it allows dark templar to be warped in.',
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 500,  # wiki中文 基本信息/生命值
        'shield': 500,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 100,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 150,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Probe.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {
            'ShadowStride': 'Teleports the Dark Templar to a nearby target location. '
                            'Has a 0.71 attack delay after use. '
                            'Cost: 100 minerals, 100 gas, 100 seconds. Requires Dark Shrine.',
        },
        'ability': {

        },
        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway, have Cybernetics Core, have Twilight Council',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': 'ShadowStride',
        'activate_unit': 'Dark Templar, Archon',

    },

    units.Protoss.FleetBeacon: {
        # wiki英文 Unit
        'name': 'FleetBeacon',
        'name_cn': '舰队航标',
        # wiki英文 Details
        'description': 'Allows the carrier and the mothership to be warped in.',
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 500,  # wiki中文 基本信息/生命值
        'shield': 500,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 60,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 300,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 200,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Probe.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {
            'Anion Pulse-Crystals': '+2 range to Phoenix attacks. '
                                    'Cost: 150 minerals, 150 gas, 64 seconds. Requires Fleet Beacon.',
            'Flux Vanes': 'Increases the void ray\'s movement speed to 4.65 and acceleration to 3.76. '
                          'Cost: 100 minerals, 100 gas, 57 seconds. Requires Fleet Beacon.',
            'Tectonic Destabilizers': 'Improves the Tempest\'s Resonance Coil to deal +40 damage vs structures. '
                                      'Cost: 150 minerals, 150 gas, 100 seconds. Requires Fleet Beacon.',
        },
        'ability': {

        },
        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway, have Stargate, have Cybernetics Core',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': 'Anion Pulse-Crystals, Flux Vanes, Tectonic Destabilizers',
        'activate_unit': 'Carrier, Mothership, Tempest',

    },

    units.Protoss.Forge: {
        # wiki英文 Unit
        'name': 'Forge',
        'name_cn': '锻炉',
        # wiki英文 Details
        'description': 'Allows the construction of photon cannons and research of Protoss ground unit upgrades.',
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 400,  # wiki中文 基本信息/生命值
        'shield': 400,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 45,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Probe.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {

        },
        'ability': {

        },
        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Nexus.',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': 'Photon Cannon',
        'activate_tech': 'Ground Weapons Upgrade, Ground Armor Upgrade, Shields Upgrade',
        'activate_unit': '',
    },

    units.Protoss.Gateway: {
        # wiki英文 Unit
        'name': 'Gateway',
        'name_cn': '传送门',
        # wiki英文 Details
        'description': 'Warps in the zealot, the stalker, the sentry, the high templar, and the dark templar.'
                       'WarpGateTransformation: Passive ability. Available after WarpGateTransformation upgrade in '
                       'Cybernetics Core. Enables gateways to transform into warp gates. Cost: 7 energy.',
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 500,  # wiki中文 基本信息/生命值
        'shield': 500,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 65,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Probe.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {

        },
        'ability': {

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': 'Cybernetics Core',
        'activate_tech': '',
        'activate_unit': 'Zealot',
    },

    units.Protoss.Nexus: {
        # wiki英文 Unit
        'name': 'Nexus',
        'name_cn': '星灵枢纽',
        # wiki英文 Details
        'description': 'Produces probes and is the place that all minerals and gas are dropped off at to be processed. '
                       'Also produces the mothership.',
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 1000,  # wiki中文 基本信息/生命值
        'shield': 1000,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 100,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 400,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Probe.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {

        },
        'ability': {
            'Chrono Boost': 'Always available. Increases the production speed of a structure by 50% for 20 seconds. '
                            'Cost: 25 energy.',
            'Strategic Recall': 'Always available. Recalls all allied units in the target area (2.5 radius) '
                                'to the Nexus. Cost: 50 energy. Duration: 0.4 seconds. Cooldown: 130 seconds '
                                '(global for all Nexuses).',
            'Battery Overcharge': 'Always available. Overcharges a target Shield Battery near a Nexus, '
                                  'increasing its shield restoration rate by 50% and allowing it to restore shields '
                                  'without consuming energy for 14 seconds. '
                                  'Cost: 50 energy. Cooldown: 60 seconds (global for all Nexuses).',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': 'Gateway',
        'activate_tech': '',
        'activate_unit': 'Probe',
    },

    units.Protoss.PhotonCannon: {
        # wiki英文 Unit
        'name': 'Photoncannon',
        'name_cn': '光子炮台',
        # wiki英文 Details
        'description': 'A defensive structure with a ranged attack effective against ground and air units.',
        'target': ['ground', 'air'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 150,  # wiki中文 基本信息/生命值
        'shield': 150,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['ground', 'air'],
        'weapon1_type_anti': [],
        'weapon1_attack': 20,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 7,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1.25,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 40,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Probe.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {

        },
        'ability': {
            'Detector': 'Passive ability. This unit or structure can detect cloaked, burrowed, '
                        'duplicated and hallucination enemies.'
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Forge',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Protoss.Pylon: {
        # wiki英文 Unit
        'name': 'Pylon',
        'name_cn': '水晶塔',
        # wiki英文 Details
        'description': 'The protoss supply building; it produces a radius of energy that is a requisite '
                       'for the placement of most other protoss structures.'
                       'Warp Conduit: Passive ability.Increases the speed of warp in for units warped into '
                       'the power field to 4 seconds(Only if the pylon is in range of a nexus or gateway/warp gate '
                       'with warp gate researched).',
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 200,  # wiki中文 基本信息/生命值
        'shield': 200,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 25,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Probe.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {

        },
        'ability': {

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },

    units.Protoss.RoboticsBay: {
        # wiki英文 Unit
        'name': 'RoboticsBay',
        'name_cn': '机械研究所',
        # wiki英文 Details
        'description': 'Formerly known as the null circuit, this structure enables a robotics facility to produce '
                       'colossi and contains upgrades for observers and warp prisms.',
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 500,  # wiki中文 基本信息/生命值
        'shield': 500,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 65,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 150,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Probe.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {
            'GraviticDrive': 'Increases the movement speed of warp prisms from Normal (2.953) to Fast (3.375). '
                             'Cost: 100 minerals, 100 gas, 57 seconds. Requires Robotics Bay.',
            'ExtendedThermalLance': 'Increases the range of the colossus\' attack from 7 to 9. '
                                    'Cost: 150 minerals, 150 gas, 100 seconds. Requires Robotics Bay.',
            'GraviticBoosters': 'Increases observer movement speed by 1.31. '
                                'Cost: 100 minerals, 100 gas, 57 seconds. Requires Robotics Bay.',
        },
        'ability': {

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway, have Cybernetics Core, have Robotics Facility',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': 'Gravitic Boosters, Gravitic Drive, Extended Thermal Lances',
        'activate_unit': 'Colossus, Disruptor',

    },

    units.Protoss.RoboticsFacility: {
        # wiki英文 Unit
        'name': 'RoboticsFacility',
        'name_cn': '机械台',
        # wiki英文 Details
        'description': 'Warps in the warp prism, observer, colossus, and immortal.',
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 450,  # wiki中文 基本信息/生命值
        'shield': 450,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 65,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Probe.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {

        },
        'ability': {

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway, have Cybernetics Core',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': 'Robotics Bay',
        'activate_tech': '',
        'activate_unit': 'Observer, Warp Prism, Immortal',

    },

    units.Protoss.ShieldBattery: {
        # wiki英文 Unit
        'name': 'ShieldBattery',
        'name_cn': '护盾充能器',
        # wiki英文 Details
        'description': 'Recharges the shields of protoss units and defensive structures.',
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 150,  # wiki中文 基本信息/生命值
        'shield': 150,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 40,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Probe.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {

        },
        'ability': {
            'Restore': 'Always available. Active skill. Restores target unit or structure\'s shields at a rate of '
                       '3 shields per 1 energy. Autocasting targets units and defensive structures only.',
        },
        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway, have Cybernetics Core',
        'require_tech': '',
        'require_unit': '',
        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Protoss.Stargate: {
        # wiki英文 Unit
        'name': 'Stargate',
        'name_cn': '星门',
        # wiki英文 Details
        'description': 'Warps in the phoenix, void ray and carrier.',
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 600,  # wiki中文 基本信息/生命值
        'shield': 600,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 60,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 150,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Probe.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {

        },
        'ability': {

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway, have Cybernetics Core',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': 'Fleet Beacon',
        'activate_tech': '',
        'activate_unit': 'Phoenix, Oracle, Void Ray',
    },

    units.Protoss.TemplarArchive: {
        # wiki英文 Unit
        'name': 'TemplarArchives',
        'name_cn': '圣堂武士文献馆',
        # wiki英文 Details
        'description': 'Allows the high templar unit to be warped in.',
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 500,  # wiki中文 基本信息/生命值
        'shield': 500,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 50,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 200,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Probe.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {
            'Shadow Stride': 'Teleports the Dark Templar to a nearby target location. '
                             'Has a 0.71 attack delay after use. '
                             'Range:5, Cooldown: 14, Cost: 100 Minerals, 100 gas, 100 seconds'
        },
        'ability': {

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway, have Cybernetics Core, have Twilight Council',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': 'Shadow Stride',
        'activate_unit': 'High Templar, Archon',
    },

    units.Protoss.TwilightCouncil: {
        # wiki英文 Unit
        'name': 'TwilightCouncil',
        'name_cn': '光影议会',
        # wiki英文 Details
        'description': 'Contains upgrades for stalkers and zealots.',
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 500,  # wiki中文 基本信息/生命值
        'shield': 500,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 50,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Probe.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {
            'Charge': 'The zealot charges towards a target enemy unit or structure, boosting its speed to 8.47 for '
                      'the duration. Also increases the zealot\'s normal movement speed to 4.725. '
                      'Cost: 100 minerals, 100 gas, 100 seconds. Requires Twilight Council.',
            'Blink': 'Stalkers instantly teleport over short distances, allowing them to strike from '
                     'unexpected quarters, catch fleeing foes, or escape unfavorable encounters. '
                     'Cost: 100 minerals, 100 gas, 121 seconds. Requires Twilight Council.',
            'Resonating Glaives': 'Increases the attack speed of the Adept by 45%. '
                                  'Cost: 100 minerals, 100 gas, 100 seconds. Requires Twilight Council.',
        },
        'ability': {

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway, have Cybernetics Core',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': 'Templar Archives, Dark Shrine',
        'activate_tech': 'Charge, Blink, Resonating Glaives',
        'activate_unit': '',
    },

    units.Protoss.WarpGate: {
        # wiki英文 Unit
        'name': 'WarpGate',
        'name_cn': '折跃门',
        # wiki英文 Details
        'description': 'The gateway has the ability to transform into a warp gate, '
                       'which can warp-in units at any spot within the psionic matrix.',
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 500,  # wiki中文 基本信息/生命值
        'shield': 500,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 10,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 0,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Gateway.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {
            'WarpGateTransformation': 'Enables gateways to transform into warp gates. '
                                      'Cost: 50 minerals, 50 gas, 100 seconds. Requires Cybernetics Core.',
        },
        'ability': {

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway, have Cybernetics Core',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': 'Warp Gate Transformation',
        'activate_unit': '',
    },

    units.Protoss.AdeptPhaseShift: {
        # wiki英文 Unit
        'name': 'AdeptPhaseShift',
        'name_cn': '使徒影子',
        # wiki英文 Details
        'description': 'An invulnerable psionic image come from Adept that can move but not attack. '
                       'After 7 seconds, the adept teleports to the images location. '
                       'The shade may be canceled at any time, and the adept would not teleport. '
                       'The shade has a sight radius of 2.',
        # 可以对什么对象造成伤害，ground/air
        'target': [''],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': [''],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['psionic'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [''],

        # 生存
        'health': 0,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.5,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [''],
        'weapon1_type_anti': [''],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 11,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 0,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'built from Adept.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway/WarpGate , have Cybernetics Core',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },

    units.Protoss.DisruptorPhased: {
        # wiki英文 Unit
        'name': 'DisruptorPhased',
        'name_cn': '自爆球',
        # wiki英文 Details
        'description': 'A ball of energy that detonates after 2.1 seconds,shoot out by the Disruptor, dealing '
                       '145 splash damage and an additional 55 shield damage to nearby ground units and structures. '
                       'The Disruptor is immobile while this is active.',
        'target': ['ground'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'mechanical'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 0,                   # wiki中文 基本信息/生命值
        'shield': 0,                   # wiki中文 基本信息/护盾
        'health_armor': 0,              # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,      # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 5.95,                # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['ground'],
        'weapon1_type_anti': ['shield'],
        'weapon1_attack': 145,                           		# wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 55,                              # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,         # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,        # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 1.5,                              # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,                              # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 21,                               # wiki中文 作战/武器/攻击间隔


        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 4,                                    # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,                                # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 50,                             # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,                    # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 150,                        # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Shoot out by the Disruptor',      # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {
        },
        'ability': {
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway, have Cybernetics Core, have Robotics Facility, have Robotics Bay',
        'require_tech': '',
        'require_unit': '',
        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },


    units.Protoss.Interceptor: {
        # wiki英文 Unit
        'name': 'Interceptor',
        'name_cn': '截击机',
        # wiki英文 Details
        'description': 'The Interceptor is a small, autonomous flying unit that gives the Protoss Carrier its '
                       'offensive capabilities. Each Carrier warps in with an initial set of 4 Interceptors that can '
                       'attack immediately. Additional Interceptors are trained in the Carrier itself. Each Carrier '
                       'can support a maximum of 8 Interceptors at any one time. Unlike most offensive units, '
                       'Interceptors require no supply points.',
        # 可以对什么对象造成伤害，ground/air
        'target': ['ground', 'air'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['light', 'mechanical'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 40,  # wiki中文 基本信息/生命值
        'shield': 40,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 10.5,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': ['ground', 'air'],
        'weapon1_type_anti': [],
        'weapon1_attack': 5,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 2,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 2,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 2.14,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 9,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 15,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'Built from Carrier.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Gateway/WarpGate, have Stargate, have Cybernetics Core, have FleetBeacon',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Protoss.WarpPrismPhasing: {
        # wiki英文 Unit
        'name': 'WarpPrismPhasing',
        'name_cn': '折跃棱镜(相位模式)',
        # wiki英文 Details
        'description': 'Immobile energy supply unit. Can load or unload units. '
                       'Capable of transforming into a mobile transport unit.',
        'target': [],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'mechanical', 'psionic'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 80,  # wiki中文 基本信息/生命值
        'shield': 100,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        # 作战 weapon1
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 1.5,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 0,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'transform from WarpPrism.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # 默认值为0
        'upgrade': {
        },
        'ability': {
            'Transport Mode': 'Always available. The WarpPrismPhasing can transform to WarpPrism. Cost: 0.75 seconds.',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Robotics Facility, have Cybernetics Core, have Gateway',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': ''
    },

}

if __name__ == "__main__":
    for key in DATA_PROTOSS.keys():
        print(key)
    print(f"unit number: {len(DATA_PROTOSS.keys())}\n")

    for key in protoss_research_conditions.keys():
        print(f"{str(actions.FUNCTIONS[key])}: \n\t\t{protoss_research_conditions[key]}")
    for key in protoss_train_conditions.keys():
        print(f"{str(actions.FUNCTIONS[key])}: \n\t\t{protoss_train_conditions[key]}")
    for key in protoss_build_conditions.keys():
        print(f"{str(actions.FUNCTIONS[key])}: \n\t\t{protoss_build_conditions[key]}")
