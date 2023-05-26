import sys
sys.path.append('./gen-py')
  
# my替换为你的thrift的文件名，如：abc.thrift就替换成abc
# MyRpc替换成IDL文件中定义的service名，命名：service MyRpc{...}就替换成MyRpc
from test import TestRpc
from test.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

# import socket

# 这里需要实现IDL文件my.thrift里定义的接口：login
class MyRpcHandler:
    def dosomething(self, age, passwd):
        print(' passwd: ' + passwd)
        return True


handler = MyRpcHandler()
processor = TestRpc.Processor(handler)
# 监听端口
transport = TSocket.TServerSocket('127.0.0.1',30303)
# 选择传输层
tfactory = TTransport.TBufferedTransportFactory()
# 选择传输协议
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

# 创建服务端 这里可选择几种方式提供服务，还有：
# 1. TSimpleServer：单线程服务器端，使用标准的阻塞式I/O;
# 2. TThreadedServer：为每个 client 请求创建单独的线程进行业务处理，所以同一个client的请求都是顺序处理的 ;
# 3. TThreadPoolServer：预先建立一个线程池（self.threads）,每个线程负责从队列 clients 中获取客户端连接TSocket 对象进行处理
# 等等...
server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

print("Starting python server...")
# 启动服务
server.serve()
print("done!")
