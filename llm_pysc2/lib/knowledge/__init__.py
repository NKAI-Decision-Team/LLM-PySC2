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


from llm_pysc2.lib.knowledge.neutral import DATA_NEUTRAL
from llm_pysc2.lib.knowledge.protoss import DATA_PROTOSS
from llm_pysc2.lib.knowledge.terran import DATA_TERRAN
from llm_pysc2.lib.knowledge.zerg import DATA_ZERG
from pysc2.lib import units

DATA_SC2_UNITS = dict()
DATA_SC2_UNITS.update(DATA_TERRAN)
DATA_SC2_UNITS.update(DATA_ZERG)
DATA_SC2_UNITS.update(DATA_PROTOSS)
DATA_SC2_UNITS.update(DATA_NEUTRAL)

knowledge_dict = {}
knowledge_dict.update(DATA_PROTOSS)
knowledge_dict.update(DATA_TERRAN)
knowledge_dict.update(DATA_ZERG)
unit_dict = {v: k for k, v in units.Neutral.__dict__.items() if
             isinstance(v, int)}
unit_dict.update({v: k for k, v in units.Protoss.__dict__.items()
                  if isinstance(v, int)})
unit_dict.update({v: k for k, v in units.Terran.__dict__.items()
                  if isinstance(v, int)})
unit_dict.update({v: k for k, v in units.Zerg.__dict__.items() if
                  isinstance(v, int)})

if __name__ == '__main__':
  print(DATA_SC2_UNITS)
  print(knowledge_dict)