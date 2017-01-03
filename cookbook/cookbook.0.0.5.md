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
- docker==1.10.3
- virtualenv==15.10
- fabric==
- jsonschema
- gevent


```shell
sudo docker run --name onbuild --net=host -it docker.neg/centos:7.2.1511 /bin/bash

# in container
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak

cat <<'EOF' > /etc/yum.repos.d/CentOS-Base.repo
# CentOS-Base.repo
#
# The mirror system uses the connecting IP address of the client and the
# update status of each mirror to pick mirrors that are updated to and
# geographically close to the client.  You should use this for CentOS updates
# unless you are manually picking other mirrors.
#
# If the mirrorlist= does not work for you, as a fall back you can try the
# remarked out baseurl= line instead.
#
#

[base]
name=CentOS-$$releasever - Base
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/$releasever/os/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=os
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7

#released updates
[updates]
name=CentOS-$releasever - Updates
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/$releasever/updates/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=updates
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7

#additional packages that may be useful
[extras]
name=CentOS-$releasever - Extras
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/$releasever/extras/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=extras
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7

#additional packages that extend functionality of existing packages
[centosplus]
name=CentOS-$releasever - Plus
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/$releasever/centosplus/$basearch/
#mirrorlist=http://mirrorlist.centos.org
gpgcheck=1
enabled=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
EOF

yum update

yum groupinstall 'Development Tools'
yum install git
yum install python-devel
yum install docker
# apk add freetds freetds-dev
yum install openssl openssl-devel

# install pip
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python get-pip.py

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple virtualenv
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple fabric
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple jsonschema
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gevent

virtualenv /tmp/matrix

cd ~
git clone http://trgit2/by46/matrix.git
cd matrix
python setup.py

exit

# on host
# export container
sudo docker export onbuild > matrix.tar

# import container as a image

cat matrix.tar | sudo docker import - docker.neg/matrix:0.0.5

sudo docker push docker.neg/matrix:0.0.5

# start container
sudo docker pull docker.neg/matrix:0.0.5

sudo docker run --rm -it -v /home/benjamin/git/otter:/home/matrix -v /var/run/docker.sock:/var/run/docker.sock docker.neg/matrix:0.0.5 /usr/local/bin/matrix.sh

```