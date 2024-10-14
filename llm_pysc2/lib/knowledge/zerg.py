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

DATA_ZERG = {

    units.Zerg.Drone: {
        # wiki英文 Unit
        'name': 'Drone',
        'name_cn': '工蜂',
        # wiki英文 Details
        'description': 'Harvests resources and spawns structures. Is sacrificed when creating new structures.'
                       'The drone morphs into structures and harvests minerals and vespene gas.',
        # 可以对什么对象造成伤害，ground/air
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target': ['ground'],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['light', 'biological'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 40,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 3.94,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': ['ground'],
        'weapon1_attack': 5,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0.2,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1.07,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 1,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 12,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 50,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'train from Larva.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Larva',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.Zergling: {
        # wiki英文 Unit
        'name': 'Zergling',
        'name_cn': '跳虫',
        # wiki英文 Details
        'description': 'Fast but weak melee attacker ideal for swarming attacks in large numbers.',
        'target': ['ground'],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['light', 'biological'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 35,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 4.13,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': ['ground'],
        'weapon1_attack': 5,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 1,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0.5,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0.5,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 8.5,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 25,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Larva.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade
            'Metabolic Boost': 'Increases zergling movement speed. The zerglings "grow wings".'
                               'Cost 100 mineral, 100 gas and 79 seconds. In Spawning Pool.',
            'Adrenal Glands': 'Increases zergling attack rate to 0.35.'
                              'Cost 200 mineral, 200 gas and 93 seconds. In Spawning Pool.'
        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Baneling Morph': 'Available after Baneling Nest built.'
                              'Transforms zergling into baneling, a glowing green creature with a suicide attack.'
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Spawning Pool',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Larve',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': 'Baneling(after Baneling Nest built)',

    },
    units.Zerg.Queen: {
        # wiki英文 Unit
        'name': 'Queen',
        'name_cn': '虫后',
        # wiki英文 Details
        'description': 'The queen a powerful attacking ground dwelling support unit ideal for zerg defense.',
        # 可以对什么对象造成伤害，ground/air
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target': ['ground', 'air'],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['biological', 'psionic'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        'type_anti': [],

        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑

        # 生存
        'health': 175,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0.9375,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_target': ['ground'],
        'weapon1_type_anti': [],
        'weapon1_attack': 4,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 5,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 2,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0.71,  # wiki中文 作战/武器/攻击间隔

        'weapon2_target': ['air'],
        'weapon2_type_anti': [],
        'weapon2_attack': 9,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 7,  # wiki中文 作战/武器/射程，近战为1
        'weapon2_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon2_cooldown': 0.71,  # wiki中文 作战/武器/攻击间隔
        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 36,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'produced from Hatchery/Lair/Hive.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 200,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Create Creep Tumor': 'Always available(can only be used once by a creep tumor).'
                                  'The queen forces a creep tumor out of her bowels.Alternatively, each creep tumor '
                                  'may create a single additional creep tumor, using the same build time but no energy '
                                  'cost. This changes the tumor s appearance. Creep tumors can only be created upon '
                                  'the creep, and within a range.'
                                  'Cost 25 energy and 11 seconds,cooldown:13.57 seconds',
            'Spawn Larva': 'Always available.'
                           'Queens can target a hatchery/lair/hive, causing it to eventually spawn four larvae. '
                           'These join any already-present larvae. The larva-producing structure will not naturally '
                           'produce any more larvae until the total falls below three. The larva count for any given '
                           'hatchery/lair/hive cannot exceed nineteen, no matter how many times spawn larva is cast. '
                           'Cost 25 energy and 29 seconds,cooldown:1.8 seconds.',
            'Transfusion': 'Always available.'
                           'The queen instantly restores 75 hit points to target biological unit or structure, '
                           'plus an additional 50 health over the next 7.14 seconds. Can only be used while on creep.'
                           'cost 50 energy ,cooldown:1 seconds. ',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Spawning pool',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.Baneling: {
        # wiki英文 Unit
        'name': 'Baneling',
        'name_cn': '爆虫',
        # wiki英文 Details
        'description': 'This green rolling unit is mutated from the zergling. It has a huge suicidal attack. '
                       'A huge swarm of banelings will create devastating results to a base of enemy.',
        # 可以对什么对象造成伤害，ground/air
        'target': ['ground'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['biological'],
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['light', 'structure'],

        # 生存
        'health': 30,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 3.5,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_target': ['ground'],
        'weapon1_type_anti': ['light'],
        'weapon1_attack': 16,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 19,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 2,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 1,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0.59,  # wiki中文 作战/武器/攻击间隔

        'weapon2_target': ['ground'],
        'weapon2_type_anti': ['structure'],
        'weapon2_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon2_attack_bonus': 80,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 5,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 1,  # wiki中文 作战/武器/射程，近战为1
        'weapon2_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon2_cooldown': 0,  # wiki中文 作战/武器/攻击间隔
        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0.5,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 14,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 25,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 25,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Zergling.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade
            'Centrifugal Hooks': 'Increases the speed of banelings to 4.13.'
                                 'Cost 100 mineral, 100 gas and 71 seconds. In Baneling Nest.Required Lair.'
        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Enable Attack Building': 'Always available.'
                                      'Allows banelings to automatically target structures.',
            'Disnable Attack Building': 'Always available.'
                                        'do not Allows banelings to automatically target structures.',
            'Explode': 'Always available.'
                       'Banelings can be ordered to detonate, instantly dealing damage around them, '
                       'even if burrowed. The ability is not smartcast.'
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Baneling Nest',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Zergling',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.OverlordTransport: {
        'name': 'OverlordTransport',
        'name_cn': '运输王虫',
        'description': 'Zerg Air Transport Unit, used for airdrops and harass enemy base',
        'target': [],
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 200,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0.902,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': -8,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 18,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Larva.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade
            'Pneumatized Carapace': 'ncrease speed of the overlord from 0.902 to 2.63, overlords with Ventral Sacs '
                                    'from 1.099 to 2.83, and the overseer 2.62 to 4.73".'
                                    'Cost 100 mineral, 100 gas and 43 seconds. '
                                    'In Hatchery (with at least 1 other lair or hive)/Lair/Hive.',
        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Mutate Ventral Sacs': 'Available after Lair built.'
                                   'Upgrades an individual overlord, allowing it to transport units. '
                                   'Increases movement speed to 1.28 (3.00 with Pneumatized Carapace).',
            'Overseer Morph': 'Available after Lair built'
                              'The overlord can morph into an overseer, which becomes a detector.',
            'Excrete Creep': 'Available after Lair built.'
                             'The overlord creates a 2x2 patch of creep through an activated ability, '
                             'the radius steadily expanding.duartion 11 seconds',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Overlord',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',
    },

    units.Zerg.Overlord: {
        # wiki英文 Unit
        'name': 'Overlord',
        'name_cn': '王虫',
        # wiki英文 Details
        'description': 'Produces control and is no longer a detector like the StarCraft I version.',
        'target': [],
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 200,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0.902,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': -8,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 18,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Larva.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade
            'Pneumatized Carapace': 'ncrease speed of the overlord from 0.902 to 2.63, overlords with Ventral Sacs '
                                    'from 1.099 to 2.83, and the overseer 2.62 to 4.73".'
                                    'Cost 100 mineral, 100 gas and 43 seconds. '
                                    'In Hatchery (with at least 1 other lair or hive)/Lair/Hive.',
        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Mutate Ventral Sacs': 'Available after Lair built.'
                                   'Upgrades an individual overlord, allowing it to transport units. '
                                   'Increases movement speed to 1.28 (3.00 with Pneumatized Carapace).',
            'Overseer Morph': 'Available after Lair built'
                              'The overlord can morph into an overseer, which becomes a detector.',
            'Excrete Creep': 'Available after Lair built.'
                             'The overlord creates a 2x2 patch of creep through an activated ability, '
                             'the radius steadily expanding.duartion 11 seconds',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Larva',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': 'Overseer(After Lair Built), OverlordTransport(After Lair Built)',

    },
    units.Zerg.Overseer: {
        # wiki英文 Unit
        'name': 'Overseer',
        'name_cn': '眼虫',
        # wiki英文 Details
        'description': 'Produces control and is no longer a detector like the StarCraft I version.'
                       'This unit or structure can detect cloaked, burrowed, duplicated and hallucination enemies.',
        'target': [],
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 200,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.62,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': -8,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 18,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 50,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 50,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Overload.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade
            'Pneumatized Carapace': 'ncrease speed of the overlord from 0.902 to 2.63, overlords with Ventral Sacs '
                                    'from 1.099 to 2.83, and the overseer 2.62 to 4.73".'
                                    'Cost 100 mineral, 100 gas and 43 seconds. '
                                    'In Hatchery (with at least 1 other lair or hive)/Lair/Hive.'

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Contaminate': 'Always available'
                           'The overseer disables a building, which becomes covered in slime. '
                           'It cannot produce units, larva or research upgrades while contaminated.'
                           'cost 125 energy,duration 30 seconds',
            'Spawn Changeling': 'Always available'
                                'The overseer can create a changeling, which can spy on enemy forces.'
                                'cost 50 energy,duration 150 seconds',
            'Oversight Mode': 'Always available'
                              'The overseer can switch to Oversight Mode. '
                              'In Oversight Mode the overseer is immobile and gains 50% increased sight radius. '
                              'Can switch back to Overseer Mode to move again.'
                              'need 3 seconds',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Lair',
        'require_tech': '',
        'require_unit': 'sacrifice 1  Overload',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.Roach: {
        # wiki英文 Unit
        'name': 'Roach',
        'name_cn': '蟑螂',
        # wiki英文 Details
        'description': 'Exceptionally tough short ranged unit able to quickly regenerate and move while burrowed.',

        'target': ['ground'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological'],
        'type_anti': [],
        
        # 生存
        'health': 145,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 3.15,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_target': ['ground'],
        'weapon1_type_anti': [],
        'weapon1_attack': 16,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 2,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 4,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1.43,  # wiki中文 作战/武器/攻击间隔

        # 'weapon2_target': ['ground'],
        # 'weapon2_type_anti': [],
        # 'weapon2_attack': 16,  # wiki中文 作战/武器/伤害，基础伤害
        # 'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        # 'weapon2_attack_upgrade_base_damage_offset': 2,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        # 'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        # 'weapon2_attack_range': 1,  # wiki中文 作战/武器/射程，近战为1
        # 'weapon2_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        # 'weapon2_cooldown': 1.43,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 19,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 75,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 25,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Larva.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade
            'Glial Reconstitution': 'Increases Roach movement speed to 4.2 while unburrowed, '
                                    'and to 4.4 while burrowed under creep.'
                                    'Cost 100 mineral, 100 gas and 70 seconds. In Roach Warren.',
            'Tunneling Claws': 'The roach can move while burrowed. It moves faster when burrowed beneath the creep. '
                               'Glial Reconstitution has no impact on burrowing speed.While it can be researched '
                               'earlier, Tunneling Claws cannot be used until burrowing has been evolved.'
                               'Cost 100 mineral, 100 gas and 79 seconds. In Roach Warren.Required Lair.'
        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Ravager Morph': 'Always available.'
                             'The roach can morph into a ravager. Costs 1 supply.'

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Roach Warren',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Larva',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': 'Ravager',

    },
    units.Zerg.Ravager: {
        # wiki英文 Unit
        'name': 'Ravager',
        'name_cn': '破坏者',
        # wiki英文 Details
        'description': 'An artillery unit that evolves from the roach. '
                       'Can use corrosive bile to destroy force fields and hit clumps of units at range.',

        'target': ['ground'],
        # 自己可以受到什么类型伤害，ground/air，只有神族的巨像等少数单位能够同时受到两种伤害
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['biological'],
        'type_anti': [],
        
        # 生存
        'health': 120,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 3.85,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_target': ['ground'],
        'weapon1_type_anti': [],
        'weapon1_attack': 16,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 2,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 6,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1.6,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 3,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 12,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 25,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 75,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Roach.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Corrosive Bile': 'Always available.'
                              'Launches a glob of bile into the air that descends on target point after 2 seconds, '
                              'dealing 60 damage to enemies in an area of effect. '
                              'Hits both air and ground units, destroys force fields.'
                              'range 9,duration 2,cooldown 7 seconds.'
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Roach Warren',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Roach',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.Hydralisk: {
        # wiki英文 Unit
        'name': 'Hydralisk',
        'name_cn': '刺蛇',
        # wiki英文 Details
        'description': 'Basic ranged attacker of the zerg swarm.',

        'target': ['ground', 'air'],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['light', 'biological'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 90,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 3.15,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': ['ground'],
        'weapon1_attack': 12,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 1,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0.59,  # wiki中文 作战/武器/攻击间隔

        'weapon2_target': ['ground', 'air'],
        'weapon2_type_anti': [],
        'weapon2_attack': 12,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon2_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon2_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon2_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon2_attack_range': 5,  # wiki中文 作战/武器/射程，近战为1
        'weapon2_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon2_cooldown': 0.59,  # wiki中文 作战/武器/攻击间隔
        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 24,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 50,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Larva.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade
            'Muscular Augments': 'Increases zergling movement speed. The zerglings "grow wings".'
                                 'Cost 100 mineral, 100 gas and 64 seconds. In Hydarlisk Den.',
            'Grooved Spines': 'Increases hydralisk range by 1.'
                              'Cost 75 mineral, 75 gas and 50 seconds. In Hydarlisk Den.'
        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Morph to Lurker': 'Available after Lurker Den built.'
                               'Morph a Hydylisk to a Lurker'
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Hydarlisk Den',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Larva',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': 'Lurker(After Lurker Den Built)',

    },
    units.Zerg.Lurker: {
        # wiki英文 Unit
        'name': 'Lurker',
        'name_cn': '潜伏者',
        # wiki英文 Details
        'description': 'A long ranged siege unit that evolves from the hydralisk. '
                       'Must burrow to attack, but does damage in a line.',

        'target': ['ground'],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['armored'],

        # 生存
        'health': 200,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 4.13,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': ['armored'],
        'weapon1_target': ['ground'],
        'weapon1_attack': 20,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 10,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 2,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 8,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1.25,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 3,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 18,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 50,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Hydarlisk.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade
            'Adaptive Talons': 'Reduces Lurker burrow time from 2 to 1.07 seconds.'
                               'Cost 100 mineral, 100 gas and 57 seconds. Required Hive.In Lurker Den.',
            'Seismic Spines': 'Increases the Lurker’s range from 8 to 10.'
                              'Cost 150 mineral, 150 gas and 57 seconds. Required Hive.In Lurker Den.'
        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Lurker Den',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Hydarlisk',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.Mutalisk: {
        # wiki英文 Unit
        'name': 'Mutalisk',
        'name_cn': '异龙',
        # wiki英文 Details
        'description': 'The basic air offensive unit of the zerg with high movement speed.'
                       'Mutalisks regenerate more quickly than other zerg units (1.4 HP/second).',

        'target': ['ground', 'air'],
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['light', 'biological'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 120,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 5.6,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': ['ground', 'air'],
        'weapon1_attack': 9,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 3,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1.09,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 24,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Larva.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Spire',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Larva',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.Corruptor: {
        # wiki英文 Unit
        'name': 'Corruptor',
        'name_cn': '腐化者',
        # wiki英文 Details
        'description': 'Attacks and "corrupts" other air units, increasing damage taken.',
        'target': ['air'],
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': ['massive'],

        # 生存
        'health': 200,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 2,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 4.725,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': ['massive'],
        'weapon1_target': ['air'],
        'weapon1_attack': 14,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 6,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 6,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1.36,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 2,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 29,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Larva.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Brood Lord Morph': 'Available after Greater spire built.'
                                'The corruptor can morph into a brood lord.',
            'Caustic Spray': 'Always available.'
                             'Emits a stream of acid that deals an initial 30 damage, then deals 7 damage per second '
                             'for 4.3 seconds, then increases to 35 damage per second.Channeled ability. '
                             'Corruptor can not move while ability is in use. Can only target enemy structures. '
                             'Exclusive to Legacy of the Void. Replaces Corruption.'
                             'Cooldown 32 seconds.'
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Spire',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Larva',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': 'Brood Lord(After Greater Spire Built)',

    },

    units.Zerg.BroodLord: {
        # wiki英文 Unit
        'name': 'Brood lord',
        'name_cn': '巢虫领主',
        # wiki英文 Details
        'description': 'High hit point aerial ground attacker which replaced the swarm guardian, '
                       'evolving from the corruptor.'
                       'The Brood Lord shoots Broodlings at its target. '
                       'A Broodling is a small creature that can attack ground units.',

        'target': ['ground'],
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'massive'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 225,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.62,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': ['ground'],
        'weapon1_attack': 20,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 2,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 10,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1.79,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 4,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 24,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 150,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Corruptor.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Greater Spire',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Corruptor',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.Viper: {
        # wiki英文 Unit
        'name': 'Viper',
        'name_cn': '飞蛇',
        # wiki英文 Details
        'description': 'Aerial support unit, able to blind groups of ranged units and '
                       'abduct enemy units to its position.',

        'target': [],
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['Psionic', 'biological', 'armored'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 150,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 4.13,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 3,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 29,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 200,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Larva.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Abduct': 'Always available.'
                      'The viper targets a unit and pulls that unit to the viper s location. '
                      'This allows it to pull allies to safety, or pull enemy units out of position. '
                      'The ability can pull units up and down cliffs.'
                      'cost 75 energy,range 9.',
            'Blinding Cloud': 'Always available.'
                              'The viper spits a green cloud. Ground units and structures in the cloud have '
                              'their range reduced to one.'
                              'cost 100 energy,range 11.',
            'Consume': 'Always available.'
                       'The ability deals 150 damage on a friendly building (except a creep tumor) '
                       'over 14 seconds to gain 50 energy. The ability does not work on units.'
                       'range 1,cooldown 7 seconds.',
            'Parasitic Bomb': 'Always available.'
                              'Creates a parasitic cloud on an air unit after a 0.7 second delay, '
                              'dealing 120 damage over 7 seconds to that unit and any air units around it. '
                              'Cloud has a radius of 3. Cloud persists for the remaining duration if the target '
                              'is destroyed. Does not stack with other parasitic bombs.'
                              'cost 125 energy,range 8,duration 7 seconds.',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Hive',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Larve',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.Infestor: {
        # wiki英文 Unit
        'name': 'Infestor',
        'name_cn': '感染者',
        # wiki英文 Details
        'description': 'Zerg spellcaster. Provides ground support and can move while burrowed.'
                       'Can move while burrowed',
        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionicpsionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'psionic', 'biological'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 90,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 3.15,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
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
        'produce_time': 36,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 150,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Larva.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 200,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Fungal Growth': 'Always available.'
                             'An infestor launches a projectile with a speed of 15;[14] enemy units within the area of '
                             'effect (2.25 radius) have their speed reduced by 75% and suffer 25damage over 3 seconds. '
                             'Cloaked and burrowed units are revealed.Fungal Growth stops the use of Blink, '
                             'Tactical Jump and prevents units from burrowing or unburrowing. '
                             'Affected units can not be loaded into buildings or transports.'
                             'cost 75 energy,range 10,duration 3 seconds.',
            'Microbial Shroud': 'Always available.'
                                'Creates a shroud that obscures ground units below in a radius of 3.5, '
                                'reducing the damage they take from air units by 50%. Lasts 11 seconds.'
                                'cost 75 energy,range 9,duration 11 seconds.',
            'Neural Parasite': 'Available after Neural Parasite upgrade in Infestation Pit.'
                               'The infestor takes control of target enemy unit. '
                               'cost 100 energy,range 7,duration 15 seconds.'
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Infestation Pit',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Larva',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.SwarmHost: {
        # wiki英文 Unit
        'name': 'Swarm Host',
        'name_cn': '虫群宿主',
        # wiki英文 Details
        'description': 'Siege unit, spawns timed locusts to send at targets.',

        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 160,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 3.15,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 3,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 29,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 75,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Hydarlisk.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade
            'Spawn Locust': 'Always available.'
                            'Spawns 2 Locusts.Locust have a 18 seconds timed life.'
                            'cool down 43 seconds.',
        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Infestation Pit',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Larva',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.Ultralisk: {
        # wiki英文 Unit
        'name': 'Ultralisk',
        'name_cn': '雷兽',
        # wiki英文 Details
        'description': 'Massive zerg melee attacker able to deal splash damage with its melee attack. '
                       'Also has a headbut attack vs buildings. Other differences from its StarCraft I counterpart are '
                       'it now having four kaiser blades instead of two, and its ability to burrow.'
                       'Immune to snare, stun, slow and mind control effects.',
        'target': ['ground'],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'massive', 'biological'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 500,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 2,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 4.13,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': ['ground'],
        'weapon1_attack': 35,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 3,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 1,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0.61,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 6,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 39,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 275,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 200,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Larva.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade
            'Chitinous Plating': '+2 bonus to ultralisk armor.'
                                 'Cost 150 mineral, 150 gas and 79 seconds. In Ultralisk Cavern.',
            'Anabolic Synthesis': 'Increases Ultralisk speed when off creep from 4.13 to 4.96. '
                                  'The Ultralisk on-creep speed will remain the same at 5.37.'
                                  'Cost 150 mineral, 150 gas and 42 seconds. In Ultralisk Cavern.'
        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Ultralisk Cavern',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Larve',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.BanelingNest: {
        # wiki英文 Unit
        'name': 'Baneling Nest',
        'name_cn': '爆虫巢穴',
        # wiki英文 Details
        'description': 'Required for baneling production and researches baneling upgrades.',
        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 850,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
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
        'produce_time': 43,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 50,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Drone.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Spawning Pool',
        'require_tech': '',
        'require_unit': 'sacrifice 1 drone',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': 'Centrifugal Hook(need Lair)',
        'activate_unit': 'Baneling',

    },
    units.Zerg.CreepTumor: {
        # wiki英文 Unit
        'name': 'Creep Tumor',
        'name_cn': '菌毯肿瘤',
        # wiki英文 Details
        'description': 'This burrowed structure resembling an eyeball extends the creep, '
                       'much like the creep colony in StarCraft I. '
                       'Creep tumors are spawned by queens and each can spawn one additional creep tumor.',
        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['light', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 100,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
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
        'produce_time': 0,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 0,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'produced by Queen.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Create Creep Tumor': 'Always available.'
                                  'Spawn a additional Creep Tumor.'
                                  'need 11 seconds to create new Creep Tumor and  cooldown 14 seconds. '
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
    units.Zerg.EvolutionChamber: {
        # wiki英文 Unit
        'name': 'Evolution_Chamber',
        'name_cn': '进化腔',
        # wiki英文 Details
        'description': 'Provides basic upgrades for the zerg ground units.',
        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 750,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
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
        'produce_cost_mineral': 75,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Drone.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Hatchery',
        'require_tech': '',
        'require_unit': 'sacrifice 1 drone',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': 'Melee Attacks(level 2 need Lair. level 3 need Hive).'
                         'Missile Attacks(level 2 need Lair. level 3 need Hive)'
                         'Ground Carapace(level 2 need Lair. level 3 need Hive)',
        'activate_unit': '',

    },
    units.Zerg.Extractor: {
        # wiki英文 Unit
        'name': 'Extractor',
        'name_cn': '萃取房',
        # wiki英文 Details
        'description': 'Allows drones to extract vespene gas.',
        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 500,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
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
        'produce_time': 21,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 500,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Drone.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': 'sacrifice 1 drone',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.GreaterSpire: {
        # wiki英文 Unit
        'name': 'Greater Spire',
        'name_cn': '巨型尖塔',
        # wiki英文 Details
        'description': 'Upgrade of the spire, enables production of brood lords.',
        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 1000,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
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
        'produce_time': 71,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 150,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Spire.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Hive',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Spire',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': 'Flyer Attacks(level 2 need Lair.level 3 need Hive). '
                         'Flyer Carapace(level 2 need Lair.level 3 need Hive)',
        'activate_unit': 'Brood Lord',

    },
    units.Zerg.Hatchery: {
        # wiki英文 Unit
        'name': 'Hatchery',
        'name_cn': '孵化场',
        # wiki英文 Details
        'description': 'Spawns larvae to be morphed into other zerg strains, generates creep and digests minerals and '
                       'gas into a usable form. The queen is spawned directly from the hatchery.',
        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 1500,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
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
        'produce_time': 71,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 300,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Drone.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade
            'Mutate into Lair': 'Transforms a hatchery into a lair.'
                                'Cost 150 mineral, 100 gas and 57 seconds.Required Spawning Pool.'

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Birth Queen': 'produce a Queen''cost 150 minerals and 36 seconds.Required Spawning Pool.',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': 'sacrifice 1 drone',

        # 激活选项，这一部分需要游戏知识
        'activate_building': 'Spawning Pool.Evolution Chamber',
        'activate_tech': 'Burrow.Pneumatized Crapace',
        'activate_unit': 'Larva / Drone / Overload',

    },
    units.Zerg.Hive: {
        # wiki英文 Unit
        'name': 'Hive',
        'name_cn': '主巢',
        # wiki英文 Details
        'description': 'Upgrade of the lair giving access to the most advanced buildings.',
        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 2500,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
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
        'produce_time': 71,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 200,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 150,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Lair.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Birth Queen': 'produce a Queen''cost 150 minerals and 36 seconds.Required Spawning Pool.',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'Infestion Pit',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Lair',

        # 激活选项，这一部分需要游戏知识
        'activate_building': 'Greater Spire.Ultralisk Den',
        'activate_tech': '',
        'activate_unit': 'Viper',

    },
    units.Zerg.HydraliskDen: {
        # wiki英文 Unit
        'name': 'Hydralisk Den',
        'name_cn': '刺蛇巢',
        # wiki英文 Details
        'description': 'Required for the production of hydralisks and researches hydralisk upgrades.',
        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 850,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
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
        'produce_time': 29,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Drone.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Lair',
        'require_tech': '',
        'require_unit': 'sacrifice 1 drone',

        # 激活选项，这一部分需要游戏知识
        'activate_building': 'Lurker Den',
        'activate_tech': 'Grooved Spine.Muscular Augments',
        'activate_unit': 'Hydralisk',

    },
    units.Zerg.InfestationPit: {
        # wiki英文 Unit
        'name': 'Infestation_Pit',
        'name_cn': '感染深渊',
        # wiki英文 Details
        'description': 'Required for the production of hydralisks and researches hydralisk upgrades.',
        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 850,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
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
        'produce_time': 36,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Drone.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Lair',
        'require_tech': '',
        'require_unit': 'sacrifice 1 drone',

        # 激活选项，这一部分需要游戏知识
        'activate_building': 'Hive',
        'activate_tech': 'Neural Parasite',
        'activate_unit': 'Infestor.Swarm Host',

    },
    units.Zerg.Lair: {
        # wiki英文 Unit
        'name': 'Lair',
        'name_cn': '虫穴',
        # wiki英文 Details
        'description': 'Upgrade of the hatchery giving access to more advanced buildings '
                       'and providing upgrades for overlords and overseers.',
        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 2000,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
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
        'produce_time': 57,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 100,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Hatchery.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade
            'Mutate into Hive': 'Transforms a hatchery into a Hive.'
                                'Cost 200 mineral, 150 gas and 71 seconds.Required Spawning Pool.'

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Birth Queen': 'produce a Queen''cost 150 minerals and 36 seconds.Required Spawning Pool.',
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'Spawning Pool',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Hatchery',

        # 激活选项，这一部分需要游戏知识
        'activate_building': 'Hive.Spire.Infestation Pit.Hydralisk Den.Nydus Network',
        'activate_tech': '',
        'activate_unit': 'Overseer.Overload with Ventral Sacs',

    },
    units.Zerg.LurkerDen: {
        # wiki英文 Unit
        'name': 'Lurker Den',
        'name_cn': '潜伏者巢穴',
        # wiki英文 Details
        'description': 'Enables hydralisks to morph into lurkers. Contain upgrades for lurkers.',
        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 850,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
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
        'produce_time': 57,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 150,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Drone.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Hydralisk Den',
        'require_tech': '',
        'require_unit': 'sacrifice 1 drone',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': 'Adaptive Talons.Seismic Spines',
        'activate_unit': 'Lurker',

    },
    units.Zerg.NydusNetwork: {
        # wiki英文 Unit
        'name': 'Nydus_Network',
        'name_cn': '虫道网络',
        # wiki英文 Details
        'description': 'Enables creation of nydus worms and acts as an entrance to the nydus transport system.',
        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 850,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
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
        'produce_time': 36,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 150,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Drone.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Summon Nydus Worm': 'Always available.'
                                 'A nydus network can create multiple nydus worms at any point visible to the player. '
                                 'The worm spawns creep when it emerges. The nydus worm gains 3 armor as it emerges.'
                                 'cost 75 minerals and 75 gas.cooldown 14 seconds.need 14 seconds to build Nydus Worm.'
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Lair',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Drone',

        # 激活选项，这一部分需要游戏知识
        'activate_building': 'Nydus Worm',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.NydusCanal: {
        # wiki英文 Unit
        'name': 'NydusCanal',
        'name_cn': '坑道虫',
        # wiki英文 Details
        'description': 'The new transport structure for the zerg, similar to the nydus canal of StarCraft I. '
                       'Produced from the nydus network. Unlike nydus canals which could only be placed on creep, '
                       'nydus worms may be spawned anywhere within sight range.',
        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 300,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
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
        'produce_time': 14,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 75,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 75,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'built by Nydus Network.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Nydus Network',
        'require_tech': '',
        'require_unit': '',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.RoachWarren: {
        # wiki英文 Unit
        'name': 'Roach Warren',
        'name_cn': '蟑螂温室',
        # wiki英文 Details
        'description': 'Enables production of roaches and researches roach upgrades.',
        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 850,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
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
        'produce_time': 39,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Drone.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Spawning Pool',
        'require_tech': '',
        'require_unit': 'sacrifice 1 drone',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': 'Glial Reconstitutuion(need Lair).Tunneling Claws(need Lair)',
        'activate_unit': 'Roach''Ravager',

    },
    units.Zerg.SpawningPool: {
        # wiki英文 Unit
        'name': 'Spawning Pool',
        'name_cn': '分裂池',
        # wiki英文 Details
        'description': 'Required for production of zerglings and queens and researches zergling upgrades.',
        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 1000,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
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
        'produce_time': 46,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 200,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Drone.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Hatchery',
        'require_tech': '',
        'require_unit': 'sacrifice 1 drone',

        # 激活选项，这一部分需要游戏知识
        'activate_building': 'Roach Warren.Baneling Nest.Spine Crawler.Spore Crawler.Lair',
        'activate_tech': 'Metabolic Boost.Adrenal Glands(need Hive)',
        'activate_unit': 'Zerglings.Queen',

    },
    units.Zerg.SpineCrawler: {
        # wiki英文 Unit
        'name': 'Spine Crawler',
        'name_cn': '脊针爬虫',
        # wiki英文 Details
        'description': 'A mobile creep-bound defensive structure that attacks ground units.',
        'target': ['ground'],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 300,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 2,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 1.4,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': ['armored'],
        'weapon1_target': ['ground'],
        'weapon1_attack': 25,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 5,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 7,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1.32,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 36,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 100,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Drone.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Uproot/Root': 'Always available.'
                           'Uproots/Roots the Spine Crawler.'

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Spawning Pool',
        'require_tech': '',
        'require_unit': 'sacrifice 1 drone',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.Spire: {
        # wiki英文 Unit
        'name': 'Spire',
        'name_cn': '尖塔',
        # wiki英文 Details
        'description': 'Required to produce mutalisks and corruptors and provides upgrades for aerial units.',
        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 850,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
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
        'produce_time': 71,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 200,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 200,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Drone.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade
            'Mutate into Greater Spire': 'Transforms a hatchery into a Greater Spire.'
                                         'Cost 100 mineral, 150 gas and 71 seconds.Required Hive.'

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Lair',
        'require_tech': '',
        'require_unit': 'sacrifice 1 drone',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': 'Flyer Attacks(level 2 need Lair.level 3 need Hive). '
                         'Flyer Carapace(level 2 need Lair.level 3 need Hive)',
        'activate_unit': 'Mutalisk, Corruptor',

    },
    units.Zerg.SporeCrawler: {
        # wiki英文 Unit
        'name': 'Spore Crawler',
        'name_cn': '孢子爬虫',
        # wiki英文 Details
        'description': 'A mobile creep-bound anti-air defensive structure.',
        'target': ['air'],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 400,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 1.4,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': ['biological'],
        'weapon1_target': ['air'],
        'weapon1_attack': 15,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 15,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 7,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0.61,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 21,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 75,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Drone.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Uproot/Root': 'Always available.'
                           'Uproots/Roots the Spore Crawler.'

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Spawning Pool',
        'require_tech': '',
        'require_unit': 'sacrifice 1 drone',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.UltraliskCavern: {
        # wiki英文 Unit
        'name': 'Ultralisk_Cavern',
        'name_cn': '雷兽窟',
        # wiki英文 Details
        'description': 'Required to produce ultralisks and researches ultralisk upgrades.',
        'target': [],
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological', 'structure'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 850,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 0,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': [],
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
        'produce_time': 46,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 150,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 200,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Spire.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Hive',
        'require_tech': '',
        'require_unit': 'sacrifice 1 Drone',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': 'Chitinous Plating.Anabolic Synthesis',
        'activate_unit': 'Ultralisk',

    },

    units.Zerg.LurkerBurrowed: {
        # wiki英文 Unit
        'name': 'LurkerBurrowed',
        'name_cn': '潜地的潜伏者',
        # wiki英文 Details
        'description': 'A long ranged siege unit that evolves from the hydralisk. '
                       'Must burrow to attack, but does damage in a line.',
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['armored', 'biological'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 200,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 1,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 0,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': ['armored'],
        'weapon1_target': ['ground'],
        'weapon1_attack': 20,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 10,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 2,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 8,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 1.25,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 3,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 0,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 0,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'morph from Hydarlisk.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade
            'Adaptive Talons': 'Reduces Lurker burrow time from 2 to 1.07 seconds.'
                               'Cost 100 mineral, 100 gas and 57 seconds. Required Hive.In Lurker Den.',
            'Seismic Spines': 'Increases the Lurker’s range from 8 to 10.'
                              'Cost 150 mineral, 150 gas and 57 seconds. Required Hive.In Lurker Den.'
        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': 'have Lurker Den',
        'require_tech': '',
        'require_unit': 'a Lurker',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.Broodling: {
        # wiki英文 Unit
        'name': 'Broodling',
        'name_cn': '巢虫',
        # wiki英文 Details
        'description': 'Produced from destroyed buildings and brood lord attacks.',
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['light', 'biological'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 20,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 4.13,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': ['ground'],
        'weapon1_attack': 4,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 1,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0.57,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 0,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 0,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'produced by Brooding Lord.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

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
    units.Zerg.Locust: {
        # wiki英文 Unit
        'name': 'Locust',
        'name_cn': '蝗虫',
        # wiki英文 Details
        'description': 'Produced from Swarm Host.Life span 18 seconds。',
        'target_self': ['ground'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['light', 'biological'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 50,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.62,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': ['ground'],
        'weapon1_attack': 10,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 1,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 3.,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 1,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0.43,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 0,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 0,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'produced by LocustFlying.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能

        },

        # 前置条件，这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': 'Swarm Host',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    },
    units.Zerg.LocustFlying: {
        # wiki英文 Unit
        'name': 'LocustFlying',
        'name_cn': '蝗虫飞行形态',
        # wiki英文 Details
        'description': 'Produced from Swarm Host.Life span 18 seconds。',
        'target_self': ['air'],
        # wiki中文 基本信息/属性
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_self': ['light', 'biological'],
        # wiki中文 作战/武器，克制的对象(有伤害加成的)
        # biological生物/mechanical机械/psionic灵能/light轻甲/armored重甲/massive巨型/structure建筑
        'type_anti': [],

        # 生存
        'health': 50,  # wiki中文 基本信息/生命值
        'shield': 0,  # wiki中文 基本信息/护盾
        'health_armor': 0,  # wiki中文 基本信息/护甲 无升级时
        'armor_upgrade_offset': 1,  # wiki中文 基本信息/护甲 每次护甲升级时的偏移量
        'speed': 2.62,  # wiki中文 基本信息/移动速度

        # 作战
        'weapon1_type_anti': [],
        'weapon1_target': ['ground'],
        'weapon1_attack': 0,  # wiki中文 作战/武器/伤害，基础伤害
        'weapon1_attack_bonus': 0,  # wiki中文 作战/武器/伤害，克制附加伤害
        'weapon1_attack_upgrade_base_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量
        'weapon1_attack_upgrade_bonus_damage_offset': 0,  # wiki中文 作战/武器/伤害，攻击升级偏移量（克制伤害）
        'weapon1_attack_range': 0.,  # wiki中文 作战/武器/射程，近战为1
        'weapon1_attack_times': 0,  # wiki中文 作战/武器/多重攻击，没有时为1重攻击
        'weapon1_cooldown': 0,  # wiki中文 作战/武器/攻击间隔

        # 对于可移动单位是训练成本/ 对于建筑是建造成本
        'supply': 0,  # wiki中文 基本信息/占用舱载空间，即在游戏中占用的人口
        'warp_time': 0,  # wiki中文 生产/生产时间2，单位，秒，没有时置零
        'produce_time': 0,  # wiki中文 生产/生产时间1，单位，秒
        'produce_cost_mineral': 0,  # wiki中文 生产/成本，水晶(蓝色)
        'produce_cost_gas': 0,  # wiki中文 生产/成本，瓦斯(绿色)
        'produce_from': 'produced by Swarm Host.',  # wiki中文 生产/生产设施

        # 技能
        'energy': 0,  # wiki中文 基本信息/能量，默认值为0
        'upgrade': {  # wiki英文 升级，不记录公共升级，如ground_weapon_upgrade

        },
        'ability': {  # wiki英文 作战/技能，只记录主动技能
            'Swoop': 'Always available.'
                     'Orders flying locust to land at target location, so it may attack enemies.'
                     'Cooldown 0 seconds.'
        },

        # 前置条件，这一部分需要游戏知识
        'require_building': '',
        'require_tech': '',
        'require_unit': 'Swarm Host',

        # 激活选项，这一部分需要游戏知识
        'activate_building': '',
        'activate_tech': '',
        'activate_unit': '',

    }

}

if __name__ == "__main__":
    for key in DATA_ZERG.keys():
        print(key)
    print(f"unit number: {len(DATA_ZERG.keys())}")

    # units.Zerg.LurkerBurrowed
    # units.Zerg.Broodling
    # units.Zerg.Locust
    # units.Zerg.LocustFlying
