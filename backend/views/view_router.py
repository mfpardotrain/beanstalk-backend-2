from django.views.decorators.csrf import csrf_exempt
from .base_view import BaseView
from ..controllers.authenticated_farm_controller import AuthenticatedFarmController
from ..controllers.authenticated_user_controller import AuthenticatedUserController
from ..controllers.create_user_controller import CreateUserController
from ..controllers.authenticated_farm_vegetable_controller import AuthenticatedFarmVegetableController
from ..controllers.authenticated_market_info_controller import AuthenticatedMarketInfoController
from ..controllers.authenticated_market_controller import AuthenticatedMarketController
from ..controllers.order_controller import OrderController
from ..controllers.search_controller import SearchController
from ..serializers import *
from ..models import *


# User routes
@csrf_exempt
def user_route(request):
    return BaseView(controller=AuthenticatedUserController, request=request, model=FarmBoy, serializer=UserSerializer).perform()


@csrf_exempt
def create_user_route(request):
    return BaseView(controller=CreateUserController, request=request, model=FarmBoy, serializer=UserSerializer).perform()


# Farmer routes
@csrf_exempt
def farm_route(request):
    return BaseView(request=request, model=Farm, serializer=FarmSerializer).perform()


@csrf_exempt
def farmer_farm_route(request):
    return BaseView(controller=AuthenticatedFarmController, request=request, model=Farm, serializer=FarmSerializer).perform()


@csrf_exempt
def farmer_market_info_route(request):
    return BaseView(controller=AuthenticatedMarketInfoController, request=request, model=MarketInfo, serializer=MarketInfoSerializer).perform()


@csrf_exempt
def farmer_farm_vegetable_route(request):
    return BaseView(controller=AuthenticatedFarmVegetableController, request=request, model=FarmVegetable, serializer=FarmVegetableSerializer).perform()


@csrf_exempt
def farmer_market_route(request):
    return BaseView(controller=AuthenticatedMarketController, request=request, model=Market, serializer=MarketSerializer).perform()


# Customer routes
@csrf_exempt
def order_route(request):
    return BaseView(controller=OrderController, request=request, model=Order, serializer=OrderSerializer).perform()


@csrf_exempt
def market_farm_search_route(request):
    return BaseView(controller=SearchController, request=request, model=None, serializer=None).perform()

