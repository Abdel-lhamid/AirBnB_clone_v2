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
