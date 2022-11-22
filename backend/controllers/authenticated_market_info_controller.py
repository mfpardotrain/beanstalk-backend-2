from .authenticated_controller import AuthenticatedController
from ..models import Market
from ..serializers import MarketInfoPostSerializer


class AuthenticatedMarketInfoController(AuthenticatedController):
    def create(self):
        market = Market.objects.get(id=self.data["market"]["id"])
        market.farms.add(self.user.farm)
        self.fix_data()
        self.serializer = MarketInfoPostSerializer
        serializer = self.serializer(data=self.data, partial=False)
        return self.validate_serializer(serializer)

    def fix_data(self):
        self.data["farmer"] = self.user.id
        self.data["market"] = self.data["market"]["id"]
        self.data["created_by"] = str(self.user)
        self.data["updated_by"] = str(self.user)
        self.data["farm"] = self.user.farm.id
        self.data["market_duration_minutes"] = self.get_market_duration()

    def get_market_duration(self):
        start = self.data["cron_string"].split(" ")
        end = self.data["end_cron_string"].split(" ")
        duration = (int(end[0]) + (int(end[1]) * 60)) - (int(start[0]) + (int(start[1]) * 60))
        return duration

    def get_by_user(self):
        obj = self.model.objects.filter(farmer=self.user.id).all()
        serializer = self.serializer(instance=obj, many=True)
        return self.standard_json_response(status=200, message="success", data=serializer.data)

    def delete(self):
        market = Market.objects.get(id=self.data["market"]["id"])
        market.farms.remove(self.user.farm)
        try:
            data = self.model.objects.filter(created_by=self.user.username).get(id=self.object_id).delete()
            return self.standard_json_response(status=200, message="success", data=data)
        except self.model.DoesNotExist:
            return self.standard_json_response(status=400, message=f"{self.model} does not exist with that id", data={})
