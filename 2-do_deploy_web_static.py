#!/usr/bin/python3
'''
Fabric script to distributes a .tgz archive
onto a server
'''
from fabric.api import *
from datetime import datetime
from os.path import exists
import argparse

env.hosts = ['100.26.229.143', '54.237.104.144']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    '''
    this method distributes the archive
    '''
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        archive_no_ext = archive_name.split('.')[0]
        target_path = "/data/web_static/releases/" + archive_no_ext

        put(archive_path, '/tmp', use_sudo=True)
        run('sudo mkdir -p {}'.format(target_path))
        run('sudo tar -xzf /tmp/{} -C {}'.format(archive_name, target_path))
        run('sudo rm /tmp/{}'.format(archive_name))
        run('sudo mv {}/web_static/* {}/'.format(target_path, target_path))
        run('sudo rm -rf {}/web_static'.format(target_path))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(target_path))
        return True
    except Exception as e:
        return False
