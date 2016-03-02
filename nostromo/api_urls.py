from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from account.api import UserModelViewSet
from nostromo.api import DataSetPushView

api_router = routers.DefaultRouter()
api_router.register(r'account', UserModelViewSet, base_name="account")
api_router.register(r'push', DataSetPushView, base_name="push")

urlpatterns = [
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(api_router.urls)),
]

