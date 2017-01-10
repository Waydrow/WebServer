#!usr/bin/python
# -*- coding: utf-8 -*-

import sys

# 取参数
paramStr = sys.argv[1]
# 分离参数
paramArr = paramStr.split('&')
paramDic = {}

# 取出每个参数的值
for param in paramArr:
    key, value = param.split('=')
    paramDic[key] = value

print '''\
    <html>
    <body>
    <p>a + b = {0}</p>
    </body>
    </html>
    '''.format((int(paramDic['a']) + int(paramDic['b'])))