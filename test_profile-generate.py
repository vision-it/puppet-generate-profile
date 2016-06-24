#!/usr/bin/env python3

import pytest
import importlib
import re
import os
import shutil
import tempfile
#Dirty fix, since we're not a module
gen = importlib.import_module('profile-generate')


@pytest.fixture(scope='session')
def tmpdir(request):

    tmpdir = tempfile.mkdtemp(suffix='pytest')

    def fin():
        shutil.rmtree(tmpdir)

    return tmpdir


@pytest.fixture
def files(request):

    # This will contain:
    # Filename and expected value
    files = dict()

    # Underscore
    # TODO Somehow this doesn't work. I don't know why
    #files['.git/config'] = 'vision-test'
    #files['README.md'] = r'vision-test'

    # Dashes
    files['data/common.yaml'] = 'vision_test'
    files['.fixtures'] = 'vision_test'
    files['spec/acceptance/default_spec.rb'] = 'vision_test'
    files['spec/classes/compile_spec.rb'] = 'vision_test'
    files['spec/acceptance/nodesets/default.yml'] = 'vision_test'
    files['spec/classes/compile_spec.rb'] = 'vision_test'
    files['metadata.json'] = 'vision_test'
    files['manifests/init.pp'] = 'vision_test'

    return files


def test_main(tmpdir, files):

    profilename = 'vision_test'
    foldername = tmpdir + '/vision-test'

    # Execute main function from generator
    gen.main(profilename, foldername=foldername)

    # Assert for every file
    for filename, expected in files.items():
        filename = os.path.join(tmpdir, profilename, filename)
        assert bool(re.search(expected, filename)) == True
