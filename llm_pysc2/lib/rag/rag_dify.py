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

# Thanks https://zhuanlan.zhihu.com/p/682543197


import requests
import os


# View Knowledge Base List
# https://docs.dify.ai/zh-hans/guides/knowledge-base/maintain-dataset-via-api#zhi-shi-ku-lie-biao
def dify_dataset_list(api_base, api_key, dataset_id=None, **kwargs):
  url = f"{api_base}/datasets?page=1&limit=20"
  headers = {'Authorization': f'Bearer {api_key}'}
  response = requests.get(url, headers=headers)
  return response


# View Knowledge Base Documents List
def dify_document_list(api_base, api_key, dataset_id, **kwargs):
  url = f"{api_base}/datasets/{dataset_id}/documents"
  headers = {'Authorization': f'Bearer {api_key}'}
  response = requests.get(url, headers=headers)
  return response


# TODO: GET/datasets/{dataset_id}/documents/{batch}/indexing-status
def dify_batch_indexing_status(api_base, api_key, dataset_id, **kwargs):
  pass


# Create a Document from Text
# https://docs.dify.ai/zh-hans/guides/knowledge-base/maintain-dataset-via-api#tong-guo-wen-ben-chuang-jian-wen-dang
def dify_document_create_by_text(api_base, api_key, dataset_id, **kwargs):
  name = str(kwargs.get('name', 'default_document'))
  text = str(kwargs.get('text', 'default_text'))
  url = f"{api_base}/datasets/{dataset_id}/document/create_by_text"
  headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
  data = {
    "name": name,
    "text": text,
    "indexing_technique": "high_quality",
    "process_rule": {
      "mode": "automatic",
    }
  }
  response = requests.post(url, headers=headers, json=data)
  return response


# Create documents from a File
# https://docs.dify.ai/guides/knowledge-base/maintain-dataset-via-api#create-documents-from-a-file
def dify_document_create_by_file(api_base, api_key, dataset_id, **kwargs):
  path = str(kwargs.get('path', 'None'))
  if not os.path.isfile(path):
    raise FileExistsError(f"{path} is not a file path")
  url = f"{api_base}/datasets/{dataset_id}/document/create_by_file"
  headers = {'Authorization': f'Bearer {api_key}'}
  form_data = {
    'data': (
      None,
      '{"indexing_technique":"high_quality","process_rule":{"rules":{"pre_processing_rules":[{"id":"remove_extra_spaces","enabled":true},{"id":"remove_urls_emails","enabled":true}],"segmentation":{"separator":"Now, start generating your analysis and actions:","max_tokens":4000}},"mode":"custom"}}',
      'text/plain'
    )
  }
  files = {'file': (os.path.basename(path), open(path, 'rb'), 'application/octet-stream')}
  response = requests.post(url, headers=headers, data=form_data, files=files)
  files['file'][1].close()

  return response


# Update documents from a text
# https://docs.dify.ai/guides/knowledge-base/maintain-dataset-via-api#update-a-chunk-in-a-document
def dify_document_update_by_text(api_base, api_key, dataset_id, **kwargs):
  name = str(kwargs.get('name', 'None'))
  text = str(kwargs.get('text', 'None'))
  document_id = str(kwargs.get('document_id', 'None'))
  if name == 'None':
    raise AssertionError(f"name needed")
  if text == 'None':
    raise AssertionError(f"text needed")
  if document_id == 'None':
    raise AssertionError(f"document_id needed")
  url = f"{api_base}/datasets/{dataset_id}/documents/{document_id}/update-by-text"
  headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
  data = {
    "name": name,
    "text": text,
    "indexing_technique": "high_quality",
    "process_rule": {
      "mode": "automatic"
    }
  }
  response = requests.post(url, headers=headers, json=data)
  return response


# Update documents from a file
def dify_document_update_by_file(api_base, api_key, dataset_id, **kwargs):
  path = str(kwargs.get('path', 'None'))
  document_id = str(kwargs.get('document_id', 'None'))
  if not os.path.isfile(path):
    raise FileExistsError(f"{path} is not a file path")
  if document_id == 'None':
    raise AssertionError(f"document_id needed")
  url = f"{api_base}/datasets/{dataset_id}/documents/{document_id}/update-by-file"
  headers = {'Authorization': f'Bearer {api_key}'}
  form_data = {
    'data': (
      None,
      '{"indexing_technique":"high_quality","process_rule":{"rules":{"pre_processing_rules":[{"id":"remove_extra_spaces","enabled":true},{"id":"remove_urls_emails","enabled":true}],"segmentation":{"separator":"Now, start generating your analysis and actions:","max_tokens":998}},"mode":"custom"}}',
      'text/plain'
    )
  }
  files = {'file': (os.path.basename(path), open(path, 'rb'), 'application/octet-stream')}
  response = requests.post(url, headers=headers, data=form_data, files=files)
  files['file'][1].close()

  return response


# Delete Document
def dify_document_delete(api_base, api_key, dataset_id, **kwargs):
  document_id = str(kwargs.get('document_id', 'None'))
  if document_id == 'None':
    raise AssertionError(f"document_id needed")
  url = f"{api_base}/datasets/{dataset_id}/documents/{document_id}"
  headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
  response = requests.delete(url, headers=headers)
  return response


# Create a segments
def dify_segment_create_by_text(api_base, api_key, dataset_id, **kwargs):
  text = str(kwargs.get('text', 'None'))
  document_id = str(kwargs.get('document_id', 'None'))
  if text == 'None':
    raise AssertionError(f"text needed")
  if document_id == 'None':
    raise AssertionError(f"document_id needed")
  url = f"{api_base}/datasets/{dataset_id}/documents/{document_id}/segments"
  headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
  data = {"segments": [
      {
        "content": text,
        # "answer": "1",  # Q/A mode
        # "keywords": ["a"]  # optional
      }
    ]
  }
  response = requests.post(url, headers=headers, json=data)
  return response


# Update a segments
def dify_segment_update_by_text(api_base, api_key, dataset_id, **kwargs):
  text = str(kwargs.get('text', 'None'))
  document_id = str(kwargs.get('document_id', 'None'))
  segment_id = str(kwargs.get('segment_id', 'None'))
  if text == 'None':
    raise AssertionError(f"text needed")
  if document_id == 'None':
    raise AssertionError(f"document_id needed")
  if segment_id == 'None':
    raise AssertionError(f"segment_id needed")
  url = f"{api_base}/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}"
  headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
  data = {
    "segment": {
      "content": text,
      # "answer": "1",
      # "keywords": ["a"],
      # "enabled": False
    }
  }
  response = requests.post(url, headers=headers, json=data)
  return response


# Create a segments QA
def dify_segment_qa_create_by_text(api_base, api_key, dataset_id, **kwargs):
  text_q = str(kwargs.get('text_q', 'None'))
  text_a = str(kwargs.get('text_a', 'None'))
  document_id = str(kwargs.get('document_id', 'None'))
  if text_q == 'None':
    raise AssertionError(f"text_q needed")
  if text_a == 'None':
    raise AssertionError(f"text_a needed")
  if document_id == 'None':
    raise AssertionError(f"document_id needed")
  url = f"{api_base}/datasets/{dataset_id}/documents/{document_id}/segments"
  headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
  data = {"segments": [
      {
        "content": text_q,
        "answer": text_a,
        # "keywords": ["a"]  # optional
      }
    ]
  }
  response = requests.post(url, headers=headers, json=data)
  return response


# Update a segments QA
def dify_segment_qa_update_by_text(api_base, api_key, dataset_id, **kwargs):
  text_q = str(kwargs.get('text_q', 'None'))
  text_a = str(kwargs.get('text_a', 'None'))
  document_id = str(kwargs.get('document_id', 'None'))
  segment_id = str(kwargs.get('segment_id', 'None'))
  if text_q == 'None':
    raise AssertionError(f"text_q needed")
  if text_a == 'None':
    raise AssertionError(f"text_a needed")
  if document_id == 'None':
    raise AssertionError(f"document_id needed")
  if segment_id == 'None':
    raise AssertionError(f"segment_id needed")
  url = f"{api_base}/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}"
  headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
  data = {
    "segment": {
      "content": text_q,
      "answer": text_a,
      # "keywords": ["a"],
      # "enabled": False
    }
  }
  response = requests.post(url, headers=headers, json=data)
  return response


# Delete Segment
def dify_segment_delete(api_base, api_key, dataset_id, **kwargs):
  document_id = str(kwargs.get('document_id', 'None'))
  segment_id = str(kwargs.get('segment_id', 'None'))
  if document_id == 'None':
    raise AssertionError(f"document_id needed")
  if segment_id == 'None':
    raise AssertionError(f"segment_id needed")
  url = f"{api_base}/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}"
  headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
  response = requests.delete(url, headers=headers)
  return response

# Retrieve
def dify_retrieve(api_base, api_key, dataset_id, **kwargs):
  query = kwargs.get('query', 'None')
  top_k = int(kwargs.get('top_k', 1))
  # if not isinstance(query, str):
  #   query = str(query)
  if query == 'None':
    raise AssertionError(f"query needed")
  url = f"{api_base}/datasets/{dataset_id}/retrieve"
  headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
  data = {
    # "state": state,
    "query": query,
    "retrieval_model": {
        "search_method": "hybrid_search",  # always needed
        "reranking_enable": False,
        # "reranking_mode": None,
        # "reranking_model": {
        #     "reranking_provider_name": "",
        #     "reranking_model_name": ""
        # },
        "weights": 0.5,
        "top_k": top_k,
        "score_threshold_enabled": False,
        "score_threshold": None
    }
  }
  response = requests.post(url, headers=headers, json=data)
  return response


if __name__ == "__main__":

  from pprint import pprint
  api_base = 'http://127.0.0.1/v1'  # 'http://127.0.0.1/v1' for local
  api_key = 'YOUR-DIFY-API-KEY'
  dataset_id = 'YOUR-DIFY-DATASET-ID'
  document_id = 'YOUR-DIFY-DOCUMENT-ID'
  segment_id = 'YOUR-DIFY-SEGMENT-ID'
  example_file_path = f"{os.path.dirname(os.path.abspath(__file__))}/../../docs/rag/empty.txt"

  # View Knowledge Base List
  print('--' * 50 + f"\nCall dify_dataset_list()")
  response = dify_dataset_list(api_base, api_key)
  pprint(response.json())
  print(type(response.json()))

  # View Knowledge Base Documents List
  # dataset_id = '69a3140c-e1a8-46a7-bda3-716385f0b749'
  # print('--' * 50 + f"\nCall dify_dataset_document_list()")
  # response = dify_document_list(api_base, api_key, dataset_id)
  # pprint(response.json())

  # print('--' * 50 + f"\nCall dify_dataset_document_list()")
  # response = dify_batch_indexing_status(api_base, api_key, dataset_id)
  # pprint(response.json())

  # # Create a Document from Text
  # print('--' * 50 + f"\nCall dify_document_create_by_text()")
  # kwargs = {'name': 'user input document name', 'text': 'user input text'}
  # response = dify_document_create_by_text(api_base, api_key, dataset_id, **kwargs)
  # pprint(response.json())

  # # Create a Document from File
  # print('--' * 50 + f"\nCall dify_document_create_by_file()")
  # kwargs = {'path': example_file_path}
  # response = dify_document_create_by_file(api_base, api_key, dataset_id, **kwargs)
  # pprint(response.json())

  # # Update a Document from Text
  # print('--' * 50 + f"\nCall dify_document_update_by_text()")
  # kwargs = {'name': 'user updated document name', 'text': 'user updated text', 'document_id': f'{document_id}'}
  # response = dify_document_update_by_text(api_base, api_key, dataset_id, **kwargs)
  # pprint(response.json())

  # # Update a Document from File
  # print('--' * 50 + f"\nCall dify_document_update_by_file()")
  # kwargs = {'path': example_file_path, 'document_id': f'{document_id}'}
  # response = dify_document_update_by_file(api_base, api_key, dataset_id, **kwargs)
  # pprint(response.json())

  # # Create a Segment from Text
  # print('--' * 50 + f"\nCall dify_segment_create_by_text()")
  # kwargs = {'text': 'user created segment', 'document_id': f'{document_id}'}
  # response = dify_segment_create_by_text(api_base, api_key, dataset_id, **kwargs)
  # pprint(response.json())

  # # Update a Segment from Text
  # print('--' * 50 + f"\nCall dify_segment_update_by_text()")
  # kwargs = {'text': 'user updated segment', 'document_id': f'{document_id}', 'segment_id': f'{segment_id}'}
  # response = dify_segment_update_by_text(api_base, api_key, dataset_id, **kwargs)
  # pprint(response.json())

  # # Delete Document
  # print('--' * 50 + f"\nCall dify_document_delete()")
  # kwargs = {'document_id': f'{document_id}'}
  # response = dify_document_delete(api_base, api_key, dataset_id, **kwargs)
  # pprint(response.json())

  # # Delete Segment
  # print('--' * 50 + f"\nCall dify_segment_delete()")
  # kwargs = {'document_id': f'{document_id}', 'segment_id': f'{segment_id}'}
  # response = dify_segment_delete(api_base, api_key, dataset_id, **kwargs)
  # pprint(response.json())

  # Retrieve
  # print('--' * 50 + f"\nCall dify_retrieve()")
  # query = """
  # Here is a StarCraft-2 game state:
  #
  # Team Adept-1 Info:
	# Team minimap position: [50, 26]
	# Controlled Team Units:
	# 	Unit: Adept    Tag: 0x100240001    ScreenPos: [64, 60]    Health: 14(10 %)    Weapon Ready
	# Nearby Ally Units:
	# 	Unit: AdeptPhaseShift    Tag: 0x1015c0006    ScreenPos: [72, 104]    Health: 140
	# Nearby Enemy Units:
	# 	Unit: Drone    Tag: 0x1012c0001    ScreenPos: [49, 71]    Distance: 3    Health: 40(100 %)
	# 	Unit: Drone    Tag: 0x101440001    ScreenPos: [47, 83]    Distance: 5    Health: 40(100 %)    Buff: Buffs.CarryMineralFieldMinerals
	# 	Unit: Drone    Tag: 0x1011c0001    ScreenPos: [49, 93]    Distance: 7    Health: 40(100 %)    Buff: Buffs.CarryMineralFieldMinerals
	# 	Unit: Hatchery    Tag: 0x1010c0001    ScreenPos: [29, 98]    Distance: 10    Health: 1500(100 %)    Buff: Buffs.QueenSpawnLarvaTimer
	# 	Unit: Queen    Tag: 0x100540001    ScreenPos: [33, 76]    Distance: 6    Health: 175(100 %)    Energy: 126
	# 	Unit: Queen    Tag: 0x100200001    ScreenPos: [39, 84]    Distance: 6    Health: 166(94 %)    Energy: 184
	#
  # retrieve the most similar state from the database and print it out:
  # """
  # kwargs = {'query': query}
  # response = dify_retrieve(api_base, api_key, dataset_id, **kwargs)
  # pprint(response.json(), width=200)





#   test_data_to_dify = True
#   # test_data_to_dify = False
#   if test_data_to_dify:
#
#     # test: data to dify
#     text_sars = {"s": "Team Adept-1 Info:\n\tTeam minimap position: [21, 31]\n\tControlled Team Units:\n\t\tUnit: Adept    Tag: 0x100240001    ScreenPos: [64, 61]    Health: 140(100 %)    Weapon Ready\n\t\tUnit: Adept    Tag: 0x100500001    ScreenPos: [64, 66]    Health: 140(100 %)    Weapon Ready\n\tNearby Ally Units:\n\t\tUnit: Nexus    Tag: 0x100d80001    ScreenPos: [24, 61]    Health: 2000(100 %)    Energy: 51\nValid Actions:\n\tTeam Adept-1 Valid Actions:\n\t\t<Stop()>\n\t\t<No_Operation()>\n\t\t<Hold_Position()>\n\t\t<Move_Minimap(minimap)>\n\t\t<Move_Screen(screen)>\n\t\t<Attack_Unit(tag)>\n\t\t<Ability_AdeptPhaseShift_Screen(screen)>\n\t\t<Ability_AdeptPhaseShift_Minimap(minimap)>\n\nTasks:\n\tTeam Adept-1' task: Go to minimap coordinate [52, 32], and try to avoid been detected or attacked before arrival.\n\n", "a": "### Analysis:  Team Adept-1 is tasked with moving to minimap coordinate [52, 32] while avoiding detection or being attacked. The team has two Adepts with full health and ready weapons. Since they are near the Nexus, they are likely in a safe position for now, but they need to move quickly without drawing attention. The Adept's ability, *Psionic Transfer*, allows for rapid movement and can help in case of danger, as the phase shift will temporarily make them invulnerable and reposition them.\n\nActions:\n\tTeam Adept-1:\n\t\t<Ability_AdeptPhaseShift_Minimap([52, 32])>\n\t\t<Move_Minimap([52, 32])>\n\t\t<Move_Minimap([52, 32])>", "r": "**Reflections:**\n  1. The actions **<Ability_AdeptPhaseShift_Minimap([52, 32])>** and **<Move_Minimap([52, 32])>** are valid according to the 'Valid Actions' listed for **Team Adept-1** in s_t1. The ability and movement actions match the expected formats.\n  2. The analysis provided for **Team Adept-1** seems correct: the task is to reach the minimap coordinate [52, 32] while avoiding detection or being attacked. The action to use the **AdeptPhaseShift** ability to minimize detection risk is well-placed, though the inclusion of two **Move_Minimap([52, 32])** actions is redundant since the team can only move once per command. It\u2019s also unclear why both movement actions are issued when the Phase Shift ability should be prioritized first for safety.\n  3. While the decision to use **<Ability_AdeptPhaseShift_Minimap([52, 32])>** is appropriate to avoid detection and potential attack, issuing **<Move_Minimap([52, 32])>** right after it is redundant, as the team would already be using the phase shift to avoid direct threats. The second **Move_Minimap([52, 32])** would likely result in wasted resources or uncoordinated movement.\n\n**Suggestions:**\n  This is a **partially good** decision, but with redundancy. We should **remove the second Move_Minimap([52, 32])** and focus on the **<Ability_AdeptPhaseShift_Minimap([52, 32])>** action to safely reposition the team and avoid detection, only following up with **<Move_Minimap([52, 32])>** if additional movement is required after the phase shift. This would streamline the strategy and avoid unnecessary actions.", "s_": "Team Adept-1 Info:\n\tTeam minimap position: [21, 31]\n\tControlled Team Units:\n\t\tUnit: Adept    Tag: 0x100500001    ScreenPos: [83, 67]    Health: 140(100 %)    Weapon Ready\n\t\tUnit: Adept    Tag: 0x100240001    ScreenPos: [83, 62]    Health: 140(100 %)    Weapon Ready\n\tNearby Ally Units:\n\t\tUnit: AdeptPhaseShift    Tag: 0x101500001    ScreenPos: [96, 63]    Health: 140\n\t\tUnit: AdeptPhaseShift    Tag: 0x101540001    ScreenPos: [95, 68]    Health: 140\n\t\tUnit: Nexus    Tag: 0x100d80001    ScreenPos: [24, 61]    Health: 2000(100 %)    Energy: 52\n\t\tUnit: Probe    Tag: 0x100f80001    ScreenPos: [1, 88]    Health: 40(100 %)\nTeam AdeptPhase-1 Info:\n\tTeam minimap position: [25, 31]\n\tControlled Team Units:\n\t\tUnit: AdeptPhaseShift    Tag: 0x101500001    ScreenPos: [68, 63]    Health: 140\n\t\tUnit: AdeptPhaseShift    Tag: 0x101540001    ScreenPos: [67, 68]    Health: 140\n\tNearby Ally Units:\n\t\tUnit: Adept    Tag: 0x100240001    ScreenPos: [54, 63]    Health: 140(100 %)\n\t\tUnit: Adept    Tag: 0x100500001    ScreenPos: [53, 68]    Health: 140(100 %)\n"}
#     text_sa_t = text_sars['s'] + '\n\n' + text_sars['a']
#     text_r_t = text_sars['r']
#
#     # test: query/answer mode, data to dify
#     query = \
# """
# Team Stalker-1 Info:
# 	Team minimap position: [32, 30]
# 	Team screen edge (screen coordinate range valid for actions): 0 < x < 255, 0 < y < 255
# 	Controlled Team Units:
# 		Unit: Stalker    Tag: 0x100000001    ScreenPos: [124, 114]    Health: 160(100 %)    Weapon Cooldown Time: 0.86s
# 		Unit: Stalker    Tag: 0x100580001    ScreenPos: [131, 138]    Health: 144(90 %)    Weapon Cooldown Time: 0.59s
# 		Unit: Stalker    Tag: 0x100b80001    ScreenPos: [133, 151]    Health: 128(80 %)    Weapon Cooldown Time: 0.64s
# 		Unit: Stalker    Tag: 0x100ac0001    ScreenPos: [130, 125]    Health: 128(80 %)    Weapon Cooldown Time: 0.68s
# 	Nearby Ally Units:
# 		Unit: Stalker    Tag: 0x100740001    ScreenPos: [107, 122]    Health: 160(100 %)
# 		Unit: Stalker    Tag: 0x100140001    ScreenPos: [110, 107]    Health: 160(100 %)
# 		Unit: Stalker    Tag: 0x1001c0001    ScreenPos: [122, 178]    Health: 160(100 %)
# 		Unit: Stalker    Tag: 0x100680001    ScreenPos: [111, 171]    Health: 160(100 %)
# 		Unit: Stalker    Tag: 0x100a80001    ScreenPos: [121, 147]    Health: 160(100 %)
# 		Unit: Stalker    Tag: 0x100540001    ScreenPos: [109, 156]    Health: 160(100 %)
# 		Unit: Stalker    Tag: 0x100940001    ScreenPos: [123, 165]    Health: 160(100 %)
# 		Unit: Stalker    Tag: 0x100480001    ScreenPos: [120, 132]    Health: 160(100 %)
# 	Nearby Enemy Units:
# 		Enemy Unit: Ravager    Tag: 0x100bc0001    ScreenPos: [207, 117]    Distance: 7    Health: 120(100 %)
# 		Enemy Unit: Roach    Tag: 0x1008c0001    ScreenPos: [187, 155]    Distance: 6    Health: 128(88 %)
# 		Enemy Unit: Roach    Tag: 0x1003c0001    ScreenPos: [204, 140]    Distance: 7    Health: 145(100 %)
# 		Enemy Unit: Roach    Tag: 0x100500001    ScreenPos: [205, 155]    Distance: 7    Health: 145(100 %)
# 		Enemy Unit: Roach    Tag: 0x100a40001    ScreenPos: [191, 167]    Distance: 7    Health: 145(100 %)
# 		Enemy Unit: Roach    Tag: 0x100900001    ScreenPos: [184, 135]    Distance: 5    Health: 145(100 %)
# 		Enemy Unit: Roach    Tag: 0x100980001    ScreenPos: [203, 130]    Distance: 7    Health: 145(100 %)
# 		Enemy Unit: Roach    Tag: 0x100a00001    ScreenPos: [186, 145]    Distance: 5    Health: 145(100 %)
# 		Enemy Unit: Roach    Tag: 0x100440001    ScreenPos: [182, 114]    Distance: 5    Health: 145(100 %)
# 		Enemy Unit: Roach    Tag: 0x1009c0001    ScreenPos: [194, 137]    Distance: 6    Health: 77(53 %)
# 		Enemy Unit: Roach    Tag: 0x1006c0001    ScreenPos: [198, 148]    Distance: 7    Health: 145(100 %)
# 		Enemy Unit: Roach    Tag: 0x100380001    ScreenPos: [184, 125]    Distance: 5    Health: 145(100 %)
# 		Enemy Unit: Roach    Tag: 0x100800001    ScreenPos: [196, 159]    Distance: 7    Health: 145(100 %)
# 		Enemy Unit: Roach    Tag: 0x1002c0001    ScreenPos: [184, 103]    Distance: 6    Health: 145(100 %)
# 		Enemy Unit: Roach    Tag: 0x100340001    ScreenPos: [193, 115]    Distance: 6    Health: 145(100 %)
# 		Enemy Unit: Roach    Tag: 0x100280001    ScreenPos: [194, 105]    Distance: 6    Health: 145(100 %)
#
# 	Team Stalker-3 Valid Actions:
# 		<Hold_Position()>
# 		<Move_Minimap(minimap)>
# 		<Move_Screen(screen)>
# 		<Attack_Unit(tag)>
# 		<Ability_Blink_Screen(screen)>
# 		<Select_Unit_Blink_Screen(tag, screen)>
#
# Tasks:
# 	Team Stalker-1' task: Kill as much as enemy units as possible. If no enemy found, hold the position.
# 	Team Stalker-2' task: Kill as much as enemy units as possible. If no enemy found, hold the position.
# 	Team Stalker-3' task: Kill as much as enemy units as possible. If no enemy found, hold the position.
# """
#
#     answer = \
# """
# Hypothesis:
#   It is suggested to continue with the current plan of moving all teams to minimap coordinates [32, 32] while maintaining focus on avoiding combat. Given the absence of threats, it would be best to proceed as planned without engaging in unnecessary actions or distractions.
# """
#     dataset_id = '69a3140c-e1a8-46a7-bda3-716385f0b749'
#     document_id = '57e3f8c5-80f1-4048-ba52-d40e7e7ab247'
#     # kwargs = {'document_id': document_id, 'text_q': text_sa_t, 'text_a': text_r_t}
#     # kwargs = {'document_id': document_id, 'text_q': query, 'text_a': answer}
#     # response = dify_segment_qa_create_by_text(api_base, api_key, dataset_id, **kwargs)
#     # pprint(response.json(), width=200)
#
#     # test: query/answer mode, pure text mode
#     # kwargs = {'document_id': document_id, 'text': text_sa_t + "\n" + text_r_t}
#     # response = dify_segment_create_by_text(api_base, api_key, dataset_id, **kwargs)
#     # pprint(response.json(), width=200)
#
#     text_query = """
# Team Stalker-1 Info:
# 	Team minimap position: [20, 33]
# 	Team screen edge (screen coordinate range valid for actions): 7 < x < 23, 0 < y < 23
# Warning! controlled team near the map edge! Pay attention to using coordinates within the boundary!(7 < x < 23, 0 < y < 23)
# 	Controlled Team Units:
# 		Unit: Stalker    Tag: 0x100080001    ScreenPos: [13, 10]    Health: 160(100 %)    Weapon Ready
# 		Unit: Stalker    Tag: 0x100040001    ScreenPos: [12, 12]    Health: 160(100 %)    Weapon Ready
# 		Unit: Stalker    Tag: 0x100000001    ScreenPos: [12, 10]    Health: 160(100 %)    Weapon Ready
# 	Nearby Enemy Units:
# 		Enemy Unit: Zealot    Tag: 0x100100001    ScreenPos: [23, 11]    Distance: 10    Health: 150(100 %)
# 		Enemy Unit: Zealot    Tag: 0x1000c0001    ScreenPos: [23, 10]    Distance: 10    Health: 150(100 %)
#
# Valid Actions:
# 	Team Stalker-1 Valid Actions:
# 		<Attack_Unit(tag)>
# 		<Move_Screen(screen)>
# 		<Select_Unit_Move_Screen(tag, screen)>
#
# Tasks:
# 	Team Stalker-1' task: Hold position and attack incoming enemies.
# Please note that **Tasks** are the most important information, all your decisions must aimed at completing the tasks.
# """
#     api_base, api_key, dataset_id = 'http://127.0.0.1/v1', 'dataset-cS2LCXGmve8rawYw6QWIJClh', '4e46c039-1a3f-435d-bc9b-700a81ad9645'
#     # test: retrieval
#     kwargs = {'query': text_query, 'top_k': 3}
#     response = dify_retrieve(api_base, api_key, dataset_id, **kwargs)
#     pprint(response.json(), width=200)