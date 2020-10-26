# QSim
## Introduction
```
#############################################
#                 Introduction              #
#############################################
# 这里是一些调用的例子
# 介绍了该模块是如何工作的

from QSim import QuantumRegister
from QSim import Tools

qubit = new QuantumRegister(3)
qubit.addGate('H',0)
qubit.addGate('CNOT',0,1)

result = qubit.measure()
print(result)
```

## Options
```
测试
pytest --disable-warnings  
```
