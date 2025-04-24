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


BASIC_COMBAT_RULES = \
"""
1. Concentrating firepower is always necessary, attack different unit at the same time will definitely reduce killing speed and leading to terrible result. Always concentrating all teams' fire at one unit that (1)with highest DPS(most valuable) (2)most vulnerable (3)closest.
"""

# BASIC_COMBAT_RULES = \
# """
#   1. Try to kill more and loss less. Always concentrating firepower on the most vulnerable enemy to quickly kill enemy units.
#   2. Try to kill enemy as quick as possible, retreat promptly when/before enemy reinforcements arrive.
#   3. When sacrificing your unit can earn much more profits, you can choose to sacrifice your unit.
#   4. Use your skills well to achieve optimal tactical results. Especially when controlling support units. Be aware that some skills may have side effects or long cooldowns, use them with caution.
#   5. Always remember the tactical **tasks** given by superior. Sometimes you have to sacrifice whole team to ensure the achievement of tactical objectives.
#   6. Try to handle micro operations well. Move during weapon cooling, attack while weapon ready, retreat heavily damaged unit and complete a kill as soon as possible.
#   7. All teams should **concentrating fire** on the same unit(Usually the most vulnerable unit or unit with highest DPS). Do not attack multi-unit at the same time.
#   8. Sequence actions as "skills/abilities -> attack -> move".
#   9. Every coordinate mentioned in analysis should be clearly marked whether it is screen coordinates or minimap coordinates.
#   10. Using <Select_Unit_Move_Screen> to repositioning low health units to safer location while still ensuring attacking the nearest enemy. At the same time, use healther units to engage in forward combat and bear damage for those vulnerable units.
#   11. When you use **Move** action, please ensure that the moving path is **valid(within the allowed range)**, **long enough**, **safe** and **keep enemies in attack range**.
#   12. Usually, the camera will focus you units that screen [12, 12] is the position of your units. If you need to relocate your units, move your units to a position away from [12, 12].
#   13. Sometimes movement can lead to missed opportunities for attacks and causing allys be concentrated by the enemies. In high-intensity combat, use movement with caution(only when necessary).
#   14. Concentrating firepower is always necessary. Always concentrating all teams' fire at one unit that (1)with highest DPS(most valuable) (2)most vulnerable (3)closest.
# """

#   11. When you use **Move** action, please ensure that the moving path is **long enough** and **safe** for the next several seconds.

BASIC_COMMAND_RULES = \
"""
# Analyse following aspect in your decision process:
# \t1. (Combat Deployment) Analyse the situation, always make deployment for attack/defend/retreat at each step. As default choice, ask your units to defend your area. If you have enough units, rise attack to defeat your enemy.
# \t2. (Scan Deployment) If you are prepared for combat, make scan deployment to find out enemy's strengths. Note that unit for scan will be killed by enemy units.
# \t3. (Final Combat) If game time > 12:00 and you have enough units (DO NOT have to be 200 supply), raise attack to defeat the enemy.
"""

BASIC_DEVELOP_RULES = \
"""
# Analyse following aspect in your decision process:
# \t1. (Supply) If run out of supply (less than 10) and no building for supply is under construction, build Pylon/OverLord/SupplyDepot (depend on your race).
# \t2. (Economy Building: Base) If you have enough minerals (more than 400), build Nexus/Hatchery/CommandCenter (depend on your race).
# \t3. (Economy Building: Gas) If you run out of gas (much less than minerals), build Assimilator/Extractor/Refinery (depend on your race).
# \t4. (Building: Unit Training) If you have too less unit training buildings, or there are abundant resources but all the unit training buildings are working, build unit training buildings.
# \t5. (Building: Research) If you have too less research buildings, or there are abundant resources but all the research buildings are working, build research buildings.
# \t6. (Unit Training/Warping) If you have enough idle unit training buildings but few combat units, or have a lot resource, train/warp units as much as possible.
# \t7. (Tech Upgrading) If you have idle research buildings and enough resource, or have a lot resource, update your technology.
# \t8. (Early Stage Expand) If you do not have 'the second base building (such as Nexus)', the 'CyberneticCore', the 'TwilightCouncil' and 'first two Gateway', try to build them as quick as possible.
# \t9. (Middle Stage Develop) During the middle stage of the game, try to build buildings for training high value units, and train units as much as possible (especially high value units) to increase strength.
# \t10. (Final Stage Develop) During the final stage of the game, train or warp more units to fight with enemy, do not build building if we have enough buildings.
"""

BASIC_BUILD_RULES = \
"""
Analyse following aspect in your decision process:
\t1. (Minimap Position) According to image 'rgb_minimap', where is/are our base/bases and where should we go? give minimap position. (Our base units and buildings are green points/squares in the minimap)
\t2. (Build) You can build on any position of the screen (unless it is blocked by other buildings) direct use the action <Build_XXX_Screen([x, y])>. You can build more than one buildings at a step by generate many action <Build_XXX_Screen([x, y])>.
\t3. (Move) You should move to a plain location near the base building, and build buildings there. Don't be far away from the base building, keep base building in your sight(screen), unless you are building a new one.
\t4. (Actions Sequence) First <Build_xxx_Screen(screen)> or <Build_xxx_Near(tag)> then <Move_xxx(xxx)> (note that, do not move and build at the same screen position)
"""

# \t1. (Supply) If run out of supply (less than 10) and no building for supply is under construction, build Pylon/OverLord/SupplyDepot (depend on your race).
# \t2. (Economy Building: Base) If you have enough minerals (more than 400), build Nexus/Hatchery/CommandCenter (depend on your race).
# \t3. (Economy Building: Gas) If you run out of gas (much less than minerals), build Assimilator/Extractor/Refinery (depend on your race).
# \t4. (Building: Unit Training) If you have too less unit training buildings, or there are abundant resources but all the unit training buildings are working, build unit training buildings.
# \t5. (Building: Research) If you have too less research buildings, or there are abundant resources but all the research buildings are working, build research buildings.

# BASIC_COMBAT_RULES_REFLECTION = \
# """
#   1. Whether each action of a_t1 are in a legal form that shown in the 'Valid Actions Part' of s_t1?
#   2. Whether each action of a_t1 is queued in correct sequence?
#   3. Whether the args of a_t1 are appropriate? for example, whether the attacked unit is the most important target?
#   4. Whether concentrated firepower on the most vulnerable enemy? Can a single attack kill this unit? (calculate the total damage of one hit are needed)
# whether the position of moving is appropriate in the micro-operation.
# """

def get_rules(agent_name):
  if 'Commander' in agent_name:
    return BASIC_COMMAND_RULES
  if 'Developer' in agent_name:
    return BASIC_DEVELOP_RULES
  if 'CombatGroup' in agent_name:
    return BASIC_COMBAT_RULES
  if 'Builder' in agent_name:
    return BASIC_BUILD_RULES
  return 'No specific rule, make decisions according to the situation'

class BasePrompt:

  def __init__(self, name, log_id, config):
    self.name = name
    self.config = config
    self.log_id = log_id
    self.sp = ''
    self.eip = ''
    self.eop = ''
    # self.screen_img_rgb_prompt = ''
    # self.screen_img_fea_prompt = ''
    # self.minimap_img_rgb_prompt = ''
    # self.minimap_img_fea_prompt = ''


class CombatGroupPrompt(BasePrompt):

  def __init__(self, name, log_id, config):
    super(CombatGroupPrompt, self).__init__(name, log_id, config)

    output_format = \
"""
Analysis:
  xxxxx
Actions:
  Team TeamName-1:
    <ActionName1(...)>  # format like **ActionName1(...)** and -ActionName1(...)- are not valid, must use <>
    <ActionName2(...)>
  Team TeamName-2:
    <ActionName1(...)>
"""

    # Part 1
    self.sp = \
f"""
1.Identity
  You are a {self.config.AGENTS[self.name]['describe']}.
  Your should command your troops, complete the tactical tasks assigned by the superior. You will have several teams of units, you can command these teams to fight together or perform different tasks.

2.Rules
{get_rules(self.name)}

3.Action Output
  You should make decisions according to observed information, tactic task and rules, give analysis and decisions for each team. For example, if you have 2 teams name as 'TeamName-1' and 'TeamName-2', you should output as:
  {output_format}
      
Note that actions must in the shape <ActionName(...)>, do not generate action like 'ActionName(...)' or **ActionName(...)**.
"""
    self.eip = """xxxxx"""
    self.eop = f"""{output_format}"""

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
#       self.eip += \
# """
# Communication:
#   From Commander:
#     Your task is to attack the enemy workers of an enemy base near minimap [48,32]. Intelligence shows that two enemy Queens are located on the minimap [44,32]. Try to avoid being detected by enemy Queens before arriving.
#
# Available Communication Tragets:
#   Commander: Protoss military supreme commander. Responsible for making macro decision through communication, and controls nexus for massrecall for tactical objectives.
# Available Communication Functions:
#   <MessageTo(AgentName, message)>
#   <MessageTo(ChannelName, message)>
#   <ListenTo(ChannelName)>
# Args explanation:
#   (1)AgentName: refers to a name mentioned in Available Communication Tragets.
#   (2)ChannelName: shape as Channel-i, i refers to an integer.
#   (2)message: any text wrapped between ''' and '''.
# """

      self.eop += \
"""
Communications:
    <MessageTo(Commander, '''Copy that, we have arrived enemy base, and started attack enemy workers''')>
"""



class CommanderPrompt(BasePrompt):  # TODO: Design a prompt specifically for the supreme military commander
  def __init__(self, name, log_id, config):
    super(CombatGroupPrompt, self).__init__(name, log_id, config)
    # self.sp = ''
    # self.eip = ''
    # self.eop = ''


class DeveloperPrompt(BasePrompt):  # TODO: Design a prompt specifically for the supreme logistics commander
  def __init__(self, name, log_id, config):
    super(CombatGroupPrompt, self).__init__(name, log_id, config)
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
  from llm_pysc2.cfg.config import ProtossAgentConfig
  config = ProtossAgentConfig()
  prompt = CombatGroupPrompt('CombatGroup1', log_id=0, config=config)

  print("--" * 25 + "System Prompt" + "--" * 25)
  print(prompt.sp)
  print("--" * 25 + "Example Input Prompt" + "--" * 25)
  print(prompt.eip)
  print("--" * 25 + "Example Output Prompt" + "--" * 25)
  print(prompt.eop)