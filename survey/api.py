import logging

from datetime import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

from survey.models import UserSurvey
from survey.serializers import UserSurveysSerializer
import json
from rest_framework.decorators import detail_route


logger = logging.getLogger("api")

class SurveysViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = UserSurveysSerializer
    def get_permissions(self):
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        k = super().list(request, *args, **kwargs)
        k.data = k.data['results']
        return k


    def get_queryset(self):
        if self.request.user.is_authenticated():
            qs = UserSurvey.objects.filter(user=self.request.user)
            passed = self.request.query_params.get("passed", None)
            if passed :
                if passed == 'true':
                    qs = qs.filter(passed_at__isnull=False)
                elif passed == 'false':
                    qs = qs.filter(passed_at__isnull=True)
            new = self.request.query_params.get("new", None)
            if new :
                if new == 'true':
                    qs = qs.filter(new=True)
                elif new == 'false':
                    qs = qs.filter(new=False)
            return qs

        return UserSurvey.objects.none()


class SpecificSurveyViewSet(mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    serializer_class = UserSurveysSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def retrieve(self, request,pk=None):
        if pk:
            qs = UserSurvey.objects.filter(user=self.request.user,pk=pk)
            if qs.exists():

                serializer = self.serializer_class(qs.last())
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Wrong input", "error_code": "303"},
                        status=status.HTTP_400_BAD_REQUEST)


