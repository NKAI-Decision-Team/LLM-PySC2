# Copyright 2017 Google Inc. All Rights Reserved.
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
"""A random agent for starcraft."""
import os
import random
import time

import numpy as np

from pysc2.agents import base_agent
from pysc2.lib import actions


class RandomAgent(base_agent.BaseAgent):
    """A random agent for starcraft."""

    def __init__(self):
        super(RandomAgent, self).__init__()

    def step(self, obs):
        super(RandomAgent, self).step(obs)

        function_id = np.random.choice(obs.observation.available_actions)
        args = [[np.random.randint(0, size) for size in arg.sizes]
                for arg in self.action_spec.functions[function_id].args]

        return actions.FunctionCall(function_id, args)


if __name__ == "__main__":
    os.system("python -m pysc2.bin.agent --map Simple64 --agent_race protoss")
