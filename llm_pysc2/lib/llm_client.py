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


from llamaapi import LlamaAPI
from zhipuai import ZhipuAI
from openai import OpenAI


from loguru import logger
from threading import Event
import threading
import random
import time


def gpt_query_runtime(self, event):
  llm_response = self.client.chat.completions.create(
  # llm_response = self.client.ChatCompletion.create(
    model=self.model_name,
    messages=self.messages,
    temperature=self.temperature
  )
  if event.is_set():
    return
  self.query_token_in = llm_response.usage.prompt_tokens
  self.query_token_out = llm_response.usage.completion_tokens
  self.llm_response = llm_response.choices[0].message.content
  # print(self.query_token_in)
  # print(self.query_token_out)
  # print(self.llm_response)


class GptClient:

  def __init__(self, name, log_id, config):

    self.model_name = config.AGENTS[name]['llm']['model_name']
    self.api_base = config.AGENTS[name]['llm']['api_base']
    self.api_key = config.AGENTS[name]['llm']['api_key']
    self.temperature = config.temperature

    self.client = OpenAI(
      api_key=self.api_key,
      base_url=self.api_base,
    )
    self.client.api_base = self.api_base
    self.client.api_key = self.api_key

    self.agent_name = name
    self.log_id = log_id
    self.config = config
    self.system_prompt = ''
    self.example_i_prompt = ''
    self.example_o_prompt = ''
    self.messages = []
    self.llm_response = None
    self.query_runtime = gpt_query_runtime
    # if 'gpt' in self.model_name or self.model_name == 'default':
    #   logger.info(f"[ID {self.log_id}] {self.agent_name} {self.model_name} GptClient initialized")
    logger.info(f"[ID {self.log_id}] {self.agent_name} {self.model_name} GptClient initialized")

    self.num_query = 0
    self.query_time = 0
    self.query_token_in = 0
    self.query_token_out = 0
    self.total_query_time = 0
    self.total_query_token_in = 0
    self.total_query_token_out = 0
    self.ave_query_time = 0
    self.ave_query_token_in = 0
    self.ave_query_token_out = 0

  def set_prompt(self, prompt):
    self.system_prompt = prompt.sp
    self.example_i_prompt = prompt.eip
    self.example_o_prompt = prompt.eop

  def wrap_message(self, obs_prompt, base64_images):

    if (base64_images is not None) and (self.model_name not in vision_model_names):
      logger.warning(f"[ID {self.log_id}] {self.agent_name} {self.model_name}: Model may not accept img, img discarded. vision_model_names: \n {vision_model_names}")
    if (base64_images is None) and (self.model_name in vision_model_names):
      logger.warning(f"[ID {self.log_id}] {self.agent_name} {self.model_name}: Vision available but img disabled")
    self.messages = [
      {"role": "system", "content": self.system_prompt},
      {"role": "user", "content": self.example_i_prompt},
      {"role": "assistant", "content": self.example_o_prompt},
    ]
    if (base64_images is not None and self.model_name in vision_model_names):
      for key in base64_images:
        if base64_images[key] is None:
          continue
        img_name = f'feature_map_{key}_screen' if key not in ['rgb_minimap', 'rgb_screen'] else key
        self.messages.append({"role": "user", "content": [
          {"type": "text", "text": f'This is the {img_name} image:'},  # obs_prompt
          {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_images[key]}"}}]}
        )
      logger.warning(f"[ID {self.log_id}] {self.agent_name} {self.model_name}: You are using image input, be care of the cost")
    self.messages.append({"role": "user", "content": obs_prompt})

  def query(self, obs_prompt, base64_images: "Dict or None"=None):

    # 重置 messages 列表
    self.wrap_message(obs_prompt, base64_images)

    # 尝试发送请求并获取回复
    max_retries = self.config.MAX_LLM_QUERY_TIMES
    events = [Event() for _ in range(max_retries)]
    for retries in range(max_retries):
      try:
        # tracemalloc.start()

        self.llm_response = None
        logger.success(f"[ID {self.log_id}] {self.agent_name} Start calling llm api!")
        logger.debug(f"[ID {self.log_id}] {self.agent_name} input prompt: \n{obs_prompt}")

        self.thread = threading.Thread(target=self.query_runtime, args=(self, events[retries]))
        self.thread.start()

        # 超时错误
        query_start_time = float(time.time())
        while not isinstance(self.llm_response, str):
          time.sleep(0.1)
          if float(time.time()) - query_start_time > self.config.MAX_LLM_RUNTIME_ERROR_TIME:
            events[retries].is_set()
            logger.error(f"[ID {self.log_id}] {self.agent_name} LLM query runtime error")
            raise RuntimeError(f"{self.agent_name} LLM query runtime error")

        if isinstance(self.llm_response, str):
          self.num_query += 1
          self.query_time = float(time.time()) - query_start_time
          self.total_query_time += self.query_time
          self.total_query_token_in += self.query_token_in
          self.total_query_token_out += self.query_token_out
          self.ave_query_time = self.total_query_time / self.num_query
          self.ave_query_token_in = self.total_query_token_in / self.num_query
          self.ave_query_token_out = self.total_query_token_out / self.num_query
          # current_dir = os.path.dirname(os.path.abspath(__file__))
          # self.log_dir_path = f"{current_dir}/../../llm_log/temp-{self.log_id}"
          # if not os.path.exists(self.log_dir_path):
          #   os.mkdir(self.log_dir_path)
          # if not os.path.exists(self.log_dir_path + f"/{self.agent_name}"):
          #   os.mkdir(self.log_dir_path + f"/{self.agent_name}")
          # path = self.log_dir_path + f"/{self.agent_name}/cost_temp.txt"
          # client_cost = f"time={self.query_time:.2f}, ave_time={self.ave_query_time:.2f}, " \
          #               f"token_in={self.query_token_in}, ave_token_in={self.ave_query_token_in:.2f}, " \
          #               f"token_out={self.query_token_out}, ave_token_out = {self.ave_query_token_out:.2f}"
          # utils.write_to_file(json.dumps({self.num_query: client_cost}), path)

        answer = self.llm_response
        logger.success(f"[ID {self.log_id}] {self.agent_name} Get llm response!")
        logger.debug(f"[ID {self.log_id}] {self.agent_name} llm response: \n{answer}")
        self.llm_response = None

        return answer
      except Exception as e:
        # 输出错误信息
        logger.error(f"[ID {self.log_id}] {self.agent_name} Error when calling the OpenAI API: {e}")
        # print(f"Error when calling the OpenAI API: {e}")

        # 如果达到最大尝试次数，返回一个特定的回复
        if retries >= max_retries - 1:
          logger.error \
            (f"[ID {self.log_id}] {self.agent_name} Maximum number of retries reached. The OpenAI API is not responding.")
          return "I'm sorry, but I am unable to provide a response at this time due to technical difficulties."

        # 重试前等待一段时间，使用 exponential backoff 策略
        sleep_time = min((2 ** retries) + random.random(), 8 + random.random())
        logger.info(f"[ID {self.log_id}] {self.agent_name} Waiting for {sleep_time} seconds before retrying...")
        time.sleep(sleep_time)

    logger.error(f"[ID {self.log_id}] {self.agent_name} Can not get llm response after try {max_retries} times!")
    return f'[ID {self.log_id}] {self.agent_name} Can not get llm response after try {max_retries} times!'

# for config's auto check
vision_model_names = [
  'gpt-4o', 'gpt-4o-all', 'gpt-4o-mini',
]
video_model_names = [

]

FACTORY = {
  'default': GptClient,
  'gpt-3.5-turbo': GptClient,

  'gpt-4o': GptClient,
  'gpt-4o-all': GptClient,
  'gpt-4o-mini': GptClient,

  'deepseek-v3': GptClient,
  'deepseek-r1': GptClient,
}

if __name__ == "__main__":
  from llm_pysc2.cfg.config import ProtossAgentConfig
  config = ProtossAgentConfig()
  model_name = 'gpt-3.5-turbo'
  api_base = 'https://api.xty.app/v1'
  api_key = ''
  config.reset_llm(model_name, api_base, api_key)
  c = GptClient('CombatGroup0', 0, config)
  response = c.query('hello')
  print(response)