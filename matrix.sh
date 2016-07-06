#!/usr/bin/env sh

MATRIX_HOME=$(cd `dirname $0`; pwd)

WORKDIR=/home/matrix
TMP=/tmp/images
DEP=/tmp/matrix

alias fab="fab --fabfile=${MATRIX_HOME}/fabfile.py"

# check volume directory exists
[ ! -d ${WORKDIR} ] && exit 80

# check matrix.json exists
[ ! -f "${WORKDIR}/matrix.json" ] && exit 84

# check matrix.json validate
fab valid_matrix_json:src=${WORKDIR},matrix=${MATRIX_HOME}
[ $? -gt 0 ] && exit 85


cd ${WORKDIR}

# virtualenv ${DEP}

source ${DEP}/bin/activate

if [ -f requirements.txt ]; then
	pip install --trusted-host 10.16.78.86 -i http://10.16.78.86:3141/simple -r requirements.txt
	# check install result
	[ $? -gt 0 ] && exit 81
fi

if [ -f build.sh ]; then
	chmod +x build.sh
	./build.sh
	# check run custom build.sh exit status
	[ $? -gt 0 ] && exit 82
fi

mkdir ${TMP}

# collect source file
mkdir -p ${TMP}/opt
cp  -rvf ${WORKDIR} ${TMP}/opt/biz

# collect dependency libs
mkdir -p ${TMP}/usr/lib/python2.7/
cp -rvf ${DEP}/lib/python2.7/site-packages ${TMP}/usr/lib/python2.7/

# package resource
tar zcf images.tgz -C ${TMP}  .

# generate Dockerfile
fab gen_docker_file:matrix=${MATRIX_HOME}

# build images
docker build -t $(fab image_name | head -n 1) .

# check docker build result
[ $? -gt 0 ] && exit 83

exit 0

