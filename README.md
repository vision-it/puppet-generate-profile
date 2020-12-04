[![Build Status](https://travis-ci.com/vision-it/puppet-generate-profile.svg?branch=master)](https://travis-ci.com/vision-it/puppet-generate-profile)

# Puppet Profile Generator

Uses the vision-skeleton Puppet Profile to generate a new Puppet Profile with the given name.

## Setup

```bash
# Use virtual environment
$ pyvenv .venv
$ source .venv/bin/activate

$ pip3 install -r requirements.txt
```

## Usage

```bash
# Generate a new Profile from the skeleton
$ python3 profile-generate.py --name vision_profilename
```

You can also specify the name of the local folder and the name of the repository:

```bash
$ python3 profile-generate.py --name profilename --github vision-othername --folder myfolder
```
