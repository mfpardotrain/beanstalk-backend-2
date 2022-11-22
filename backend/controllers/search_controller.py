from ..models import Market, MarketInfo
from .base_controller import BaseController
from ..serializers import MarketSerializer, MarketVegetableSerializer


class SearchController(BaseController):
    def get(self):
        markets = MarketSerializer(Market.objects.all(), many=True).data
        farms = MarketVegetableSerializer(MarketInfo.objects.all(), many=True).data
        for farm in farms:
            farm['name'] = farm['farm']['name'] + ' at ' + farm['market']['name']
            farm['type'] = 'farm'
        for market in markets:
            market['type'] = 'market'
        data = markets + farms
        return self.standard_json_response(status=200, message='success', data=data)

