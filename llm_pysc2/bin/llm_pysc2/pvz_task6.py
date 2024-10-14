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

from llm_pysc2.agents.configs.llm_pysc2 import ConfigPysc2_Combat
from llm_pysc2.agents import MainAgent, LLMAgent
import os


class MainAgentLLMPysc2(MainAgent):
  def __init__(self):
    config = ConfigPysc2_Combat()
    for agent_name in list(config.AGENTS.keys()):
        for team in config.AGENTS[agent_name]['team']:
          team['task'] = [
            {'time': None, 'pos': [32, 32], 'info': "Go to minimap coordinate [32, 32]."},
            {'time': None, 'pos': None, 'info': "Kill as much as enemy units as possible. If no enemy found, hold the position."},
          ]
    super(MainAgentLLMPysc2, self).__init__(config, LLMAgent)

  def step(self, obs):
    return super().step(obs)


level = 1
map_name = f"pvz_task6_level{level}"


if __name__ == "__main__":
  map_name = f"pvz_task6_level1"
  os.system(f"python -m pysc2.bin.agent --map {map_name} --agent_race protoss --parallel 1 "
            "--agent llm_pysc2.bin.llm_pysc2.pvz_task6.MainAgentLLMPysc2")
