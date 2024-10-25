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

# 通讯格式
#  Communication:
#   <MessageTo(AgentName, '''xxxxxxxxxx''')>
#   <MessageTo(ChannelName, '''xxxxxxxxxx''')>
#   <ListenTo(ChannelName)>


from loguru import logger


def communication_info_transmission(self: "llm_pysc2 MainAgent"):

  if self.config.ENABLE_COMMUNICATION:
    for receiver_name in self.AGENT_NAMES:
      receiver_agent = self.agents[receiver_name]
      receiver_agent.last_text_c_inp = ''
      receiver_agent.last_text_c_tar = ''

      # communication data transmission
      for sender_name in self.AGENT_NAMES:
        sender_agent = self.agents[sender_name]
        cmo = sender_agent.communication_message_o
        cmi = receiver_agent.communication_message_i
        receiver_agent.communication_message_i = receiver_agent.communicator.receive(cmi, cmo, receiver_name, sender_name)

      # Generate text communication info
      # if len(receiver_agent.communication_message_i.keys()) > 0:
      for sender_name in receiver_agent.communication_message_i.keys():
        info_sender_name = f"\n\tIn {sender_name}" if 'Channel' in sender_name else f"\n\tFrom {sender_name}"
        received_message = f"{receiver_agent.communication_message_i[sender_name]}"
        receiver_agent.last_text_c_inp += f"{info_sender_name}: {received_message}"
      if len(receiver_agent.last_text_c_inp) != 0:
        receiver_agent.last_text_c_inp = f"\n\nCommunication information:" + receiver_agent.last_text_c_inp

      # Generate Communication Target
      receiver_agent.last_text_c_tar = "\n\nAvailable Communication Targets:"
      for agent_name in self.AGENT_NAMES:
        agent = self.agents[agent_name]
        if agent_name != receiver_name and agent.enable:
          description = agent.config.AGENTS[agent_name]['describe'] if agent_name in agent.config.AGENTS.keys() else ''
          receiver_agent.last_text_c_tar += f"\n\t{agent_name}: {description}"

      # Generate Communication Rules
      receiver_agent.last_text_c_tar += "\nAvailable Communication Functions:"
      receiver_agent.last_text_c_tar += "\n\t<MessageTo(AgentName, message)>"
      receiver_agent.last_text_c_tar += "\n\t<MessageTo(ChannelName, message)>"
      receiver_agent.last_text_c_tar += "\n\t<ListenTo(ChannelName)>"
      receiver_agent.last_text_c_tar += "\nArgs explanation:"
      receiver_agent.last_text_c_tar += "\n\t(1)AgentName: refers to a name mentioned in Available Communication Targets."
      receiver_agent.last_text_c_tar += "\n\t(2)ChannelName: shape as Channel-i, i refers to an integer."
      receiver_agent.last_text_c_tar += "\n\t(2)message: any text wrapped between ''' and '''."

      logger.debug(f"[ID {self.log_id}] 7.0 LLMAgent {receiver_name} get communication message: ")
      logger.debug(f"[ID {self.log_id}]     LLMAgent communication_message_i: {receiver_agent.communication_message_i}")
      logger.debug(f"[ID {self.log_id}]     LLMAgent received message: {receiver_agent.last_text_c_tar}")
    logger.success(f"[ID {self.log_id}] 7.0 All LLMAgent get communication message")
  else:
    logger.success(f"[ID {self.log_id}] 7.0 All LLMAgent skip communication stage")


class DefaultCommunicator():
  def __init__(self, name, log_id, config):
    self.agent_name = name
    self.log_id = log_id
    self.config = config
    logger.info(f"[ID {self.log_id}] {self.agent_name} DefaultCommunicator initialized")

  def receive(self, cmi: dict, cmo: dict, agent_name_receiver: str, agent_name_sender: str):
    for key in cmo.keys():
      if key == agent_name_receiver:  # message send to me
        cmi[agent_name_sender] = f"\n\t\t" + cmo[agent_name_receiver]
      if key in cmi.keys() and 'Channel' in key:  # message send to the channel currently listened to
        cmi[key] += f"\n\t\tFrom {agent_name_sender}: {cmo[key]}"
    return cmi

  def send(self, raw_text_a: str) -> (dict, dict, str):
    cmi, cmo, processed_text_c = {}, {}, ''

    lines = raw_text_a.splitlines()
    start_recognize = False
    for line in lines:
      if ("Communications:" in line) or ("Communication:" in line) or \
          ("communications:" in line) or ("Communication:" in line):
        processed_text_c += line
        start_recognize = True
      if ("Actions:" in line) or ("Action:" in line) or \
          ("actions:" in line) or ("action:" in line):
        start_recognize = False
      if start_recognize:
        if "<" in line and ">" in line and "(" in line and ")" in line:
          action_text = line.split("<")[1].split(">")[0]
          action_name = action_text.split("(")[0]
          action_args = action_text.split("(")[1].split(")")[0]
          if action_name == 'ListenTo':
            message_receiver = action_args
            if "Channel" in message_receiver:
              cmi[action_args] = ''
              processed_text_c +=  "\n" + line
          elif action_name == 'MessageTo':
            if "'''" in line and len(action_args.split("'''")) == 3:
              message_text = action_args.split("'''")[1]
              message_receiver = action_args.split("'''")[0].split(",")[0]
              cmo[message_receiver] = message_text
              processed_text_c += "\n" + line
          else:
            pass

    return cmi, cmo, processed_text_c


PROTOSS_FACTORY = {'default': DefaultCommunicator}
TERRAN_FACTORY = {}
ZERG_FACTORY = {}

FACTORY = {
  'protoss': PROTOSS_FACTORY,
  'terran': TERRAN_FACTORY,
  'zerg': ZERG_FACTORY,
}


if __name__ == "__main__":
  from llm_pysc2.agents.configs.config import ProtossAgentConfig
  config = ProtossAgentConfig()
  communicator = DefaultCommunicator('AgentName', log_id=0, config=config)

  # send message from CombatGroup0
  text0 = \
"""
Communications:
    <MessageTo(Commander, '''We are xxxxxxx, we need xxxxx, we plan to do xxxxx''')>
    <MessageTo(Channel-1, '''We are yyyyyyy, we need yyyyy, we plan to do yyyyy''')>
    <ListenTo(Channel-1)>
"""
  cmi0, cmo0, processed_text_c0 = communicator.send(text0)
  print("CombatGroup0 send info: \n", processed_text_c0)
  print("CombatGroup0 send info recognized: ", cmo0)
  print("--" * 25)

  # send message from CombatGroup1
  text1 = \
"""
Communications:
    <MessageTo(Developer, '''We are aaaaaaa, we need aaaaa, we plan to do aaaaa''')>
    <MessageTo(Channel-1, '''We are bbbbbbb, we need bbbbb, we plan to do bbbbb''')>
    <ListenTo(Channel-1)>
"""
  cmi1, cmo1, processed_text_c1 = communicator.send(text1)
  print("CombatGroup1 send info: \n", processed_text_c1)
  print("CombatGroup1 send info recognized: ", cmo1)
  print("--" * 25)

  # CombatGroup3 receive message
  cmi = {"Channel-1": ''}
  print("CombatGroup3 listen to: ", cmi)
  cmi = communicator.receive(cmi, cmo0, 'CombatGroup3', 'CombatGroup0')
  cmi = communicator.receive(cmi, cmo1, 'CombatGroup3', 'CombatGroup1')
  print("CombatGroup3 received: ", cmi)
  last_text_c_inp = f"Communication:"
  for message_sender in cmi.keys():
    if 'Channel' not in message_sender:
      last_text_c_inp += f"\n\tFrom {message_sender}: {cmi[message_sender]}"
    else:
      last_text_c_inp += f"\n\tIn {message_sender}: {cmi[message_sender]}"
  print(last_text_c_inp)
  print("--" * 25)

  # Developer receive message
  cmi = {}
  print("Developer listen to: ", cmi)
  cmi = communicator.receive(cmi, cmo0, 'Developer', 'CombatGroup0')
  cmi = communicator.receive(cmi, cmo1, 'Developer', 'CombatGroup1')
  print("Developer received: ", cmi)
  last_text_c_inp = f"Communication:"
  for message_sender in cmi.keys():
    if 'Channel' not in message_sender:
      last_text_c_inp += f"\n\tFrom {message_sender}: {cmi[message_sender]}"
    else:
      last_text_c_inp += f"\n\tIn {message_sender}: {cmi[message_sender]}"
  print(last_text_c_inp)
  print("--" * 25)
