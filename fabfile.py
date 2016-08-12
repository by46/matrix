#! /usr/bin/env python
import argparse
import fnmatch
import json
import locale
import logging
import os
import re
import shutil
import sys
from contextlib import contextmanager
from distutils.text_file import TextFile

import jsonschema

INCLUDE = []
INCLUDE_regexps = []
EXCLUDE = []
EXCLUDE_regexps = []


# -------------------------
# copy file
# --------------------------
@contextmanager
def cd(directory):
    """Change the current working directory, temporarily.
    Use as a context manager: with cd(d): ...
    """
    old_dir = os.getcwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(old_dir)


def get_all_file_in(dirname):
    name_list = []
    for root, dirs, files in os.walk(dirname):
        # for dir in dirs:
        #     if isinstance(dir,bytes):
        #         name_list.append(dir.decode(locale.getpreferredencoding()))
        #     else:
        #         name_list.append(dir)
        for name in files:
            if isinstance(name, bytes):
                name_list.append(os.path.join(root, name.decode(locale.getpreferredencoding())))
            else:
                name_list.append(os.path.join(root, name))
    return name_list


def _glob_to_regexp(pat):
    pat = fnmatch.translate(pat)
    sep = r'\\\\' if os.path.sep == '\\' else os.path.sep
    return re.sub(r'((?<!\\)(\\\\)*)\.', r'\1[^%s]' % sep, pat)


def read_manifest():
    if not os.path.isfile('MANIFEST.in'):
        return
    include, include_regexps, exclude, exclude_regexps = _get_message_from_manifest('MANIFEST.in')
    INCLUDE.extend(include)
    INCLUDE_regexps.extend(include_regexps)
    EXCLUDE.extend(exclude)
    EXCLUDE_regexps.extend(exclude_regexps)


def _get_message_from_list(list):
    include, include_regexps, exclude, exclude_regexps = _get_message_from_manifest_lines(list)
    INCLUDE.extend(include)
    INCLUDE_regexps.extend(include_regexps)
    EXCLUDE.extend(exclude)
    EXCLUDE_regexps.extend(exclude_regexps)


def _get_message_from_manifest(filename):
    template = TextFile(filename,
                        strip_comments=True,
                        skip_blanks=True,
                        join_lines=True,
                        lstrip_ws=True,
                        rstrip_ws=True,
                        collapse_join=True)
    try:
        lines = template.readlines()
    finally:
        template.close()
    return _get_message_from_manifest_lines(lines)


def _get_message_from_manifest_lines(lines):
    follow = []
    follow_regexps = []
    ignore = []
    ignore_regexps = []
    for line in lines:
        try:
            cmd, rest = line.split(None, 1)
        except ValueError:
            continue
        if cmd == 'exclude':
            for pat in rest.split():
                if '*' in pat or '?' in pat or '[!' in pat:
                    ignore_regexps.append(_glob_to_regexp(pat))
                else:
                    ignore.append(pat)
        elif cmd == 'global-exclude':
            ignore.extend(rest.split())
        elif cmd == 'recursive-exclude':
            try:
                dirname, patterns = rest.split(None, 1)
            except ValueError:
                continue
            dirname = dirname.rstrip(os.path.sep)
            for pattern in patterns.split():
                if pattern.startswith('*'):
                    ignore.append(dirname + os.path.sep + pattern)
                else:
                    ignore.append(dirname + os.path.sep + pattern)
                    ignore.append(dirname + os.path.sep + '*' + os.path.sep +
                                  pattern)
        elif cmd == 'prune':
            rest = rest.rstrip('/\\')
            ignore.append(rest)
            ignore.append(rest + os.path.sep + '*')
        elif cmd == 'include':
            for pat in rest.split():
                if '*' in pat or '?' in pat or '[!' in pat:
                    follow_regexps.append(_glob_to_regexp(pat))
                else:
                    follow.append(pat)
        elif cmd == 'global-include':
            follow.extend(rest.split())
        elif cmd == 'recursive-include':
            try:
                dirname, patterns = rest.split(None, 1)
            except ValueError:
                continue
            dirname = dirname.rstrip(os.path.sep)
            for pattern in patterns.split():
                if pattern.startswith('*'):
                    follow.append(dirname + os.path.sep + pattern)
                else:
                    follow.append(dirname + os.path.sep + pattern)
                    follow.append(dirname + os.path.sep + '*' + os.path.sep +
                                  pattern)
        elif cmd == 'graft':
            rest = rest.rstrip('/\\')
            follow.append(rest)
            follow.append(rest + os.path.sep + '*')
    return follow, follow_regexps, ignore, ignore_regexps


def file_matches(filename, patterns):
    """Does this filename match any of the patterns?"""
    return any(fnmatch.fnmatch(filename, pat) or
               fnmatch.fnmatch(os.path.basename(filename), pat)
               for pat in patterns)


def file_matches_regexps(filename, patterns):
    """Does this filename match any of the regular expressions?"""
    return any(re.match(pat, filename) for pat in patterns)


def strip_sdist_extras(filelist):
    """Strip generated files that are only present in source distributions.

    We also strip files that are ignored for other reasons, like
    command line arguments, setup.cfg rules or MANIFEST.in rules.
    """
    # file_names = os.path.
    return [name for name in filelist
            if (not file_matches(os.path.basename(name), EXCLUDE)
                and not file_matches_regexps(os.path.basename(name), EXCLUDE_regexps)
                and (file_matches(os.path.basename(name), INCLUDE)
                     or file_matches_regexps(os.path.basename(name), INCLUDE_regexps)))]


def copy_files(srcdir, destdir, rule=None):
    with cd(srcdir):
        if isinstance(rule, list):
            _get_message_from_list(rule)
        elif rule is None:
            read_manifest()
    all_source_file = get_all_file_in(srcdir)
    source_file = strip_sdist_extras(all_source_file)
    for filepath in source_file:
        tmp_path = os.path.relpath(filepath, srcdir)
        destfile = os.path.join(destdir, tmp_path)
        # filename should not be absolute, but let's double-check
        # assert destfile.startswith(destdir + os.path.sep)
        destfiledir = os.path.dirname(destfile)
        if not os.path.isdir(destfiledir):
            os.makedirs(destfiledir)
        # if os.path.isdir(filename):
        #     os.mkdir(destfile)
        # else:
        shutil.copy2(filepath, destfile)


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

    hosts = settings.get('hosts', [])
    if hosts:
        settings['run'] = '\r\n'.join(['RUN echo "{ip} {host}" >> /etc/hosts'.format(**host) for host in hosts])

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
