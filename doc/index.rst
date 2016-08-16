.. recipe documentation master file, created by
sphinx-quickstart on Tue Aug 02 13:31:32 2016.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive.

Welcome to Matrix's documentation!
==================================

Matrix， 是一个制作镜像的工具，它可以让我们制作镜像变得简单。
Matrix，目前还只支持Python

Matrix产生的原因
-----------------------------

-  类似 `Python <https://www.python.org>`_ 这样的开发语言， 在使用过程中，很可能使用到第三方扩展依赖库，有些依赖库需要一个C语言编译环境，但是编译工具往往比较庞大，
   例如GCC的编译工具链就比较庞大，如果直接在Docker基础镜像中包含 `GCC <https://gcc.gnu.org/>`_ 编译工具链，就会构造的应用程序镜像的大小也会随之增加。

-  Python提供了 `PIP <https://pip.pypa.io/en/stable/>`_ 这样包管理工具，也能很好解决递归依赖的问题，但是他需要一个 `PYPI <https://pypi.python.org/pypi>`_ 仓库。
   如果依赖设置散落在众多应用程序的Dockerfile中，管理起来也是比较麻烦。

- 其实项目镜像的制作过程都是大体一致，只需要知道几个简单信息就能完成制作镜像，不用在去维护Dockerfile


Matrix能做什么
-----------------------------

- 安装Python依赖
- 制作发布镜像

如何使用
---------------------------

Matrix使用非常简单， Matrix本身也是一个镜像， 启动之后就可以在容器里面完成镜像的制作。

1. 项目根目录需要包含 ``matrix.json`` 文件，他的内容很简单， 下面给出一个简单的例子：

::

   {
     "name": "otter", // image name
     "image": "docker.neg/python:neg-biz", // image base image name
     "tag": "0.0.1", // image tag
     "port": [80, 443],
     "env": {"PATH": "/opt/matrix:$PATH", "DEBUG": true},
     "volume": ["/opt/data", "/opt/home"],
     "cmd": [ "python", "main1.py", "-P", 8080] // docker's command line
   }


2. 使用也非常简单， 以matrix镜像启动一个容器， 把你的Python项目的路径映射容器中 ``/home/matrix`` 路径，并且 ``/var/run/docker.sock`` 也映射到容器的 ``/var/run/docker.sock`` ，
执行 ``/usr/local/bin/matrix.sh``, 执行命令如下：

::

  sudo docker run --rm -v /home/benjamin/git/otter:/home/matrix -v $(which docker):$(which docker) -v /var/run/docker.sock:/var/run/docker.sock matrix:0.0.4 /usr/local/bin/matrix.sh


matrix 有时也会需要错误，你可以根据如下退出码来定位错误原因，错误码如下：

- 退出码80，/home/matrix is not exists
- 退出码81，install requirements.txt error
- 退出码82，run custom build.sh error
- 退出码83，build image error
- 退出码84，matrix.json is not exists
- 退出码85，matrix.json content invalid, read the matrix-schema.json for detail

.. attention::
   构建成功之后，代码会部署到容器中/opt/biz目录，并且当前工作目录也会被设置成/opt/biz


Contents:

.. toctree::
    :maxdepth: 2

    matrix

