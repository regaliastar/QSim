import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
sys.path.append(BASE_DIR) #添加环境变量
import json
import traceback
import yaml
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from genpy.interface import userService

from QLight.Lexer.Lexer import Lexer
from QLight.Parser.Parser import Parser
from QLight.Interp.Trans import Translate

# 读取配置文件
yaml_path = os.path.join(os.path.abspath("."),"..", "_config.yml")
yaml_file = open(yaml_path, 'r', encoding="utf-8")
file_data = yaml_file.read()
yaml_file.close()
yaml_data = yaml.load(file_data)


class QS:
    def load(self, dic):
        print('in load')
        dic = json.loads(dic)
        if dic['source_code'] == '':
            return 'source_code is empty!'
        try:
            lexer = Lexer(code=dic['source_code'])
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
            
            return json.dumps(message)
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
