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

import json

file_name = "o.txt"
# file_name = "a_pro.txt"    # processed text action
# file_name = "a_raw.txt"    # raw text action, may consist analysis and communication info
# file_name = "c_inp.txt"    # input communication info
# file_name = "c_out.txt"    # output communication info

with open(file_name, "r") as f:
    lines = f.readlines()
    for i in range(len(lines)):
        dic = json.loads(lines[i])
        loop_step = list(dic.keys())[0]
        print("--" * 25 + f" Loop {loop_step} " + "--" * 25)
        print(dic[loop_step])
