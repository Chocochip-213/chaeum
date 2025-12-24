from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .utils import AladinStockService, KakaoGeoAPI
from .serializers import BookStockQuerySerializer, BookStockResponseSerializer


class BookStockView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters = [BookStockQuerySerializer],
        responses = {200: BookStockResponseSerializer}
    )
    def get(self, request, isbn):
        serializer = BookStockQuerySerializer(data = request.query_params)
        serializer.is_valid(raise_exception = True)

        address = serializer.validated_data.get('address')
        lat = serializer.validated_data.get('lat')
        lon = serializer.validated_data.get('lon')
        user_coords = None
        if lat and lon:
            user_coords = (lat, lon)

        if not user_coords and address:
            user_coords = KakaoGeoAPI.get_coordinates(address)
        if not user_coords and request.user.is_authenticated:
            saved_addr = getattr(request.user, 'address', None)
            if saved_addr:
                address = saved_addr
                user_coords = KakaoGeoAPI.get_coordinates(saved_addr)
        if not user_coords:
            return Response(
                {"error": "주소를 입력해주세요. (백엔드에서 좌표로 변환해드립니다)"},
                status = status.HTTP_400_BAD_REQUEST
            )
        stores = AladinStockService.get_nearest_stock_stores(isbn, user_coords)
        return Response({
            "isbn": isbn,
            "user_location": {
                "address": address,
                "lat": user_coords[0],
                "lon": user_coords[1]
            },
            "count": len(stores),
            "stores": stores
        }, status = status.HTTP_200_OK)