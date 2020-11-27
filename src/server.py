import os
import sys
import json
import traceback
import yaml
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
sys.path.append(BASE_DIR) #添加环境变量

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


from Interface.genpy.interface import userService
from QLight.Lexer.Lexer import Lexer
from QLight.Parser.Parser import Parser
from QLight.Interp.Trans import Translate
from lib.QSim import QuantumRegister
from lib.QSim import Tools


class QS:
    def load(self, dic):
        print('in load')
        dic = json.loads(dic)
        if dic['source_code'] == '':
            return 'source_code is empty!'
        try:
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
        except Exception as e:
            trace_info = traceback.format_exc()
            message = {
                'info': str(e)+'\n'+str(trace_info),
                'MessageType': 'error'
            }
            return json.dumps(message)

if __name__ == "__main__":
    print('call main')
    port = yaml_data['_connect']['port']
    ip = yaml_data['_connect']['ip']
    handler = QS()
    processor = userService.Processor(handler) 
    transport = TSocket.TServerSocket(ip, port)
    # transport layer
    tfactory = TTransport.TBufferedTransportFactory()
    # binary transport protocol
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    # create server
    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    print("start server")
    server.serve()
