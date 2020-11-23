import json
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from genpy.interface import userService

class QS:
    def load(self, dic):
        dic = json.loads(dic)
        return f'QS, {dic["name"]}!'

if __name__ == "__main__":
    port = 8000
    ip = "127.0.0.1"
    handler = QS()
    processor = userService.Processor(handler) 
    transport = TSocket.TServerSocket(ip, port)
    # transport layer
    tfactory = TTransport.TBufferedTransportFactory()
    # transport protocol
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    # create server
    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    print("start server in python")
    server.serve()
    print("Done")