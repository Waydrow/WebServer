#!usr/bin/python
# coding: utf-8

'''
    create time: 2016.12.20
    author: Waydrow
    connect: waydrow@163.com
    blog: blog.waydrow.com
'''

import os, subprocess

class ServerException(Exception):
    '''服务器内部错误'''
    pass


class base_case(object):
    '''条件处理基类'''

    def handle_file(self, handler, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()

            # 根据请求路径判断文件类型
            if full_path.endswith("css"):
                handler.send_content(content, type='css')
            elif full_path.endswith("js"):
                handler.send_content(content, type='js')
            elif full_path.endswith("png"):
                handler.send_content(content, type='png')
            elif full_path.endswith("jpg"):
                handler.send_content(content, type='jpg')
            elif full_path.endswith("gif"):
                handler.send_content(content, type='gif')
            else:
                handler.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(full_path, msg)
            handler.handle_error(msg)

    # 请求根路径时
    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')

    # 测试是否满足条件, 在子类中重写
    def test(self, handler):
        assert False, 'Not implemented.'

    # 满足test条件即执行, 在子类中重写
    def act(self, handler):
        assert False, 'Not implemented.'


class case_no_file(base_case):
    '''该路径不存在'''

    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        raise ServerException("'{0}' not found".format(handler.path))


class case_existing_file(base_case):
    '''该路径是文件'''

    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        self.handle_file(handler, handler.full_path)


class case_always_fail(base_case):
    '''所有情况都不符合时的默认处理类'''

    def test(self, handler):
        return True

    def act(self, handler):
        raise ServerException("Unknown object '{0}'".format(handler.path))


class case_directory_index_file(base_case):
    '''访问根目录'''

    # 判断目标路径是否是目录 && 目录下是否有index.html
    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
               os.path.isfile(self.index_path(handler))

    # 响应index.html的内容
    def act(self, handler):
        self.handle_file(handler, self.index_path(handler))


class case_cgi_file(base_case):
    '''python脚本文件处理'''

    def run_cgi(self, handler):
        paramList = ['python', handler.full_path]
        if handler.paramStr != None:
            # 判断是否传递参数
            paramList.append(handler.paramStr)
        data = subprocess.check_output(paramList)
        handler.send_content(data)

    def test(self, handler):
        return os.path.isfile(handler.full_path) and \
            handler.full_path.endswith('.py')

    def act(self, handler):
        # 运行脚本文件
        self.run_cgi(handler)

class case_php_file(base_case):
    '''php脚本文件处理'''

    def run_cgi(self, handler):
        paramList = ['php', handler.full_path]
        if handler.paramStr != None:
            paramList.append(handler.paramStr)
        data = subprocess.check_output(paramList)
        handler.send_content(data)

    def test(self, handler):
        return os.path.isfile(handler.full_path) and \
            handler.full_path.endswith('php')

    def act(self, handler):
        self.run_cgi(handler)










