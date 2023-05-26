#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/26 14:12
# @Author  : Shark
# @Site    : 
# @File    : workServer.py
# @Software: PyCharm
import sys
import os
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from ImageService import ImageService

class ImageServiceHandler(ImageService.Iface):      #定义了一个名为ImageServiceHandler的类，继承自ImageService.Iface
    def saveImage(self, fileName, data):        #定义了一个saveImage保存图片的函数，用于保存客户端发来的图片
        # 保存图片
        with open(fileName, "wb") as f:     #打开指定的文件夹，并将其以二进制的写入模式打开
            f.write(data)           #写入data二进制数据

        # 提示保存成功
        print("保存图片成功，保存的文件名称为%s" % fileName)       #提示保存成功

# 创建thrift服务端
handler = ImageServiceHandler()         #创建一个handler的ImageServiceHandler对象，处理客户端发送的请求
processor = ImageService.Processor(handler)     #创建一个processor的ImageService.Processor对象，处理客户端发送的请求
transport = TSocket.TServerSocket(port=9090)        #创建一个名为transport的TSocket对象，用于监听9090端口
tfactory = TTransport.TBufferedTransportFactory()       #创建一个名为tfactory的 TTransport.TBufferedTransportFactory对象，用于对transport进行缓冲
pfactory = TBinaryProtocol.TBinaryProtocolFactory()     #创建了一个名为pfactory的TBinaryProtocolFactory对象，用于对transport对象进行序列化和反序列化

# 启动thrift服务端
server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)    #创建了一个名为server的TThreadPoolServer对象，用于处理客户端发送的请求。
print("Starting thrift server...")
server.serve()      #启动thrift服务端，等待客户端发送请求。
