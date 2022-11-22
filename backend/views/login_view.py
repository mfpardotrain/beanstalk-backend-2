from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


class LoginView(ObtainAuthToken):
    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'is_farmer': user.is_farmer,
            }
            return JsonResponse(status=200, data={"status": 200, "message": "success", "data": data})
        else:
            return JsonResponse(status=400, data={"status": 400, "message": serializer.errors, "data": serializer.errors})
