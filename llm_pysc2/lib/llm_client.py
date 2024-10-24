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

# import google.generativeai as genai
from llamaapi import LlamaAPI
from zhipuai import ZhipuAI
import openai

from loguru import logger
import threading
import random
import time
# import json


def gpt_query_runtime(self, ):
  llm_response = openai.ChatCompletion.create(
    model=self.model_name,
    messages=self.messages,
    temperature=self.temperature
  )
  self.query_token_in = llm_response["usage"]["prompt_tokens"]
  self.query_token_out = llm_response["usage"]["completion_tokens"]
  self.llm_response = llm_response["choices"][0]["message"]["content"]

def claude_query_runtime(self, ):
  llm_response = openai.ChatCompletion.create(
    model=self.model_name,
    messages=self.messages,
    temperature=self.temperature
  )
  self.query_token_in = llm_response.usage.prompt_tokens
  self.query_token_out = llm_response.usage.completion_tokens
  self.llm_response = llm_response.choices[0].message.content

def llama_query_runtime(self, ):
  llm_response = self.client.run({
    'model': self.model_name,
    'messages': self.messages,
    'temperature': self.temperature,}
  ).json()
  self.query_token_in = llm_response["usage"]["prompt_tokens"] if 'usage' in llm_response.keys() else 0
  self.query_token_out = llm_response["usage"]["completion_tokens"] if 'usage' in llm_response.keys() else 0
  self.llm_response = llm_response['choices'][0]["message"]["content"]

def glm_query_runtime(self, ):
  llm_response = self.client.chat.completions.create(
    model=self.model_name,  # 填写需要调用的模型名称
    messages=self.messages,
    temperature=self.temperature
  )
  self.query_token_in = 0
  self.query_token_out = 0
  self.llm_response = llm_response.choices[0].message.content

def glm4v_query_runtime(self, ):
  llm_response = self.client.chat.completions.create(
    model=self.model_name,  # 填写需要调用的模型名称
    messages=self.messages,
    temperature=self.temperature
  )
  self.query_token_in = llm_response.usage.prompt_tokens
  self.query_token_out = llm_response.usage.completion_tokens
  self.llm_response = llm_response.choices[0].message.content

# def gemini_query_runtime(self, ):
#   self.llm_response = self.model.generate_content(
#     messages=self.messages, generation_config=genai.types.GenerationConfig(temperature=self.temperature)).text

# def qwen2_query_runtime(self, ):
#   llm_response = openai.ChatCompletion.create(
#     model=self.model_name,  # 填写需要调用的模型名称
#     messages=self.messages,
#     temperature=self.temperature
#   )
#   self.query_token_in = llm_response.usage.prompt_tokens
#   self.query_token_out = llm_response.usage.completion_tokens
#   self.llm_response = llm_response.choices[0].message.content

class GptClient:

  def __init__(self, name, log_id, config):

    self.model_name = config.AGENTS[name]['llm']['model_name']
    self.api_base = config.AGENTS[name]['llm']['api_base']
    self.api_key = config.AGENTS[name]['llm']['api_key']
    self.temperature = config.temperature

    openai.api_base = self.api_base
    openai.api_key = self.api_key

    self.agent_name = name
    self.log_id = log_id
    self.config = config
    self.system_prompt = ''
    self.example_i_prompt = ''
    self.example_o_prompt = ''
    self.messages = []
    self.llm_response = None
    self.query_runtime = gpt_query_runtime
    if 'gpt' in self.model_name or self.model_name == 'default':
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

  def wrap_message(self, obs_prompt, base64_image):

    if (base64_image is not None) and (self.model_name not in vision_model_names):
      logger.warning(f"[ID {self.log_id}] {self.agent_name} {self.model_name}: Model do not accept img, img discarded")
    if (base64_image is None) and (self.model_name in vision_model_names):
      logger.warning(f"[ID {self.log_id}] {self.agent_name} {self.model_name}: Vision available but img disabled")

    if (base64_image is None) or (self.model_name not in vision_model_names):
      # 不包含图像的消息
      self.messages = [
        {"role": "system", "content": self.system_prompt},
        {"role": "user", "content": self.example_i_prompt},
        {"role": "assistant", "content": self.example_o_prompt},
        {"role": "user", "content": obs_prompt}
      ]
    else:
      # 包含图像的消息，按照指定格式
      self.messages = [
        {"role": "system", "content": self.system_prompt},
        {"role": "user", "content": self.example_i_prompt},
        {"role": "assistant", "content": self.example_o_prompt},
        # TODO: Incorrect img usage, to be update in recent commit
        {"role": "user", "content": [
          {"type": "text", "text": obs_prompt},   # obs_prompt
          {"type": "image_url", "image_url": {
            "url": f"data:image/png;base64,{base64_image}"
          }}
        ]},
      ]

  def query(self, obs_prompt, base64_image=None):

    # 重置 messages 列表
    self.wrap_message(obs_prompt, base64_image)

    # 尝试发送请求并获取回复
    max_retries = self.config.MAX_LLM_QUERY_TIMES
    for retries in range(max_retries):
      try:
        # tracemalloc.start()
        logger.success(f"[ID {self.log_id}] {self.agent_name} Start calling llm api!")
        logger.debug(f"[ID {self.log_id}] {self.agent_name} input prompt: \n{obs_prompt}")

        self.thread = threading.Thread(target=self.query_runtime, args=(self,))#保留“，”
        self.thread.start()

        # 超时错误
        query_start_time = float(time.time())
        while not isinstance(self.llm_response, str):
          time.sleep(0.1)
          if float(time.time()) - query_start_time > self.config.MAX_LLM_RUNTIME_ERROR_TIME:
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

class O1Client(GptClient):
  def __init__(self, name, log_id, config):
    super(O1Client, self).__init__(name, log_id, config)
    self.query_runtime = gpt_query_runtime
    self.temperature = 1  # Only the default (1) value is supported.
    self.client = openai
    logger.info(f"[ID {self.log_id}] {self.agent_name} {self.model_name} O1Client initialized")

  def wrap_message(self, obs_prompt, base64_image):
    super().wrap_message(obs_prompt, base64_image)
    # 不包含图像的消息
    self.messages = [
      {"role": "user", "content": self.system_prompt},
      {"role": "assistant", "content": "Understand."},
      {"role": "user", "content": self.example_i_prompt},
      {"role": "assistant", "content": self.example_o_prompt},
      {"role": "user", "content": obs_prompt}
    ]


class ClaudeClient(GptClient):
  def __init__(self, name, log_id, config):
    super(ClaudeClient, self).__init__(name, log_id, config)
    self.query_runtime = claude_query_runtime
    self.client = openai
    logger.info(f"[ID {self.log_id}] {self.agent_name} {self.model_name} ClaudeClient initialized")

class LlamaClient(GptClient):
  def __init__(self, name, log_id, config):
    super(LlamaClient, self).__init__(name, log_id, config)
    self.query_runtime = llama_query_runtime
    self.client = LlamaAPI(self.api_key, hostname=self.api_base)
    logger.info(f"[ID {self.log_id}] {self.agent_name} {self.model_name} LlamaClient initialized")

class GlmClient(GptClient):
  def __init__(self, name, log_id, config):
    super(GlmClient, self).__init__(name, log_id, config)
    self.query_runtime = glm_query_runtime
    self.client = ZhipuAI(api_key=self.api_key)
    logger.info(f"[ID {self.log_id}] {self.agent_name} {self.model_name} GlmClient initialized")

# class GeminiClient(GptClient):
#   def __init__(self, name, log_id, config):
#     super(GeminiClient).__init__(self, name, log_id, config)
#     self.query_runtime = gemini_query_runtime
#     self.model = genai.GenerativeModel(config.model_name)

# class QWen2Client(GptClient):
#   def __init__(self, name, log_id, config):
#     super(QWen2Client, self).__init__(name, log_id, config)
#     self.query_runtime = qwen2_query_runtime
#     self.client = openai

# for config's auto check
vision_model_names = [
  'gpt-4o', 'gpt-4-1106-vision-preview', 'gpt-4v-1106', 'gpt-4v-0409',
  'glm-4v', 'glm-4v-plus'
]
video_model_names = []

FACTORY = {
  'default': GptClient,
  'gpt-3.5-turbo': GptClient,
  'gpt-3.5-turbo-1106': GptClient,

  'gpt-4o': GptClient,
  'gpt-4o-mini': GptClient,
  'gpt-4-turbo': GptClient,

  # 'gpt-4-1106-vision-preview': GptClient,
  # 'gpt-4v-1106': GptClient,
  # 'gpt-4v-0409': GptClient,

  'o1-mini': O1Client,
  'o1-preview': O1Client,

  'claude-3-opus': ClaudeClient,
  'claude-3-haiku': ClaudeClient,
  'claude-3-sonnet': ClaudeClient,

  'llama3-8b': LlamaClient,
  'llama3-70b': LlamaClient,
  'llama3.1-8b': LlamaClient,
  'llama3.1-70b': LlamaClient,
  'llama3.1-405b': LlamaClient,

  'glm-4': GlmClient,
  'glm-4-plus': GlmClient,
  'glm-4-air': GlmClient,
  'glm-4-airx': GlmClient,
  'glm-4-flash': GlmClient,
  'glm-4-flashx': GlmClient,

  # 'glm-4v': GlmClient,
  # 'glm-4v-plus': GlmClient,

  # 'qwen2.5-7b-instruct': QWen2Client,
  # 'qwen2:72b': QWen2Client,  # debug for LAN LLM
  # 'gemini': GeminiClient,
}
