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

from pysc2.lib import units

DATA_TERRAN = {

    units.Terran.SCV: {
        'name': 'SCV',
        'name_cn': 'SCV',
        'description': "The builder and resource gatherer of the terran race. "
                       "Its Repair ability can be set to 'autocast'",
        'target': ['ground'],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        'type_self': ['light', 'biological', 'mechanical'],
        'type_anti': [],

        'health': 45,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 3.94,  # wiki中文 基本信息/移动速度

        'weapon1_target': ['ground'],
        'weapon1_type_anti': [],
        'weapon1_attack': 5,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 1,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 1.07,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,

        'supply': 1,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 17,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 50,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': ['CommandCenter', 'OrbitalCommand', 'PlanetaryFortress'],  # wiki中文 生产/生产设施

        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {},  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        "ability": {
            # "Repair": "Always available. Restores mechanical unit or building, terran or protoss. "
            #           "Repairing costs resources. The ability can be autocast.",
            # "Worker Abilities": "Always available. The SCV builds structures and harvests minerals and vespene gas. "
        },
        # 前置条件,这一部分需要游戏知识
        'require_building': 'CommandCenter',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Terran.Marine: {
        'name': 'Marine',
        'name_cn': '陆战队员',
        'description': 'The basic terran infantry, able to upgrade hit points with a shield.',
        'target': ['ground', 'air'],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        'type_self': ['light', 'biological'],
        'type_anti': [],

        'health': 45,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 3.15,

        'weapon1_target': ['ground', 'air'],
        'weapon1_type_anti': [],
        'weapon1_attack': 6,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 5,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0.8608,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,

        'supply': 1,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 25,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 50,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Barracks.',  # wiki中文 生产/生产设施

        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {
            'Stimpack': 'upgraded in TechLab.Every Marine and Marauder gain the Stimpack ability.'
                        'Cost 100 mineral, 100 gas and 100 seconds. Required TechLab.',

            'Combat Shield': 'upgraded in TechLab.Every Marine gains a Combat Shield that gives 10 hitpoints.'
                             'Cost 100 mineral, 100 gas and 79 seconds. Required TechLab.'},
        # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },

        "ability": {
            "Stimpack": "Upgrade in TechLab. Increases the movement speed and firing rate by 50% "
                        "for 11 seconds at the cost of 10 HP for a Marine."
        },

        'require_building': 'Barracks',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Terran.CommandCenter: {
        'name': 'CommandCenter ',
        'name_cn': '指挥中心',
        'description': 'Produces SCVs and serves as a drop off point for processing of minerals and gas. '
                       'Has the ability to carry up to five SCVs and can upgrade to the powerfully armed '
                       'PlanetaryFortress or the ability oriented OrbitalCommand.Provding 15 supply.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        'type_self': ['armored', 'mechanical', 'structure'],
        'type_anti': [],

        'health': 1500,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': '',  # wiki中文 基本信息/移动速度

        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,

        'supply': 0,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 71,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 400,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'SCV',  # wiki中文 生产/生产设施

        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {
            "Neosteel Armor": "Always available. Upgrades the armor of structures by 2 (excluding auto-turrets). "
                              "Increases the cargo space of bunkers by 2. Also provides extra cargo space for "
                              "CommandCenters and PlanetaryFortresses. Cost: 150 mineral, 150 gas, 140 s."
        },  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        "ability": {
            'OrbitalCommand': 'Always available.Transform into OrbitalCommand',
            'PlanetaryFortress': 'Always available.Transform into PlanetaryFortress',
            "Load": "Always available. "
                    "Enables the Terran player to load SCVs into a CommandCenter or PlanetaryFortress.",
            "Lift off": "Always available. "
                        "This structure can lift off, enabling it to fly. It cannot produce units or conduct "
                        "research while in flight, and must leave add-ons behind.",
            "Land": 'Available after Lift off. Select the building while it is in the air and use the Land '
                    'command to have it settle down at a designated location. When landing, ensure there is enough '
                    'space and that no units or other structures are obstructing the landing spot.',
            "Unload": "Always available. Unload all SCVs."
        },

        # 前置条件,这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': 'SCV',
    },

    units.Terran.OrbitalCommand: {
        'name': 'OrbitalCommand',
        'name_cn': '轨道控制基地',
        # wiki英文 Details
        'description': 'This upgrade to the CommandCenter provides scanner sweeps to reveal troop movements through '
                       'the fog of war and detect cloaked or burrowed units, summons MULEs, '
                       'and can increase the supply generated by SupplyDepots.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['armored', 'mechanical', 'structure'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 1500,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': '',  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,
        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 25,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'CommandCenter.',  # wiki中文 生产/生产设施
        'energy': 200,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {''},  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {  # wiki英文 作战/技能,只记录主动技能
            'Calldown: MULE': 'Always available.An OrbitalCommand summons one MULE via drop pod. If the ability is '
                              'targeted on a mineral patch the MULE will begin mining automatically, extracting 45 '
                              'minerals per trip. The ability may be used only on areas uncovered by the fog of war.'
                              'cost 50 energy,Duration: 64 s',
            'Calldown: Extra Supplies': 'Always available.The OrbitalCommand can target a SupplyDepot to permanently '
                                        'grant it an extra 8 supply. The modified SupplyDepots look different, '
                                        'but are still capable of raising and lowering themselves.'
                                        'cost 50 energy,Duration: 3 s',
            'Scanner Sweep': 'Always available.The OrbitalCommand scans a target location on the map revealing '
                             'cloaked, burrowed or hallucinated units temporarily.'
                             'cost 50 energy,Duration: 9 s',
            'Lift off': 'Always available. This structure can lift off, enabling it to fly. '
                        'It cannot produce units or conduct research while in flight, and must leave add-ons behind.',
            "Land": 'Available after Lift off.Select the building while it is in the air and use the Land command '
                    'to have it settle down at a designated location. When landing, ensure there is enough space '
                    'and that no units or other structures are obstructing the landing spot.',
            "Load": "Always available. "
                    "Enables the Terran player to load SCVs into a CommandCenter or PlanetaryFortress.",
            "Unload": "Always available. "
                      "Unload all SCVs."
        },

        # 前置条件,这一部分需要游戏知识
        'require_building': 'Barracks',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': 'MULE',

    },

    units.Terran.PlanetaryFortress: {
        'name': 'PlanetaryFortress',
        'name_cn': '行星要塞',
        # wiki英文 Details
        'description': 'This immobile upgrade of the CommandCenter grants it weapons to attack enemy '
                       'ground units and a large boost to armor.Provides 11 supply.',
        'target': ['ground'],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['armored', 'mechanical', 'structure'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 1500,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 3,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        'weapon1_target': ['ground'],
        'weapon1_type_anti': [],
        'weapon1_attack': 40,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 6,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 1.43,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,
        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 36,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 150,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'CommandCenter.',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {
            'Hi-Sec Auto Tracking': "Increases the attack range of automated defenses: missile turrets, auto-turrets, "
                                    "point defense drones, and the PlanetaryFortress by +1. "
                                    "Cost: 100 mineral, 100 gas, Duration: 57 s.",
            "Neosteel Armor": "Always available. "
                              "Upgrades the armor of structures by 2 (excluding auto-turrets). Increases the cargo "
                              "space of bunkers by 2. Also provides extra cargo space for CommandCenters and "
                              "PlanetaryFortresses. Cost: 150 mineral, 150 gas, 140 s."
        },  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {  # wiki英文 作战/技能,只记录主动技能
            'Load': 'Enables the Terran player to load SCVs into a CommandCenter or PlanetaryFortress.',
            'Unload': 'Unload all SCVs'
        },

        # 前置条件,这一部分需要游戏知识
        'require_building': 'Engineering Bay',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },

    units.Terran.Barracks: {
        'name': 'Barracks',
        'name_cn': '兵营',
        # wiki英文 Details
        'description': 'Produces terran infantry units.Marine/Reaper/Marauder '
                       '(with TechLab)/Ghost (with TechLab and GhostAcademy).',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['armored', 'mechanical', 'structure'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 1000,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 46,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'CommandCenter.',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {},  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {  # wiki英文 作战/技能,只记录主动技能
            "Lift off": "Always available. This structure can lift off, enabling it to fly. It cannot produce units "
                        "or conduct research while in flight, and must leave add-ons behind.",
            "Land": 'Available after Lift off.Select the building while it is in the air and use the Land command '
                    'to have it settle down at a designated location. When landing, ensure there is enough space '
                    'and that no units or other structures are obstructing the landing spot.',
            'Create Reactor': 'Always available. This structure can create a Reactor.',
            'Create TechLab': 'Always available. This structure can create a TechLab.'
        },

        # 前置条件,这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': ['Factory', 'GhostAcademy'],
        'activate_tech': '',
        'activate_unit': 'Marine/Reaper/Marauder (with TechLab)/Ghost (with TechLab and GhostAcademy)',

    },

    units.Terran.Bunker: {
        'name': 'Bunker',
        'name_cn': '地堡',
        # wiki英文 Details
        'description': 'Provides protection for terran infantry.',
        'target': ['ground', 'air(with Marine)'],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['armored', 'mechanical', 'structure'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 400,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 29,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'SCV',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {},  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {  # wiki英文 作战/技能,只记录主动技能
            'Salvage': 'Always available. Removes the structure and returns 75% of the structures mineral and vespene '
                       'gas cost. The process may not be aborted once started. '
                       'A bunker cannot be salvaged while units are still in it.'
        },

        # 前置条件,这一部分需要游戏知识
        'require_building': 'Barrack',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },

    units.Terran.Factory: {
        'name': 'Factory',
        'name_cn': '工厂',
        # wiki英文 Details
        'description': 'Produces terran vehicle units.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['armored', 'mechanical', 'structure'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 1250,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 43,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'SCV',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {},  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {  # wiki英文 作战/技能,只记录主动技能
            "Lift off": "Always available. This structure can lift off, enabling it to fly. It cannot produce units "
                        "or conduct research while in flight, and must leave add-ons behind.",
            "Land": 'available after Lift off.Select the building while it is in the air and use the Land command '
                    'to have it settle down at a designated location. When landing, ensure there is enough space and '
                    'that no units or other structures are obstructing the landing spot.',
            'Create Reactor': 'Always available.This structure can create a Reactor.',
            'Create TechLab': 'Always available.This structure can create a TechLab.'
        },

        # 前置条件,这一部分需要游戏知识
        'require_building': 'Barrack',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': 'Starport',
        'activate_tech': '',
        'activate_unit': 'Hellion/Hellbat/SiegeTank(with TechLab)/ '
                         'Thor(with TechLab and Armory)/WidowMine/Cyclone(with TechLab)',

    },

    units.Terran.Starport: {
        'name': 'Starport',
        'name_cn': '星港',
        # wiki英文 Details
        'description': 'Produces terran air units.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['armored', 'mechanical', 'structure'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 1300,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 36,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'SCV',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {},  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {  # wiki英文 作战/技能,只记录主动技能
            "Lift off": "Always available. This structure can lift off, enabling it to fly. "
                        "It cannot produce units or conduct research while in flight, and must leave add-ons behind.",
            "Land": 'available after Lift off.Select the building while it is in the air and use the Land command '
                    'to have it settle down at a designated location. When landing, ensure there is enough space '
                    'and that no units or other structures are obstructing the landing spot.',
            'Create Reactor': 'Always available. This structure can create a Reactor.',
            'Create TechLab': 'Always available. This structure can create a TechLab.',
        },

        # 前置条件,这一部分需要游戏知识
        'require_building': 'Factory',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': 'FusionCore',
        'activate_tech': '',
        'activate_unit': 'Viking/MedivacDropship/Liberator/Raven (with TechLab)/'
                         'Banshee (with TechLab)/Battlecruiser (with TechLab and FusionCore)',

    },

    units.Terran.EngineeringBay: {
        'name': 'EngineeringBay',
        'name_cn': '工程站',
        # wiki英文 Details
        'description': 'Upgrades infantry and buildings.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['armored', 'mechanical', 'structure'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 850,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 36,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 125,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'SCV',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {},  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        "ability": {
            # "Infantry Weapons": "Always available. +1 damage for Marines and reapers; +1 base damage and +1 bonus damage for marauders and Ghosts."' Level 1/2/3 cost: {100 mineral, 100 gas, Duration: 160 s}/{175 mineral, 175 gas, Duration: 190 s}/{250 mineral, 250 gas, Duration: 220s}.',
            # "Infantry Armor": "Always available. +1 to armor for SCVs, Marines, firebats, marauders, medics, reapers, spectres, and Ghosts. Level 1/2/3 cost: {100 mineral, 100 gas, Duration: 160 s}/{175 mineral, 175 gas, Duration: 190 s}/{250 mineral, 250 gas, Duration: 220s}.",
        },  # wiki英文 作战/技能,只记录主动技能        },

        # 前置条件,这一部分需要游戏知识
        'require_building': 'Barracks',
        'require_tech': 'Infantry Weapons/Infantry Armor level2 requires Factory ',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': ['Missile turret', 'SensorTower', 'PlanetaryFortress'],
        'activate_tech': ['Hi-Sec Auto Tracking', "Neosteel Armor"],
        'activate_unit': '',

    },

    units.Terran.MissileTurret: {
        'name': 'Missile turret',
        'name_cn': '导弹炮台',
        # wiki英文 Details
        'description': 'Anti-air turret that fires two missiles at a time.',
        'target': ['air'],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['armored', 'mechanical', 'structure'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 250,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        'weapon1_target': ['air'],
        'weapon1_type_anti': [],
        'weapon1_attack': 12,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 7,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 2,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0.8608,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 25,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'SCV',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {
            'Hi-Sec Auto Tracking': "Increases the attack range of automated defenses: missile turrets, "
                                    "auto-turrets, point defense drones, and the PlanetaryFortress by +1. "
                                    "Cost: 100 mineral, 100 gas, Duration: 57 s.",
        },
        # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {
            'Detector': 'Always available.This unit or structure can detect cloaked, '
                        'burrowed, duplicated and hallucination enemies.'
        },
        # wiki英文 作战/技能,只记录主动技能        },

        # 前置条件,这一部分需要游戏知识
        'require_building': 'Engineering bay',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },

    units.Terran.SensorTower: {
        'name': 'SensorTower',
        'name_cn': '感应塔',
        # wiki英文 Details
        'description': 'Can sense enemy units through the fog of war.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['armored', 'mechanical', 'structure'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 250,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 25,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 125,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'SCV',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {},  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {
            'Radar': 'Always available. Able to expose enemy movements within its radar capability. '
                     'Does not reveal the area.'},
        # wiki英文 作战/技能,只记录主动技能        },

        # 前置条件,这一部分需要游戏知识
        'require_building': 'Engineering bay',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },

    units.Terran.SupplyDepot: {
        'name': 'SupplyDepot',
        'name_cn': '补给站',
        # wiki英文 Details
        'description': 'Provides 8 supply required for additional terran units and can submerge, '
                       'enabling troops to walk over it.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['armored', 'mechanical', 'structure'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 250,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速

        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 25,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 125,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'SCV',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {},  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {
            'Lower': 'Lowers the structure into the ground so ground units may pass over it. ',
            # wiki英文 作战/技能,只记录主动技能        },
            'Raise': 'Available after Lower.The structure may be raised back to block pathing. Friendly units '
                     'standing on the structure are pushed toward the nearest edge when the structure is '
                     'raised. Enemy units standing on top prevent the structure from being raised.'
        },
        # 前置条件,这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },

    units.Terran.Refinery: {
        'name': 'Refinery',
        'name_cn': '精炼厂',
        # wiki英文 Details
        'description': 'Refines vespene gas for collection by SCVs.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['armored', 'mechanical', 'structure'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 500,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速

        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 30,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 75,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'SCV',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {},  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {},  # wiki英文 作战/技能,只记录主动技能        },

        # 前置条件,这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },

    units.Terran.GhostAcademy: {
        'name': 'GhostAcademy',
        'name_cn': '幽灵研究院',
        # wiki英文 Details
        'description': 'This structure enables Ghosts to be produced and provides researches for them. '
                       'In addition, it stores nuclear missiles for launch.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['armored', 'mechanical', 'structure'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 1250,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速

        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 40,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 50,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'SCV',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {},  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {
            'Arm Silo with Nuke': 'Arms the silo with a tactical nuke.Nukes take 20 seconds to land, but they deal '
                                  'up to 300 (+200 vs. structures) damage in a large radius.'},
        # wiki英文 作战/技能,只记录主动技能        },

        # 前置条件,这一部分需要游戏知识
        'require_building': 'Barracks',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': ['Cloak', 'Enhanced Shockwaves'],
        'activate_unit': 'Ghost',

    },

    units.Terran.Armory: {
        'name': 'Armory',
        'name_cn': '军械库',
        # wiki英文 Details
        'description': 'This structure enables Ghosts to be produced and provides researches for them. In addition, '
                       'it stores nuclear missiles for launch.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['armored', 'mechanical', 'structure'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 750,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速

        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 50,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 50,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'SCV',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {
            # 'Terran ship Weapons':'+1 damage for banshees and battlecruisers,+1 air damage,+1 base ground damage and +1 bonus damage for vikings,+1 air damage,+5 ground damage for liberators.',
            #          'level1/2/3 cost {100 mineral,100 gas,Duration: 160 s}/{175 mineral,175 gas,Duration: 190 s}/{250 mineral,250 gas,Duration: 220s}'
            #         'Terran Vehicle Weapons':'+1 damage for cyclones,+1 base damage and +1 bonus damage for hellions,+2 damage for hellbats,+2 base damage and +1 bonus damage for SiegeTanks (tank mode),+4 base damage and +1 bonus damage for SiegeTanks (siege mode),+3 ground damage,+1/+3 air base damage and +1 bonus damage for thors (AoE/single-target)',
            #         'level1/2/3 cost {100 mineral,100 gas,Duration: 160 s}/{175 mineral,175 gas,Duration: 190 s}/{250 mineral,250 gas,Duration: 220s}'
            #         'Terran Vehicle and Ship Plating':'Increases the armor of terran vehicles and spacecraft.'
            #         'level 1/2/3 cost {100 mineral,100 gas,Duration: 160 s}/{175 mineral,175 gas,Duration: 190 s}/{250 mineral,250 gas,Duration: 220s}'
        },  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {},

        # 前置条件,这一部分需要游戏知识
        'require_building': 'Factory',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': 'thor',

    },

    units.Terran.FusionCore: {
        'name': 'FusionCore',
        'name_cn': '聚变芯体',
        # wiki英文 Details
        'description': 'Formerly known as the anti-matter core and the deep space relay, this structure allows '
                       'production of battlecruisers and provides researches for them.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['armored', 'mechanical', 'structure'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 750,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速

        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 46,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 150,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'SCV',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {'Weapon Refit': 'Enables use of the Battlecruiser Yamato Cannon, dealing 240 damage to a target.',
                    'cost 150 mineral,150 gas,Duration: 60 s'
                    'Caduceus Reactor': 'Increases the energy regeneration of Medivacs by 100%.',
                    'cost 150 mineral,150 gas,Duration: 60 s'
                    'Advanced Ballistics': 'Upgrades the range of the Liberators anti-ground attack to 12.'
                                           'cost 150 mineral,150 gas,Duration: 79 s'
                    },  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {},

        # 前置条件,这一部分需要游戏知识
        'require_building': 'Starport',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': 'Battlecruiser',

    },

    units.Terran.TechLab: {
        'name': 'TechLab',
        'name_cn': '科技实验室',
        # wiki英文 Details
        'description': 'Enables the production of "higher tech" units. For instance, adding a TechLab to a '
                       'Barracks will allow it to produce marauders, while adding one to a Factory will enable it to '
                       'build SiegeTanks. Upgrades Marine combat shields and specific upgrades and special abilities '
                       'for the hellion, SiegeTank, viking, banshee, MedivacDropship, and raven.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['structure', 'mechanical', 'armored'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 400,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速

        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 18,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 50,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 25,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': ['Barracks', 'Factory', '	Starport'],  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {},  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {},

        # 前置条件,这一部分需要游戏知识
        'require_building': 'Engineering Bay',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': ['Combat Shield', 'StimPack', 'Infernal Pre-Igniter', 'Hurricane Engines', 'Drilling Claws',
                          'Smart Servos', 'Cloaking Field', 'Hyperflight Rotors', 'Interference Matrix'],
        'activate_unit': '',

    },

    units.Terran.Reactor: {
        'name': 'Reactor',
        'name_cn': '反应堆',
        # wiki英文 Details
        'description': 'Doubles the number of units produced from the building to which it is attached. (For instance, '
                       'adding one to a Barracks will enable it to create two Marines at the same time.)',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        'type_self': ['structure', 'mechanical', 'armored'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 400,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速

        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 36,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 50,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 50,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': ['Barracks', 'Factory', '	Starport'],  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {},  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {},  # 前置条件,这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Terran.MULE: {
        'name': 'MULE',
        'name_cn': '矿骡',
        # wiki英文 Details
        'description': 'A temporary unit summoned by an OrbitalCommand that harvests minerals for a limited time span.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['light', 'mechanical'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 60,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 3.94,  # wiki中文 基本信息/移动速

        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 0,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 0,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Orbit command',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {},  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {},

        # 前置条件,这一部分需要游戏知识
        'require_building': 'Orbit command',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },

    units.Terran.Marauder: {
        'name': 'Marauder',
        'name_cn': '劫掠者',
        # wiki英文 Details
        'description': 'The replacement for the firebat.Its attack slows enemy '
                       'units and deals high damage vs armored units.',
        'target': ['ground'],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['armored', 'Biological'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 60,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.25,  # wiki中文 基本信息/移动速

        'weapon1_target': ['ground'],
        'weapon1_type_anti': ['armored'],
        'weapon1_attack': 10,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 10,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 2,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 6,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 1.5,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 30,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 25,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Orbit command',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {
            'Stimpack': 'Every Marine and Marauder gain the Stimpack ability. '
                        'Cost 100 mineral, 100 gas and 100 seconds. Required TechLab.',
            'Concussive Shells': 'Marauder attacks slow the movement speed of non-massive enemy units by 50%. '
                                 'Only affects one target at a time. '
                                 'Cost 50 mineral, 50 gas and 60 seconds. Required TechLab.'
            },  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {  # wiki英文 作战/技能,只记录主动技能
            'Stimpack': 'Available after upgraded in TechLab. Increases the movement speed and firing rate by 50% '
                        'for 11s at the cost of 10 HP for a Marine.'
        },

        # 前置条件,这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': 'TechLab',
        'activate_tech': '',
        'activate_unit': '',

    },

    units.Terran.Ghost: {
        'name': 'Ghost',
        'name_cn': '幽灵',
        # wiki英文 Details
        'description': 'Stealth specialist with access to several powerful abilities',
        'target': ['ground', 'air'],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['Biological', 'Psionic'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 60,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.25,  # wiki中文 基本信息/移动速

        'weapon1_target': ['ground'],
        'weapon1_type_anti': ['armored'],
        'weapon1_attack': 10,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 10,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 2,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 4,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 6,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 1.5,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 29,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 200,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Orbit command',  # wiki中文 生产/生产设施
        'energy': 200,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {
            'Cloak': 'upgrade in GhostAcademy''Enables Ghosts to cloak.'
                     'cost 150minerals ,150 gas ,120 s'
            # 'Enhanced Shockwaves':'Increases the radius of Ghosts EMP Round from 1.5 to 2 (+0.5).'好像被删了
        },  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {  # wiki英文 作战/技能,只记录主动技能
            'EMP Shot': 'Drains 100 shields from protoss units and drains 100 energy from units in the area of effect, '
                        'including friendly units. Shield upgrades have no effect.The EMP field has an area-of-effect '
                        'of 1.5.Cloaked units are revealed for a short time. Burrowed units are not.'
                        'Cost 75 Energy,Range 10',
            'Steady Targeting': 'always available''After carefully aiming for 1.43 seconds while not taking damage, '
                                'the Ghost fires a sniper round dealing 130 damage (+40 vs Psionic). Ignores armor. '
                                'Can only target biological units.This ability is cancelled if the target moved a over '
                                '13.5 range away from the Ghost. This ability can also be manually cancelled.'
                                'Cost 50 Energy ,Range 10,Cooldown,1.43',
            'Cloak': 'Enables Ghosts to cloak.'
                     'cost 25 (+0.9 per second) energy',
            'Nuclear Strike': 'Ghosts and spectres can call down nuclear strikes, dealing 300 damage + 200 vs '
                              'buildings.The launching player sees a large red symbol on the target area while the '
                              'opponent only sees a red dot. When the Ghost is aiming the nuke, it will be "frozen", '
                              'but it can still be given the order to "move away", which it will do the moment '
                              'it is unfrozen.'
                              'Cost 100 Minerals, 100  gas, 14 second drop time seconds ,Range  12'

        },

        # 前置条件,这一部分需要游戏知识
        'require_building': ['GhostAcademy', 'TechLab'],
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },

    units.Terran.Reaper: {
        'name': 'Reaper',
        'name_cn': '死神',
        # wiki英文 Details
        'description': 'Exceptionally fast infantry that uses dual pistols, '
                       'can jet pack up and down ledges and uses explosives vs buildings.',
        'target': ['ground'],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['Biological', 'Light'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 60,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 5.25,  # wiki中文 基本信息/移动速

        'weapon1_target': ['ground'],
        'weapon1_type_anti': ['light'],
        'weapon1_attack': 10,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 10,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 6,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 1.07,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 1,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 45,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 50,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 50,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Barracks',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {
        },  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {  # wiki英文 作战/技能,只记录主动技能
            'Combat Drugs': 'Always available''Drains 100 shields from protoss units and drains 100 energy from units '
                            'in the area of effect, including friendly units. Shield upgrades have no effect. The EMP '
                            'field has an area-of-effect of 1.5.Cloaked units are revealed for a short time. '
                            'Burrowed units are not.',
            'Jet Pack': 'Always available. '
                        'Reapers can jump up and down cliffs.',
            'KD8 Charge': 'Always available. '
                          'Explodes after a short delay, dealing 5 damage and knocking back nearby units.'
        },

        # 前置条件,这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },

    units.Terran.Hellion: {
        'name': 'Hellion',
        'name_cn': '恶火战车',
        # wiki英文 Details
        'description': 'Formerly known as the Jackal, this fast vehicle is armed with a '
                       'flamethrower suited for destroying masses of weaker units.',
        'target': ['ground'],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['mechanical', 'Light'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['Light'],

        # 生存
        'health': 90,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 4.25,  # wiki中文 基本信息/移动速

        'weapon1_target': ['ground'],
        'weapon1_type_anti': ['light'],
        'weapon1_attack': 8,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 6,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 5,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 2.5,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 30,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Factory',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {
            'Infernal Pre-Igniter': 'Available after upgraded in TechLab. Increases the hellions attack damage by '
                                    '+5 (to +11) vs light units and the hellbats attack damage by +12 vs light units. '
                                    'Cost 150 minerals,150 gas ,110 s',
            'Smart Servos': 'Available after upgraded in TechLab. Allows Hellions, Hellbats, Vikings, and Thors to '
                            'transform quickly between combat modes.'
                            'cost 150 minerals,150 gas ,110 s',
        },  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {
            'Hellion Transformation': 'Armory required. The Hellion/Hellbat transforms from one mode to another. '
                                      'The ability is not smartcast.'
            # wiki英文 作战/技能,只记录主动技能
        },

        # 前置条件,这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },

    units.Terran.Hellbat: {
        'name': 'Hellbat',
        'name_cn': '恶蝠',
        # wiki英文 Details
        'description': 'Transformable variant unit from the hellion, better equipped for close combat.',
        'target': ['ground'],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['mechanical', 'Light', 'biological'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['Light'],

        # 生存
        'health': 135,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.25,  # wiki中文 基本信息/移动速

        'weapon1_target': ['ground'],
        'weapon1_type_anti': ['light'],
        'weapon1_attack': 18,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 12,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 2,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 2,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 2,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 2,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 30,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Factory',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {
            'Infernal Pre-Igniter': 'Available after upgraded in TechLab. Increases the hellions attack damage by '
                                    '+5 (to +11) vs light units and the hellbats attack damage by +12 vs light units. '
                                    'The flame changes to a blue color.The flame color on the icon was changed '
                                    'to blue in patch 1.3.5.'
                                    'cost 150 minerals,150 gas ,110 s',
            'Smart Servos': 'Available after upgraded in TechLab. Allows Hellions, Hellbats, Vikings, and Thors to '
                            'transform quickly between combat modes.'
                            'cost 150 minerals,150 gas ,110 s',
        },  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {
            'Hellion Transformation': 'Armory required. The Hellion/Hellbat transforms from one mode to another. '
                                      'The ability is not smartcast. Requires Armory.'
            # wiki英文 作战/技能,只记录主动技能
        },
        # 前置条件,这一部分需要游戏知识
        'require_building': 'Armory',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Terran.Cyclone: {
        'name': 'Hellbat',
        'name_cn': '飓风',
        # wiki英文 Details
        'description': 'Mobile assault unit, armed with twin Typhoon missile pods that engage air and ground threats',
        'target': ['ground', 'air'],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['mechanical', 'armored'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['mechanical'],

        # 生存
        'health': 130,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 3.94,  # wiki中文 基本信息/移动速

        'weapon1_target': ['ground', 'air'],
        'weapon1_type_anti': ['mechanical'],
        'weapon1_attack': 11,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 3,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 6,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0.812,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 45,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 125,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 50,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Factory',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {
            'Hurricane Engines': 'upgraded in TechLab''Increases the move speed of Cyclones from 3.94 to 4.73.'
                                 'cost 100 minerals,100 gas ,140 s',
        },  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {
            'Lock On': 'always available''Locks the Cyclones weapons on the target unit, increasing the Cyclone\'s '
                       'range to 9 and allowing it to move while firing. Canceled if the target moves out of range '
                       '(9) or vision. Can be set to autocast.',
            # wiki英文 作战/技能,只记录主动技能
        },
        # 前置条件,这一部分需要游戏知识
        'require_building': 'TechLab',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Terran.WidowMine: {
        'name': 'WidowMine',
        'name_cn': '寡妇雷',
        # wiki英文 Details
        'description': 'Mobile defensive unit, buries and launches missiles at foes',
        'target': ['ground', 'air'],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['mechanical', 'light'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['mechanical'],

        # 生存
        'health': 130,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.8125,  # wiki中文 基本信息/移动速

        'weapon1_target': ['ground', 'air'],
        'weapon1_type_anti': ['mechanical'],
        'weapon1_attack': 11,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 3,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 6,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0.812,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 30,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 75,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 25,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Factory',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {
            'Drilling Claws': 'Available after upgraded in TechLab. Reduces the time Activate Mine takes to burrow '
                              'and unburrow the WidowMine from 3 seconds to 1.07 seconds.Unlocks the Concealment '
                              'upgrade, preventing the WidowMine from being revealed by default when reloading.'
                              'cost 75 minerals, 75 gas, 110 s'
        },  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {
            'Sentinel Missiles': 'Always available. '
                                 'The WidowMine fires a sentinel missile that deals 125 damage (+35 vs. shields) '
                                 'and 40 (+25 vs. shields) splash damage to units within 1.75 radius. '
                                 'The ability is automatically activated when the WidowMine burrows and can only be '
                                 'deactivated when the mine unburrows.The attack damages any friendlies except itself '
                                 'or other WidowMines[7]Reveals the WidowMine when on cooldown, unless the player '
                                 'has constructed an Armory.The ability is autocast.'
        },
        # 前置条件,这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Terran.SiegeTank: {
        'name': 'SiegeTank',
        'name_cn': '攻城坦克',
        # wiki英文 Details
        'description': 'Terran tank that can transform into a stationary siege cannon mode, '
                       'allowing it to strike targets at a greater range.',
        'target': ['ground'],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['mechanical', 'armored'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['mechanical'],

        # 生存
        'health': 175,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.25,  # wiki中文 基本信息/移动速

        'weapon1_target': ['ground'],
        'weapon1_type_anti': ['armored'],
        'weapon1_attack': 15,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 10,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 2,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 7,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 1.04,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': ['ground'],
        'weapon2_type_anti': ['armored'],
        'weapon2_attack': 40,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 30,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 4,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 13,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 3,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 3,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 45,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 125,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Factory',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {},  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {
            'Siege Tech': 'always available''The SiegeTank transforms, becoming stationary '
                          'and using a different weapon.The ability is not smartcast.'
        },  # 前置条件,这一部分需要游戏知识
        'require_building': 'TechLab',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Terran.Thor: {
        'name': 'Thor',
        'name_cn': '雷神',
        # wiki英文 Details
        'description': 'This intimidating mechanical unit is named after the Norse god of thunder. '
                       'Can deal splash damage to air units and fire powerful cannons at ground targets.',
        'target': ['ground', 'air'],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['mechanical', 'armored', 'heavy'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['light'],

        # 生存
        'health': 400,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 1.875,  # wiki中文 基本信息/移动速

        'weapon1_target': ['air'],
        'weapon1_type_anti': ['light'],
        'weapon1_attack': 6,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 6,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 10,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 4,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 3,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': ['ground'],
        'weapon2_type_anti': [],
        'weapon2_attack': 30,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 7,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 4,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 3,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 6,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 43,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 300,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 200,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Factory',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {
            'Smart Servos': 'upgraded in TechLab''Allows Hellions, Hellbats, Vikings, '
                            'and Thors to transform quickly between combat modes.'
                            'cost 150 minerals,150 gas,110 s'
            },  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {
            'High Impact Payload': 'always available''Activates the Thor\'s 250mm Punisher Cannons, '
                                   'which strike a single air target for 35 damage.',
            'Explosive Payload': 'Always available.Arms the Thor\'s Javelin missile launchers, '
                                 'which deal splash damage to nearby air units and additional damage to Light units.'
        },
        'require_building': ['TechLab', 'Armory'],
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Terran.Medivac: {
        'name': 'MedivacDropship',
        'name_cn': '医疗运输机',
        # wiki英文 Details
        'description': 'A dual-purpose unit combining the old dropship and the medic, '
                       'it is capable of transporting ground units and healing infantry.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['air'],

        'type_self': ['mechanical', 'armored'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['light'],

        # 生存
        'health': 150,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 1.875,  # wiki中文 基本信息/移动速

        'weapon1_target': ['air'],
        'weapon1_type_anti': ['light'],
        'weapon1_attack': 6,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 6,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 10,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 4,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 3,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': ['ground'],
        'weapon2_type_anti': [],
        'weapon2_attack': 30,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 7,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 4,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 3,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 43,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Starport',  # wiki中文 生产/生产设施
        'energy': 200,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {
            'Ignite Afterburners': 'Available after upgraded in FusionCore. '
                                   'The MedivacDropship gains a speed and acceleration boost to 5.95 for 5.71 seconds.'
                                   'cost 150 minerals,150 gas,110 s'
            },  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {
            'Healing': 'Always available. The MedivacDropship heals a friendly biological unit nearby it. '
                       'Can be set to autocast. May only be cast on one unit as a time, and may not be '
                       'stacked by multiple medivacs.',
            'load': 'Always available. load/unload units',
            'unload': 'Always available. unload units'
        },
        'require_building': '',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Terran.VikingFighter: {
        'name': 'Viking',
        'name_cn': '维京战机',
        # wiki英文 Details
        'description': 'A dual-purpose unit combining the old dropship and the medic, '
                       'it is capable of transporting ground units and healing infantry.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['air'],

        'type_self': ['mechanical', 'armored'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['armored'],

        # 生存
        'health': 135,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.75,  # wiki中文 基本信息/移动速

        'weapon1_target': ['air'],
        'weapon1_type_anti': ['armored'],
        'weapon1_attack': 10,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 4,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 9,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 2,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 2,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 42,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 75,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Starport',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {
            'Smart Servos': 'upgraded in TechLab''Allows Hellions, Hellbats, Vikings, and Thors to transform '
                            'quickly between combat modes.'
                            'cost 150 minerals,150 gas,110 s'
        },  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {},
        'require_building': '',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Terran.VikingAssault: {
        'name': 'Viking',
        'name_cn': '维京战机',
        # wiki英文 Details
        'description': 'A dual-purpose unit combining the old dropship and the medic, '
                       'it is capable of transporting ground units and healing infantry.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['mechanical', 'armored'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['mechanical'],

        # 生存
        'health': 135,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.75,  # wiki中文 基本信息/移动速

        'weapon1_target': ['ground'],
        'weapon1_type_anti': ['mechanical'],
        'weapon1_attack': 12,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 8,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 9,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 2,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 2,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 42,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 75,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Starport',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {
            'Smart Servos': 'upgraded in TechLab''Allows Hellions, Hellbats, Vikings, and Thors to transform '
                            'quickly between combat modes.'
                            'cost 150 minerals,150 gas,110 s'
            },  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {},
        'require_building': '',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Terran.Liberator: {
        'name': 'liberator',
        'name_cn': '解放者',
        # wiki英文 Details
        'description': 'Transformable medium-sized gunship, armed with anti-ground cannons after '
                       'transforming into a stationary air platform.',
        'target': ['ground', 'air'],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['air'],

        'type_self': ['mechanical', 'armored'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 180,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 3.375,  # wiki中文 基本信息/移动速

        'weapon1_target': ['air'],
        'weapon1_type_anti': [],
        'weapon1_attack': 5,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 4,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 5,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 2,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 1.8,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': ['ground'],
        'weapon2_type_anti': [],
        'weapon2_attack': 75,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 5,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 10,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 1.6,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 3,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 60,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 125,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Starport',  # wiki中文 生产/生产设施
        'energy': 0,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {
            'Advanced Ballistics': 'Available after upgraded in FusionCore. '
                                   'Upgrades the range of the Liberators anti-ground attack to 12'
                                   'cost 150 minerals,150 gas,110 s'
            },  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {
            'Defender Mode': 'always available''Deploys into Defender mode. In this mode, liberators have a '
                             'long-ranged narrow attack that can inflict high single target damage. Bonus vision '
                             'is gained in this mode. Liberators cannot move in this mode.',
            'Fighter Mode': 'always available''Reverts to Fighter Mode. In this mode, Liberators can move, '
                            'but they can only target air units.'
        },
        'require_building': '',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Terran.Raven: {
        'name': 'Raven',
        'name_cn': '铁鸦',
        # wiki英文 Details
        'description': 'this air detector creates smaller independent munitions.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['air'],

        'type_self': ['mechanical', 'light'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 140,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.9492,  # wiki中文 基本信息/移动速

        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 48,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 150,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Starport',  # wiki中文 生产/生产设施
        'energy': 200,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {
            'Interference Matrix': 'upgraded in TechLab''Disables a Mechanical or Psionic unit, rendering it unable '
                                   'to attack or use abilities for 11 seconds. Reveals cloaked units.'
                                   'cost 50 minerals,50 gas,80s'
        },  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {
            'Detector': 'always available''This unit or structure can detect cloaked, burrowed, '
                        'duplicated and hallucination enemies.',
            'Interference Matrix': 'upgraded in TechLab''Disables a Mechanical or Psionic unit, rendering it unable '
                                   'to attack or use abilities for 11 seconds. Reveals cloaked units.',
            'Auto-Turret': 'always available''The Raven deploys an auto-turret. The turret has building-type '
                           'armor and a high rate of fire.',
            'Anti-Armor Missile': 'always available''Deploys a missile which flies immediately to its target unit, '
                                  'reducing armor and shield armor of affected units by 2 for 21 seconds.'
        },
        'require_building': '',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Terran.Banshee: {
        # wiki英文 Unit
        'name': 'Banshee',
        'name_cn': '女妖战机',
        # wiki英文 Details
        'description': 'A cloak-capable gunship able to only attack ground-based targets.',
        # 可以对什么对象造成伤害,ground/air
        'target': ['ground'],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑

        'type_self': ['light', 'mechanical'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],
        'weapon1_target': ['ground'],
        'weapon1_type_anti': [],
        'weapon1_attack': 12,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 6,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 2,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 1.25,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 生存
        'health': 140,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 3.85,  # wiki中文 基本信息/移动速度

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 3,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': '',  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 60,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Starport',  # wiki中文 生产/生产设施

        # 技能
        'energy': 200,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade
            'Hyperflight Rotors': 'upgraded in TechLab''Increases Banshee speed from 3.85 to 5.25.'
                                  'Cost 125 mineral, 125 gas and 140 seconds. ',
            'Enable ShadowStride ability': 'upgraded in TechLab''Enables terran Banshees to cloak.'
                                           'Cost 100 mineral, 100 gas and 110 seconds. In DarkShrine.'

        },
        'ability': {  # wiki英文 作战/技能,只记录主动技能
            'Cloak': 'Enables terran Banshees to cloak.'
        },

        # 前置条件,这一部分需要游戏知识
        'require_building': 'TechLab',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },

    units.Terran.Battlecruiser: {
        # wiki英文 Unit
        'name': 'Battlecruiser',
        'name_cn': '战列巡航舰',
        # wiki英文 Details
        'description': 'The capital ship of the terran fleet, this powerful spacecraft is capable of firing a '
                       'Yamato Cannon that deals large damage to a single target.',
        # 可以对什么对象造成伤害,ground/air
        'target': ['ground', 'air'],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑

        'type_self': ['armored', 'mechanical', 'heavy'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],
        'weapon1_target': ['ground'],
        'weapon1_type_anti': [],
        'weapon1_attack': 8,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 6,  # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 2,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0.225,  # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': ['air'],
        'weapon2_type_anti': [],
        'weapon2_attack': 5,  # wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,  # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,  # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0.225,  # wiki中文 作战/武器/攻击间隔

        # 生存
        'health': 550,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 3,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 1.875,  # wiki中文 基本信息/移动速度

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 6,  # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 90,  # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 400,  # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 300,  # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Starport',  # wiki中文 生产/生产设施

        # 技能
        'energy': 200,  # wiki中文 基本信息/能量,默认值为0
        'upgrade': {  # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade
            'Yamato Cannon': 'Available after upgraded in FusionCore. '
                             'Blasts a target with a devastating plasma cannon, causing 240 damage.'
                             'Cost 150 mineral, 150 gas and 140 seconds.',
        },
        'ability': {  # wiki英文 作战/技能,只记录主动技能
            'Yamato Cannon': 'Available after upgraded in FusionCore. '
                             'Blasts a target with a devastating plasma cannon, causing 240 damage.'
                             'Cost 150 mineral, 150 gas and 140 seconds.',
            'Tactical Jump': 'always available. '
                             'The user warps to the target location. Vanishes from the map, but has a 1 second '
                             'vulnerably phase before warping.',
        },

        # 前置条件,这一部分需要游戏知识
        'require_building': ['TechLab', 'FusionCore'],
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },

    units.Terran.AutoTurret: {
        # wiki英文 Unit
        'name': 'AutoTurret',
        'name_cn': '自动机炮',
        # wiki英文 Details
        'description': 'The Auto-Turret is a temporary and immobile structure deployed by the Raven at the cost of '
                       '50 energy. It automatically attacks nearby air and ground targets that come within its range.',
        # 可以对什么对象造成伤害,ground/air
        'target': ['ground', 'air'],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑

        'type_self': ['mechnical', 'armored', 'structure'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],
        'weapon1_target': ['ground'],
        'weapon1_type_anti': [],
        'weapon1_attack': 18,                           		# wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,                              # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,         # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,        # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 6,                              # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,                              # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0.57,                               # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,                           			# wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,                              # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,         # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,        # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,                             # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,                              # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,                               	# wiki中文 作战/武器/攻击间隔

        # 生存
        'health': 140,                   # wiki中文 基本信息/生命值
        'shield': 0,                   # wiki中文 基本信息/护盾
        'health_armor': 0,              # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,      # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 3.85,                # wiki中文 基本信息/移动速度

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 3,                                    # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': '',                                # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 60,                             # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 150,                    # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 100,                        # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': 'Starport',      # wiki中文 生产/生产设施

        # 技能
        'energy': 200,                                    # wiki中文 基本信息/能量,默认值为0
        'upgrade': {                                    # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade
            'Hi-Sec Auto Tracking': 'upgraded in Engineering Bay. Adds +1 attack range to Auto-Turrets, '
                                    'Missile Turrets, and Planetary Fortresses.'
                                    'Cost 100 mineral, 100 gas and 57 seconds. ',
        },
        'ability': {                                    # wiki英文 作战/技能,只记录主动技能
            'Cloak': 'Enables terran Banshees to cloak.'
        },

        # 前置条件,这一部分需要游戏知识
        'require_building': 'StarportTechLab',
        'require_tech': '',
        'require_unit': 'Raven',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },

    units.Terran.StarportTechLab: {
        'name': 'StarportTechLab',
        'name_cn': '科技实验室',
        # wiki英文 Details
        'description': 'Enables the production of "higher tech" units.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['structure', 'mechanical', 'armored'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 400,                   # wiki中文 基本信息/生命值
        'shield': 0,                   # wiki中文 基本信息/护盾
        'health_armor': 1,              # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,      # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,                # wiki中文 基本信息/移动速

        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,                           		# wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,                              # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,         # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,        # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,                              # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,                              # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,                               # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,                           			# wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,                              # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,         # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,        # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,                             # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,                              # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,                               	# wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,                                    # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,                                # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 18,                             # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 50,                    # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 25,                        # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': ['Barracks', 'Factory', 'Starport'],      # wiki中文 生产/生产设施
        'energy': 0,                                    # wiki中文 基本信息/能量,默认值为0
        'upgrade': {},                                    # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {},

        # 前置条件,这一部分需要游戏知识
        'require_building': 'Engineering Bay',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': ['Cloaking Field', 'Hyperflight Rotors', 'Interference Matrix'],
        'activate_unit': ['Raven', 'Banshee']

    },
    units.Terran.FactoryTechLab: {
        'name': 'FactoryTechLab',
        'name_cn': '科技实验室',
        # wiki英文 Details
        'description': 'Enables the production of "higher tech" units. Adding one to a Factory will enable it to build '
                       'SiegeTanks.Upgrades and special abilities for the hellion, SiegeTank, viking, banshee, '
                       'MedivacDropship, and raven.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['structure', 'mechanical', 'armored'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 400,                   # wiki中文 基本信息/生命值
        'shield': 0,                   # wiki中文 基本信息/护盾
        'health_armor': 1,              # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,      # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,                # wiki中文 基本信息/移动速

        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,                           		# wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,                              # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,         # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,        # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,                              # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,                              # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,                               # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,                           			# wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,                              # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,         # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,        # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,                             # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,                              # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,                               	# wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,                                    # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,                                # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 18,                             # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 50,                    # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 25,                        # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': ['Barracks', 'Factory', 'Starport'],      # wiki中文 生产/生产设施
        'energy': 0,                                    # wiki中文 基本信息/能量,默认值为0
        'upgrade': {},                                    # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {},

        # 前置条件,这一部分需要游戏知识
        'require_building': 'Engineering Bay',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': ['Infernal Pre-Igniter', 'Hurricane Engines', 'Drilling Claws', 'Smart Servos'],
        'activate_unit': 'SiegeTank',

    },

    units.Terran.BarracksTechLab: {
        'name': 'BarracksTechLab',
        'name_cn': '科技实验室',
        # wiki英文 Details
        'description': 'Enables the production of "higher tech" units. For instance, adding a TechLab to a Barracks '
                       'will allow it to produce marauders.',
        'target': [],
        # 自己可以受到什么类型伤害,ground/air,只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],

        'type_self': ['structure', 'mechanical', 'armored'],
        # wiki中文 作战/武器,克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 400,                   # wiki中文 基本信息/生命值
        'shield': 0,                   # wiki中文 基本信息/护盾
        'health_armor': 1,              # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 2,      # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,                # wiki中文 基本信息/移动速

        'weapon1_target': [],
        'weapon1_type_anti': [],
        'weapon1_attack': 0,                           		# wiki中文 作战/武器/伤害,基础伤害
        'weapon1_attack_bonus': 0,                              # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,         # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,        # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,                              # wiki中文 作战/武器/射程,近战为1
        'weapon1_attack_times': 0,                              # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon1_cooldown': 0,                               # wiki中文 作战/武器/攻击间隔

        # 作战 weapon2
        'weapon2_target': [],
        'weapon2_type_anti': [],
        'weapon2_attack': 0,                           			# wiki中文 作战/武器/伤害,基础伤害
        'weapon2_attack_bonus': 0,                              # wiki中文 作战/武器/伤害,克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,         # wiki中文 作战/武器/伤害,攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,        # wiki中文 作战/武器/伤害,攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 0,                             # wiki中文 作战/武器/射程,近战为1
        'weapon2_attack_times': 0,                              # wiki中文 作战/武器/多重攻击,没有时为1重攻击
        'weapon2_cooldown': 0,                               	# wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,                                    # wiki中文 基本信息/占用舱载空间,即在游戏中占用的人口
        'warp_time': 0,                                # wiki中文 生产/生产时间2,单位,秒,没有时置零
        'produce_time': 18,                             # wiki中文 生产/生产时间1,单位,秒
        'produce_cost_mineral': 50,                    # wiki中文 生产/成本,水晶(蓝色)
        'produce_cost_gas': 25,                        # wiki中文 生产/成本,瓦斯(绿色)
        'produce_from': ['Barracks'],      # wiki中文 生产/生产设施
        'energy': 0,                                    # wiki中文 基本信息/能量,默认值为0
        'upgrade': {},                                    # wiki英文 升级,不记录公共升级,如ground_weapon_upgrade        },
        'ability': {},

        # 前置条件,这一部分需要游戏知识
        'require_building': 'Engineering Bay',
        'require_tech': '',
        'require_unit': '',

        # 激活选项,这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': ['Combat Shield', 'StimPack'],
        'activate_unit': ' Marauder',

    },


}

if __name__ == "__main__":
    for key in DATA_TERRAN.keys():
        print(key)
    print(f"unit number: {len(DATA_TERRAN.keys())}")

    # units.Terran.AutoTurret
    # units.Terran.StarportTechLab
    # units.Terran.FactoryTechLab
    # units.Terran.BarracksTechLab
