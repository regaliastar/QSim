from lib.QSim import QuantumRegister
from lib.QSim import Tools
import numpy as np

tools = Tools()

#ccccccccccccccccc
def t():
    print('######## t #########')
    tools = Tools()
    coef1 = [1 / np.sqrt(2), np.sqrt(1 / 2)]
    seqs1 = ['000', '100']
    wf1 = tools.wave_func(coef1, seqs1)
    print(wf1)
    print(wf1.A1)

    answer = np.array([np.sqrt(1 / 2), 0, 0, 0, np.sqrt(1 / 2), 0, 0, 0])
    print(answer)

    # 在QuantumRegister中，对wf调用了A1
    qubit = QuantumRegister(coef=coef1, basis=seqs1)
    print(qubit.getAmplitudes())
    print('@a2wf')
    print(qubit.a2wf())
    print(tools.print_wf(qubit.a2wf()))

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

# test_entangled()
t()
test_entangled()