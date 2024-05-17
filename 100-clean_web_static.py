#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""

from fabric.api import env, local, run, cd
from datetime import datetime

env.hosts = ['54.175.87.70', '3.84.255.47']


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    try:
        number = int(number)
        if number < 0:
            number = 0
    except ValueError:
        number = 0

    with cd('/data/web_static/releases'):
        # Get list of archives sorted by modification time in descending order
        archives = run('ls -lt | grep web_static | '
                       'awk \'{print $9}\'').split('\n')

        # Remove empty strings from the list
        archives = list(filter(None, archives))

        # Keep only the most recent 'number' archives
        archives_to_keep = archives[:number]

        # Delete the rest of the archives
        archives_to_delete = archives[number:]
        for archive in archives_to_delete:
            run('rm -rf {}'.format(archive))

    with cd('/home/<your_username>/AirBnB_clone_v2/versions'):
        # Get list of local archives sorted by modification time in descending order
        local_archives = local('ls -lt | grep web_static | '
                              'awk \'{print $9}\'', capture=True).split('\n')

        # Remove empty strings from the list
        local_archives = list(filter(None, local_archives))

        # Keep only the most recent 'number' local archives
        local_archives_to_keep = local_archives[:number]

        # Delete the rest of the local archives
        local_archives_to_delete = local_archives[number:]
        for local_archive in local_archives_to_delete:
            local('rm -rf {}'.format(local_archive))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: fab -f 100-clean_web_static.py do_clean:number=<number>")
        exit(1)

    do_clean(sys.argv[2])
