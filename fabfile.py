#! /usr/bin/env python
import argparse
import json
import logging
import os.path
import sys

import jsonschema


def load_settings(src):
    full_path = os.path.join(src, 'matrix.json')
    with open(full_path, 'rb') as f:
        try:
            return json.load(f)
        except ValueError as e:
            logging.error("%s is invalid json file: %s", full_path, e)
            sys.exit(1)


def gen_docker_file(src='.', matrix='.'):
    settings = load_settings(src)
    cmd = settings.get('cmd', [])
    settings['cmd'] = ','.join('"%s"' % x for x in cmd)

    port = settings.get('port', [])
    settings['expose'] = ''
    if port:
        settings['expose'] = 'EXPOSE ' + ' '.join(str(x) for x in port)

    volume = settings.get('volume', [])
    settings['volume'] = ''
    if volume:
        settings['volume'] = 'VOLUME [ ' + ', '.join('"%s"' % v for v in volume) + ' ]'

    env = settings.get('env', {})
    settings['env'] = '\r\n'.join(['ENV {0} {1}'.format(*item) for item in env.iteritems()])

    docker_file_template = os.path.join(matrix, 'Dockerfile.in')
    with open(docker_file_template, 'rb') as f:
        template = f.read()
        docker_file = os.path.join(src, 'Dockerfile')
        with open(docker_file, 'wb') as out:
            out.write(template.format(**settings))


def image_name(src='.'):
    settings = load_settings(src)
    print '{name}:{tag}'.format(name=settings.get('name'), tag=settings.get('tag', 'latest')),


def valid_matrix_json(src='.', matrix='.'):
    with open(os.path.join(src, 'matrix.json'), 'rb') as meta:
        meta_json = json.load(meta)
        with open(os.path.join(matrix, 'matrix-schema.json'), 'rb') as schema:
            schema_json = json.load(schema)
            jsonschema.validate(meta_json, schema_json)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate Dockerfile from source tree",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--src', dest='src', help='The source code path')
    opts = parser.parse_args(sys.argv[1:])
    gen_docker_file(opts.src)
