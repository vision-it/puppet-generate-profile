#!/usr/bin/env python3


import os
import fileinput
import sys
import git
import re
from argparse import ArgumentParser


def get_files(folder):
    """
    Gets all the files in the specified folder and returns a list.
    :param folder: Name of the root folder
    """

    files = list()

    for root, dirnames, filenames in os.walk(folder):
        # Ignore all files in .git
        if not re.search('git', root):
            for f in filenames:
                files.append(os.path.join(root,f))

    return files


def pull(origin, directory):
    """
    Pulls from a remote repository and stores it in the directory.
    :param origin: URL of the remote git repository
    """

    repo = None

    try:
        os.mkdir(directory)
    except FileExistsError:
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


def replace_marker(filename, profilename, marker='skeleton'):
    """
    Changes a specifies marker in a filename to something else

    :param filename: the filename which you want to change
    :param profilename: The profile name to insert
    :param marker: The marker which will be replaced. Default: skeleton
    """

    lines = []

    with open(filename) as infile:
        for line in infile:
            line = line.replace(marker, profilename)
            lines.append(line)

    with open(filename, 'w') as outfile:
        for line in lines:
            outfile.write(line)


def commandline():

    # Command line arguments
    argumentparser = ArgumentParser(description='Pulls the skeleton-profile from git and fills templates')
    argumentparser.add_argument('--name', required=True, help='Name of the new profile.')
    argumentparser.add_argument('--github', required=False, help='Name of the github repository')
    argumentparser.add_argument('--folder', required=False, help='Name of the local folder')

    args = argumentparser.parse_args()

    return (args.name, args.github, args.folder)


def main(profilename, githubname=None, foldername=None):

    # Normalize the command line arguments
    profilename_without_prefix = re.sub('vision_', '', profilename)

    if githubname is None:
        githubname = profilename.replace('_', '-')

    if foldername is None:
        foldername = profilename.replace('_', '-')


    # Pulling the skeleton from git
    print("Cloning Puppet Profile Skeleton...")
    repo = pull('https://github.com/vision-it/vision-skeleton', foldername)


    # Setting the new url
    new_url = 'git@github.com:vision-it/' + githubname + '.git'
    set_remote_url(repo, new_url)


    # Changing the template marker in the files
    files = get_files(foldername)
    for f in files:
        # This sucks and needs to
        if str(f).endswith('README.md'):
            replace_marker(f, profilename_without_prefix)
        else:
            replace_marker(f, profilename)


    print("Skeleton cloned to " + foldername)


if __name__ == '__main__':
    name, gitname, folder = commandline()
    main(name, gitname, folder)
