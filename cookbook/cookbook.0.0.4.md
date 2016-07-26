Matrix
=========================
Matrix是一个用于构建镜像的镜像。

那为什么需要这样一个镜像？
1. 因为像Python这样的语言，在安装很多第三方包的时候，需要从源码进行编译，需要一个完整的编译工具链， 这样的工具链无形的增加的镜像的大小，并且只会使用一次 

Build
---------------------

Pre-installed
---------------------
- build-base
- git
- python
- python-dev
- py-pip
- freetds
- freetds-dev
- docker
- virtualenv
- fabric
- jsonschema
- gevent


```shell
sudo docker run --name onbuild --net=host -i docker.neg/alpine:3.3 /bin/sh

# in container

cat << EOF > /etc/apk/repositories
https://mirrors.tuna.tsinghua.edu.cn/alpine/v3.3/main
https://mirrors.tuna.tsinghua.edu.cn/alpine/v3.3/community
EOF

apk update

apk add build-base
apk add git
apk add python python-dev
apk add py-pip
apk add freetds freetds-dev
apk add docker
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple virtualenv
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple fabric
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple jsonschema

virtualenv /tmp/matrix

pip --trusted-host scmesos06 install -i https://scmesos06/simple gevent
exit

# on host
# export container
sudo docker export onbuild > matrix.tar

# import container as a image

cat matrix.tar | sudo docker import - matrix:0.0.4

# start container
sudo docker run --rm -v /home/benjamin/git/otter:/home/matrix -v $(which docker):$(which docker) -v /var/run/docker.sock:/var/run/docker.sock docker.neg/matrix:0.0.4 /usr/local/bin/matrix.sh

```