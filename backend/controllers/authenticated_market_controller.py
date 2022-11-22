from .authenticated_controller import AuthenticatedController


class AuthenticatedMarketController(AuthenticatedController):
    def get(self):
        filtered = self.model.objects.all().exclude(farms=self.user.farm)
        serializer = self.serializer(instance=filtered, many=True)
        return self.standard_json_response(status=200, message="success", data=serializer.data)

    def delete(self):
        return self.standard_json_response(status=501, message="Not Implemented", data={})

    def fix_data(self):
        self.data["created_by"] = str(self.user)
        self.data["updated_by"] = str(self.user)
