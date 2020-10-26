from lib.QSim import QuantumRegister
from lib.QSim import Tools
import numpy as np

qubit = QuantumRegister(3)
tools = Tools()
# test 构造方法一
print('# test 构造方法一')
print(qubit.getAmplitudes())
qubit.addGate('H',0)
qubit.addGate('CNOT',0,1)
print(qubit.getAmplitudes())

result = qubit.measure()
print(result)

# test 构造方法二
print('# test 构造方法二')
qubit_2 = QuantumRegister(basis='111')
print(qubit_2.getAmplitudes())
qubit_2.addGate('X',0)
print(qubit_2.getAmplitudes())
print(qubit_2.measure())

# test 构造方法三
print('# test 构造方法三')
qubit_3 = QuantumRegister(coef=[1/2,1/2,1/2,1/2], basis=['00','01','10','11'])
print(qubit_3.getAmplitudes())
qubit_3.addGate('X',0)
print(qubit_3.getAmplitudes())
print(qubit_3.measure())

# test basis
print('# test basis')
b = tools.basis('001')
print(b.A1)

#test wave_func
print('#test wave_func')
coef1 = [1j/np.sqrt(3), np.sqrt(2/3)]
seqs1 = ['000', '100']
wf1 = tools.wave_func(coef1, seqs1)
print(wf1)
coef2 = [np.sqrt(1/3), np.sqrt(1/3), np.sqrt(1/3)]
seqs2 = ['000', '001', '010']
wf2 = tools.wave_func(coef2, seqs2)
print(wf2)

#test print_wf // 命令行无法显示LaTeX
print('#test print_wf')
print(tools.print_wf(wf1))
print(tools.print_wf(wf2))

#ccccccccccccccccc
tools = Tools()
coef1 = [1 / np.sqrt(2), np.sqrt(1 / 2)]
seqs1 = ['000', '100']
wf1 = tools.wave_func(coef1, seqs1)
answer = np.array([np.sqrt(1/2), 0, 0, 0, np.sqrt(1/2), 0, 0, 0])
print(wf1.A1)
print(answer)