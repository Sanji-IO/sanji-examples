#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
import sys
import unittest

from sanji.connection.mockup import Mockup
from sanji.message import Message

try:
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
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

        # 1. capability
        message = Message({"data": {"message": "call get()"},
                          "query": {}, "param": {}})

        def resp1(code=200, data=None):
            self.assertEqual(code, 200)
            self.assertEqual(data, [1, 2])

        self.hellosanji.get(message=message, response=resp1, test=True)

        # 2. id
        message = Message(
            {"data": {"message": "call get()"},
             "param": {"id": 2},
             "query": {}})

        def resp2(code=200, data=None):
            self.assertEqual(code, 200)
            self.assertEqual(data, "Hello MOXA")

        self.hellosanji.get(message=message, response=resp2, test=True)

        # 3. collection get
        message = Message(
            {"data": {"message": "call get()"},
             "query": {"collection": "true"},
             "param": {}})

        ret_msg = []
        ret_msg.append({"id": 1, "message": "Hello World"})
        ret_msg.append({"id": 2, "message": "Hello MOXA"})

        def resp3(code=200, data=None):
            self.assertEqual(code, 200)
            self.assertEqual(data, {"collection": ret_msg})
        self.hellosanji.get(message=message, response=resp3, test=True)

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

    def test_post(self):
        message = Message({"data": {"message": "call post()"}})

        # case 1: post successfully
        def resp1(code=200, data=None):
            self.assertTrue("id" in data)

        self.hellosanji.post(message=message, response=resp1, test=True)

        # case 2: post bad request
        del message.data

        def resp2(code=200, data=None):
            self.assertEqual(400, code)
            self.assertEqual(data, {"message": "Invalid Post Input."})

        self.hellosanji.post(message=message, response=resp2, test=True)

    def test_delete(self):
        message = Message(
            {"data": {"message": "call delete()"}, "param": {"id": 40}})

        # case 1: post successfully
        def resp1(code=200, data=None):
            self.assertEqual(self.hellosanji.message, "delete index: 40")

        self.hellosanji.delete(message=message, response=resp1, test=True)

        # case 2: delete bad request
        del message.param["id"]

        def resp2(code=200, data=None):
            self.assertEqual(400, code)
            self.assertEqual(data, {"message": "Invalid Delete Input."})

        self.hellosanji.delete(message=message, response=resp2, test=True)


if __name__ == "__main__":
    unittest.main()
