#! /usr/bin/env python
import os.path
from fabric.api import local

if __name__ == '__main__':
    tmp = '/usr/local/bin'
    local('cp -rvf Dockerfile.in {0}'.format(tmp))
    local('cp -rvf matrix-schema.json {0}'.format(tmp))
    local('cp -rvf fabfile.py {0}'.format(tmp))
    local('cp -rvf matrix.sh {0}'.format(tmp))

    local('chmod +x {0}'.format(os.path.join(tmp, 'matrix.sh')))

