# QSim
`QSim`：一款轻量级量子编程模拟器  
`QLight`：解释型编程语言
## 文档树
* /QLight
   * /Parser 语法分析程序。包含对语法文件的解析，语法树的生成等
   * /Optimizer 优化器。优化线路的执行
   * /Interpreter 解释器。将Qlight转为能执行的Python文件
   * /Lexer 词法分析器。
   * main.py 入口文件
* /lib
   * Gates.py 定义量子门
   * Qsim.py 执行引擎
* /views 视图文件
* /test 测试文件
* main.py 程序入口
## Introduction
```
#############################################
#                 Introduction              #
#############################################
# 这里是一些调用的例子
# 介绍了Qsim.py模块是如何工作的

from QSim import QuantumRegister
from QSim import Tools

qubit = QuantumRegister(3)
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
