
import os
import sys
import time
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
# sys.path.append(BASE_DIR)
from lib.QSim import QuantumRegister
from lib.QSim import Tools
tools = Tools()
import numpy as np
start_time = time.process_time()
    
qubit = QuantumRegister(4)
qubit.applyGate('H',0)
qubit.applyGate('X',0,1)
m1 = qubit.measure(place=0, count=1)
# show( 0 )
# show( m1 )
# show( None )

t_cost = time.process_time() - start_time
_wf = tools.print_wf(qubit.a2wf())
# print(_wf)
    
