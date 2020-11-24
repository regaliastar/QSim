import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
sys.path.append(BASE_DIR) #添加环境变量
import json
import yaml

from QLight.Lexer.Lexer import Lexer
from QLight.Parser.Parser import Parser
from QLight.Interp.Trans import Translate

# 读取配置文件
yaml_path = os.path.join(os.path.abspath("."), "_config.yml")
yaml_file = open(yaml_path, 'r', encoding="utf-8")
file_data = yaml_file.read()
yaml_file.close()
yaml_data = yaml.load(file_data)

if __name__ == "__main__":

    source_code = '''quantum(4)
    H 0
    X 0 1'''
    lexer = Lexer(code=source_code)
    lexer.scanner()
    lexer.log() # views/log 
    parser = Parser(lexer.getTOKEN())
    parser.parse()
    parser.log()
    
    translate = Translate(parser.tree)
    translate.main()
    # translate.log(file_name=yaml_data['_filepath'])
    result = translate.getResult()
    _wf = ''
    namespace = {}
    exec(compile(result, '<string>', 'exec'), locals() ,namespace)
    print('_wf: {}'.format(namespace['_wf']))
    # print(json.dumps(result))
