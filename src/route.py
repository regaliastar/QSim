import os
import sys
import json
import yaml

from QLight.Lexer.Lexer import Lexer
from QLight.Parser.Parser import Parser
from QLight.Interp.Trans import Translate
from lib.QSim import QuantumRegister
from lib.QSim import Tools

# 读取配置文件
def guessPackaged():
    return os.path.basename(os.getcwd()) != 'QSim'
yaml_path = ''
print('guessPackaged: {}'.format(guessPackaged()))
if guessPackaged():
    # 已经打包
    yaml_path = os.path.join(os.path.abspath("."), "..", "_config.yml")
else:
    # 没有打包
    yaml_path = os.path.join(os.path.abspath("."), "_config.yml")
yaml_file = open(yaml_path, 'r', encoding="utf-8")
file_data = yaml_file.read()
yaml_file.close()
yaml_data = yaml.load(file_data)

class Route:
    def debug(dic):
        print('debug')
        lexer = Lexer(code=dic['source_code'])
        lexer.scanner()
        lexer.log()
        parser = Parser(lexer.getTOKEN())
        parser.parse()
        parser.log()
        translate = Translate(parser.tree)
        translate.main()
        symbalTable = translate.getSymbalTable()
        translate.log(file_name=yaml_data['_filepath'])
        result = translate.getResult()

        # 定义命名空间
        namespace = {}
        
        # 执行脚本
        exec(result, namespace)
        message = {
            'info': namespace['_wf'],
            'wave_func': '波函数'+namespace['_wf'],
            't_cost': namespace['t_cost'],
            'memory_cost': namespace['memory_cost'],
            'show': [],
            'MessageType': 'info',
            'symbalTable': symbalTable
        }
        # 解析符号表中的show字段
        for index, dic in enumerate(symbalTable['show']): 
            value = ''
            for k in dic:
                value = dic[k]
            if value == None:
                message['show'].append(namespace['_wf'],)
            elif not value.isdigit():
                message['show'].append(str(namespace[value]))
        msg_str = json.dumps(message)

        # 初始化变量 !important
        del message['show']
        message['show'] = []
        translate.initSymbalTable()

        return msg_str
    
    def quit():
        print('quit')

    def le(source_code):
        print('lexer')
        lexer = Lexer(code=source_code)
        lexer.scanner()
        return lexer.getTOKEN()

    def tpy(source_code):
        print('tpy')
        lexer = Lexer(code=source_code)
        lexer.scanner()
        parser = Parser(lexer.getTOKEN())
        parser.parse()
        translate = Translate(parser.tree)
        translate.main()
        symbalTable = translate.getSymbalTable()
        return translate.getResult()
    
    def shell():
        pass