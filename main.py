from lib.QSim import QuantumRegister
from lib.QSim import Tools
from lib.GateManager import GateManager
import numpy as np
import logging

tools = Tools()

#ccccccccccccccccc
def t():
    coef = [1 / np.sqrt(2), -np.sqrt(1 / 2)]
    basis = ['0', '1']
    qubit = QuantumRegister(coef=coef, basis=basis)
    print(qubit.getAmplitudes())
    qubit.applyGate('Z',0)
    print(qubit.getAmplitudes())

def test_entangled():
    print('test_entangled')
    qubit = QuantumRegister(2)
    tools = Tools()
    qubit.applyGate('H', 0)
    qubit.applyGate('CNOT2_01', 0, 1)

    coef2 = [1 / np.sqrt(2), np.sqrt(1 / 2)]
    seqs2 = ['00', '11']
    wf2 = tools.wave_func(coef2, seqs2)
    print(tools.print_wf(wf2))
    print(wf2)
    print(type(wf2))

    wf = qubit.a2wf()
    print(type(wf))
    print(qubit.getAmplitudes())
    print(wf)
    print(tools.print_wf(wf))
    measured = qubit.measure()
    assert measured[0] == measured[1]

def test_teleport():
    '''
    量子隐态传输实验：量子通信网络的基础，Alice:q[0,1], Bob:q[2], 要传输的 phi=q[0]
    假设 phi = sqrt(1/2)|0> + sqrt(1/2)|1>
    '''
    log = logging.getLogger('test_teleport')
    tools = Tools()
    qubit = QuantumRegister(basis='000')
    # 先制备Bell态
    qubit.applyGate('H',1)
    qubit.applyGate('X',1,2)
    # 假设 phi = sqrt(1/2)|0> + sqrt(1/2)|1>
    qubit.applyGate('H',0)
    phi = '|psi> = {}|{}>+{}|{}>'.format(1/np.sqrt(2),'0',1/np.sqrt(2),'1')
    # 开始隐态传输
    print('开始隐态传输: ' + tools.print_wf(qubit.a2wf()))
    qubit.applyGate('X',0,1)
    qubit.applyGate('H',0)
    print('CX,H: ' + tools.print_wf(qubit.a2wf()))
    m1 = qubit.measure(place=0)
    print('m1: ' + tools.print_wf(qubit.a2wf()))
    m2 = qubit.measure(place=1)
    print('m2: ' + tools.print_wf(qubit.a2wf()))
    print(qubit.getBasicInfo())
    if m2 == 1:
        qubit.applyGate('X', 2)
        print(qubit.getBasicInfo())
    if m1 == 1:
        qubit.applyGate('Z',2)
        print(qubit.getBasicInfo())
    Bob_wf = tools.print_wf(qubit.a2wf())
    print('m1: {},m2: {}'.format(m1, m2))
    print('Bob_wf: '+Bob_wf)
    assert phi == Bob_wf

test_teleport()
# test_entangled()
print('########## 外面 ##########')
