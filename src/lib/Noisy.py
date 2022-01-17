import os
import sys
import json
import traceback
import yaml
import numpy as np

class Noisy:
  def __init__(self) -> None:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
    sys.path.append(BASE_DIR) #添加环境变量

    # 读取配置文件
    def guessPackaged():
        return os.path.basename(os.getcwd()) != 'QSim'
    yaml_path = ''
    print('guessPackaged: {}'.format(guessPackaged()))
    if guessPackaged():
        # 已经打包
        yaml_path = os.path.join(os.path.abspath("."), "..", "_config.yml")
    else:
        # 没有打包
        yaml_path = os.path.join(os.path.abspath("."), "_config.yml")
    yaml_file = open(yaml_path, 'r', encoding="utf-8")
    file_data = yaml_file.read()
    yaml_file.close()
    yaml_data = yaml.load(file_data)
    self._simulation_env = yaml_data['_simulation_env']
    self._single_error_rate = yaml_data['_single_error_rate']
    self._double_error_rate = yaml_data['_double_error_rate']
    self._measure_error_rate = yaml_data['_measure_error_rate']

  def isSimulationEnv(self):
    return self._simulation_env
  
  def applyNoisy(self, n, errorRate):
    errorRate = float(errorRate)
    return n * (1 - errorRate)

  # @params gate np.array
  def getNoisyGate(self, gate):
    if not self.isSimulationEnv():
      return gate
    for x in np.nditer(gate, op_flags=['readwrite']): 
      if gate.size == 4:
        x[...] = self.applyNoisy(x, self._single_error_rate)
      else:
        x[...] = self.applyNoisy(x, self._double_error_rate)
    return gate
