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
        'FuncStatement': ['func'],
        'Measurement': ['measure'],
        'GateOp': ['I','X','Y','Z','H','S','T','V','V_H','SWAP'],
    }
    def __init__(self, TOKEN):
        self.EOF = [0, '$']
        self.TOKEN = TOKEN
        self.current_token = -1

    def getNextToken(self):
        self.current_token += 1
        if self.current_token >= len(self.TOKEN):
            return self.EOF
        return self.TOKEN[self.current_token]

    def FuncStatementAnalyzer(self, token):
        pass

    def parser(self):
        id = ''
        while id != 0:
            id = self.getNextToken()[0]
            if id >= 100 and id < 200:
                pass
            elif id >= 200 and id < 300:
                pass
            elif id >= 300 and id < 400:
                pass
            elif id >= 400 and id < 500:
                pass
            elif id == 500:
                pass
            elif id == 600:
                pass
            else:
                pass

if __name__ == '__main__':
    print('parser')
    lexer = Lexer('QLight/code_0.txt')
    lexer.scanner()
    parser = Parser(lexer.getTOKEN())

