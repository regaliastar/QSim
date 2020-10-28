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

def test_Bell():
    '''
    制备Bell态
    ---H---*---
           |
    -------X---
    '''
    log = logging.getLogger('test_entangled')
    qubit = QuantumRegister(2)
    tools = Tools()
    qubit.applyGate('H', 0)
    qubit.applyGate('X', 0, 1)
    wf = qubit.a2wf()
    log.debug(tools.print_wf(wf))
    measured = qubit.measure(count=100)
    for m in measured['value']:
        assert m[0] == m[1]
    log.debug(measured)

def test_Deutsch():
    '''
    因为 f = CNOT 是平衡函数，因此测量q[0]必为0
    :return:
    '''
    qubit = QuantumRegister(basis='01')
    qubit.applyGate('H',0)
    qubit.applyGate('H',1)
    qubit.applyGate('X',0,1)
    qubit.applyGate('H',0)
    m = qubit.measure(place=0)
    assert m == 1