

# Problems

Last Edit: 2024/10.


### Game Installation

(1) Suggest game version >= 5.0.13 (92440), set language to English, and install the game in the default path. 

### Build

(1) Must run `pip install -e .` at the same path of the setup.py file. 

### Map 

(1) Map xxx not found: please check (i) whether the map in game Map directory (ii) whether the map 
listed in any of the file of pysc2.map.xxx.

### LLM

(1) If llm_runtime_error occur too many times, please check (i) Is the network disconnected 
or unable to access api_mase; (ii) Some large models interact extremely slow, is the runtime 
parameter (config.MAX_LLM_RUNTIME_ERROR_TIME) set in config sufficient?

(2) GLM model may encounter HTTP error code 1001: "Header中未收到Authorization参数，无法进行身份验证。", 
we do not know how to deal with it yet...

### Run

(1) advise --rgb_screen_size 128/256/512/1024 if you want to use image observation, too large value may
lead to some bugs in camera moving or selecting unit, and end in endless loop(or cost too much time
in figure generation, and cost lots of tokens in llm query).

### Replay

(1) The absolute path of the folder where replies are stored cannot be too long, or the replay may be damaged
("unable to open replay" when load the rep).

