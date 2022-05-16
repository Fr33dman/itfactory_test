import re

from django.utils import timezone
from rest_framework import serializers

from shop.models import TradePoint, WorkerVisit, Worker
from shop.utils import normalize_phone_number, validate_phone_number


class TradePointModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradePoint
        fields = ('id', 'name')


class WorkerVisitModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkerVisit
        fields = '__all__'

    def validate_longitude(self, longitude):
        matches = re.fullmatch(
            '^(\+|-)?((\d((\.)|\.\d{1,6})?)|(0*?[0-8]\d((\.)|\.\d{1,6})?)|(0*?90((\.)|\.0{1,6})?))$',
            longitude
        )
        if not matches:
            raise serializers.ValidationError(
                'Долгота не соответствует формату'
            )
        return longitude

    def validate_latitude(self, latitude):
        matches = re.fullmatch(
            '^(\+|-)?((\d((\.)|\.\d{1,6})?)|(0*?\d\d((\.)|\.\d{1,6})?)|(0*?1[0-7]\d((\.)|\.\d{1,6})?)|(0*?180((\.)|\.0{1,6})?))$',
            latitude
        )
        if not matches:
            raise serializers.ValidationError(
                'Долгота не соответствует формату'
            )
        return latitude

    def validate(self, attrs):
        trade_point = attrs.get('trade_point')
        worker = attrs.get('worker')
        can_visit = TradePoint.objects.filter(id=trade_point.id, workers__id=worker.id).first()
        if not can_visit:
            raise serializers.ValidationError(
                'Вы не можете посетить данную торговую точку'
            )
        attrs['date'] = timezone.now()
        print(attrs)
        return attrs

    def to_representation(self, instance):
        result = {
            'id': instance.id,
            'date': instance.date,
        }
        return result


class ViewSerializer(serializers.Serializer):
    worker = serializers.CharField(max_length=12, write_only=True)
    trade_points = serializers.SerializerMethodField(read_only=True)

    def validate_worker(self, phone):
        return validate_phone_number(phone)

    def get_trade_points(self, phone):
        phone = normalize_phone_number(phone)
        queryset = TradePoint.objects.filter(workers__phone_number=phone)
        trade_points = TradePointModelSerializer(queryset, many=True)
        return trade_points.data


class VisitSerializer(serializers.Serializer):
    worker = serializers.CharField(max_length=12, write_only=True)
    trade_point = serializers.IntegerField(write_only=True)
    longitude = serializers.CharField(max_length=255, write_only=True)
    latitude = serializers.CharField(max_length=255, write_only=True)
    result = WorkerVisitModelSerializer(read_only=True)

    def validate_worker(self, phone):
        return validate_phone_number(phone)

    def validate(self, attrs):
        print(attrs)
        trade_point = attrs.get('trade_point')
        phone = attrs.get('phone')
        can_visit = TradePoint.objects.filter(id=trade_point, workers__phone_number=phone).exists()
        if not can_visit:
            raise serializers.ValidationError(
                'Вы не можете посетить данную торговую точку'
            )
        worker = Worker.objects.filter(phone_number=phone).first()
        visit = WorkerVisit(
            date=timezone.now(),
            trade_point_id=trade_point,
            worker_id=worker.pk,
            longitude=attrs.get('longitude'),
            latitude=attrs.get('latitude'),
        ).save()
        attrs['result'] = WorkerVisitModelSerializer(visit).data
        return attrs

