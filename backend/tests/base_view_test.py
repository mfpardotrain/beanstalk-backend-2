from django.test import TestCase
from ..views.base_view import BaseView


class BaseViewTest(TestCase):
    def setUp(self):
        self.methods = [method for method in dir(BaseView)]
        pass

    def test_base_controller_implements_perform(self):
        self.assertTrue("perform" in self.methods)

    def test_base_controller_implements_data(self):
        self.assertTrue("data" in self.methods)

    def test_base_controller_implements_authenticate(self):
        self.assertTrue("authenticate" in self.methods)

    def test_base_controller_implements_method(self):
        self.assertTrue("method" in self.methods)

    def tearDown(self):
        # Clean up run after every test method.
        pass
