User Guide
================

Create Project
--------------------------------

该命令通过预定义的项目模板，快速创建项目骨架，并且可以额外设置Jenkins相关Job。命令具体参数如下：

::

  usage: recipe.exe create [-h] [-t TEMPLATE] [-o OUT] [-d] [-r REPO] name

  positional arguments:
    name

  optional arguments:
   -h, --help            show this help message and exit
   -t TEMPLATE, --template TEMPLATE
                           project template name
   -o OUT, --output-dir OUT
                           Where to output the generated project dir into
   -d, --deploy        Create CI task on Jenkins after create project
                           successfully.
   -r REPO, --repo REPO  the git repo on trgit2,
                           like: http://trgit2/dfis/recipe.git


- 参数 ``--template`` 用于指定项目模板， 默认值为python.flask
- 参数 ``--output-dir`` 用于指定项目输出的路径，默认情况下，会当前工作目录生成项目骨架
- 参数 ``--deploy`` 用于指定创建完项目骨架之后，在jenkins上创建相关Job， 默认情况下，会创建以下jenkins job：

	+ Analysis_<name>
	+ UT_<name>
	+ Build_<name>
	+ AT_<name>
	+ IT_<name>
	+ Deploy_<name>

- 参数 ``--repo`` 用于指定jenkins上获取代码的VCS

.. important::
    现在只支持GIT版本管理，并且git仓库必须是public类型的。

Deploy Project
----------------------------

deploy命令用于创建Jenkins相关的Job，适用于你的项目已经存在，但还是没有Jenkins相关的Job，
那么你就可以通过该命令快速创建Jenkins job，命令具体参数如下：

::

  usage: recipe.exe deploy [-h] [-t TEMPLATE] [-r REPO] name

  positional arguments:
     name

  optional arguments:
     -h, --help            show this help message and exit
     -t TEMPLATE, --template TEMPLATE
                          project template name
     -r REPO, --repo REPO  the git repo on trgit2, like:
                          http://trgit2/dfis/recipe.git

- 参数 ``--template`` 指定项目模板，因为不同模板创建的Jenkins Job可能会不一样，默认值为python.flask
- 参数 ``--repo`` 指定项目的GIT仓库地址

.. important::
    现在只支持GIT版本管理，并且git仓库必须是public类型的。

List Templates
------------------------------

Recipe 提供了多种项目模板，你可以通过 ``list`` 命令查看所有可用的模板，命令具体参数如下：

::

  usage: recipe.exe list [-h]

  optional arguments:
    -h, --help  show this help message and exit

Recipe Version
------------------------

你可以通过 ``version`` 命令来查看recipe的当前版本

::

  usage: recipe.exe version [-h]

  optional arguments:
    -h, --help  show this help message and exit

Install Templates
-------------------------

.. important::
    该功能还在开发中