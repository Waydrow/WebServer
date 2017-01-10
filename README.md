## WebServer By Python

### 项目简介

本项目为用python开发的一款简易web服务器, 现实现功能如下  
 - `Get`请求
 - `Post`请求
 - 解析`php`脚本文件
 - 解析`python`脚本文件
 - 支持识别`html/css/javascript/jpg/png/gif`等多种文件格式
 - 文件上传  
项目托管在github上, [https://github.com/Waydrow/WebServer](https://github.com/Waydrow/WebServer)

### 目录结构

#### 根目录

- `Base`目录: 存储自定义方法  
- `admin`目录: 存储处理前台get post的python脚本
- `cgi-bin`目录: 支持其他扩展文件 如php
- `public`目录: 存储外部静态资源文件, 如css, js, 图片等
- `upload`目录: 服务器上传文件目录
- `server.py`: web server by python  
- `index.html`: 网站根目录  
- `calc.html`: get请求演示方法  
- `fileupload_server.py`: 上传文件服务器脚本

#### Base目录

- `__init__.py`: init文件  
- `casefile.py`: 请求方式判断的自定义类  

#### admin目录

- `calc.py`: 处理根目录下 `calc.html` 的请求
- `post.py': 暂无用

#### cgi-bin目录

- `info.php`: php脚本文件运行测试
- `login.php`: 处理前台 `index.html` 的post请求

### 运行说明

#### server.py
在根目录下运行`server.py`文件, 服务器端口为8081,   
访问路径 [localhost:8081](localhost:8081)  或 [127.0.0.1:8081](127.0.0.1:8081)  
该服务器可实现get, post, 解析php, python, 加载css/js/png/jpg等功能

测试方法:
- `index.html`  
- `calc.html`

#### fileupload_server.py
在根目录下运行`fileupload_server.py`文件, 服务器端口为8082  
访问路径 [localhost:8082](localhost:8082)  或 [127.0.0.1:8082](127.0.0.1:8082)
该服务器可实现上传文件功能

测试方法:   
运行程序后打开根路径即可, 上传图片后存储到项目根目录下的`upload`文件夹中  


## License
Copyright 2017 Waydrow

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.