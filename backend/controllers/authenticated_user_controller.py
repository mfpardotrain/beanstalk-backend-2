from .authenticated_controller import AuthenticatedController


class AuthenticatedUserController(AuthenticatedController):
    def get_by_user(self):
        obj = self.model.objects.filter(id=self.user.id).first()
        serializer = self.serializer(instance=obj)
        return self.standard_json_response(status=200, message="success", data=serializer.data)

    def update(self):
        try:
            obj = self.model.objects.get(id=self.user_id)
            serializer = self.serializer(data=self.data, instance=obj, partial=True)
            return self.validate_serializer(serializer)
        except self.model.DoesNotExist:
            return self.standard_json_response(status=400, message=f"{self.model} does not exist with that id", data={})
