from lib.QSim import QuantumRegister
from lib.QSim import Tools
import numpy as np

qubit = QuantumRegister(3)
tools = Tools()

#ccccccccccccccccc
tools = Tools()
coef1 = [1 / np.sqrt(2), np.sqrt(1 / 2)]
seqs1 = ['000', '100']
wf1 = tools.wave_func(coef1, seqs1)
answer = np.array([np.sqrt(1/2), 0, 0, 0, np.sqrt(1/2), 0, 0, 0])
print(wf1.A1)
print(answer)
