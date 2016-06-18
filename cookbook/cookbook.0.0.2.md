Matrix
=========================
Matrix是一个用于构建镜像的镜像。

那为什么需要这样一个镜像？
1. 因为像Python这样的语言，在安装很多第三方包的时候，需要从源码进行编译，需要一个完整的编译工具链， 这样的工具链无形的增加的镜像的大小，并且只会使用一次 

Build
---------------------

Pre-installed
---------------------
1. build-base
2. git
3. python
4. python-dev
5. py-pip
6. freetds
7. freetds-dev
8. docker
9. virtualenv
10. fabric
11. jsonschema

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

exit

# on host
# export container
sudo docker export matrix > matrix.tar

# import container as a image

cat matrix.tar | sudo docker import - matrix:0.0.2

# start container
sudo docker run --rm -v /home/benjamin/git/otter:/home/matrix -v /var/run/docker.sock:/var/run/docker.sock docker.neg/matrix:0.0.2 /usr/local/bin/matrix.sh

```