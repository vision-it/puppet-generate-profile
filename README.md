[![Build Status](https://travis-ci.org/vision-it/puppet-generate-profile.svg?branch=master)](https://travis-ci.org/vision-it/puppet-generate-profile)

# Puppet Profile Generator

Clones the puppet-profile-skeleton and modifies some files to include the new profile name.

## Setup

```bash
$ pip3 install -r requirements.txt
```

## Usage

```bash
$ python3 profile-generate.py --name vision_profilename
```

You can also specify the name of the local folder and the name of the repository:

```bash
$ python3 profile-generate.py --name profilename --github vision-othername --folder myfolder
```

