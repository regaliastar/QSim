import pytest
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
sys.path.append(BASE_DIR) #添加环境变量
from src.lib.QSim import QuantumRegister
from src.lib.QSim import Tools
import numpy as np
import logging

#############################################
#                 模块化测试                 #
#             验证制备各种模型的能力          #
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
    Deutsch算法：常数函数 => 0，平衡函数 => 1
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

def test_teleport():
    '''
    量子隐态传输实验：量子通信网络的基础，Alice:q[0,1], Bob:q[2], 要传输的 phi=q[0]
    假设 phi = sqrt(1/2)|0> + sqrt(1/2)|1>
    '''
    tools = Tools()
    qubit = QuantumRegister(basis='000')
    # 先制备Bell态
    qubit.applyGate('H',1)
    qubit.applyGate('X',1,2)
    # 假设 phi = sqrt(1/2)|0> + sqrt(1/2)|1>
    qubit.applyGate('H',0)
    phi = '{}|{}>+{}|{}>'.format(1/np.sqrt(2),'0',1/np.sqrt(2),'1')
    # 开始隐态传输
    qubit.applyGate('X',0,1)
    qubit.applyGate('H',0)
    m1 = qubit.measure(place=0)
    m2 = qubit.measure(place=1)
    if m2 == 1:
        qubit.applyGate('X', 2)
    if m1 == 1:
        qubit.applyGate('Z',2)
    Bob_wf = tools.print_wf(qubit.a2wf())
    assert phi == Bob_wf
