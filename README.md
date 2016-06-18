# Matrix

1. 类似[Python](https://www.python.org)这样的开发语言， 在使用过程中，很可能使用到第三方扩展依赖库，这些依赖库需要一个C语言编译环境，但是编译工具往往比较庞大，
例如GCC的编译工具链就比较庞大，如果直接在Docker基础镜像中包含[GCC](https://gcc.gnu.org/)编译工具链，就会构造的应用程序镜像的大小也会随之增加。
2. Python提供了[PIP](https://pip.pypa.io/en/stable/)这样包管理工具，也能很好解决递归依赖的问题，但是他需要一个[PYPI](https://pypi.python.org/pypi)私有仓库。
如果这个私有仓库的设置散落在众多应用程序的Dockerfile中，管理起来也是比较麻烦，特别是私有仓库迁移，可能对应用程序来说更是要命。  


这就是matrix产生原因，是构建Python项目变得容易，简单。

## Usage

如果要使用matrix来构建镜像，项目根目录中需要包含一个matrix.json元数据描述文件， 来告诉matrix如何构建镜像。可以查看matrix-schema.json文件来了解matrix.json
的详细定义。

### matrix-schema.json

```json

{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "image": {
      "type": "string"
    },
    "tag": {
      "type": "string"
    },
    "port": {
      "type": "array",
      "items": {
        "type": "integer"
      }
    },
    "env": {
      "type": "object"
    },
    "volume": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "cmd": {
      "type": "array"
    }
  },
  "required": [
    "name",
    "image",
    "tag"
  ]
}

```

使用也非常简单， 以matrix镜像启动一个容器， 把你的Python项目的路径映射容器中/home/matrix路径，并且/var/run/docker.sock 也映射到容器的/var/run/docker.sock，
执行/usr/local/bin/matrix.sh, 执行命令如下：

```shell
sudo docker run --rm -v /home/benjamin/git/otter:/home/matrix -v /var/run/docker.sock:/var/run/docker.sock matrix:0.0.2 /usr/local/bin/matrix.sh

```

## Exit Status

1. 80 - /home/matrix is not exists
2. 81 - install requirements.txt error
3. 82 - run custom build.sh error
4. 83 - build image error
5. 84 - matrix.json is not exists
6. 85 - matrix.json content invalid, read the matrix-schema.json for detail