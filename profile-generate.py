#!/usr/bin/env python3


import os
import fileinput
import sys
import git
from argparse import ArgumentParser


FOLDER = 'cloned-profile'
FILES = (
    '.fixtures.yml',
    'manifests/init.pp',
    'metadata.json'
)


def pull(origin):
    """
    Pulls from a remote repository and stores it in the directory.
    :param origin: URL of the remote git repository
    """

    repo = None

    try:
        os.mkdir(FOLDER)
    except:
        pass

    try:
        repo = git.Repo.clone_from(origin, FOLDER)
    except git.exc.GitCommandError as exception:
        print("ERROR: Could not Clone from Repo. Exiting...")
        print(exception)
        sys.exit(1)

    return repo


def set_remote_url(repo, new_url):
    """
    Changes the target url of the previously pulled repo.
    :param new_url: New remote url of the repository
    """

    try:
        origin = repo.remotes.origin
        cw = origin.config_writer
        cw.set("url", new_url)
        cw.release()
    except git.exc.GitCommandError as exception:
        print("ERROR: Could not change Remote URL")
        print(exception)
        sys.exit(1)


def replace_marker(filename, profilename, marker='PROFILE_NAME'):
    """
    Changes a specifies marker in a filename to something else

    :param filename: the filename which you want to change
    :param profilename: The profile name to insert
    :param marker: The marker which will be replaced. Default: PROFILE_NAME
    """

    lines = []

    with open(filename) as infile:
        for line in infile:
            line = line.replace(marker, profilename)
            lines.append(line)

    with open(filename, 'w') as outfile:
        for line in lines:
            outfile.write(line)

def main():

    argumentparser = ArgumentParser(description='Pulls the skeleton-profile from git and fills templates')
    argumentparser.add_argument('--name', required=False, help='Name of the new profile')
    args = argumentparser.parse_args()
    profilename = str(args.name)

    # If no commandline argument was passed
    if profilename is None:
        profilename = input('Please input profile name: ')

    # Pulling the skeleton from git
    print("Cloning Puppet Profile Skeleton")
    repo = pull('https://github.com/vision-it/vision-profile-skeleton')

    # Setting the new url
    new_url = 'git@github.com:vision-it/' + profilename + '.git'
    set_remote_url(repo, new_url)

    # Changing the template marker in the files
    for f in FILES:
        replace_marker(FOLDER + '/' + f, profilename)

    print("Skeleton cloned to " + FOLDER + "...")
    sys.exit(0)

if __name__ == '__main__':
    main()
