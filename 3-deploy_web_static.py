#!/usr/bin/python3
"""
Fabric script that deploys an archive to your web servers
"""

from fabric.api import env, local, put, run
from os.path import exists
from datetime import datetime

env.hosts = ['54.175.87.70', '3.84.255.47']


def do_pack():
    """
    Compresses the content of web_static folder into a .tgz archive
    """
    try:
        now = datetime.utcnow()
        file_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(
            now.year,
            now.month,
            now.day,
            now.hour,
            now.minute,
            now.second
        )
        print("file name before creation" + file_name)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        print(e)
        return None


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


def deploy():
    """
    Creates and distributes an archive to the web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
