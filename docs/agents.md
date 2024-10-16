

# Agents

Last Edit: 2024/10. 


## MainAgent

MainAgent is an object that directly interact with pysc2 environment. 

The MainAgent is responsible for SubAgents initializing, Logger in initializing, camera calibration, unit grouping, 
automatic economic management in complete game(such as worker training, idle worker redirecting, 
stopping over-mining workers), mainloop managing, camera controlling, unit selecting, 
communication information transmission.

### camera calibration

View code in `llm_pysc2.agents.main_agent_funcs.main_agent_func0` for more information.

### unit grouping

View code in `llm_pysc2.agents.main_agent_funcs.main_agent_func1` for more information.

### auto economic management

View code in `llm_pysc2.agents.main_agent_funcs.main_agent_func2` 
and `llm_pysc2.agents.main_agent_funcs.main_agent_func3` for more information.

### gathering scattered team 

View code in `llm_pysc2.agents.main_agent_funcs.main_agent_func4` for more information.

### mainloop managing

View `docs/mainloop.md` and  code in `llm_pysc2.agents.llm_pysc2_agent_main.MainAgent.step` 
(from the line `while float(time.time()) - t0 < self.config.MAX_LLM_WAITING_TIME:` to the end) 
for more information.

### camera moving

we defined an action in pysc2.lib.actions:

    pysc2.lib.actions.FUNCTIONS.llm_pysc2_move_camera

and use raw_units' world coordinate to move pysc2 camera.

(1) in camera calibration

View code in `llm_pysc2.lib.main_agent_funcs.main_agent_func0` for more information.

(2) in unit grouping

View code in `llm_pysc2.lib.main_agent_funcs.main_agent_func1` for more information.

(3) in main loop

View code in `llm_pysc2.agents.llm_pysc2_agent_main.MainAgent.step` for more information.

### unit selection

(1) in unit grouping

First try 

    pysc2.lib.actions.FUNCTIONS.select_point('select', (unit.x, unit.y))

If can not select the unit, change to `select_rect` function, and gradually increase the rectangular range 
until the unit is selected.

(2) in main loop

If `team['select_type'] == 'select'`, MainAgent will try to select the one of the current loop step 
unselected unit of `team['unit_tags']` by

    pysc2.lib.actions.FUNCTIONS.select_point('select', (unit.x, unit.y))

If `team['select_type'] == 'select_all_type'`, MainAgent will try to select the first unit of `team['unit_tags']` by

    pysc2.lib.actions.FUNCTIONS.select_point('select_all_type', (unit.x, unit.y))

If `team['select_type'] == 'group'`, MainAgent will try to recall the team by

    actions.FUNCTIONS.select_control_group('recall', int(team['game_group']))

If can not select the unit, change to `select_rect` function, and gradually increase the rectangular range 
until the unit is selected.

## SubAgent

SubAgent is an object that directly interact with LLMs, and they are the real decision-makers. 

A SubAgent is responsible for llm query message preparing, querying llm, recognizing valid text actions, 
recognizing valid text args, translating text-actions into pysc2 functions, detecting communication actions 
and generating received communication text.

### unit teams

View code in `llm_pysc2/agents/configs/config.py` for more information.

### llm client

View code in `llm_pysc2/lib/llm_client.py` for more information.

### llm basic prompt

View code in `llm_pysc2/lib/llm_prompt.py` for more information.

### translator_a(action)

View `docs/actions.md` for more information.

### translator_o(observation)

View `docs/observations.md` for more information.
