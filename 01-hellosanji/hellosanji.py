#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import os
from sanji.core import Sanji
from sanji.core import Route
from sanji.model_initiator import ModelInitiator
from sanji.connection.mqtt import Mqtt


class Hellosanji(Sanji):

    def init(self, *args, **kwargs):
        path_root = os.path.abspath(os.path.dirname(__file__))
        self.model = ModelInitiator("hellosanji", path_root)
        self.message = "Hello Sanji!"

    @Route(methods="get", resource="/hellosanji")
    def get(self, message, response):

        if hasattr(message, "param"):
            if "query" in message.param:
                if "collection" in message.param["query"]:
                    if message.param["query"]["collection"] == "true":
                        # collection=true
                        return response(data=self.model.db["conversationList"])
            if "id" in message.param:
                rsp_msg = None
                for item in self.model.db["conversationList"]:
                    if item["id"] == message.param["id"]:
                        # information of specific id
                        rsp_msg = item["message"]

                return response(data=rsp_msg)

        # capability
        id_list = []
        for item in self.model.db["conversationList"]:
            id_list.append(item["id"])
        return response(data=id_list)

    @Route(methods="put", resource="/hellosanji")
    def put(self, message, response):
        if hasattr(message, "data"):
            self.message = message.data["message"]
            return response()
        return response(code=400, data={"message": "Invaild Input."})

    @Route(methods="post", resource="/hellosanji")
    def post(self, message, response):
        if hasattr(message, "data"):
            self.message = {"id": 53}
            return response(data=self.message)
        return response(code=400, data={"message": "Invalid Post Input."})

    @Route(methods="delete", resource="/hellosanji/:id")
    def delete(self, message, response):
        if hasattr(message, "param"):
            if "id" in message.param:
                self.message = "delete index: %s" % message.param["id"]
                return response()

        return response(code=400, data={"message": "Invalid Delete Input."})


if __name__ == "__main__":
    FORMAT = "%(asctime)s - %(levelname)s - %(lineno)s - %(message)s"
    logging.basicConfig(level=0, format=FORMAT)
    logger = logging.getLogger("Hellosanji")

    hellosanji = Hellosanji(connection=Mqtt())
    hellosanji.start()
