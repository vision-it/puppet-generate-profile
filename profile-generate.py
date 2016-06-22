#!/usr/bin/env python3


import os
import fileinput
import sys
import git
from argparse import ArgumentParser


# TODO Dynamisch mit regex (grep -r) machen -.-
FILES = (
    '.fixtures.yml',
    'manifests/init.pp',
    'metadata.json',
    'spec/acceptance/nodesets/default.yml',
    'data/common.yaml',
    'spec/acceptance/default_spec.rb',
    'spec/classes/compile_spec.rb'
)

def create_filelist(grep):
    pass

def pull(origin, directory):
    """
    Pulls from a remote repository and stores it in the directory.
    :param origin: URL of the remote git repository
    """

    repo = None

    try:
        os.mkdir(directory)
    except:
        pass

    try:
        repo = git.Repo.clone_from(origin, directory)
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

    new_url = str(new_url).replace('_','-')

    try:
        origin = repo.remotes.origin
        cw = origin.config_writer
        cw.set("url", new_url)
        cw.release()
    except git.exc.GitCommandError as exception:
        print("ERROR: Could not change Remote URL")
        print(exception)
        sys.exit(1)


def replace_marker(filename, profilename, marker='vision_skeleton'):
    """
    Changes a specifies marker in a filename to something else

    :param filename: the filename which you want to change
    :param profilename: The profile name to insert
    :param marker: The marker which will be replaced. Default: vision_skeleton
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

    # Command line arguments
    argumentparser = ArgumentParser(description='Pulls the skeleton-profile from git and fills templates')
    argumentparser.add_argument('--name', required=True, help='Name of the new profile. Like so: new_profile')
    args = argumentparser.parse_args()
    profilename = str(args.name)
    foldername = str(profilename).replace('_','-')

    # Pulling the skeleton from git
    print("Cloning Puppet Profile Skeleton...")
    repo = pull('https://github.com/vision-it/vision-skeleton', foldername)

    # Setting the new url
    new_url = 'git@github.com:vision-it/' + profilename + '.git'
    set_remote_url(repo, new_url)


    # Changing the template marker in the files
    for f in FILES:
        replace_marker(foldername + '/' + f, profilename)

    print("Skeleton cloned to " + foldername + "...")
    sys.exit(0)

if __name__ == '__main__':
    main()
