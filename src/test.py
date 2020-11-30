import os
import sys
import json
import traceback
import yaml

from Interface.genpy.interface import userService

from QLight.Lexer.Lexer import Lexer
from QLight.Parser.Parser import Parser
from QLight.Interp.Trans import Translate

from route import Route

# 读取配置文件
# yaml_path = os.path.join(os.path.abspath("."), "_config.yml")
# yaml_file = open(yaml_path, 'r', encoding="utf-8")
# file_data = yaml_file.read()
# yaml_file.close()
# yaml_data = yaml.load(file_data)

# print('basename: {}'.format(os.path.basename(os.getcwd()) == 'QSim'))
# '''
# 测试 service.py的内容

# log打印位置 QSim/log
# '''
# if __name__ == "__main__":

#     source_code1 = '''quantum(4)
#     H 0
#     X 0 1
#     m1 = measure(0)
#     show(0)
#     show(m1)
#     show()'''
#     lexer = Lexer(code=source_code1)
#     lexer.scanner()
#     lexer.log() # views/log 

#     parser = Parser(lexer.getTOKEN())
#     parser.parse()
#     parser.log()
    
#     translate = Translate(parser.tree)
#     translate.main()
#     symbalTable = translate.getSymbalTable()
#     translate.log(file_name=yaml_data['_filepath'])
#     result = translate.getResult()
#     print(symbalTable)
#     namespace = {}
#     exec(result, namespace)
#     # print('namespace: {}'.format(namespace))
#     message = {
#         'info': namespace['_wf'],
#         'wave_func': namespace['_wf'],
#         't_cost': namespace['t_cost'],
#         'show': [],
#         'MessageType': 'info'
#     }
#     for index, dic in enumerate(symbalTable['show']): 
#         value = dic[str(index)]
#         if value == None:
#             message['show'].append(namespace['_wf'],)
#         elif not value.isdigit():
#             message['show'].append(str(namespace[value]))
        
#     print(json.dumps(message))

source_code1 = '''quantum(4)
H 0
X 0 1
m1 = measure(0)
show(0)
show(m1)
show()'''
dic1 = {
    '_filepath': 'log/gene.py',
    '_algo': 'DAG',
    'route': 'debug',
    'source_code': source_code1
}
if __name__ == "__main__":
    res = Route.debug(dic1)
    print(res)
    pass