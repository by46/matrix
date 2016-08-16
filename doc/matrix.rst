matrix.json Schema
====================

matrix.json为matrix提供元数据， 用于制作镜像。

Schemas
-----------------------------
matrix.json 内容为json格式， 包含多个字段：

- name
  必填字段， string类型； 指定最终产生的镜像名称，建议此字段使用项目名
- image
  必填字段， string类型； 指定基础镜像， 建议根据不同业务合理选择基础镜像
- tag
  必填字段， string类型；指定最终产生镜像的tag， 建议使用MAJOR.MINOR.PATCH模式版本号管理镜像，例如：0.0.1
- port
  可选字段， 数组类型， 数组中元素必须为整型；用于指定镜像内的使用端口， 目前只支持TCP端口
- volume
  可选字段，数组类型， 数组中元素必须为字符串；用于指定镜像内使用的卷。
- nev
  可选字段， 字典类型， 字典key为环境变量的名称， 字典value为环境变量的值；用于指定构建变量中使用的环境变量
- cmd
  可选字段， 数组类型，数组中元素必须为字符串；用于指定镜像启动命令

下面给出一个完整的例子：

::

  {
  "name": "otter",
  "image": "docker.neg/python:neg-biz",
  "tag": "0.0.1",
  "port": [80, 443],
  "env": {"PATH": "/opt/matrix:$PATH", "DEBUG": true},
  "volume": ["/opt/data", "/opt/home"],
  "cmd": [ "python", "main.py", "-P", 8080]
  }