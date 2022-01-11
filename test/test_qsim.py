import pytest
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
sys.path.append(BASE_DIR) #添加环境变量
from src.lib.QSim import QuantumRegister
from src.lib.QSim import Tools
from src.lib.GateManager import GateManager
import numpy as np
import logging

logging.basicConfig(filename='log/test.log', level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

#############################################
#          单元测试 QuantumRegister         #
#           测试接口函数是否符合预期           #
#############################################
# 构造函数
def test_constructor_1():
    qubit = QuantumRegister(3)
    qubit.applyGate('X', 0)
    qubit.applyGate('X', 0, 1)
    measured = qubit.measure()
    for i in measured['value']:
        assert i == '110'

def test_constructor_2():
    qubit = QuantumRegister(basis='00001')
    qubit.applyGate('X', 0)
    measured = qubit.measure()
    for i in measured['value']:
        assert i == '10001'

def test_constructor_3():
    coef = [1/2, 1/2, 1/2, 1/2]
    qubit = QuantumRegister(coef=coef, basis=['00','01','10','11'])
    qubit.applyGate('X', 0)
    a = qubit.getAmplitudes()
    assert (a == coef).all()

# 测试 addGate方法
def test_addGate():
    qubit = QuantumRegister(basis='1000')
    qubit.applyGate('X', 0, 1)
    qubit.applyGate('X', 1, 0)
    measured = qubit.measure()
    for i in measured['value']:
        assert i == '0100'

# 测试 gate2matrix
def test_gate2Matrix():
    qubit = QuantumRegister(basis='1000')
    # 控制位在上
    Matrix1 = GateManager.gate2Matrix('X', 0, 2)
    Matrix2 = GateManager.gate2Matrix('X', 2, 4)
    Matrix3 = GateManager.gate2Matrix('X', 0, 1)
    CNOT3_02 = np.matrix('1 0 0 0 0 0 0 0; 0 1 0 0 0 0 0 0; 0 0 1 0 0 0 0 0; 0 0 0 1 0 0 0 0; 0 0 0 0 0 1 0 0; 0 0 0 0 1 0 0 0; 0 0 0 0 0 0 0 1; 0 0 0 0 0 0 1 0')
    CNOT = np.matrix("1 0 0 0; 0 1 0 0; 0 0 0 1; 0 0 1 0")
    assert (CNOT3_02 == np.mat(Matrix1)).all()
    assert (CNOT3_02 == np.mat(Matrix2)).all()
    assert (CNOT == np.mat(Matrix3)).all()
    # 控制位在下
    CNOT4_30 = np.eye(16, 16)
    CNOT4_30[np.array([1, 9])] = CNOT4_30[np.array([9, 1])]
    CNOT4_30[np.array([3, 11])] = CNOT4_30[np.array([11, 3])]
    CNOT4_30[np.array([5, 13])] = CNOT4_30[np.array([13, 5])]
    CNOT4_30[np.array([7, 15])] = CNOT4_30[np.array([15, 7])]
    Matrix4 = GateManager.gate2Matrix('X', 3, 0)
    assert (CNOT4_30 == np.mat(Matrix4)).all()
    # 测试其他门是否满足

def test_measure():
    tools = Tools()
    log = logging.getLogger('test_measure')
    qubit = QuantumRegister(3)
    qubit.applyGate('H', 0)
    qubit.applyGate('X', 0, 1)
    # log.debug(tools.print_wf(qubit.a2wf()))
    m2 = qubit.measure(place=2)
    # log.debug(tools.print_wf(qubit.a2wf()))
    assert m2 == 0
    m0 = qubit.measure(place=0)
    # log.debug(tools.print_wf(qubit.a2wf()))
    assert m0 == qubit.measure(place=1)


#############################################
#                 测试 Tools                #
#############################################
# test basis
def test_basis():
    tools = Tools()
    arr = [0, 1, 0, 0, 0, 0, 0, 0]
    b = tools.basis('001')
    assert (b.A1 == arr).all()

# test wave_func
def test_wave_func():
    tools = Tools()
    coef1 = [1 / np.sqrt(2), np.sqrt(1 / 2)]
    seqs1 = ['000', '100']
    wf1 = tools.wave_func(coef1, seqs1)
    answer = np.array([np.sqrt(1/2), 0, 0, 0, np.sqrt(1/2), 0, 0, 0])
    assert (np.isclose(wf1.A1, answer)).all()

# test print_wf, a2wf
def test_print_wf():
    tools = Tools()
    answer = '|psi> = {}|{}>+{}|{}>'.format(1/np.sqrt(2),'00',1/np.sqrt(2),'11')
    q1 = QuantumRegister(2)
    q1.applyGate('H', 0)
    q1.applyGate('X', 0, 1)
    wf1 = tools.print_wf(q1.a2wf())
    assert answer == wf1
    q2 = QuantumRegister(basis='00')
    q2.applyGate('H', 0)
    q2.applyGate('X', 0, 1)
    wf2 = tools.print_wf(q2.a2wf())
    assert answer == wf2
    coef = [1/np.sqrt(2), 1/np.sqrt(2)]
    basis = ['00', '11']
    q3 = QuantumRegister(coef=coef, basis=basis)
    wf3 = tools.print_wf(q3.a2wf())
    assert answer == wf3
