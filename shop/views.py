from django.utils import timezone
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from src.mixins import SerializerViewSetMixin
from shop.models import Worker
from shop.utils import normalize_phone_number
from shop.serializers import ViewSerializer, WorkerVisitModelSerializer


class TradePointViewSet(ViewSet, SerializerViewSetMixin):

    serializers = {
        'view': ViewSerializer,
        'visit': WorkerVisitModelSerializer,
    }

    @action(methods=['GET'], detail=False, url_path='view/(?P<phone>[+0-9]{11,12})')
    def view(self, request, phone):
        serializer = self.get_serializer_class()(phone)
        response = serializer.data
        return Response(response)

    @action(methods=['POST'], detail=False, url_path='visit/(?P<phone>[+0-9]{11,12})')
    def visit(self, request, phone):
        phone = normalize_phone_number(phone)
        worker = Worker.objects.filter(phone_number=phone).first()
        data = {
            'worker': worker.pk,
            **request.data,
        }
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.create(serializer.validated_data)
        response = serializer_class(instance=instance).data
        return Response(response)
