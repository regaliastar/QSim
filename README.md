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
qubit.applyGate('H',0)
qubit.applyGate('X',0,1)

result = qubit.measure()
print(result)
```

## Options
```
测试
pytest --disable-warnings  
```
