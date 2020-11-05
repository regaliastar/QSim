# QSim
`QLight`：一种轻量级解释型编程语言  
`QSim`：配套的量子编程模拟器  
## Document-tree
* /QLight
   * /Parser 语法分析程序。包含对语法文件的解析，语法树的生成等
   * /Optimizer 优化器。优化线路的执行
   * /Interpreter 解释器。将Qlight转为能执行的Python文件
   * /Lexer 词法分析器。
   * main.py 入口文件
* /lib  定义了QLight的原生库函数
   * Gates.py 定义量子门
   * Qsim.py 执行引擎
* /views 视图文件
* /test 测试文件
* main.py 程序入口
## Grammar
```
#############################################
#                 LL(1)文法设计              #
#############################################
INT := [0-9]+
Array := [a-zA-Z]*\[INT\]
Identifier := [_a-zA-Z]+[_a-zA-Z0-9]*
Compare := >|<|==|>=|<=

Argument    ---------> Identifier | Array
Measurement ---------> measure ( Argument | Identifier )
QuantumRegister -----> quantum (INT)
GateOp      ---------> I|X|Y|Z|H|S|T|V|V_H|SWAP Argument|Array Array|φ
Factor      ---------> INT
Expression  ---------> Factor [+|-|*|/|Compare Expression]
Bool        ---------> [!] Identifier|Expression
IFStatement ---------> if(Bool) { ; Statement}
WhileStatement ------> while(Bool) { ; Statement}
FuncStatement -------> func Identifier() { ; Statement}
Statement   ---------> GateOp | Measurement | IFStatement | WhileStatement | FuncStatement
Declare     ---------> Identifier = quantum(INT)|INT
Program     ---------> Declare { ; Statement}
FuncCall    ---------> Identifier([INT]*)
```
## Introduction
```
#############################################
#                 QLight语法实例             #
#############################################
// 注释
// 函数
func bell(){
    q[2] = quantum(2)
    H q[0]
    X q[0] q[1]
    return q
}
bell()
// 量子隐态传输
q[3] = quantum(3)
H q[1]
X q[1] q[1]
H q[0]  // phi = sqrt(1/2)|0> + sqrt(1/2)|1>
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
