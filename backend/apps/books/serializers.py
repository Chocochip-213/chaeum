from rest_framework import serializers


class BookStockQuerySerializer(serializers.Serializer):
    address = serializers.CharField(required=False, help_text="사용자 주소 (예: 서울 강남구)")
    lat = serializers.FloatField(required=False, help_text="위도 (GPS)")
    lon = serializers.FloatField(required=False, help_text="경도 (GPS)")

class StoreStockSerializer(serializers.Serializer):
    name = serializers.CharField()
    branch_code = serializers.CharField()
    distance_km = serializers.FloatField()
    link = serializers.URLField()
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    stock_status = serializers.CharField()

class BookStockResponseSerializer(serializers.Serializer):
    isbn = serializers.CharField()
    user_location = serializers.DictField()
    count = serializers.IntegerField()
    stores = StoreStockSerializer(many=True)