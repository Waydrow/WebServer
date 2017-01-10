#!usr/bin/python
# -*- coding: utf-8 -*-

'''
    create time: 2016.12.11
    author: Waydrow
    connect: waydrow@163.com
    blog: blog.waydrow.com
'''

import os, socket, threading
from datetime import datetime
from Base.casefile import case_always_fail, \
    case_existing_file, case_no_file, \
    case_directory_index_file, case_cgi_file, \
    case_php_file,\
    ServerException

class HttpServer:

    def __init__(self, serverAddr, RequestHandler):
        self.serverAddr = serverAddr
        self.requestHandler = RequestHandler

    def serve_forever(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind(self.serverAddr)
        server_sock.listen(10)

        while True:
            print "Waiting for connection..."
            clientsock, addr = server_sock.accept()
            print "received from: ", addr
            # 创建一个线程处理请求, 实现多线程
            thread = threading.Thread(target=self.startThread, args=(clientsock, addr, ))
            thread.setDaemon(True)
            thread.start()
            # handler = RequestHandler(clientsock, addr)

        # 关闭连接
        server_sock.close()

    def startThread(self, clientsock, addr):
        # 调用 RequestHandler
        handler = RequestHandler(clientsock, addr)

class HttpRequestHandler:
    bufsize = 1024
    http_response = "HTTP/1.1 "
    # Server接收到GET请求时 isGet = True, 接收到Post请求时isPost = True
    isPost = False
    isGet = False

    def __init__(self, clientsock, addr):
        self.clientsock = clientsock
        self.client_address = addr
        self.date_time_string = datetime.now()
        self.analyze()

    def analyze(self):
        # 接收数据, bufsize指明一次性读取的数据量
        data = self.clientsock.recv(self.bufsize)

        # 去除多余空格
        if data.replace(" ", "") == "":
            print "data为空"
            return

        # 按照 \r\n 回车换行 分行
        data = data.split('\r\n')
        print 'http data', data

        # 取第一行报文
        firstLine = data[0]
        arr = firstLine.split(' ')
        # 请求方式 Get/Post/...
        self.command = arr[0]
        # http
        self.protocol = arr[2]

        # 判断请求方式
        if self.command == "POST":
            self.isPost = True
            # 获取请求路径
            self.path = arr[1]
            # 获取报文中携带的参数
            self.paramStr = data[-1]
            # 若没有参数, 将paramStr置为None
            if self.paramStr == "":
                self.paramStr = None

        elif self.command == "GET":
            self.isGet = True
            # 取参数
            if '?' in arr[1]:
                # 带参数
                self.path, self.paramStr = arr[1].split('?')
            else:
                self.path = arr[1]
                self.paramStr = None

        else:
            pass

        # 保存请求信息的headers
        self.headers = {}
        for line in data[1:]:
            if ':' in line:
                key, value = line.split(':', 1)
                self.headers[key] = value
        # 按照请求方式分为调用不同的函数处理
        if self.isPost:
            self.do_POST()
        elif self.isGet:
            self.do_GET()
        else:
            pass
        # time.sleep(20)

    # 发送响应
    def send_response(self, status):
        if status == 200:
            self.http_response += "200 " + "OK"
        elif status == 404:
            self.http_response += "404 " + "Not found"
        self.http_response += "\r\n"

    # 发送headers
    def send_header(self, key, value):
        self.http_response += str(key) + ": " + str(value) + "\r\n"

    # 结束headers
    def end_header(self):
        self.http_response += "\r\n"

    # socket回复, 回复信息
    def write(self, page):
        self.http_response += str(page)
        self.clientsock.send(self.http_response)
        self.clientsock.close()


class RequestHandler(HttpRequestHandler):
    '''处理请求并返回页面'''

    # 页面模板
    Page = '''\
        <html>
        <body>
        <table border=1s>
            <tr> <td>Header</td> <td>Value</td> </tr>
            <tr> <td>Date and time</td> <td>{date_time}</td> </tr>
            <tr> <td>Client host</td> <td>{client_host}</td> </tr>
            <tr> <td>Client port</td> <td>{client_port}</td> </tr>
            <tr> <td>Command</td> <td>{command}</td> </tr>
            <tr> <td>Path</td> <td>{path}</td> </tr>
        </table>
        </body>
        </html>
    '''

    Error_Page = """\
    <html>
    <body>
    <h1>你走错地方了哦!</h1>
    <h1>没有找到 {path}</h1>
    <p>{msg}</p>
    </body>
    </html>
    """

    # 请求的各种情况的集合
    Cases = [case_no_file(),
             case_cgi_file(),
             case_php_file(),
             case_existing_file(),
             case_directory_index_file(),
             case_always_fail()]

    # 处理 get 请求
    def do_GET(self):
        try:
            # 文件完整路径
            self.full_path = os.getcwd() + self.path

            # 遍历所有可能的情况
            for case in self.Cases:
                handler = case
                # 如果满足该类情况
                if handler.test(self):
                    handler.act(self)
                    break

        except Exception as msg:
            self.handle_error(msg)

    # 处理 post 请求
    def do_POST(self):
        try:
            # 文件完整路径
            self.full_path = os.getcwd() + self.path

            # 遍历所有可能的情况
            for case in self.Cases:
                handler = case
                # 如果满足该类情况
                if handler.test(self):
                    handler.act(self)
                    break

        except Exception as msg:
            self.handle_error(msg)

    # 发送content内容, type参数标志请求文件的格式, 默认为html
    def send_content(self, content, status = 200, type = 'html'):
        self.send_response(status)
        # 根据文件格式写入不同的content-type
        if type == 'css':
            self.send_header("Content-Type", "text/css; charset=utf-8")
        elif type == 'js':
            self.send_header("Content-type", "text/javascript; charset=utf-8")
        elif type == 'png':
            self.send_header("Content-type", "image/png")
        elif type == 'jpg':
            self.send_header("Content-type", "image/jpg")
        elif type == 'gif':
            self.send_header("Content-type", "image/gif")
        else:
            self.send_header("Content-Type", "text/html")
        # 写入content-length
        self.send_header("Content-Length", str(len(content)))
        self.end_header()
        self.write(content)

    # 404
    def handle_error(self, msg):
        content = self.Error_Page.format(path = self.path, msg = msg)
        self.send_content(content, 404)

if __name__ == '__main__':
    serverAddress = ('127.0.0.1', 8081)
    server = HttpServer(serverAddress, RequestHandler)
    server.serve_forever()
