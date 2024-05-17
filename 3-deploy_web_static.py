#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""

from fabric.api import env, local, put, run
from datetime import datetime
import os

env.hosts = ['54.175.87.70', '3.84.255.47']


def do_pack():
    """
    Creates a .tgz archive from the contents of the web_static folder
    """
    dt = datetime.now().strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        archive_path = "versions/web_static_{}.tgz".format(dt)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        base_name = file_name.split(".")[0]
        release_path = "/data/web_static/releases/{}/".format(base_name)

        # Upload the archive to the /tmp/ directory on the web server
        put(archive_path, "/tmp/")

        # Create the release directory
        run("mkdir -p {}".format(release_path))

        # Uncompress the archive to the release directory
        run("tar -xzf /tmp/{} -C {}".format(file_name, release_path))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(file_name))

        # Move the contents of the uncompressed folder to the release path
        run("mv {}web_static/* {}".format(release_path, release_path))

        # Delete the uncompressed folder
        run("rm -rf {}web_static".format(release_path))

        # Delete the current symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(release_path))

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
