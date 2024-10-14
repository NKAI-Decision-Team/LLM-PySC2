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

from llm_pysc2.agents.configs.llm_pysc2 import ConfigPysc2_Defend
from llm_pysc2.agents import MainAgent, LLMAgent
import os


class MainAgentLLMPysc2(MainAgent):
  def __init__(self):
    config = ConfigPysc2_Defend()
    for team in config.AGENTS['CombatGroup1']['team']:
      team['task'] = [
        {'time': '0:00', 'pos': None, 'info': "Protect our nexus and probes from enemy airdrops. At Game time 0:00, "
                                              "2 airdrops detected from minimap [24, 32] and [12, 24] to [16, 32]"},
        {'time': '0:10', 'pos': None, 'info': "Protect our nexus and probes from enemy airdrops. At Game time 0:10, "
                                              "2 airdrops detected from minimap [20, 24] and [20, 40] to [16, 32]"},
        {'time': '0:20', 'pos': None, 'info': "Protect our nexus and probes from enemy airdrops. At Game time 0:20, "
                                              "2 airdrops detected from minimap [24, 32] and [12, 40] to [16, 32]"},
        {'time': '0:30', 'pos': None, 'info': "Protect our nexus and probes from enemy airdrops. At Game time 0:30, "
                                              "2 airdrops detected from minimap [24, 32] and [10, 32] to [16, 32]"},
      ]
    super(MainAgentLLMPysc2, self).__init__(config, LLMAgent)

  def step(self, obs):
    return super().step(obs)


level = 1
map_name = f"pvz_task3_level{level}"


if __name__ == "__main__":
  map_name = f"pvz_task3_level1"
  os.system(f"python -m pysc2.bin.agent --map {map_name} --agent_race protoss --parallel 1 "
            "--agent llm_pysc2.bin.llm_pysc2.pvz_task3.MainAgentLLMPysc2")
