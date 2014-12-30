#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging

from time import sleep
from sanji.core import Sanji
from sanji.core import Route
from sanji.connection.mqtt import Mqtt


class Event(Sanji):

    @Route(methods="put", resource="/network/cellulars/ipchange")
    def sub_event(self, message):
        print message.to_dict()

    # This function will be executed after registered.
    def run(self):
        count = 0
        while True:
            count = count + 1
            if count >= 254:
                count = 1
            # event would not have response
            self.publish.event.put("/network/cellulars/ipchange",
                                   data={"ip": "192.168.1.%s" % (count,)})
            sleep(5)


if __name__ == "__main__":
    FORMAT = "%(asctime)s - %(levelname)s - %(lineno)s - %(message)s"
    logging.basicConfig(level=0, format=FORMAT)
    logger = logging.getLogger('Event')

    event = Event(connection=Mqtt())
    event.start()
