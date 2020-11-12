# QSim
`QLight`：一种轻量级解释型编程语言  
`QSim`：配套的量子模拟器  

*QSim*是基于*Python+JavaScript*实现的量子计算机模拟器。内核计算使用`numpy`，界面使用`electron`框架

在前端界面书写的*QLight*文本会被解释成Python语句执行，脚本文件和量子线路*mvvm*绑定，做到所见即所算。你也可以将线路保存为*LaTeX*语句或字符集合

*Qsim*的*API*库实现了量子线路最新论文的算法，使用时通过配置`config`文件加载

## Demo
*To be written...*

## Introduction
```
#############################################
#                 Quick start               #
#############################################
// 量子隐态传输
q = quantum(3)
H q[1]
X q[1] q[2]     // bell state
H q[0]          // phi = sqrt(1/2)|0> + sqrt(1/2)|1>
X q[0] q[1]
H q[0]
m1 = measure(q[0])
m2 = measure(q[1])
if(m2 == 1){
    X q[2]
}
if(m1 == 1){
    Z q[2]
}

#############################################
#                 Introduction              #
#############################################
# 这里是一些调用的例子
# 介绍了Qsim.py模块是如何工作的

from QSim import QuantumRegister
from QSim import Tools

qubit = QuantumRegister(3)
qubit.applyGate('H', 0)
qubit.applyGate('X', 0, 1)

result = qubit.measure()
print(result)
```
## Options
```
// env
pip install -r requirements.txt

// test
pytest --disable-warnings  
```
## API docs
*To be written...*

