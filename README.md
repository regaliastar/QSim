# QSimor
`QLight`：一种轻量级解释型编程语言  
`QSimor`：配套的量子模拟器  

*QSim*是基于*Python+Node.js*实现的量子计算机模拟器。内核计算使用`numpy`，界面使用`electron`框架

在前端界面书写的*QLight*文本会被解释成Python语句执行，脚本文件和量子线路*mvvm*绑定，做到所见即所算。你也可以将线路保存为*LaTeX*语句或字符集合

*Qsimor*的*API*库实现了量子线路论文的算法，使用时通过配置`_config.yml`文件加载

## Introduction
```
#############################################
#                 Quick start               #
#############################################
// Quantum Teleportation
// Declare quantum state, Alice transmits data to Bob
Alice_1 = quantum(1)
Alice_2 = quantum(1)
Bob = quantum(1)
H Bob
X Bob Alice_2
X Alice_1 Alice_2
H Alice_1
// Quantum version of the IF statement
if(Alice_1 == 1){
  X Bob
}
if(Alice_2 == 1){
  Z Bob
}
show()

#############################################
#                 Introduction              #
#############################################
# 这里是一些调用的例子
# 介绍了QSim.py模块是如何工作的

from QSim import QuantumRegister
from QSim import Tools

qubit = QuantumRegister(3)
qubit.applyGate('H', 0)
qubit.applyGate('X', 0, 1)

result = qubit.measure()
print(result)
```

## Terminal
*QSimor*集成了命令行界面，你可以通过命令行方便的进行操控量子操作
```
Usage: qsim [options]

Options:
-v, version info
-h, help information
-d, debug source code
-q, quit program
-s, save code from textarea
-l, generate lexer token
-tpy, translate QLight to python
-tqasm, translate QLight to QASM
-env, get current env
```

## Install
```
// python env
pip install -r requirements.txt

// nodejs env
npm install

// open interface
npm start

// test
pytest --disable-warnings  

// bulid package
npm run build-server
npm run pack-app-win
```

## Bits and pieces
* 若服务器自动连接失败，可以右键`reload`界面
