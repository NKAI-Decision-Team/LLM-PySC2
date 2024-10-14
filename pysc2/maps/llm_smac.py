from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pysc2.maps import lib


class llm_smac(lib.Map):
  directory = "llm_smac"
  download = ""
  players = 2
  # game_steps_per_episode = 16 * 60 * 30  # 30 minute limit.
  game_steps_per_episode = 22 * 60 * 30  # 30 minute limit.


llm_smac_maps = {
  "1c3s5z",
  "2c_vs_64zg",
  "2s3z",
  "2s_vs_1sc",
  "3s5z",
  "3s5z_vs_3s6z",
  "3s_vs_3z",
  "3s_vs_4z",
  "3s_vs_5z",
}


def get_smac_map_registry():
  return llm_smac_maps


for name in llm_smac_maps:
  globals()[name] = type(name, (llm_smac,), dict(filename=name))
