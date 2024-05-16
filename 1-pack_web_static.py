#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from
the contents of the web_static folder
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Compresses the content of web_static folder into a .tgz archive
    """
    try:
        now = datetime.now()
        file_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(
            now.year,
            str(now.month).zfill(2),
            str(now.day).zfill(2),
            str(now.hour).zfill(2),
            str(now.minute).zfill(2),
            str(now.second).zfill(2)
        )
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        print(e)
        return None
