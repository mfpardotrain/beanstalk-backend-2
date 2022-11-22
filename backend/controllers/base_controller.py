from django.http import JsonResponse


class BaseController:
    def __init__(self, view, **kwargs):
        # attributes
        self.serializer = view.serializer
        self.model = view.model
        self.data = view.data()
        self.method = view.method
        self.user = view.user
        self.request = view.request
        self.object_id = self.data.get("id", False)
        self.user_id = self.data.get("user_id", False)

        # subclass initialize
        self.after_initialize(kwargs)
        return

    def perform(self):
        method = self.method
        if method == "GET":
            return self.get()
        elif method == "POST":
            return self.post()
        elif method == "DELETE":
            return self.delete()
        else:
            raise ValueError("No method called " + self.method)

    # private methods

    # post methods
    def post(self):
        if self.object_id:
            return self.update()
        else:
            return self.create()

    def create(self):
        serializer = self.serializer(data=self.data, partial=False)
        return self.validate_serializer(serializer)

    def update(self):
        return self.standard_json_response(status=501, message="Not Implemented", data={})

    # get methods
    def get(self):
        if self.object_id:
            return self.get_by_id()
        elif self.user_id:
            return self.get_by_user()
        else:
            return self.get_all()

    def get_by_id(self):
        try:
            obj = self.model.objects.get(id=self.object_id)
        except self.model.DoesNotExist:
            return self.standard_json_response(status=400,
                                               message=f"{self.model} does not exist with that id",
                                               data={})
        serializer = self.serializer(instance=obj, many=False)
        return self.standard_json_response(status=200, message="success", data=serializer.data)

    def get_by_user(self):
        obj = self.model.objects.filter(farmer=self.user.id).all()
        serializer = self.serializer(instance=obj, many=True)
        return self.standard_json_response(status=200, message="success", data=serializer.data)

    def get_all(self):
        obj = self.model.objects.all()
        serializer = self.serializer(instance=obj, many=True)
        return self.standard_json_response(status=200, message="success", data=serializer.data)

    # delete methods
    def delete(self):
        try:
            data = self.model.objects.get(id=self.object_id).delete()
            return self.standard_json_response(status=200, message="success", data=data)
        except self.model.DoesNotExist:
            return self.standard_json_response(status=400, message=f"{self.model} does not exist with that id", data={})
        return self.standard_json_response(status=501, message="Not Implemented", data={})

    @staticmethod
    def standard_json_response(status, data, message):
        return JsonResponse(status=status, data={"status": status, "message": message, "data": data})

    # can be overwritten by subclasses
    def after_initialize(self, kwargs):
        return

    def validate_serializer(self, serializer):
        if serializer.is_valid():
            serializer.save()
            return self.standard_json_response(status=200, message="success", data=serializer.data)
        else:
            return self.standard_json_response(status=400, message="failure", data=serializer.errors)
