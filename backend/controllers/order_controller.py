from rest_framework.authentication import TokenAuthentication

from .base_controller import BaseController
from ..utils.farm_vegetable_order_validator import FarmVegetableOrderValidator
from ..utils.payment_validator import PaymentValidator
from ..utils.market_order_validator import MarketOrderValidator
from ..utils.cron_utils import CronUtils
from ..models import *

import math


class OrderController(BaseController):
    def after_initialize(self, kwargs):
        # authentication
        user_auth_tuple = TokenAuthentication().authenticate(self.request)
        if user_auth_tuple is None:
            self.user = False
            self.user_email = "guest"  # TODO: change this to guest email when guest frontend fleshed out
            self.user_id = None
            self.token = False
        else:
            (user, token) = user_auth_tuple
            self.user = user
            self.user_email = user.email
            self.user_id = user.id
            self.token = token

    def initialize_post_request(self):
        # configs
        self.STRIPE_PERCENT_FEE = .029
        self.STRIPE_CONSTANT_FEE = 30
        self.BEANSTALK_PERCENT_FEE = .05
        self.BEANSTALK_CONSTANT_FEE = 30

        # frontend request data
        self.vegetables = self.data['vegetables'].values()
        self.market_info = MarketInfo.objects.get(id=self.data['market_info']['id'])
        self.farm = Farm.objects.get(id=self.data['market_info']['farm']['id'])
        self.farmer = FarmBoy.objects.get(id=self.data['market_info']['farmer']['id'])

        # mutable
        self.data_errors = []
        self.serializer_errors = []
        self.vegetable_serializers = []
        self.stripe_checkout_session_id = "None"

    def post(self):
        self.initialize_post_request()
        order = self.initialize_order()
        FarmVegetableOrderValidator().prepare_order(self)

        if self.has_errors():
            return self.handle_errors()

        MarketOrderValidator().prepare_order(self)

        if self.has_errors():
            return self.handle_errors()

        PaymentValidator().prepare_order(self)

        if self.has_errors():
            return self.handle_errors()

        self.vegetable_orders = self.save_farm_vegetables()
        order.amount = self.calculate_price()
        order.fee = self.calculate_fee(order.amount)
        order.stripe_checkout_session_id = self.stripe_checkout_session_id

        order.save()
        order.farm_vegetables.set([vegetable_order.id for vegetable_order in self.vegetable_orders])
        return self.standard_json_response(status=200, message='success', data=None)

    def initialize_order(self):
        return self.model(
            market_info=self.market_info,
            farmer=self.farmer,
            farm=self.farm,
            customer=self.user,
            market_pickup_date=CronUtils(cron_string=self.market_info.cron_string).get_next_date(),
            amount=None,
            fee=None,
            stripe_checkout_session_id="none",  # TODO: update with stripe
            status='pending payment',
            created_by=self.user_email,
            updated_by=self.user_email,
        )

    def has_errors(self):
        return self.has_data_errors() or self.has_serializer_errors()

    def has_data_errors(self):
        return self.data_errors

    def has_serializer_errors(self):
        return self.serializer_errors

    def handle_errors(self):
        errors = self.data_errors + self.serializer_errors
        return self.standard_json_response(status=400, message="Failed data validation", data=errors)

    def save_farm_vegetables(self):
        return [serializer.save() for serializer in self.vegetable_serializers]

    def calculate_price(self):
        total = 0
        for vegetable in self.vegetable_orders:
            total += vegetable.price * float(vegetable.order_amount)
        return total

    def calculate_fee(self, amount):
        return math.ceil(((amount + self.STRIPE_CONSTANT_FEE) / (1 - self.STRIPE_PERCENT_FEE - self.BEANSTALK_PERCENT_FEE)) - amount)
