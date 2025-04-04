
from llm_pysc2.lib.knowledge.neutral import DATA_NEUTRAL
from llm_pysc2.lib.knowledge.protoss import DATA_PROTOSS
from llm_pysc2.lib.knowledge.terran import DATA_TERRAN
from llm_pysc2.lib.knowledge.zerg import DATA_ZERG

DATA_SC2_UNITS = dict()
DATA_SC2_UNITS.update(DATA_TERRAN)
DATA_SC2_UNITS.update(DATA_ZERG)
DATA_SC2_UNITS.update(DATA_PROTOSS)
DATA_SC2_UNITS.update(DATA_NEUTRAL)

if __name__ == '__main__':
  print(DATA_SC2_UNITS)