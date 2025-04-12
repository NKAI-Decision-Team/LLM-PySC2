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


from pysc2.lib.actions import FUNCTIONS as F


# standard action object
AN_ACTION = {'name': '', 'arg': [], 'func': []}

HOLD_POSITION = {
  'name': 'Hold_Position',   'arg': [],  'func': [(274, F.HoldPosition_quick, ('queued'))]}
HOLD_POSITION_NO_OP = {
  'name': 'No_Operation', 'arg': [], 'func': [(0, F.no_op, ())]}

MOVE_SCREEN = {
  'name': 'Move_Screen', 'arg': ['screen'],
  'func': [(331, F.Move_screen, ('queued', 'screen')), (331, F.Move_screen, ('now', 'screen'))]}
MOVE_MINIMAP = {
  'name': 'Move_Minimap', 'arg': ['minimap'],
  'func': [(332, F.Move_minimap, ('queued', 'minimap')), (332, F.Move_minimap, ('now', 'minimap'))]}
SU_MOVE_SCREEN = {
  'name': 'Select_Unit_Move_Screen', 'arg': ['tag', 'screen'],
  'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
           (331, F.Move_screen, ('now', 'screen')),
           (331, F.Move_screen, ('queued', 'screen'))]}
SU_MOVE_MINIMAP = {
  'name': 'Select_Unit_Move_Minimap', 'arg': ['tag', 'minimap'],
  'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
           (332, F.Move_minimap, ('now', 'minimap')),
           (332, F.Move_minimap, ('queued', 'minimap'))]}

ATTACK_00S = {
  'name': 'Attack_Unit', 'arg': ['tag'],
  'func': [(12, F.Attack_screen, ('queued', 'screen_tag'))]}
ATTACK_02S = {
  'name': 'Attack_Unit', 'arg': ['tag'],
  'func': [(12, F.Attack_screen, ('queued', 'screen_tag')),
           (0, F.no_op, ()), (0, F.no_op, ()), (0, F.no_op, ()),
           (0, F.no_op, ()), (0, F.no_op, ())]}
SU_ATTACK_00S = {
  'name': 'Select_Unit_Attack_Unit', 'arg': ['tag', 'tag'],
  'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
           (12, F.Attack_screen, ('queued', 'screen_tag2'))]}
SU_ATTACK_02S = {
  'name': 'Select_Unit_Attack_Unit', 'arg': ['tag', 'tag'],
  'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
           (12, F.Attack_screen, ('queued', 'screen_tag2')),
           (0, F.no_op, ()), (0, F.no_op, ()), (0, F.no_op, ()),
           (0, F.no_op, ()), (0, F.no_op, ())]}