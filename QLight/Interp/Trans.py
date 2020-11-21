'''
根据QSim将Parser生成的语法树翻译成Pyhton代码
if __name__ == '__main__':
    将生成的py文件保存在 log/auto.py
date: 2020-11-10
'''
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
sys.path.append(BASE_DIR) #添加环境变量
from string import Template
from Lexer.Lexer import Lexer
from Parser.Parser import Parser
import logging
logging.basicConfig(filename='log/translate.log', level=logging.DEBUG)
log = logging.getLogger('translate')

py_template = {
    'header':
    '''
import pytest
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
sys.path.append(BASE_DIR)
from lib.QSim import QuantumRegister
from lib.QSim import Tools
tools = Tools()
import numpy as np
    ''',
    'footer':
    '''
_wf = tools.print_wf(qubit.a2wf())
print(_wf)
    ''',
    'FuncStatement':
Template('''
def $FuncStatement_Name($ParameterList):
    $Statement
'''),
    'IFStatement':
Template('''
if $bool_str:
    $Statement
'''),
    'Declare_func':
Template('''$name = $FuncCall_Name($ParameterList)'''),
    'Declare_INT':
Template('''$Iden = $INT'''),
    'GateOp':
Template('''qubit.applyGate('$GateOp_Name',$placeList)'''),
    'FuncCall':
Template('''$FuncCall_Name($ParameterList)'''),
    'measure':
Template('''qubit.measure(place=$place, count=$count)'''),
    'Declare_quantum':
Template('''qubit = QuantumRegister($numQubits)'''),
    'Declare_measure':
Template('''$Iden = qubit.measure(place=$place, count=$count)'''),
}

class pyFileHandler():
    '''维护生成的代码'''
    def __init__(self):
        self.result = []
        self.result.append(py_template['header'])

    def insert(self, _value, _type):
        s = py_template[_type].substitute(_value)
        self.result.append(s)

    def generate_file(self, file_name=None):
        if not file_name:
            file_name = 'log/auto'
        self.result.append(py_template['footer'])
        self.file = open(file_name + '.py', 'w+', encoding = 'utf-8')
        self.file.write('\n'.join(self.result) + '\n')
        self.file.close()

class Translate:
    def __init__(self, tree):
        self.tree = tree
        self.fileHandler = pyFileHandler()

    def log(self):
        self.fileHandler.generate_file()

    def process_statement(self, node):
        '''处理大括号内的情况，如if,while,func'''
        if not node:
            return
        child = node.first_son
        statement_list = []
        while child:
            if child.value == 'Declare_func':
                dict = self.Declare_func(child)
                s = py_template['Declare_func'].substitute(dict)
                statement_list.append(s)
            elif child.value == 'Declare_INT':
                dict = self.Declare_INT(child)
                self.fileHandler.insert(dict, 'Declare_INT')
            elif child.value == 'Declare_quantum':
                dict = self.Declare_quantum(child)
                s = py_template['Declare_quantum'].substitute(dict)
                statement_list.append(s)
                pass
            elif child.value == 'Declare_measure':
                dict = self.Declare_measure(child)
                self.fileHandler.insert(dict, 'Declare_measure')
            elif child.value == 'GateOp':
                dict = self.GateOp(child)
                s = py_template['GateOp'].substitute(dict)
                statement_list.append(s)
            elif child.value == 'FuncStatement':
                dict = self.FuncStatement(child)
                s = py_template['FuncStatement'].substitute(dict)
                statement_list.append(s)
            elif child.value == 'FuncCall':
                if child.first_son.value == 'measure':
                    dict = self.measure(child)
                    s = py_template['measure'].substitute(dict)
                    statement_list.append(s)
                else:
                    dict = self.FuncCall(child)
                    s = py_template['FuncCall'].substitute(dict)
                    statement_list.append(s)
            child = child.right
        statement_str = ''.join(statement_list) + '\n'
        return statement_str

    def FuncStatement(self, node):
        if not node:
            return
        child = node.first_son
        FuncStatement_Name = ''
        ParameterList = ''
        Statement_str = ''
        while child:
            if child.type == 'FuncStatement_Name':
                FuncStatement_Name = child.value
            elif child.value == 'ParameterList' and child.type == None:
                pl = self.tree.find_all_child(child)
                for p in pl:
                    ParameterList += ',' + p.value
                ParameterList = ParameterList[1:]   # 去除第一个,
            elif child.value == 'Statement' and child.type == None:
                Statement_str = self.process_statement(child)
            else:
                raise ValueError('Failed to analyze child: {}'.format(child.format())) 
            child = child.right
        return dict(FuncStatement_Name=FuncStatement_Name,ParameterList=ParameterList,Statement=Statement_str)

    def IFStatement(self, node):
        if not node:
            return
        child = node.first_son
        bool_str = ''
        statement_str = ''
        while child:
            if child.value == 'Bool' and child.type == None:
                bs = self.tree.find_all_child(child)
                for b in bs:
                    bool_str += b.value
            elif child.value == 'Statement' and child.type == None:
                statement_str = self.process_statement(child)
            else:
                raise ValueError('Failed to analyze child: {}'.format(child.format())) 
            child = child.right
        return dict(bool_str=bool_str, statement=statement_str)

    def Return(self, node):
        pass

    def Expression(self, node):
        if not node:
            return
        child = node.first_son
        Expression_str = ''
        while child:
            Expression_str += child.value
        return Expression_str

    def Declare_func(self, node):
        if not node:
            return
        child = node.first_son
        name = ''
        FuncCall_Name = ''
        ParameterList = ''
        '''按层遍历'''
        while child:
            # print(child.format())
            if child.type == 500:
                name = child.value
            elif child.value == '=':
                pass
            elif child.value == 'FuncCall' and child.type == None:
                list = self.tree.find_all_child(child)
                for n in list:
                    if n.type == 'FuncCall_Name':
                        FuncCall_Name = n.value
                    elif n.value == 'ParameterList' and n.type == None:
                        pl = self.tree.find_all_child(n)
                        for p in pl:
                            ParameterList += ',' + p.value
                        ParameterList = ParameterList[1:]   # 去除第一个,
            else:
                raise ValueError('Failed to analyze child: {}'.format(child.format())) 
            child = child.right
        return dict(name=name,FuncCall_Name=FuncCall_Name,ParameterList=ParameterList)

    def GateOp(self, node):
        if not node:
            return
        child = node.first_son
        GateOp_Name = ''
        placeList = ''
        while child:
            if child.type == 'GateOp_Name':
                GateOp_Name = child.value
            elif child.value == 'ParameterList' and child.type == None:
                list = self.tree.find_all_child(child)
                for n in list:
                    placeList += ',' + n.value
                placeList = placeList[1:]   # 去除第一个,
            else:
                raise ValueError('Failed to analyze child: {}'.format(child.format())) 
            child = child.right  
        return dict(GateOp_Name=GateOp_Name, placeList=placeList)

    def FuncCall(self, node):
        if not node:
            return
        child = node.first_son
        FuncCall_Name = ''
        ParameterList = ''
        while child:
            if child.type == 'FuncCall_Name':
                FuncCall_Name = child.value
            elif child.value == 'ParameterList' and child.type == None:
                pl = self.tree.find_all_child(child)
                for p in pl:
                    ParameterList += ',' + p.value
                ParameterList = ParameterList[1:]   # 去除第一个,
            else:
                raise ValueError('Failed to analyze child: {}'.format(child.format()))
            child = child.right  
        return dict(FuncCall_Name=FuncCall_Name, ParameterList=ParameterList)

    def measure(self, node):
        if not node:
            return
        child = node.first_son
        place = '-1'
        count = '1'
        while child:
            if child.value == 'measure':
                pass
            elif child.value == 'ParameterList' and child.type == None:
                pl = self.tree.find_all_child(child)
                '''这里需要分别处理measure(q), measure(q[0])的情况'''
                for p in pl:
                    if p.type == 500:
                        pass
                    elif p.type == 600:
                        place = p.value
            else:
                raise ValueError('Failed to analyze child: {}'.format(child.format()))
            child = child.right
        return dict(place=place, count=count)
    
    def Declare_quantum(self, node):
        if not node:
            return
        child = node.first_son
        numQubits = '-1'
        qubit = 'qubit'
        while child:
            if child.value == 'quantum':
                pass
            elif child.type == 500:
                qubit = child.value
            elif child.value == '=':
                pass
            elif child.value == 'FuncCall' and child.type == None:
                list = self.tree.find_all_child(child)
                for n in list:
                    if n.type == 'FuncCall_Name':
                        pass
                    elif n.value == 'ParameterList' and n.type == None:
                        pl = self.tree.find_all_child(n)
                        numQubits = pl[0].value
            elif child.type == None and child.value == 'ParameterList':
                # 函数式声明quantumRegister
                list = self.tree.find_all_child(child)
                numQubits = list[0].value
            else:
                raise ValueError('Failed to analyze child: {}'.format(child.format()))
            child = child.right
        return dict(qubit=qubit, numQubits=numQubits)

    def Declare_measure(self, node):
        if not node:
            return
        child = node.first_son
        Iden = 'm'
        place = '-1'
        count = '1'
        while child:
            if child.type == 500:
                Iden = child.value
            elif child.value == '=':
                pass
            elif child.value == 'FuncCall' and child.type == None:
                list = self.tree.find_all_child(child)
                for n in list:
                    if n.type == 'FuncCall_Name':
                        pass
                    elif n.value == 'ParameterList' and n.type == None:
                        pl = self.tree.find_all_child(n)
                        '''这里需要分别处理measure(q), measure(q[0])的情况'''
                        for p in pl:
                            if p.type == 500:
                                pass
                            elif p.type == 600:
                                place = p.value
            else:
                raise ValueError('Failed to analyze child: {}'.format(child.format()))
            child = child.right
        return dict(Iden=Iden, place=place, count=count)

    def Declare_INT(self, node):
        if not node:
            return
        child = node.first_son
        Iden = 'Iden'
        INT = ''
        while child:
            if child.type == 500:
                Iden = child.value
            elif child.value == '=':
                pass
            elif child.type == 'INT':
                INT = child.value
            else:
                raise ValueError('Failed to analyze child: {}'.format(child.format()))
            child = child.right
        return dict(Iden=Iden, INT=INT)

    def main(self):
        tree = self.tree
        childs = tree.find_all_child(tree.root)
        for child in childs:
            if child.value == 'Declare_func':
                dict = self.Declare_func(child)
                self.fileHandler.insert(dict, 'Declare_func')
            elif child.value == 'Declare_INT':
                dict = self.Declare_INT(child)
                self.fileHandler.insert(dict, 'Declare_INT')
            elif child.value == 'Declare_quantum':
                dict = self.Declare_quantum(child)
                self.fileHandler.insert(dict, 'Declare_quantum')
            elif child.value == 'Declare_measure':
                dict = self.Declare_measure(child)
                self.fileHandler.insert(dict, 'Declare_measure')
            elif child.value == 'GateOp':
                dict = self.GateOp(child)
                self.fileHandler.insert(dict, 'GateOp')
            elif child.value == 'FuncStatement':
                dict = self.FuncStatement(child)
                self.fileHandler.insert(dict, 'FuncStatement')
            elif child.value == 'FuncCall':
                if child.first_son == 'measure':
                    dict = self.measure(child)
                    self.fileHandler.insert(dict, 'measure')
                else:
                    dict = self.FuncCall(child)
                    self.fileHandler.insert(dict, 'FuncCall')

if __name__ == '__main__':
    print('translate')
    lexer = Lexer('QLight/code_2.txt')
    lexer.scanner()
    lexer.log()
    parser = Parser(lexer.getTOKEN())
    parser.parse()
    parser.log()
    translate = Translate(parser.tree)
    translate.main()
    translate.log()