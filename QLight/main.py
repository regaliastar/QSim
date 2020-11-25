from Lexer.Lexer import Lexer
from Parser.Parser import Parser
from Interp.Trans import Translate
import logging
logging.basicConfig(filename='log/main.log', level=logging.DEBUG)
log = logging.getLogger('main')

if __name__ == '__main__':
    print('main')
    lexer = Lexer(file_path='QLight/code_2.txt')
    print(lexer.source_code)
    lexer.scanner()
    lexer.log()
    parser = Parser(lexer.getTOKEN())
    parser.parse()
    parser.log()
    translate = Translate(parser.tree)
    translate.main()
    symbalTable = translate.getSymbalTable()
    print(symbalTable)
    translate.log()
