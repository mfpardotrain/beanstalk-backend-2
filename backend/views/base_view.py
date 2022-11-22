from rest_framework.parsers import JSONParser
from ..controllers.base_controller import BaseController


class BaseView:
    def __init__(self, controller=BaseController, **kwargs):
        self.user = False
        self.model = kwargs["model"]
        self.serializer = kwargs["serializer"]
        self.request = kwargs["request"]
        self.controller = controller
        self.method = self.request.method

    def perform(self):
        return self.controller(self).perform()

    def data(self):
        if len(self.request.body) > 0:
            return JSONParser().parse(self.request)
        else:
            return {}
