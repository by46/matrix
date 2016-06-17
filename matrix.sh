#!/usr/bin/env sh

PWD=$(cd `dirname $0`; pwd)

WORKDIR=/home/matrix
TMP=/tmp/images
DEP=/tmp/matrix

alias fab="fab --fabfile=${PWD}"

cd ${WORKDIR}

virtualenv ${DEP}

source ${DEP}/bin/activate

if [ -f requirements.txt ]; then
	pip install --trusted-host 10.16.78.86 -i http://10.16.78.86:3141/simple -r requirements.txt
fi

if [ -f build.sh ]; then
	chmod +x build.sh
	./build.sh
fi

mkdir ${TMP}

# collect source file
mkidr -p ${TMP}/opt/biz
cp  -rvf .* ${TMP}/opt/biz

# collect dependency libs
mkdir -p ${TMP}/usr/lib/python2.7/
cp -rvf /usr/lib/python2.7/site-packages ${TMP}/usr/lib/python2.7/

# package resource
tar zcf images.tgz -C ${TMP}  .

# generate Dockerfile

fab gen_docker_file:matrix=${PWD}

# build images
# TODO(benjamin): get image name and version
echo docker build -t $(fab image_name | head -n 1) .

docker build -t $(fab image_name | head -n 1) .

