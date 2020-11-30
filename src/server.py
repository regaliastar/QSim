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
from route import Route

class QS:
    def load(self, dic):
        try:
            print('in load')
            dic = json.loads(dic)
            if dic['route'] == 'debug':
                if dic['source_code'] == '':
                    return 'source_code is empty!'
                result = Route.debug(dic)
                return result
            if dic['route'] == 'le':
                if dic['source_code'] == '':
                    return 'source_code is empty!'
                result = Route.le(dic['source_code'])
                return result
            if dic['route'] == 'ast':
                if dic['source_code'] == '':
                    return 'source_code is empty!'
                result = Route.ast(dic['source_code'])
                return result
            if dic['route'] == 'tpy':
                if dic['source_code'] == '':
                    return 'source_code is empty!'
                result = Route.tpy(dic['source_code'])
                return result

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
