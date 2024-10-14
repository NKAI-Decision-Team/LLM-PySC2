

# Actions

Last Edit: 2024/10. 


## Action space

Default action space of Protoss can be seen in `./llm_pysc2/lib/llm_action.py` and 
`./llm_pysc2/agents/configs/config.py`. Note that `./llm_pysc2/lib/llm_action.py` 
is a executable file, run it to see action space of each predefined agent.

For example, Agent CombatGroup1's action space is:

    CombatGroup1
        Protoss.Stalker
             <Stop()>
             <No_Operation()>
             <Hold_Position()>
             <Move_Minimap(minimap)>
             <Move_Screen(screen)>
             <Ability_Blink_Screen(screen)>
             <Attack_Unit(tag)>
             <Select_Unit_Blink_Screen(tag, screen)>


## Text action

Text action is used to interact with LLMs and can intuitively inform LLM of 
the action's purpose, without any more explanation.

A valid text action looks like:

    <ActionName()>
    <ActionName(arg0)>
    <ActionName(arg0, arg1)>

shape as:

    <Attack_Unit(tag)>              (text action standard form)
    <Attack_Screen(screen)>         (text action standard form)

or

    <Attack_Unit(0x100030001)>      (text action instance form)
    <Attack_Screen([23, 37])>       (text action instance form)

We use `<>` for action recognition, `()` for arg recognition, `[]` for coordinate recognition and
`0x` used for tag recognition (a hexadecimal number). Note that text actions cannot be directly applied to the pysc2 engine. If you want redefine actions, 
follow the instructions in `Structured Action` section.


## Structured Action

Structured action is the bridge between text action and pysc2 functions.
We defined most of the structured actions in `./llm_pysc2/lib/llm_action.py` and 
 `./llm_pysc2/agent/configs/config.py`

A structured action shapes as:

    {'name': '', 'arg': [], 'func': [(func_id, func, tuple_arg_types), ...]}

For example, you can define an action called `Select_Unit_Attack_Screen` as:

    {'name': 'Select_Unit_Attack_Screen', 'arg': ['tag', 'screen'], 
     'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
              (12, F.Attack_screen, ('queued', 'screen'))]},

or `Select_Unit_Attack_Unit` as:

    {'name': 'Select_Unit_Attack_Unit', 'arg': ['tag', 'tag'], 
     'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
              (12, F.Attack_screen, ('queued', 'screen_tag2'))]},

where `F` refers to `pysc2.lib.action.FUNCTIONS`. However, if you need to redefine 
actions and adapt it to our environment, you need to learn the rules of designing action name,
action arg and tuple_arg_types.


### (1) Action Name

In principle, action name can be any string. But the following fields are used as keywords, with relevant functions:

    Build_              Automatic parameter validity verification: pathable, buildable, blocked, have power/creep, etc.
    Board_              Automatic parameter validity verification: tag must refers to a transportor
    Select_Workers_     Automatic add function: select all screen workers (dangerous action)

    Attack              Automatic parameter validity verification: can not select ally unit
    Load                Automatic parameter validity verification: can not select unit except ally
    Follow              Automatic parameter validity verification: can not select unit except ally
    MassRecall          Automatic parameter validity verification: can not select unit except ally
    Chrono_Boost        Automatic parameter validity verification: can not select unit not boostable

    _Minimap            Automatic parameter validity verification: within minimap range
    _Screen             Automatic parameter validity verification: within minimap range

    Train_              Automatic add function: Camera move + select unit (relevant idle building)
    Research_           Automatic add function: Camera move + select unit (relevant idle building)

For example, you can define actions like:

    <Select_Unit_Attack_Minimap(tag, screen)>
    <All_Unit_Attack_Minimap(minimap)>
    <All_Unit_Attack_Enemy_Base()>
    <All_Unit_Retreat()>
    <Suicide_Unit(tag)>

the most important thing in designing action name is making the large language model 
intuitively and correctly understand the meaning of an action.


### (2) Action Args

Action's arg should be a combination of the following keywords:

    minimap, screen, tag

When an action is called, these args look like:

    [12, 32], [55, 70], 0x1000a3001

And the optional combination forms can be enumerated as below:

    'arg': []
    'arg': ['tag']              'arg': ['tag', 'tag']
    'arg': ['screen']           'arg': ['tag', 'screen']
    'arg': ['minimap']          'arg': ['tag', 'minimap']

### (3) Func triple list

Func triple list is the last part of a structured action. 

There is no rules in the length of the func triple list, what important is the rules of
how to define a func triple.

a func triple shape as

    (func_id, func, tuple_arg_types)

where func_id refers to the function index in `pysc2.lib.action.FUNCTIONS`, 
func is the function of `pysc2.lib.action.FUNCTIONS`, tuple_arg_types should 
consistent with the standard pysc2 function parameter list.

elements of tuple_arg_types should follow the transform rule:

| arg in pysc2 | arg in func triple | description                                                                                    |
|--------------|--------------------|------------------------------------------------------------------------------------------------|
| 'select'     | 'select'           | select mode, in F.select_point or F.select_rect                                                | 
| 'queued'     | 'queued'           | act when former functions finished execution                                                   | 
|              | 'now'              | act immediately, discard unfinished actions                                                    |
| 'world'      | 'world'            | world coordinate                                                                               |
|              | 'world_tag'        | world coordinate of the unit with the first tag                                                |
| 'screen'     | 'screen'           | screen coordinate                                                                              |
|              | 'screen_tag'       | screen coordinate of the unit with the first tag                                               |
|              | 'screen_tag2'      | screen coordinate of the unit with the second tag <br/> (only when 'arg': ['tag', 'tag'])      |
|              | 'screen1_tag'      | screen coordinate of the unit with the first tag, <br/> -0.5 for x and y, used for select_rect |
|              | 'screen2_tag'      | screen coordinate of the unit with the first tag, <br/> +0.5 for x and y, used for select_rect |
| 'minimap'    | 'minimap'          | minimap coordinate                                                                             |
|              | 'minimap_tag'      | minimap coordinate of the unit with the first tag                                              |
|              | 'minimap_tag2'     | minimap coordinate of the unit with the second tag <br/> (only when 'arg': ['tag', 'tag'])     |

For example, if there are two unit:

    Adept    tag: 0x1001a0001    screen: [64, 64]
    Drone    tag: 0x100400001    screen: [96, 32]

and the environment detected a text action like

    <Select_Unit_Attack_Unit(0x1001a0001, 0x100400001)>

which is the action we mentioned above (`Select_Unit_Attack_Unit`):

    {'name': 'Select_Unit_Attack_Unit', 'arg': ['tag', 'tag'], 
     'func': [(3, F.select_rect, ('select', 'screen1_tag', 'screen2_tag')),
              (12, F.Attack_screen, ('queued', 'screen_tag2'))]},

the environment will automatically complete coordinate search and check parameter 
validity, then recall the following pysc2 functions:

    F.select_rect('select', [63.5, 63.5], [64.5, 64.5])
    F.Attack_screen('queued', [96, 32])

and finally realize the purpose of "Select Adept Attack Drone"


## Test your defined actions

We provide a dedicated debugging feature: you can "act like a LLM", write text actions
input a txt file, the environment will then read the text and convert detected actions
into a pysc2 function.

First, disable llm, in `./llm_pysc2/agents/configs/config.py`, set :
 
    config.LLM_SIMULATION_TIME = 5

Then, run an experiment, LLM query step will be replaced with a time.sleep(5), 
and a new log directory will be generated in `./llm_log` and
enter the directory of current experiment and open an agent's folder. Then write the action 
you want to test to the `./llm_log/EXPERIEMNT_DIR/SUBAGENT_DIR/a_inp.txt`. For example:

    Actions:
        Team TEAMNAME:
            <ActionYouWantToTest()>
            <ActionYouWantToTest(YourArg)>
            <ActionYouWantToTest(YourArg, YourArg)>
 
and view file `./llm_log/EXPERIEMNT_DIR/SUBAGENT_DIR/a_his.txt` to see the 
recognition status of your actions and the args.

    


