#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_EFMlrs
----------------------------------

Tests for `EFMlrs` module.
"""

import unittest
import tempfile
from shutil import copyfile, rmtree

import efmlrs
from efmlrs import pre
from efmlrs import post

TEST_DIR        = ''
TEMP_DIR        = 'test_EFMlrs'

class TestEFMlrs(unittest.TestCase):

    def setUp(self):
        pass

    def test_pre_at_ecoli5010(self):
        # create temporary working directory for test
        TEST_DIR = tempfile.mkdtemp(TEMP_DIR)

        # argument definitions
        PATH  = 'tests/example_models/'
        MODEL = 'ecoli5010.xml'

        # copy model
        copyfile(PATH + MODEL, TEST_DIR + "/" + MODEL)

        # do pre test (in TEST_DIR)
        pre.start(
            TEST_DIR + "/" + MODEL,
            '*',
            False
        )

        # clean up
        rmtree(TEST_DIR)
        assert(efmlrs.__version__)

    def test_post_at_ecoli5010(self):
        # create temporary working directory for test
        TEST_DIR = tempfile.mkdtemp(TEMP_DIR)

        # argument definitions
        PATH   = 'tests/example_results/'
        EFMS   = 'ecoli5010_cmp_mplrs.efms'
        INFO   = 'ecoli5010.info'
        OUTPUT = 'ecoli5010_decomp.efms'

        # copy compressed efms file to temp directory
        copyfile(PATH + EFMS, TEST_DIR + "/" + EFMS)

        # copy info file to temp directory
        copyfile(PATH + INFO, TEST_DIR + "/" + INFO)

        # do post test (in TEST_DIR)
        post.start(
            TEST_DIR + "/" + EFMS,
            TEST_DIR + "/" + OUTPUT,
            TEST_DIR + "/" + INFO,
            False
        )

        # clean up
        rmtree(TEST_DIR)
        assert(efmlrs.__version__)

    def tearDown(self):
        pass
