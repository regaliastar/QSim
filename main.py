from lib.QSim import QuantumRegister
from lib.QSim import Tools
import numpy as np

qubit = QuantumRegister(3)
tools = Tools()
# test 1
qubit.add('H',0)
# qubit.add('X',1)
qubit.add('CNOT',0,1)

result = qubit.measure()
print(result)

# test basis
b = tools.basis('001')
print(b.A1)

#test wave_func
coef1 = [1j/np.sqrt(3), np.sqrt(2/3)]
seqs1 = ['000', '100']
wf1 = tools.wave_func(coef1, seqs1)
print(wf1)

#test print_wf // 命令行无法显示LaTeX
pwf = tools.print_wf(wf1)
print(pwf)

