'''
根据QSim将Parser生成的语法树翻译成Pyhton代码
date: 2020-11-6
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
    'FuncStatement':
Template('''
def $FuncStatement_Name($ParameterList):
    $Statement
'''),
    'Declare_QR':
Template('''
$name = QuantumRegister($ParameterList)
'''),
    'Declare_INT':
Template('''
$name = $INT
'''),
    'GateOp':
Template('''
$GateOp_Name $ParameterList
'''),
    'FuncCall':
Template('''
$FuncCall_Name($ParameterList)
''')
}

class FileHandler():
    '''维护生成的代码'''
    def __init__(self):
        self.result = []

    def insert(self, value, _type):
        s = py_template[_type].substitute(value)
        self.result.append(s)

    def generate_file(self, file_name=None):
        if not file_name:
            file_name = 'log/auto'
        self.file = open(file_name + '.py', 'w+')
        self.file.write('\n'.join(self.result) + '\n')
        self.file.close()

class Translate:
    def __init__(self, tree):
        self.tree = tree

    def FuncStatement(self, node=None):
        current_node = node.first_son
        while current_node:
            if current_node.value == 'FuncStatement':
                pass


if __name__ == '__main__':
    print('translate')
    lexer = Lexer('QLight/code_0.txt')
    lexer.scanner()
    log.debug(lexer.getTOKEN())
    parser = Parser(lexer.getTOKEN())
    parser.main()
    parser.tree.show()
    translate = Translate(parser.tree)
    # fileHandler = FileHandler()
    # v = dict(FuncStatement_Name='m', ParameterList='', Statement='measure(q)')
    # fileHandler.insert(v, 'FuncStatement')
    # fileHandler.generate_file()