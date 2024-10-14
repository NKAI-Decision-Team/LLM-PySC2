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

from llm_pysc2.agents.configs.llm_pysc2 import ConfigPysc2_Harass
from llm_pysc2.agents import MainAgent, LLMAgent
import os


class MainAgentLLMPysc2(MainAgent):
  def __init__(self):
    config = ConfigPysc2_Harass()
    for team in config.AGENTS['CombatGroup8']['team']:
      team['task'] = [
        {'time': None, 'pos': [52, 32], 'info': "Go to minimap coordinate [52, 32], and try to avoid been detected or attacked before arrival."},
        {'time': None, 'pos': None, 'info': "Kill as much as enemy workers as possible."},
      ]
    super(MainAgentLLMPysc2, self).__init__(config, LLMAgent)

  def step(self, obs):
    return super().step(obs)


level = 1
map_name = f"pvz_task2_level{level}"


if __name__ == "__main__":
  os.system(f"python -m pysc2.bin.agent --map {map_name} --agent_race protoss --parallel 1 "
            "--agent llm_pysc2.bin.llm_pysc2.pvz_task2.MainAgentLLMPysc2")
