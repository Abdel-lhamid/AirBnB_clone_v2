#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['54.175.87.70', '3.84.255.47']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Uncompress the archive to the folder
        # /data/web_static/releases/<archive filename without extension>
        file_name = archive_path.split('/')[-1]
        file_folder = '/data/web_static/releases/' + file_name[:-4] + '/'
        run('mkdir -p {}'.format(file_folder))
        run('tar -xzf /tmp/{} -C {}'.format(file_name, file_folder))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(file_name))

        # Move the contents of the uncompressed folder to its parent folder
        run('mv {}web_static/* {}'.format(file_folder, file_folder))

        # Delete the uncompressed folder
        run('rm -rf {}web_static'.format(file_folder))

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link linked to the new version of your code
        run('ln -s {} /data/web_static/current'.format(file_folder))
        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False
