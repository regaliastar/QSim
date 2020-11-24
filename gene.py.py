
import pytest
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
sys.path.append(BASE_DIR)
from lib.QSim import QuantumRegister
from lib.QSim import Tools
tools = Tools()
import numpy as np
    
qubit = QuantumRegister(4)
qubit.applyGate('Z',0)

_wf = tools.print_wf(qubit.a2wf())
print(_wf)
    

_wf = tools.print_wf(qubit.a2wf())
print(_wf)
    
