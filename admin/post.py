#!usr/bin/python
# -*- coding: utf-8 -*-

import sys

paramStr = sys.argv[1]
paramArr = paramStr.split('&')
paramDic = {}

for param in paramArr:
    key, value = param.split('=')
    paramDic[key] = value

print '''\
    <html>
    <body>
    <p>username: {0}</p>
    <p>introduction: {1}</p>
    <p>argv[0]: {2}</p>
    </body>
    </html>
    '''.format(paramDic['username'], paramDic['introduction'], sys.argv[0])