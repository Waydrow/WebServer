# !/usr/bin/python
# -*- coding: utf-8 -*-

'''
    create time: 2016.12.20
    author: Waydrow
    connect: waydrow@163.com
    blog: blog.waydrow.com
'''

import BaseHTTPServer, SocketServer, cgi
from os import curdir, sep, path

# 页面模板
uploadhtml = '''\
<html><body>
<p>xxx</p>
<form enctype="multipart/form-data" action="/" method="post">
<p>File: <input type="file" name="filename"></p>
<p><input type="submit" value="upload"></p>
</form>
</body></html>
'''


class WebHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        # 若请求为根路径
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(uploadhtml)
            return
        try:
            f = open(curdir + sep + self.path)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'], })
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write('<Html>upload success<br/><br/>')
        self.wfile.write('client: %s<br/>' % str(self.client_address))
        # 接收发送来的filename
        field_item = form['filename']
        if field_item.filename:
            # fn为上传文件路径
            fn = curdir + sep + 'upload/' + field_item.filename
            # 若该文件已经上传过
            if path.exists(fn):
                self.wfile.write(
                    'file <a href="%s">%s</a> alreay exist<br/>' % (field_item.filename, field_item.filename))
            else:
                # 存入服务器路径中, upload文件夹下
                upfile = open(fn, 'wb')
                file_data = field_item.file.read()
                upfile.write(file_data)
                upfile.close()
                file_len = len(file_data)
                del file_data
                self.wfile.write('file <a href="%s">%s</a> upload success, size: %d bytes<br/>' % (
                field_item.filename, field_item.filename, file_len))
        self.wfile.write('</html>')


class ThreadingHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass


if __name__ == '__main__':
    server_address = ('0.0.0.0', 8082)
    httpd = ThreadingHTTPServer(server_address, WebHandler)
    print "Web Server On %s:%d" % server_address
    httpd.serve_forever()
