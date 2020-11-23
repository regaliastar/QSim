import json
import yaml
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
sys.path.append(BASE_DIR) #添加环境变量
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
            translate.log()
            # translate.log(file_name=yaml_data['_filepath'])
            result = translate.getResult()
            return json.dumps(result)
        except Exception:
            return json.dumps(Exception)

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
    print("start server in python")
    server.serve()
    print("Done")