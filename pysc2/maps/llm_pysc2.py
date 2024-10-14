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
