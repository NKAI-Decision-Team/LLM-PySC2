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


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pysc2.maps import lib


class llm_pysc2(lib.Map):
  directory = "llm_pysc2"
  download = ""
  players = 2
  # game_steps_per_episode = 16 * 60 * 30  # 30 minute limit.
  game_steps_per_episode = 22 * 60 * 30  # 30 minute limit.


llm_pysc2_maps = [
  "debug_map",
  "pvz_task1_level1",
  "pvz_task2_level1",
  "pvz_task3_level1",
  "pvz_task4_level1",
  "pvz_task5_level1",
  "pvz_task6_level1",
  "pvz_task7_level1",
  "pvz_task8_level1",

  "pvz_task1_level2",
  "pvz_task2_level2",
  "pvz_task3_level2",
  "pvz_task4_level2",
  "pvz_task5_level2",
  "pvz_task6_level2",
  "pvz_task7_level2",
  "pvz_task8_level2",

  "pvz_task1_level3",
  "pvz_task2_level3",
  "pvz_task3_level3",
  "pvz_task4_level3",
  "pvz_task5_level3",
  "pvz_task6_level3",
  "pvz_task7_level3",
  "pvz_task8_level3",
]

for name in llm_pysc2_maps:
    globals()[name] = type(name, (llm_pysc2,), dict(filename=name))
