import sys

from chat import ChatService
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class ChatHandler:
    messages = []

    def sendMessage(self, message):
        self.messages.append(message)

    def getMessages(self):
        return self.messages

if __name__ == '__main__':
    handler = ChatHandler()
    processor = ChatService.Processor(handler)
    transport = TSocket.TServerSocket(port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # 创建线程池
    server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
    server.setNumThreads(10)  # 设置线程池大小为10

    print('Starting the server...')
    server.serve()
    print('done.')
