import sys
sys.path.append('./gen-py')
 
# my替换为你的thrift的文件名，如：abc.thrift就替换成abc
# MyRpc替换成IDL文件中定义的service名，命名：service MyRpc{...}就替换成MyRpc
from test import TestRpc
from test.ttypes import *
from test.constants import *
 
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
 
try:
    # Make socket
    transport = TSocket.TSocket('127.0.0.1', 30303)
     
    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)
     
    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
     
    # Create a client to use the protocol encoder
    client = TestRpc.Client(protocol)  # MyRpc替换成IDL文件中定义的service名，命名：service MyRpc{...}就替换成MyRpc
     
    # 连接服务端
    transport.open()   
     
    # 这里客户端调用login实际是通过rpc方式调用服务端的login功能，就如在本地调用login一样
    ret = client.dosomething(23, '12345')
    print(ret)

    transport.close()
          
except Thrift.TException as tx:
    print("%s" % (tx.message))
