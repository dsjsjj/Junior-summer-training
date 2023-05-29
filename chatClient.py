import sys

from chat import ChatService
from chat.ttypes import Message

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QFileDialog
from PyQt5.QtCore import QTimer, Qt

class ChatClient(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.transport = TSocket.TSocket('localhost', 9090)
        self.transport = TTransport.TBufferedTransport(self.transport)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = ChatService.Client(self.protocol)

        self.transport.open()

        self.lastMessageCount = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.getMessages)
        self.timer.start(1000)

    def initUI(self):
        self.setWindowTitle('Chat Client')
        self.resize(600, 500)

        self.messages = QTextEdit()
        self.messages.setReadOnly(True)

        self.input = QTextEdit()

        self.sendButton = QPushButton('发送消息')
        self.sendButton.clicked.connect(self.sendMessage)

        self.fileButton = QPushButton('发送文件')
        self.fileButton.clicked.connect(self.sendFile)

        self.sendButton.setFixedSize(100, 30)
        self.fileButton.setFixedSize(100, 30)
        self.sendButton.setStyleSheet('background-color: blue; color: white;')
        self.fileButton.setStyleSheet('background-color: blue; color: white;')

        vbox = QVBoxLayout()
        vbox.addWidget(self.messages)
        vbox.addWidget(self.input)

        hbox = QHBoxLayout()
        hbox.addWidget(self.sendButton)
        hbox.addWidget(self.fileButton)

        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def sendMessage(self):
        message = Message()
        message.text = self.input.toPlainText()
        self.client.sendMessage(message)
        self.input.clear()  # 清空发送框

    def sendFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '.', 'All Files (*)')

        message = Message()
        message.text = filename
        self.client.sendMessage(message)

    def getMessages(self):
        messages = self.client.getMessages()
        if len(messages) > self.lastMessageCount:
            newMessages = messages[self.lastMessageCount:]
            for message in newMessages:
                if message.filename:
                    with open(message.filename, 'wb') as f:
                        f.write(message.data)
                else:
                    self.messages.append(message.text)
            self.lastMessageCount = len(messages)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = ChatClient()
    client.show()
    sys.exit(app.exec_())
