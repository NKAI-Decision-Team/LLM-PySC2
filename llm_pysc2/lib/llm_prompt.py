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


class BasePrompt:

  def __init__(self):
    self.sp = ''
    self.eip = ''
    self.eop = ''
    self.screen_img_rgb_prompt = ''
    self.screen_img_fea_prompt = ''
    self.minimap_img_rgb_prompt = ''
    self.minimap_img_fea_prompt = ''


class CombatGroupPrompt(BasePrompt):

  def __init__(self, name, log_id, config):
    super(CombatGroupPrompt, self).__init__()
    self.name = name
    self.config = config
    self.log_id = log_id

    # Part 1
    self.sp = \
f"""
1.Identity
  You are a {self.config.AGENTS[self.name]['describe']}.
  Your should command your troops, complete the tactical tasks assigned by the superior. You will have several teams of units, you can command these teams to fight together or perform different tasks.

2.Rules
  2.1 Try to kill more and loss less. Usually, concentrating all firepower on the same target(especially the closest enemy) can improve the strike effectiveness.
  2.2 Try to kill enemy as quick as possible, retreat promptly when/before enemy reinforcements arrive.
  2.3 When sacrificing your unit can earn much more profits, you can choose to sacrifice your unit.
  2.4 Use your skills well to achieve optimal tactical results. Especially when controlling support units.
  2.5 Always remember the tactical tasks given by superior. Sometimes you have to sacrifice whole team to ensure the achievement of tactical objectives.

3.Action Output
  You should make decisions according to observed information, tactic task and rules, give analysis and decisions for each team. For example, if you have 2 teams name as 'Stalker-1' and 'Stalker-2', you should output as:
  
  Analysis: 
    xxxxx
  Actions:
    Team Stalker-1:
      xxxxx
    Team Stalker-2:
      xxxxx
"""
    self.eip = \
"""
Game Info
  Time: 0:32

Team Oracle-1 Info:
  Team minimap position: [50, 32]
  Controlled Team Units:
    Unit: Oracle    Tag: 0x100200001    Pos: (67, 59)    Health: 100    Energy: 108    Weapon_cooldown: 0
  Nearby Ally units:
    Unit: Observer    Tag: 0x100140001    Pos: (10, 70)    Health: 70    Weapon_cooldown: 0
  Nearby Enemy units:
    Unit: Drone    Tag: 0x101340001    Pos: (54, 40)    Health: 40
    Unit: Drone    Tag: 0x101280001    Pos: (61, 58)    Health: 40
    Unit: Drone    Tag: 0x1012c0001    Pos: (52, 70)    Health: 40
    Unit: Drone    Tag: 0x1014c0001    Pos: (50, 62)    Health: 40
    Unit: Drone    Tag: 0x101400001    Pos: (61, 63)    Health: 40
    Unit: Drone    Tag: 0x101380001    Pos: (58, 89)    Health: 40
    Unit: Drone    Tag: 0x101480001    Pos: (61, 71)    Health: 18
    Unit: Drone    Tag: 0x101300001    Pos: (54, 94)    Health: 40
    Unit: Drone    Tag: 0x101440001    Pos: (50, 72)    Health: 40
    Unit: Drone    Tag: 0x101240001    Pos: (61, 63)    Health: 40
    Unit: Overlord    Tag: 0x101500001    Pos: (18, 67)    Health: 200
    Unit: Hatchery    Tag: 0x101100001    Pos: (34, 67)    Health: 1500
    Unit: SpawningPool    Tag: 0x1011c0002    Pos: (50, 110)    Health: 197    Build_progress: 10%
    Unit: Queen    Tag: 0x1000c0001    Pos: (50, 40)    Health: 175    Energy: 25
    Unit: Queen    Tag: 0x100580001    Pos: (57, 54)    Health: 175    Energy: 25

Here are some description of screen units:
  Protoss.Oracle
    A light, psionic, support and harassment ship. Can grant vision and harass light units and workers with its pulsar beam.(Cannot attack ground units before activating Pulsar Beam)
    unit abilities:
      Revelation: Always available. Active skill. Cost: 25 energy. Reveals enemy units and structures in an area, granting vision for 20 seconds. Also reveals cloaked or burrowed units or structures.
      Pulsar Beam: Always available. Active skill. Cost: 25 energy (+1.96 energy per second). Enables the Oracle to attack ground units with high damage, particularly effective against light units.
      Stasis Ward: Always available. Active skill. Cost: 50 energy. Places a cloaked stasis ward on the ground that traps enemy units in stasis for 21 seconds upon activation.
  Protoss.Observer
    A cloaking air unit that functions as a detector.
  Protoss.StasisTrap
    Cloaked structure created by the Oracle. Used to freeze incoming units.Permanent Cloaking:This unit is permanently cloaked. They cannot be seen or directly attacked by enemy forces, unless they have detector support.
  Zerg.Drone
    Harvests resources and spawns structures. Is sacrificed when creating new structures.The drone morphs into structures and harvests minerals and vespene gas.
  Zerg.Overlord
    Produces control and is no longer a detector like the StarCraft I version.
  Zerg.Hatchery
    Spawns larvae to be morphed into other zerg strains, generates creep and digests minerals and gas into a usable form. The queen is spawned directly from the hatchery.
  Zerg.SpawningPool
    Required for production of zerglings and queens and researches zergling upgrades.
  Zerg.Queen
    The queen a powerful attacking ground dwelling support unit ideal for zerg defense.

Valid Actions:
  <Stop()>
  <No_Operation()>
  <Attack_Unit(tag)>
  <Move_Screen(screen)>
  <Move_Minimap(minimap)>
  <Ability_OracleRevelation_Screen(screen)>
  <Ability_StasisTrap_Screen(screen)>
Arg: 
  tag: refers to a hexadecimal number, shape as 0x000000000.
  screen: refers to a screen coordinate, shape as [x, y], x and y range from 0 to 128.
  minimap: refers to a minimap coordinate, shape as [x, y], x and y range from 0 to 64.
"""
    self.eop = \
"""
Analysis: 
  We are controlling a team called Oracle-1, we have met several enemy Queens, Drones and Overlord. 
  Our goal is killing as much Drone, consider that we still have enough health and energy, we should choose drone to attack, and leave the area quickly.
Actions:
  Team Oracle-1:
    <Attack_Unit(0x101480001)>
    <Move_Screen([67, 96])>
"""

    # Part 2
    if self.config.ENABLE_COMMUNICATION:
      self.sp += \
"""
4.Communication Output
  If there is Available Communicate Target, you should keep communicating with them by Communication functions. For example, if 'Commander' and 'CombatGroup4' in Available Communicate Target, you can output as:

  Communications:
    <MessageTo(Commander, '''xxxxxxxxxx''')>
    <MessageTo(CombatGroup4, '''xxxxxxxxxx''')>
"""
      self.eip += \
"""
Communication:
  From Commander: 
    Your task is to attack the enemy workers of an enemy base near minimap [48,32]. Intelligence shows that two enemy Queens are located on the minimap [44,32]. Try to avoid being detected by enemy Queens before arriving.

Available Communication Tragets:
  Commander: Protoss military supreme commander. Responsible for making macro decision through communication, and controls nexus for massrecall for tactical objectives.
Available Communication Functions:
  <MessageTo(AgentName, message)>
  <MessageTo(ChannelName, message)>
  <ListenTo(ChannelName)>
Args explanation:
  (1)AgentName: refers to a name mentioned in Available Communication Tragets.
  (2)ChannelName: shape as Channel-i, i refers to an integer.
  (2)message: any text wrapped between ''' and '''.
"""
      self.eop += \
"""
Communications:
    <MessageTo(Commander, '''Copy that, we have arrived enemy base, and started attack enemy workers''')>
"""

    # Part 3
    self.eip += \
f"""
Give each team no more than {self.config.MAX_NUM_ACTIONS} actions.
Now, start generating your analysis and actions:
"""



class CommanderPrompt(BasePrompt):  # TODO: Design a prompt specifically for the supreme military commander
  def __init__(self, name, log_id, config):
    super(CombatGroupPrompt, self).__init__()
    self.name = name
    self.config = config
    self.log_id = log_id
    # self.sp = ''
    # self.eip = ''
    # self.eop = ''


class DeveloperPrompt(BasePrompt):  # TODO: Design a prompt specifically for the supreme logistics commander
  def __init__(self, name, log_id, config):
    super(CombatGroupPrompt, self).__init__()
    self.name = name
    self.config = config
    self.log_id = log_id
    # self.sp = ''
    # self.eip = ''
    # self.eop = ''



PROTOSS_FACTORY = {
  'default': CombatGroupPrompt,
  'commander': CommanderPrompt,
  'developer': DeveloperPrompt,
}
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
  prompt = CombatGroupPrompt('CombatGroup1', log_id=0, config=config)

  print("--" * 25 + "System Prompt" + "--" * 25)
  print(prompt.sp)
  print("--" * 25 + "Example Input Prompt" + "--" * 25)
  print(prompt.eip)
  print("--" * 25 + "Example Output Prompt" + "--" * 25)
  print(prompt.eop)