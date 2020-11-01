from Token import Token
import logging
logging.basicConfig(filename='Lexer.log', level=logging.DEBUG)
log = logging.getLogger('Lexer')

class Lexer:
    def __init__(self, file_path):
        self.current_raw = 0
        self.current_column = -1
        self.EOF = '\0'
        self.source_code = self.read_source_code(file_path)
        self.TOKEN = []

    def read_source_code(self, file_path):
        f = open(file_path, "r")
        source_code = f.readlines()
        f.close()
        return source_code

    def getNextChar(self):
        self.current_column += 1
        if self.current_raw >= len(self.source_code):
            return self.EOF
        if self.current_column >= len(self.source_code[self.current_raw]):
            self.current_raw += 1
            self.current_column = -1
            return '\\n'
        return self.source_code[self.current_raw][self.current_column]

    def back(self):
        if self.current_column != -1:
            self.current_column -= 1
        else:
            self.current_raw -= 1
            self.current_column = len(self.source_code[self.current_raw])

    def recognizeId(self, ch):
        '''
        识别单词 Identity
        :param ch:
        :return:
        '''
        state = 0
        str = ''
        while state != 2:
            if state == 0:
                if ch.isalpha() or ch == '_':
                    state = 1
                    str += ch
                else:
                    raise ValueError('Failed to recognizeId ch: {}'.format(ch))
            if state == 1:
                ch = self.getNextChar()
                if ch.isalpha() or ch.isdigit() or ch == '_':
                    state = 1
                    str += ch
                else:
                    state = 2
        self.back()
        return str

    def recognizeOp(self, ch):
        '''
        识别操作数 OPERATOR
        :param ch:
        :return:
        '''
        state = 0
        str = ''
        while state != 2:
            if state == 0:
                if Token.isOPERATOR(ch):
                    state = 0
                    str += ch
                else:
                    raise ValueError('Failed to recognizeOp ch: {}'.format(ch))
            if state == 1:
                ch = self.getNextChar()
                if not Token.isOPERATOR(ch):
                    state = 1
                    str += ch
                else:
                    state = 2
        self.back()
        return str

    def scanner(self):
        ch = ''
        while ch != '\0':
            ch = self.getNextChar()
            if ch == ' ':
                log.debug(ch)
                pass
            elif ch == '\n':
                pass
            elif ch.isalpha() or ch == '_':
                Identify = self.recognizeId(ch)
                if Token.isKEYWORD(Identify):
                    pass
                elif Token.isCIRCUIT(Identify):
                    pass
                log.debug(Identify)
            elif Token.isOPERATOR(ch):
                Op = self.recognizeOp(ch)
                log.debug(Op)
                pass
            elif Token.isSEPARATOR(ch):
                pass
            else:
                pass
                log.debug(ch)


if __name__ == '__main__':
    lexer = Lexer('QLight/code_0.txt')
    lexer.scanner()
