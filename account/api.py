import logging

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from account.models import User

from account.serializers import UserSerializer, SignInSerializer, \
    SignUpSerializer


logger = logging.getLogger("api")


class UserModelViewSet(ModelViewSet):

    serializer_class = UserSerializer
    serializer_classes = {
        "signin": SignInSerializer,
        #"create": SignUpSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none()

    def get_permissions(self):
        if self.request.method in ['POST', 'OPTIONS']:
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            error_data = {
                "error": "Registration error",
                "error_code": 102,
                "errors": errors
            }
            return Response(error_data, status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        token, created = Token.objects.get_or_create(user=self.request.user)
        data = serializer.data.copy()
        data["token"] = token.key
        data["is_active"] = True
        return Response(data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        password = serializer.validated_data["password"]
        self.request.user = serializer.save(password=make_password(password))

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def signin(self, request):
        print(request.data.get("email"))
        print(request.data.get("password"))
        user = authenticate(
            username=request.data.get("email"),
            password=request.data.get("password"),
        )
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        return Response({"error": "Wrong credentials", "error_code": "101"},
                        status=status.HTTP_400_BAD_REQUEST)

