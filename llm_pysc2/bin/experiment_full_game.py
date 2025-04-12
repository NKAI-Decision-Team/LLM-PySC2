# Copyright 2025, LLM-PySC2 Contributors. All Rights Reserved.
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


from llm_pysc2.cfg import ProtossAgentConfig
from llm_pysc2.agents import *
import os

map_name = f"Simple64"
# map_name = f"debug_map"
difficult_level = 4  # 1 to 10

difficulties = ['very_easy', 'easy', 'medium',
                'medium_hard', 'hard', 'harder', 'very_hard',
                'cheat_vision', 'cheat_money', 'cheat_insane']
difficulty = difficulties[difficult_level-1]  # from sc2_env.Difficulty

# enable_image_rgb, enable_image_feature = True, False
enable_image_rgb, enable_image_feature = False, False
# enable_image_rgb, enable_image_feature = False, True


class MainAgentLLMPysc2(MainAgent):
  def __init__(self):
    config = ProtossAgentConfig()

    model_name = 'YOUR-MODEL-NAME'
    api_base = 'YOUR-API-BASE'
    api_key = 'YOUR-API-KEY'
    config.reset_llm(model_name, api_base, api_key, enable_image_rgb, enable_image_feature)

    for name in config.AGENTS.keys():
      if name not in ['Builder', 'Commander', 'Developer']:
        # config.AGENTS[name]['llm']['model_name'] = 'YOUR-MODEL-NAME'
        # config.AGENTS[name]['llm']['api_base'] = 'YOUR-API-BASE'
        # config.AGENTS[name]['llm']['api_key'] = 'YOUR-API-KEY'
        config.AGENTS[name]['llm']['img_rgb'] = False
        config.AGENTS[name]['llm']['img_fea'] = False
      else:
        config.AGENTS[name]['llm']['feature_map_names'] = ['power', 'pathable', 'buildable','height_map', 'player_relative']
      if name not in ['Commander', 'Developer']:  # , 'Developer'
        config.AGENTS_ALWAYS_DISABLE.append(name)

    config.SAFE_MODE = False
    config.LLM_SIMULATION_TIME = 0.5
    config.IGNORE_INIT_WARNINGS = True
    # config.ENABLE_MULTI_THREAD_QUERY = False
    config.MAX_LLM_DECISION_FREQUENCY = 0.2
    config.ENABLE_COMMUNICATION = True
    config.ENABLE_EASY_BUILD = True
    config.ENABLE_EASY_CONTROL = True
    config.ENABLE_EASY_WARP = True

    # config.ENABLE_AUTO_WORKER_MANAGE = False
    # config.ENABLE_EASY_BUILD = False

    super(MainAgentLLMPysc2, self).__init__(config, LLMAgent)

  def step(self, obs):
    return super().step(obs)


if __name__ == "__main__":

  if not (enable_image_rgb or enable_image_feature):
    os.system(f"python -m pysc2.bin.agent --map {map_name} --difficulty {difficulty} --agent_race protoss --parallel 1 "
              f"--agent llm_pysc2.bin.experiment_full_game.MainAgentLLMPysc2")
  elif enable_image_rgb:
    os.system(f"python -m pysc2.bin.agent --map {map_name} --difficulty {difficulty} --agent_race protoss --parallel 1 "  
              f"--agent llm_pysc2.bin.experiment_full_game.MainAgentLLMPysc2 "
              f"--feature_screen_size 256 --feature_minimap_size 64 "
              f"--rgb_screen_size 256 --rgb_minimap_size 64 "
              f"--action_space RGB")
  elif enable_image_feature:  # parallel experiments with feature map obs do not available currently, set --parallel 1
    os.system(f"python -m pysc2.bin.agent --map {map_name} --difficulty {difficulty} --agent_race protoss --parallel 1 "
              f"--agent llm_pysc2.bin.experiment_full_game.MainAgentLLMPysc2 "
              f"--feature_screen_size 256 --feature_minimap_size 64 "
              f"--rgb_screen_size 0 --rgb_minimap_size 0 "
              f"--render")
  else:
    print("Can not enable_image_rgb and enable_image_feature at the same time")
