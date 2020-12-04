#!/usr/bin/env python3

"""
Uses the vision-skeleton Puppet Profile to generate a new Puppet Profile with the given name.
"""

import os
import subprocess
import re
import shutil
from argparse import ArgumentParser


def get_files(directoryname):
    """
    Gets all the files in the specified folder and returns a list.
    :param directoryname: Name of the root folder.
    """

    files = list()

    for root, _ , filenames in os.walk(directoryname):
        # Ignore all files in .git
        if not re.search(r'\.git', root):
            for _files in filenames:
                files.append(os.path.join(root, _files))

    return files


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
    """
    Setup for CLI
    """

    # Command line arguments
    argumentparser = ArgumentParser(
        description='Pulls the visio-skeleton Profile from git and prepares a new Profile'
    )
    argumentparser.add_argument('--name', required=True,
                                help='Name of the new profile')
    argumentparser.add_argument('--github', required=False,
                                help='URL of the new GitHub repository')
    argumentparser.add_argument('--directory', required=False,
                                help='Name of the new local directory')

    args = argumentparser.parse_args()

    return (args.name, args.github, args.directory)


def main(profilename, githubname=None, directoryname=None):
    """
    Entrypoint
    """

    # Normalize the command line arguments
    profilename_without_prefix = re.sub('vision_', '', profilename)

    if githubname is None:
        githubname = profilename.replace('_', '-')

    if directoryname is None:
        directoryname = profilename.replace('_', '-')

    skeleton_url = "https://github.com/vision-it/vision-skeleton"
    repo_git_path = os.path.join(os.getcwd(), directoryname, '.git')
    new_remote_url = 'git@github.com:vision-it/' + githubname + '.git'

    print("> Cloning Puppet Profile Skeleton...")
    subprocess.run(["git", "clone", skeleton_url, directoryname], check=False)

    print("> Removing .git directory to remove history...")
    shutil.rmtree(repo_git_path)

    print("> Initializing new Profile...")
    subprocess.run(["git", "init", directoryname],
                   check=False)
    subprocess.run(["git", "checkout", "-b", "development"], cwd=directoryname,
                   check=False)
    subprocess.run(["git", "remote", "add", "origin", new_remote_url], cwd=directoryname,
                   check=False)

    # Changing the template marker in the files
    files = get_files(directoryname)
    for _files in files:
        replace_marker(_files, profilename_without_prefix)

    print("---------------------------------")
    print("Profile: " + profilename)
    print("Skeleton cloned to: " + directoryname)
    print("Github origin name: " + new_remote_url)


if __name__ == '__main__':
    name, gitname, directory = commandline()
    main(name, gitname, directory)
