import pytest
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
sys.path.append(BASE_DIR) #添加环境变量
from lib.QSim import QuantumRegister
from lib.QSim import Tools
import numpy as np
import logging

#############################################
#                 模块化测试                 #
#             验证制备各种模型的能力           #
#############################################
# 制备纠缠态
def test_entangled():
    log = logging.getLogger('test_entangled')
    qubit = QuantumRegister(2)
    tools = Tools()
    qubit.applyGate('H', 0)
    qubit.applyGate('X', 0, 1)
    wf = qubit.a2wf()
    log.debug(tools.print_wf(wf))
    measured = qubit.measure()
    assert measured[0] == measured[1]