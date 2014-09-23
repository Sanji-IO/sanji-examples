#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
from sanji.core import Sanji
from sanji.core import Route
from sanji.connection.mqtt import Mqtt


class Hellosanji(Sanji):

    def init(self):
        self.message = "Hello Sanji!"

    @Route(methods="get", resource="/hellosanji")
    def get555(self, message, response):
        response(data={"message": self.message})

    @Route(methods="put", resource="/hellosanji")
    def put(self, message, response):
        if hasattr(message, "data"):
            self.message = message.data["message"]
            return response()
        return response(code=400, data={"message": "Invaild Input."})


if __name__ == '__main__':
    FORMAT = '%(asctime)s - %(levelname)s - %(lineno)s - %(message)s'
    logging.basicConfig(level=0, format=FORMAT)
    logger = logging.getLogger('Hellosanji')

    hellosanji = Hellosanji(connection=Mqtt())
    hellosanji.start()
