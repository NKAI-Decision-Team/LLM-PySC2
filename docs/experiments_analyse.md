

# Experiments Analyse

Last Edit: 2024/10. 


## Overview

Experiments Analyse includes two parts: Data Recorde and Log Analyse.
Data Recorde is used for collect pysc2 obs, and Log Analyse script use these obs to 
calculate experiments results.

## Data Recorder

Data Recorder is defined in `llm_pysc2/lib/data_recorder.py`, initialized in `MainAgent.__init__()`, 
and used in `MainAgent.step()`.

Data Recorder has four different `save_level`:

    save_level=0 for only first and last step, which is enough for calculating winning rate, kill/death ratio, etc.
    save_level=1 for important obs when unit list changes, for example, a unit appear or disappear.
    save_level=2 for obs that action may be important, func_id > 10,
    save_level=3 for all obs

Note that, level 3 and 4 may cost lots of user time and disk space.

We set default `save_level` as `0`, and we suggest to follow the default setting.


## Log Analyser

Log Analyser is the script `llm_pysc2/lib/log_analyse.py`. When ever you run a game,
this script will be automatically copied to `llm_log`.

Run it directly

    python ./llm_log/log_analyse.py

to get experiment data like:


    num_experiments=20
    --------------------------------------------------
    {'ave_damage_dealt': 3548.45,
     'ave_damage_taken': 7343.2,
     'ave_healed': 0.0,
     'ave_kill_death_ratio': 0.7094559178110913,
     'ave_killed_resource': 6767.5,
     'ave_lost_resource': 9539.0,
     'rate_lose': 75.0,
     'rate_tie': 0.0,
     'rate_win': 25.0}

Consider that the analyser extract game data through `obs.observation.score_cumulative`, `obs.observation.score_by_category` 
and `obs.observation.score_by_vital`, you can code your own analyser script to get more game analyse data if needed.
