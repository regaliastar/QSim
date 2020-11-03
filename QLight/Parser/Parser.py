import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
sys.path.append(BASE_DIR) #添加环境变量
from Lexer.Lexer import Lexer
import logging
logging.basicConfig(filename='Parser.log', level=logging.DEBUG)
log = logging.getLogger('Parser')

class Parser:
    '''
    使用LL(1)文法
    递归下降生成语法树
    '''
    First = {
        '''
        根据grammar.txt中的文法生成First集
        这里手动填写，未来考虑自动生成
        '''
        'Argument': ['Identifier', 'Array'],
        'Measurement': ['measure'],
        'GateOp': ['I','X','Y','Z','H','S','T','V','V_H','SWAP'],
        'Factor': ['INT'],
        'Expression': ['INT'],
        'Bool': ['!', 'INT'],
        'IFStatement': ['if'],
        'WhileStatement': ['while'],
        'FuncStatement': ['func'],
        'Statement': ['I','X','Y','Z','H','S','T','V','V_H','SWAP','measure','if','while','func'],
        'Declare': ['Identifier'],
        'Program': ['Identifier']
    }
    def __init__(self, TOKEN):
        self.EOF = [0, '$']
        self.TOKEN = TOKEN
        self.current_token = -1
        self.AST = []
        self.lookahead = []

    def match(self, token):
        if self.lookahead[0] == token[0]:
            self.lookahead = self.getNextToken()

    def getNextToken(self):
        self.current_token += 1
        if self.current_token >= len(self.TOKEN):
            return self.EOF
        return self.TOKEN[self.current_token]

    def FuncStatement(self, token):
        pass

    def Declare(self, token):
        if token[0] == 500:
            self.match(token)
        pass

    def parser(self):
        token = []
        while token[0] != 0:
            token = self.getNextToken()
            if token[0] >= 100 and token[0] < 200:
                pass
            elif token[0] >= 200 and token[0] < 300:
                pass
            elif token[0] >= 300 and token[0] < 400:
                pass
            elif token[0] >= 400 and token[0] < 500:
                pass
            elif token[0] == 500:
                pass
            elif token[0] == 600:
                pass
            else:
                pass

if __name__ == '__main__':
    print('parser')
    lexer = Lexer('QLight/code_0.txt')
    lexer.scanner()
    parser = Parser(lexer.getTOKEN())

