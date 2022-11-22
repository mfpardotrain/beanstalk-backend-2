from ..models import MarketInfo

class MarketOrderValidator:
    def __init__(self):
        return

    def prepare_order(self, order):
        market_info = MarketInfo.objects.get(id=order.market_info.id)
        vegetable_ids = [vegetable.id for vegetable in market_info.farm_vegetables.all()]
        for vegetable in order.vegetables:
            if vegetable['id'] not in vegetable_ids:
                order.data_errors.append({"message": f"{vegetable.name} is not sold at {market_info.market.name}"})
