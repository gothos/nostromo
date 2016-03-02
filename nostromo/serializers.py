from rest_framework import serializers
from nostromo.models import DataSet


class DatasetSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataSet
