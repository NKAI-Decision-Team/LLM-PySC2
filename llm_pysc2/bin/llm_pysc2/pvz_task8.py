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
    config.ENABLE_COMMUNICATION = True
    config.AGENTS_ALWAYS_DISABLE.remove('Airborne')
    config.AGENTS_ALWAYS_DISABLE.remove('Commander')
    config.AGENTS_ALWAYS_DISABLE.remove('Developer')
    config.AGENTS['Commander']['team'][0]['task'] = [
      {'time': None, 'pos': None, 'info': "Organize a multiline combat to defeat enemy troops and kill their workers, "
                                          "must finish the battle before game time 1:30."},
    ]
    super(MainAgentLLMPysc2, self).__init__(config, LLMAgent)

  def step(self, obs):
    return super().step(obs)


level = 1
map_name = f"pvz_task8_level{level}"


if __name__ == "__main__":
  map_name = f"pvz_task8_level1"
  os.system(f"python -m pysc2.bin.agent --map {map_name} --agent_race protoss --parallel 1 "
            "--agent llm_pysc2.bin.llm_pysc2.pvz_task8.MainAgentLLMPysc2")
