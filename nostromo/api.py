import logging

from datetime import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

from nostromo.models import DataSet
from nostromo.serializers import DatasetSerializer
import json

logger = logging.getLogger("api")


class DataSetPushView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = DatasetSerializer
    def get_permissions(self):
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):

        processed = 0
        success = 0
        converted_data = json.loads(request.data)
        for data in converted_data:
            start_date = datetime.utcfromtimestamp(data['start']/1000)
            end_date = datetime.utcfromtimestamp(data['end']/1000)
            data_type = data["type"]

            if not DataSet.objects.filter(type=data_type, start_date=start_date, end_date=end_date, user=request.user).exists():
                DataSet.objects.create(
                    start_date=start_date,
                    end_date=end_date,
                    data=data['data'],
                    user=request.user
                )
                success += 1
            processed += 1
        duplicates = processed - success
        result = {
            'processed': processed,
            'duplicate': duplicates,
            'success': success
        }
        return Response(result, status=status.HTTP_200_OK)