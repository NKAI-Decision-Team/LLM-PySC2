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


from pysc2.lib import features, units
from llm_pysc2.lib.utils import get_ves_for_base_and_gas_building


def get_warp_info(agent) -> str:  # for Developer only

  if agent.config.ENABLE_EASY_WARP:
    return ''

  obs = agent.team_unit_obs_list[0]
  warp_source_info = ''
  pylon_info = ''
  prism_info = ''

  for unit in obs.observation.raw_units:
    if unit.alliance == features.PlayerRelative.SELF and unit.build_progress == 100:

      if unit.unit_type in [units.Protoss.WarpGate]:
        warp_source_info += f"\n\t{str(units.get_unit_type(unit.unit_type))}, "
        warp_source_info += f""  # Pysc2 do not provide cooldown status of warp gates
      if unit.unit_type == units.Protoss.Pylon:
        pylon_info += f"\n\t{str(units.get_unit_type(unit.unit_type))}, tag:{hex(unit.tag)}"
      if unit.unit_type == units.Protoss.WarpPrismPhasing:
        prism_info += f"\n\t{str(units.get_unit_type(unit.unit_type))}, tag:{hex(unit.tag)}"

  warp_target_info = pylon_info + prism_info
  if len(warp_source_info) > 0:
    warp_source_info = f"Available WarpGates:\n{obs.observation.player.warp_gate_count} WarpGate in total" + "\n\n"
    warp_target_info = f"Available WarpTrain Field Provider:" + warp_target_info + "\n\n"
  else:
    warp_target_info = ''

  return warp_source_info + warp_target_info


def get_ves_and_base_info(agent):

  if agent.config.ENABLE_EASY_BUILD:
    return ''

  obs = agent.team_unit_obs_list[0]
  _, _, ves_new_base_tags, ves_near_tags = get_ves_for_base_and_gas_building(obs)

  out_put_info = ''
  if len(ves_new_base_tags) > 0:
    out_put_info += f"Valid tag for new base (Nexus/CommandCenter/Hatchery):"
    for tag in ves_new_base_tags:
      out_put_info += f"\n\t {hex(tag)}"
    out_put_info += f"\n"

  if len(ves_near_tags) > 0:
    out_put_info += f"Valid tag for new gas building (Assimilator/Refinery/Extractor):"
    for tag in ves_near_tags:
      out_put_info += f"\n\t {hex(tag)}"
    out_put_info += f"\n"

  out_put_info += f"\n"
  return out_put_info