import pytest
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
sys.path.append(BASE_DIR) #添加环境变量
from lib.QSim import QuantumRegister
from lib.QSim import Tools
import numpy as np

#############################################
#          测试 QuantumRegister             #
#############################################
# 构造函数
def test_constructor_1():
    qubit = QuantumRegister(3)
    print(qubit.getAmplitudes())
    qubit.addGate('X', 0)
    qubit.addGate('CNOT', 0, 1)
    measured = qubit.measure()
    assert measured == '110'

def test_constructor_2():
    qubit = QuantumRegister(basis='00001')
    qubit.addGate('X', 0)
    measured = qubit.measure()
    assert measured == '10001'

def test_constructor_3():
    coef = [1/2, 1/2, 1/2, 1/2]
    qubit = QuantumRegister(coef=coef, basis=['00','01','10','11'])
    qubit.addGate('X', 0)
    wf = qubit.getAmplitudes()
    assert (wf == coef).all()

#############################################
#                 测试 Tools             #
#############################################
# test basis
def test_basis():
    tools = Tools()
    arr = [0, 1, 0, 0, 0, 0, 0, 0]
    b = tools.basis('001')
    assert (b.A1 == arr).all()

#test wave_func
def test_wave_func():
    tools = Tools()
    coef1 = [1 / np.sqrt(2), np.sqrt(1 / 2)]
    seqs1 = ['000', '100']
    wf1 = tools.wave_func(coef1, seqs1)
    answer = np.array([np.sqrt(1/2), 0, 0, 0, np.sqrt(1/2), 0, 0, 0])
    assert (np.isclose(wf1.A1, answer)).all()
