from .base_controller import BaseController
from ..models import Farm


class CreateUserController(BaseController):
    def after_initialize(self, view, kwargs):
        is_farmer = self.data['is_farmer']
        if is_farmer:
            farm_id = int(self.data['farm']['id'])
            farm = Farm.objects.get(id=farm_id)
        else:
            farm = None
        self.data.update({
            'created_by': 'initial',
            'updated_by': 'initial',
            'username': self.data['email'],
            'is_staff': False,
            'is_superuser': False,
            'farm': farm
        })

    def post(self):
        serializer = self.serializer(data=self.data, partial=False)
        return self.validate_serializer(serializer)

    def get(self):
        return self.standard_json_response(status=501, message="Not Implemented", data={})

    def delete(self):
        return self.standard_json_response(status=501, message="Not Implemented", data={})

    def validate_serializer(self, serializer):
        if serializer.is_valid():
            serializer.create(self.data)
            return self.standard_json_response(status=200, message="success", data=serializer.data)
        else:
            return self.standard_json_response(status=400, message="failure", data=serializer.errors)
