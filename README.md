# QSim

```
from QSim import QuantumRegister
from QSim import Tools

qubit = new QuantumRegister(3)
qubit.add('H',0)
qubit.add('CNOT',0,1)

result = qubit.measure()
print(result)
```