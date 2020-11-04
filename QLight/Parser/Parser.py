import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
sys.path.append(BASE_DIR) #添加环境变量
from Lexer.Lexer import Lexer
from Ast import SyntaxTree
from Ast import SyntaxTreeNode
import logging
logging.basicConfig(filename='Parser.log', level=logging.DEBUG)
log = logging.getLogger('Parser')

First = {
    '''
    根据grammar.txt中的文法生成First集
    这里手动填写，未来考虑自动生成
    '''
    'Argument': ['Identifier', 'Array'],
    'Measurement': ['measure'],
    'GateOp': ['I', 'X', 'Y', 'Z', 'H', 'S', 'T', 'V', 'V_H', 'SWAP'],
    'Factor': ['INT'],
    'Expression': ['INT'],
    'Bool': ['!', 'INT'],
    'IFStatement': ['if'],
    'WhileStatement': ['while'],
    'FuncStatement': ['func'],
    'Statement': ['I', 'X', 'Y', 'Z', 'H', 'S', 'T', 'V', 'V_H', 'SWAP', 'measure', 'if', 'while', 'func'],
    'Declare': ['Identifier'],
    'Program': ['Identifier'],
    'FuncCall': ['Identifier']
}

def log_func_call(func):
    def wrapper(*args, **kw):
        s = '函数: '+func.__name__
        for value in args:
            s += ' '+str(value)
        print(s)
        func(*args, **kw)
    return wrapper

class Parser:
    '''
    使用LL(1)文法
    递归下降生成语法树
    '''
    def __init__(self, TOKEN):
        self.EOF = [0, '$']
        self.TOKEN = TOKEN
        self.current_token = -1
        self.tree = SyntaxTree()
        self.lookahead = self.getNextToken()

    def display(self, node):
        '''DFS遍历语法树'''
        if not node:
            return
        # print('display')
        output = open('parser.txt', 'a')
        output.write('( self: %s %s, father: %s, left: %s, right: %s )\r\n' % (
        node.value, node.type, node.father.value if node.father else None, node.left.value if node.left else None,
        node.right.value if node.right else None))
        output.close()
        child = node.first_son
        while child:
            self.display(child)
            child = child.right

    def match(self, token):
        if self.lookahead[0] == token[0]:
            self.lookahead = self.getNextToken()

    def getNextToken(self):
        self.current_token += 1
        if self.current_token >= len(self.TOKEN):
            return self.EOF
        return self.TOKEN[self.current_token]

    @log_func_call
    def FuncStatement(self, token, father=None):
        if not father:
            father = self.tree.root
        Declare_tree = SyntaxTree()
        Declare_tree.current = Declare_tree.root = SyntaxTreeNode('FuncStatement')
        self.tree.add_child_node(Declare_tree.root, father)
        if token[0] != 105:
            raise ValueError('Failed to FuncStatement arguments: {}'.format(token))
        # 匹配 func
        self.match(token)
        if self.lookahead[0] == 500:
            # 匹配 函数名
            self.match(self.lookahead)
        if self.lookahead[0] == 300:
            # 匹配 (
            self.match(self.lookahead)
        else:
            raise ValueError('Failed to FuncStatement arguments: {}'.format(self.lookahead))
        '''匹配输入参数'''
        while self.lookahead[0] != 301:
            func_call_tree.add_child_node(
                SyntaxTreeNode(self.lookahead[1], self.lookahead[0]), params_list)
            self.match(self.lookahead)
        if self.lookahead[0] == 301:
            # 匹配 )
            self.match(self.lookahead)
        if self.lookahead[0] == 304:
            # 匹配 {
            '''大括号里面的内容'''
            while self.lookahead[0] != 305:
                self.Statement(Declare_tree)
            # 匹配 }
            self.match(self.lookahead)
            if self.lookahead[0] == 308:
                # 匹配 \n
                self.match(self.lookahead)
        else:
            raise ValueError('Failed to FuncStatement arguments: {}'.format(self.lookahead))

    def IFStatement(self, token, father=None):
        pass

    def WhileStatement(self, token, father=None):
        pass

    @log_func_call
    def Declare(self, token, father=None):
        if not father:
            father = self.tree.root
        Declare_tree = SyntaxTree()
        Declare_tree.current = Declare_tree.root = SyntaxTreeNode('Declare')
        self.tree.add_child_node(Declare_tree.root, father)
        if token[0] != 500:
            raise ValueError('Failed to Declare arguments: {}'.format(token))
        Declare_tree.add_child_node(
            SyntaxTreeNode(token[1], 'Identify'))
        self.match(token)
        if self.lookahead[0] == 406:
            # 匹配 =
            self.match(self.lookahead)
        else:
            raise ValueError('Failed to Declare arguments: {}'.format(token))
        '''有 整数赋值 和 函数调用赋值 两种方式'''
        if self.lookahead[0] == 600:
            # 匹配整数
            Declare_tree.add_child_node(
                SyntaxTreeNode(token[1], 'INT'))
            self.match(self.lookahead)
        elif self.lookahead[0] == 500 or self.lookahead[0] == 210 or self.lookahead[0] == 211:
            # 匹配函数调用
            Declare_tree.add_child_node(
                SyntaxTreeNode(token[1], 'FuncCall'))
            self.FuncCall(self.lookahead, Declare_tree.root)
        if self.lookahead[0] == 308:
            # 匹配 \n
            self.match(self.lookahead)

    @log_func_call
    def FuncCall(self, token, father=None):
        if not father:
            father = self.tree.root
        func_call_tree = SyntaxTree()
        func_call_tree.current = func_call_tree.root = SyntaxTreeNode('FuncCall')
        self.tree.add_child_node(func_call_tree.root, father)
        if token[0] != 500 and token[0] != 210 and token[0] != 211:
            raise ValueError('Failed to FuncCall arguments: {}'.format(token))
        # 匹配 函数名
        self.match(token)
        func_call_tree.add_child_node(
            SyntaxTreeNode(token[1], 'FuncCall_Name'))
        if self.lookahead[0] == 300:
            # 匹配 (
            self.match(self.lookahead)
        else:
            raise ValueError('Failed to FuncCall arguments: {}'.format(token))
        params_list = SyntaxTreeNode('FuncCallParameterList')
        func_call_tree.add_child_node(params_list, func_call_tree.root)
        while self.lookahead[0] != 301:
            func_call_tree.add_child_node(
                SyntaxTreeNode(self.lookahead[1], self.lookahead[0]), params_list)
            self.match(self.lookahead)
        if self.lookahead[0] == 301:
            # 匹配 )
            self.match(self.lookahead)
        if self.lookahead[0] == 308:
            # 匹配 \n
            self.match(self.lookahead)
    @log_func_call
    def GateOp(self, token, father=None):
        if not father:
            father = self.tree.root
        GateOp_tree = SyntaxTree()
        GateOp_tree.current = GateOp_tree.root = SyntaxTreeNode('GateOp')
        if token[1] not in First['GateOp']:
            raise ValueError('Failed to GateOp arguments: {}'.format(token))
        # 匹配 操作门
        self.match(token)
        GateOp_tree.add_child_node(
            SyntaxTreeNode(token[1], 'GateOp_Name'))
        params_list = SyntaxTreeNode('GateOpParameterList')
        GateOp_tree.add_child_node(params_list, GateOp_tree.root)
        self.tree.add_child_node(GateOp_tree.root, father)
        while self.lookahead[0] != 308:
            if self.lookahead[0] == 500:
                # Identify
                self.match(self.lookahead)
            if self.lookahead[0] == 302:
                # [
                self.match(self.lookahead)
            if self.lookahead[0] == 600:
                # INT
                GateOp_tree.add_child_node(
                    SyntaxTreeNode(self.lookahead[1], self.lookahead[0]), params_list)
                self.match(self.lookahead)
            if self.lookahead[0] == 303:
                # ]
                self.match(self.lookahead)
        if self.lookahead[0] == 308:
            # 匹配 \n
            self.match(self.lookahead)

    @log_func_call
    def Statement(self, father_tree):
        '''
        处理大括号里面的内容，如 if while func
        '''
        sentence_tree = SyntaxTree()
        sentence_tree.current = sentence_tree.root = SyntaxTreeNode('Statement')
        father_tree.add_child_node(sentence_tree.root, father_tree.root)
        while self.lookahead[0] != 305:
            self.lookahead = self.getNextToken()
            if self.lookahead[0] >= 100 and self.lookahead[0] < 200:
                '''关键词'''
                if self.lookahead[1] in First['FuncStatement']:
                    self.FuncStatement(self.lookahead, sentence_tree.root)
                elif self.lookahead[1] in First['IFStatement']:
                    self.IFStatement(self.lookahead, sentence_tree.root)
                elif self.lookahead[1] in First['WhileStatement']:
                    self.WhileStatement(self.lookahead, sentence_tree.root)
                pass
            elif self.lookahead[0] >= 200 and self.lookahead[0] < 300:
                '''电路操作'''
                if self.lookahead[1] in First['GateOp']:
                    self.GateOp(self.lookahead, sentence_tree.root)
                pass
            elif self.lookahead[0] >= 300 and self.lookahead[0] < 400:
                '''分隔符'''
                pass
            elif self.lookahead[0] >= 400 and self.lookahead[0] < 500:
                '''运算符'''
                pass
            elif self.lookahead[0] == 500:
                '''标志符'''
                if self.TOKEN[self.current_token+1][1] == '=':
                    self.Declare(self.lookahead, sentence_tree.root)
                elif self.TOKEN[self.current_token+1][1] == '(':
                    self.FuncCall(self.lookahead, sentence_tree.root)
                pass
            elif self.lookahead[0] == 600:
                '''整数'''
                pass

    @log_func_call
    def main(self):
        self.tree.current = self.tree.root = SyntaxTreeNode('Program')
        while self.lookahead[0] != 0:
            if self.lookahead[0] >= 100 and self.lookahead[0] < 200:
                '''关键词'''
                if self.lookahead[1] in First['FuncStatement']:
                    self.FuncStatement(self.lookahead)
                elif self.lookahead[1] in First['IFStatement']:
                    self.IFStatement(self.lookahead)
                elif self.lookahead[1] in First['WhileStatement']:
                    self.WhileStatement(self.lookahead)
                pass
            elif self.lookahead[0] >= 200 and self.lookahead[0] < 300:
                '''电路操作'''
                if self.lookahead[1] in First['GateOp']:
                    self.GateOp(self.lookahead)
                pass
            elif self.lookahead[0] >= 300 and self.lookahead[0] < 400:
                '''分隔符'''
                pass
            elif self.lookahead[0] >= 400 and self.lookahead[0] < 500:
                '''运算符'''
                pass
            elif self.lookahead[0] == 500:
                '''标志符'''
                if self.TOKEN[self.current_token+1][1] == '=':
                    self.Declare(self.lookahead)
                elif self.TOKEN[self.current_token+1][1] == '(':
                    self.FuncCall(self.lookahead)
                pass
            elif self.lookahead[0] == 600:
                '''整数'''
                pass

if __name__ == '__main__':
    print('parser')
    lexer = Lexer('QLight/code_0.txt')
    lexer.scanner()
    log.debug(lexer.getTOKEN())
    parser = Parser(lexer.getTOKEN())
    parser.main()
    parser.display(parser.tree.root)
