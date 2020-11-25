import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
sys.path.append(BASE_DIR) #添加环境变量
import json
import yaml
import time
from enum import Enum

from QLight.Lexer.Lexer import Lexer
from QLight.Parser.Parser import Parser
from QLight.Interp.Trans import Translate

# 读取配置文件
yaml_path = os.path.join(os.path.abspath("."), "_config.yml")
yaml_file = open(yaml_path, 'r', encoding="utf-8")
file_data = yaml_file.read()
yaml_file.close()
yaml_data = yaml.load(file_data)

'''
测试 service.py的内容

log打印位置 QSim/log
'''
if __name__ == "__main__":

    source_code1 = '''quantum(4)
    H 0
    X 0 1
    m1 = measure(0)
    show(0)
    show(m1)
    show()'''
    lexer = Lexer(code=source_code1)
    lexer.scanner()
    lexer.log() # views/log 

    parser = Parser(lexer.getTOKEN())
    parser.parse()
    parser.log()
    
    translate = Translate(parser.tree)
    translate.main()
    symbalTable = translate.getSymbalTable()
    translate.log(file_name=yaml_data['_filepath'])
    result = translate.getResult()
    print(symbalTable)
    namespace = {}
    exec(result, globals())
    message = {
        'info': globals()[symbalTable['_wf']],
        'wave_func': globals()[symbalTable['_wf']],
        't_cost': globals()[symbalTable['t_cost']],
        'show': [],
        'MessageType': 'info'
    }
    for index, dic in enumerate(symbalTable['show']): 
        value = dic[str(index)]
        print('{}, {}'.format(dic ,value)) 
        if value == None:
            message['show'].append(globals()[symbalTable['_wf']])
        elif not value.isdigit():
            print('value : {}'.format(globals()[value]))
            message['show'].append(str(globals()[value]))
        
    print(json.dumps(message))
