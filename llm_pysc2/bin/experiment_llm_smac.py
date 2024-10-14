
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


def get_config(map_name):
  llm_smac_configs = {
    '1c3s5z': ConfigSmac_1c3s5z(),
    '2c_vs_64zg': ConfigSmac_2c(),
    '2s3z': ConfigSmac_2s3z(),
    '2s_vs_1sc': ConfigSmac_2s(),
    '3s5z': ConfigSmac_3s5z(),
    '3s5z_vs_3s6z': ConfigSmac_3s5z(),
    '3s_vs_3z': ConfigSmac_3s(),
    '3s_vs_4z': ConfigSmac_3s(),
    '3s_vs_5z': ConfigSmac_3s(),
  }
  if map_name in llm_smac_configs.keys():
    return llm_smac_configs[map_name]
  else:
    raise AssertionError(f"wrong map_name: {map_name}")


map_name = '1c3s5z'
enable_image_rgb = False
enable_image_feature = False

class MainAgentLLMSmac(MainAgent):
  def __init__(self):
    config = get_config(map_name)
    model_name = 'YOUR-MODEL-NAME'
    api_base = 'YOUR-API-BASE'
    api_key = 'YOUR-API-KEY'
    config.reset_llm(model_name, api_base, api_key, enable_image_rgb, enable_image_feature)
    super(MainAgentLLMSmac, self).__init__(config, LLMAgent)

  def step(self, obs):
    return super().step(obs)


if __name__ == "__main__":

  if not (enable_image_rgb or enable_image_feature):
    os.system(f"python -m pysc2.bin.agent --map {map_name} --agent_race protoss --parallel 1 "
              f"--agent llm_pysc2.bin.experiment_llm_smac.MainAgentLLMSmac")
  elif enable_image_rgb:
    os.system(f"python -m pysc2.bin.agent --map {map_name} --agent_race protoss --parallel 1 "
              f"--agent llm_pysc2.bin.experiment_llm_smac.MainAgentLLMSmac "
              f"--feature_screen_size 256 --feature_minimap_size 64 "
              f"--rgb_screen_size 256 --rgb_minimap_size 64 "
              f"--action_space RGB")
  elif enable_image_feature:  # parallel experiments with feature map obs do not available currently, set --parallel 1
    os.system(f"python -m pysc2.bin.agent --map {map_name} --agent_race protoss --parallel 1 "
              f"--agent llm_pysc2.bin.experiment_llm_smac.MainAgentLLMSmac "
              f"--feature_screen_size 256 --feature_minimap_size 64 "
              f"--rgb_screen_size 0 --rgb_minimap_size 0 "
              f"--render")
  else:
    print("Can not enable_image_rgb and enable_image_feature at the same time")
