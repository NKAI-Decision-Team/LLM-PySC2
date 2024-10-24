

# Config

Last Edit: 2024/10. 


## Overview

Config is used for setting LLM parameters (for each agent), LLM data processing modules 
(such as obs wrapper, text action recognizer and communication), enable or disable image input,
set LLM waiting time and runtime error time, enable or disable Complete Game Auxiliary Management Options.

Configs are define in `llm_pysc2/agents/configs`, shape as:

    class AgentConfig:
      def __init__(self):
        self.race = ''
        self.model_name = 'YOUR-MODEL-NAME'
        self.api_base = 'YOUR-API-BASE'
        self.api_key = 'YOUR-API-KEY'
        ...
      def reset_llm(...):
        ...
      def auto_check(...):
        ...

## LLM parameters

    1.config.race: 
Specifies the race used by the agent in the StarCraft II game. Options include Protoss, Zerg, and Terran. Current work supports fighting as Protoss.
    
    2.config.model_name: 
Used to specify the name of the large language model (LLM) used. For specific supported types, see the FACTORY list in the llm_pysc2/lib/llm_client.py file
        
    3.config.api_base: 
Used to specify the API base URL for interacting with the large language model
        
    4.config.api_key: 
Access key, used to verify and authorize access to the LLM. The placeholder needs to be replaced with the correct key.
        
    5.config.temperature: 
Controls the diversity of the LLM output. Lower temperature values ​​(such as 0.1) generally make the model's output more certain and conservative, and the generated text has less randomness.

## LLM Agent parameters

    1.config.basic_prompt: 
The basic prompt words or prompt template when the agent interacts with LLM, which determines how LLM will generate decisions or responses. For specific supported types, see the FACTORY list in the llm_pysc2/lib/llm_prompt.py file.
    
    2.config.translator_o: 
Configuration of the observation translator. Translate the game state into input that LLM can understand. For specific supported types, see the FACTORY list in the llm_pysc2/lib/llm_observation.py file.
    
    3.config.translator_a: 
Configuration of the action translator. Convert the output of LLM into specific game actions. For specific supported types, see the FACTORY list in the llm_pysc2/lib/llm_action.py file.
        
    4.config.communicator: 
Configuration of the communication module, which is used to coordinate the communication between LLM and other modules or agents. For specific supported types, see the FACTORY list in the llm_pysc2/lib/llm_communicate.py file.
        
    5.config.ENABLE_COMMUNICATION: 
Whether to enable communication. If enabled, the agent may communicate with other agents through language models.


## LLM interaction options
    
    1.config.ENABLE_IMAGE_RGB: 
Whether to enable RGB image input. If enabled, the agent will process RGB images as one of its inputs.
    
    2.config.ENABLE_IMAGE_FEATURE: 
Whether to enable feature map input. If enabled, the agent will process feature image data extracted from the game.
    
    3.config.ENABLE_SAVE_IMAGES: 
Whether to save images.

    1.config.LLM_SIMULATION_TIME: 
Used to control the simulation time of the large language model.

    2.config.MAX_LLM_QUERY_TIMES: 
The maximum number of queries the agent can make with the LLM.

    3.config.MAX_LLM_WAITING_TIME: 
The maximum waiting time (in seconds) that the agent will wait for a response from the LLM

    4.config.MAX_LLM_RUNTIME_ERROR_TIME: 
The critical waiting time for the agent to trigger an alarm.

    5.config.MAX_LLM_DECISION_FREQUENCYLLM: 
The interaction frequency (in Hz).

    6.config.MAX_NUM_ACTIONS: 
The maximum number of actions the agent can perform after each decision.

## Auxiliary Management Options in Complete Game 
    
    1.config.ENABLE_INIT_STEPS: 
Enabled when playing a full game. This parameter is used to add worker training actions before camera calibration and other actions to avoid delaying worker training due to camera calibration.
    
    2.config.ENABLE_AUTO_WORKER_MANAGE:
Whether to automatically manage worker production. This is related to resource management in StarCraft. When this option is turned on, the agent will automatically handle the management of resource collection workers.
    
    3.config.ENABLE_AUTO_WORKER_TRAINING: 
Whether to automatically train workers. When turned on, the agent will automatically produce workers when needed to maintain economic development.

