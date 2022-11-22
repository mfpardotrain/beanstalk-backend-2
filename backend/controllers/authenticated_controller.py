from .base_controller import BaseController
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication


class AuthenticatedController(BaseController):
    def after_initialize(self, kwargs):
        user_auth_tuple = TokenAuthentication().authenticate(self.request)
        if user_auth_tuple is None:
            return JsonResponse(status=404, data={"message": "Invalid authentication", "data": None})
        else:
            (user, token) = user_auth_tuple
            self.user = user
            self.user_id = user.id
            self.token = token

    def delete(self):
        try:
            data = self.model.objects.filter(created_by=self.user.username).get(id=self.object_id).delete()
            return self.standard_json_response(status=200, message="success", data=data)
        except self.model.DoesNotExist:
            return self.standard_json_response(status=400, message=f"{self.model} does not exist with that id", data={})

    # Post methods
    def update(self):
        self.fix_data()
        try:
            obj = self.model.objects.filter(farmer=self.user.id).get(id=self.object_id)
            serializer = self.serializer(data=self.data, instance=obj, partial=True)
            return self.validate_serializer(serializer)
        except self.model.DoesNotExist:
            return self.standard_json_response(status=400, message=f"{self.model} does not exist with that id", data={})

    def create(self):
        self.fix_data()
        serializer = self.serializer(data=self.data, partial=False)
        return self.validate_serializer(serializer)

    # model specific data needs
    def fix_data(self):
        return