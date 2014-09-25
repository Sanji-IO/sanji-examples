#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
import sys
import unittest

from sanji.connection.mockup import Mockup
from sanji.message import Message

try:
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')
    from hellosanji import Hellosanji
except ImportError as e:
    print "Please check the python PATH for import test module. (%s)" \
        % __file__
    exit(1)


class TestHellosanjiClass(unittest.TestCase):

    def setUp(self):
        self.hellosanji = Hellosanji(connection=Mockup())

    def tearDown(self):
        self.hellosanji.stop()
        self.hellosanji = None

    def test_get(self):
        def resp(code=200, data=None):
            self.assertEqual(code, 200)
            self.assertEqual(data, {"message": self.hellosanji.message})
        self.hellosanji.get(message=None, response=resp, test=True)

    def test_put(self):
        message = Message({"data": {"message": "hello kitty"}})

        # case 1: put successfully
        def resp1(code=200, data=None):
            self.assertEqual(self.hellosanji.message, "hello kitty")
        self.hellosanji.put(message=message, response=resp1, test=True)

        # case 2: put bad request
        del message.data

        def resp2(code=200, data=None):
            self.assertEqual(400, code)
            self.assertEqual(data, {"message": "Invaild Input."})
        self.hellosanji.put(message=message, response=resp2, test=True)


if __name__ == "__main__":
    unittest.main()
