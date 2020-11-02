from Lexer.Lexer import Lexer
from Parser.Parser import Parser
import logging
logging.basicConfig(filename='main.log', level=logging.DEBUG)
log = logging.getLogger('main')

def main(filename):
    lexer = Lexer(filename)
    lexer.scanner()
    log.debug(lexer.getTOKEN())
    parser = Parser(lexer.getTOKEN())

if __name__ == '__main__':
    print('main')
    main('QLight/code_0.txt')
