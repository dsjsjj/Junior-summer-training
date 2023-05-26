import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QPushButton, QLabel
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from ImageService import ImageService

class MainWindow(QMainWindow):      #创建一个MainWindow类，继承自QMainWindow类
    def __init__(self):     #定义构造函数，包含类的主要逻辑
        super().__init__()      #调用QmainWindows类的构造函数初始化MainWindow类的基类

        self.resize(800, 600)
        # 创建选择图片按钮
        self.selectButton = QPushButton("选择图片", self)       #创建一个按钮名为选择图片，并添加到MainWindow中
        self.selectButton.clicked.connect(self.selectImage)     #按钮点击后，将信号连接到到selectImage函数
        self.selectButton.setGeometry(10, 10, 100, 30)      #设置selectButton按钮的位置和大小（左上角横坐标，左上角纵坐标，宽度，高度）

        # 创建发送按钮
        self.sendButton = QPushButton("发送", self)       #创建一个按钮，名为发送，并添加到MainWindow
        self.sendButton.clicked.connect(self.sendImage)     #将点击按钮之后的信号，连接到sendImage函数
        self.sendButton.setGeometry(120, 10, 100, 30)       #设置位置和大小（左上角横坐标，左上角纵坐标，宽度，高度）
        self.sendButton.setEnabled(False)           #将sendButton按钮设置为不可用状态

        # 创建图片显示区域
        self.imageLabel = QLabel(self)              #创建一个名为imageLabel的标签，并将标签添加到QMainWindow中
        self.imageLabel.setGeometry(10, 50, 300, 300)       #设置imageLabel标签的位置和大小（左上角横坐标，左上角纵坐标，宽度，高度）

        # 初始化thrift客户端
        self.transport = TSocket.TSocket("localhost", 9090)         #创建一个名为transport的Socket对象，用于与服务器通信
        self.transport = TTransport.TBufferedTransport(self.transport)      #创建一个TBufferedTransport对象，用于对transport对象进行缓冲
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)     #常见了一个名为protocol的TBinaryProtocol对象，用于对transport序列化和反序列化
        self.client = ImageService.Client(self.protocol)            #创建了一个名为client的ImageService.Client对象，用于与服务器通信

    def selectImage(self):          #创建发送图片的函数
        # 选择要发送的图片
        fileName, _ = QFileDialog.getOpenFileName(self, "选择图片", ".", "Images (*.png *.xpm *.jpg)")      #调用QFileDialog的getOpenFileName方法，用于选择图片

        # 如果用户取消选择，则退出函数
        if not fileName:        #用户没有选择，则退出函数
            return

        # 加载图片
        pixmap = QPixmap(fileName)          #加载选择的图片

        # 如果图片加载失败，则提示用户并退出函数，图片过大，则无法加载并报错
        if pixmap.isNull():
            QMessageBox.critical(self, "错误", "无法加载图片")   #是一个弹出对话框，用于提示用户发生了错误。其中，第一个参数self表示对话框的父窗口，第二个参数"错误"表示对话框的标题，第三个参数"无法加载图片"表示对话框的内容。
            return

        # 显示图片
        self.imageLabel.setPixmap(pixmap)       #显示图片
        self.sendButton.setEnabled(True)        #将发送按钮的状态设置为可用
        self.fileName = fileName            #记录选择的图片文件名

    def sendImage(self):
        # 打开thrift连接
        self.transport.open()       #调用open方法打开连接

        # 发送图片
        with open(self.fileName, "rb") as f:        #打开选择的图片文件，读取为二进制，与thrift的类型一致
            data = f.read()             ##将读取的二进制数据保存到data变量中
            self.client.saveImage(self.fileName, data)      #调用client对象的saveImage方法，将数据保存到thrift服务器中

        # 关闭thrift连接
        self.transport.close()      #关闭连接

        # 提示用户保存成功
        QMessageBox.information(self, "提示", "保存图片成功")       #弹出消息框，提示保存成功

app = QApplication(sys.argv)        #创建一个app的QApplication对象
window = MainWindow()       #创建一个名为window的MainWindow对象
window.show()           #显示MainWindow对象
sys.exit(app.exec_())       #运行程序，等待用户操作
