from django.test import TestCase
from ..controllers.base_controller import BaseController
from ..models import *
from ..serializers import *
import requests
from unittest import mock
import json


class MockView:
    def __init__(self, method):
        self.farm_data = {
            "id": None,
            "farm_name": "test_farm",
            "address": "test_road",
            "stripe_account_id": 1,
            "is_registered": True,
            "min_order_amount": 10
        }
        self.serializer = FarmSerializer
        self.model = Farm
        self.method_holder = method

    def data(self):
        return self.farm_data

    def method(self):
        return self.method_holder


class BaseControllerTest(TestCase):
    def setUp(self):
        self.methods = [method for method in dir(BaseController)]
        self.test_controller = BaseController(MockView("GET"))
        pass

    def test_base_controller_implements_perform(self):
        self.assertTrue("perform" in self.methods)

    def test_base_controller_implements_get(self):
        self.assertTrue("get" in self.methods)

    def test_base_controller_implements_post(self):
        self.assertTrue("post" in self.methods)

    def test_base_controller_implements_delete(self):
        self.assertTrue("delete" in self.methods)

    def test_base_controller_implements_object(self):
        self.assertTrue("object" in self.methods)

    def tearDown(self):
        # Clean up run after every test method.
        pass
