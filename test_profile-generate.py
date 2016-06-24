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

    # Assert for every file
    files = dict()

    # Underscore
    #files['.git/config'] = r'vision-test'
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

    gen.main(profilename, foldername=foldername)

    for filename, expected in files.items():
        filename = os.path.join(tmpdir, profilename, filename)
        assert bool(re.search(expected, filename)) == True
