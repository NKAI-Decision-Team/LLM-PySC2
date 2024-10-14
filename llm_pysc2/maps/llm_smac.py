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


class llm_smac(lib.Map):
    directory = "llm_smac"
    download = ""
    players = 2
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
