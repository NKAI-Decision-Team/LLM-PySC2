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

from llm_pysc2.cfg.llm_pysc2 import ConfigPysc2_Harass, ConfigPysc2_Defend, ConfigPysc2_Combat, ConfigPysc2_Combat_Small
from llm_pysc2.agents import *
import os


def get_config(map_name):
  if "task1" in map_name or "task2" in map_name or "harass" in map_name:
    config = ConfigPysc2_Harass()
  elif "task3" in map_name:
    config = ConfigPysc2_Defend()
  elif "task4" in map_name or "task5" in map_name or "task6" in map_name:
    config = ConfigPysc2_Combat()
    for agent_name in list(config.AGENTS.keys()):
      for team in config.AGENTS[agent_name]['team']:
        team['task'] = [
          {'time': None, 'pos': [32, 32], 'info': "Go to minimap coordinate [32, 32]."},
          {'time': '0:10', 'pos': None,
           'info': "Kill as much as enemy units as possible. If no enemy found, hold the position."},
        ]
  elif "task7" in map_name:
    config = ConfigPysc2_Combat()
    config.ENABLE_COMMUNICATION = True
    config.MAX_LLM_RUNTIME_ERROR_TIME = 60
    config.AGENTS_ALWAYS_DISABLE.remove('Commander')
    config.AGENTS['Commander']['team'][0]['task'] = [
      {'time': None, 'pos': None, 'info': "Organize frontline commanders to collaborate in defeating enemy troops, "
                                          "you should reach the goal and finish the battle before game time 1:30."},
    ]
  elif "task8" in map_name:
    config = ConfigPysc2_Combat()
    config.ENABLE_COMMUNICATION = True
    config.AGENTS_ALWAYS_DISABLE.remove('Airborne')
    config.AGENTS_ALWAYS_DISABLE.remove('Commander')
    config.AGENTS_ALWAYS_DISABLE.remove('Developer')
    config.AGENTS['Commander']['team'][0]['task'] = [
      {'time': None, 'pos': None, 'info': "Organize a multiline combat to defeat enemy troops and kill their workers, "
                                          "you should reach all the goals and finish the battle before game time 1:30."},
    ]
  elif "4s_blink_vs_" in map_name:
    config = ConfigPysc2_Combat_Small()
  else:
    raise AssertionError("wrong task index")

  return config


task = 1
level = 1
map_name = f"pvz_task{task}_level{level}"
enable_image_rgb = False
enable_image_feature = False

class MainAgentLLMPysc2(MainAgent):
  def __init__(self):
    config = get_config(task)
    model_name = 'YOUR-MODEL-NAME'
    api_base = 'YOUR-API-BASE'
    api_key = 'YOUR-API-KEY'
    config.reset_llm(model_name, api_base, api_key, enable_image_rgb, enable_image_feature)
    super(MainAgentLLMPysc2, self).__init__(config, LLMAgent)

  def step(self, obs):
    return super().step(obs)

# python -m pysc2.bin.agent --map 3s_vs_3z --agent pysc2.agents.no_op_agent.NoOpAgent

if __name__ == "__main__":

  if not (enable_image_rgb or enable_image_feature):
    os.system(f"python -m pysc2.bin.agent --map {map_name} --agent_race protoss --parallel 1 "
              f"--agent llm_pysc2.bin.experiment_llm_pysc2.MainAgentLLMPysc2")
  elif enable_image_rgb:
    os.system(f"python -m pysc2.bin.agent --map {map_name} --agent_race protoss --parallel 1 "  
              f"--agent llm_pysc2.bin.experiment_llm_pysc2.MainAgentLLMPysc2 "
              f"--feature_screen_size 256 --feature_minimap_size 64 "
              f"--rgb_screen_size 256 --rgb_minimap_size 64 "
              f"--action_space RGB")
  elif enable_image_feature:  # parallel experiments with feature map obs do not available currently, set --parallel 1
    os.system(f"python -m pysc2.bin.agent --map {map_name} --agent_race protoss --parallel 1 "
              f"--agent llm_pysc2.bin.experiment_llm_pysc2.MainAgentLLMPysc2 "
              f"--feature_screen_size 256 --feature_minimap_size 64 "
              f"--rgb_screen_size 0 --rgb_minimap_size 0 "
              f"--render")
  else:
    print("Can not enable_image_rgb and enable_image_feature at the same time")
