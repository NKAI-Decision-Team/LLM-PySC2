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


import distutils.command.build
from setuptools import setup

description = """LLM-PySC2 - LLM StarCraft II Learning Environment

LLM-PySC2 is NKAI Decision Team and NUDT Decision Team's Python component of the StarCraft II 
LLM Decision Environment. It exposes Deepmind's PySC2 Learning Environment API as a Python LLM 
Environment. This is a collaboration between NKAI and NUDT to develop StarCraft II into a rich 
environment for LLM research. LLM-PySC2 provides an interface for LLM agents to interact with 
StarCraft 2, getting textual or multimodal observations and textual actions.

Consider that we have not yet publish our paper, if you use the LLM-PySC2 environment or 
LLM-SMAC tasks in your research, please cite the LLM StarCraft II github page temporarily. 

Read the README for more information.

"""


class BuildCommand(distutils.command.build.build):

  def initialize_options(self):
    distutils.command.build.build.initialize_options(self)
    # To avoid conflicting with the Bazel BUILD file.
    self.build_base = '_build'


setup(
    name='llm-pysc2',
    version='0.1',
    description='LLM Starcraft II environment and library for training agents.',
    long_description=description,
    author='NKAI',
    author_email='734162621@qq.com',
    cmdclass={'build': BuildCommand},
    license='Apache License, Version 2.0',
    keywords='StarCraft AI',
    url='',
    packages=[
        'pysc2',
        'pysc2.agents',
        'pysc2.bin',
        'pysc2.env',
        'pysc2.lib',
        'pysc2.maps',
        'pysc2.run_configs',
        'pysc2.tests',
        'llm_pysc2',
        'llm_pysc2.agents',
        'llm_pysc2.bin',
        'llm_pysc2.lib',
    ],
    install_requires=[
        'absl-py>=0.1.0',
        'deepdiff',
        'dm_env',
        'enum34',
        'mock',
        'mpyq',
        'numpy>=1.10',
        'portpicker>=1.2.0',
        'protobuf==3.20.0',
        'openai==0.28',
        'pygame',
        'requests',
        's2clientprotocol>=4.10.1.75800.0',
        's2protocol',
        'sk-video',
        'websocket-client',
        'loguru',
        'pillow',
        'llamaapi',
        'zhipuai',
        # 'google-generativeai',
        # 'anthropic',
        # 'google',
    ],
    entry_points={
        'console_scripts': [
            'pysc2_agent = pysc2.bin.agent:entry_point',
            'pysc2_play = pysc2.bin.play:entry_point',
            'pysc2_replay_info = pysc2.bin.replay_info:entry_point',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.9',  # llamaapi requires python > 3.9
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
