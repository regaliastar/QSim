import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
sys.path.append(BASE_DIR) #添加环境变量
from Lexer.Lexer import Lexer
import logging
logging.basicConfig(filename='Parser.log', level=logging.DEBUG)
log = logging.getLogger('Parser')

class Parser:
    def __init__(self, TOKEN):
        self.TOKEN = TOKEN

if __name__ == '__main__':
    print('parser')
    lexer = Lexer('QLight/code_0.txt')
    lexer.scanner()
    parser = Parser(lexer.getTOKEN())

