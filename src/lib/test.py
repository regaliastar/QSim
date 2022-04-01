from functools import reduce
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
sys.path.append(BASE_DIR) #添加环境变量
from lib.QSim import QuantumRegister
from lib.QSim import Tools
import numpy as np

# tr1
def tr1():
  tools = Tools()
  qubit = QuantumRegister(3)
  gate = []
  gate.append(qubit.applyGate('V_H', 1, 2))
  gate.append(qubit.applyGate('X', 0, 1))
  gate.append(qubit.applyGate('V', 0, 2))
  gate.append(qubit.applyGate('V', 1, 2))
  gate.append(qubit.applyGate('X', 2, 1))
  matrix = reduce(np.dot, gate)
  print(matrix)
tr1()