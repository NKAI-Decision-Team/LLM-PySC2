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

from llm_pysc2.agents.configs.llm_smac import *
from llm_pysc2.agents import MainAgent, LLMAgent
import os


class MainAgentLLMSmac(MainAgent):
  def __init__(self):
    config = ConfigSmac_3s()
    super(MainAgentLLMSmac, self).__init__(config, LLMAgent)

  def step(self, obs):
    return super().step(obs)


if __name__ == "__main__":
  os.system(f"python -m pysc2.bin.agent --map 3s_vs_5z --agent_race protoss --parallel 1 "
            f"--agent llm_pysc2.bin.llm_smac.3s_vs_3z.MainAgentLLMSmac")
