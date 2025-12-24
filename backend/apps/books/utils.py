import requests
import json
import html  # [추가]
from haversine import haversine
from django.conf import settings
from .models import Store


class KakaoGeoAPI:
    """
    카카오 로컬 API를 사용하여 주소나 키워드를 위경도 좌표로 변환.
    """
    REST_API_KEY = settings.KAKAO_REST_API_KEY

    @classmethod
    def get_coordinates(cls, address):
        """
        주소 문자열을 받아 (위도, 경도) 튜플을 반환. 실패 시 None.
        """
        if not address:
            return None

        # 1. 주소 검색 (도로명/지번)
        url_address = "https://dapi.kakao.com/v2/local/search/address.json"

        # 2. 키워드 검색 - "강남역" 같이 주소가 아닌 키워드를 넣었을 경우
        url_keyword = "https://dapi.kakao.com/v2/local/search/keyword.json"

        headers = {"Authorization": f"KakaoAK {cls.REST_API_KEY}"}

        try:
            # 주소 검색
            params = {"query": address}
            response = requests.get(url_address, headers = headers, params = params, timeout = 5)

            if response.status_code == 200:
                data = response.json()
                documents = data.get('documents')
                if documents:
                    x = float(documents[0]['x'])  # 경도
                    y = float(documents[0]['y'])  # 위도
                    return (y, x)

            # 키워드 검색
            response = requests.get(url_keyword, headers = headers, params = params, timeout = 5)
            if response.status_code == 200:
                data = response.json()
                documents = data.get('documents')
                if documents:
                    x = float(documents[0]['x'])
                    y = float(documents[0]['y'])
                    return (y, x)

        except Exception as e:
            print(f"[KakaoGeoAPI] Error fetching coordinates for '{address}': {e}")

        return None


class AladinStockService:
    """
    알라딘 API와 로컬 DB를 연동하여 재고 및 위치 정보를 제공.
    """
    TTB_KEY = settings.ALADIN_TTB_KEY
    BASE_URL = "http://www.aladin.co.kr/ttb/api"

    @classmethod
    def get_nearest_stock_stores(cls, isbn, user_coords):
        """
        주어진 도서를 보유한 알라딘 중고매장 리스트 반환.
        user_coords (lat, lon)를 기준으로 거리를 계산하여 가까운 순서대로 정렬.
        """
        if not cls.TTB_KEY:
            print("[AladinStockService] Error: ALADIN_TTB_KEY is missing.")
            return []

        if not user_coords:
            # 좌표가 없으면 거리 계산 불가 -> 빈 리스트 혹은 정렬 안 된 전체 리스트 반환
            # 여기서는 빈 리스트 반환
            return []

        # 알라딘 API 호출 (해당 도서를 보유한 매장 리스트 가져오기)
        api_stores = cls._fetch_off_store_list(isbn)
        if not api_stores:
            return []  # 재고 있는 매장이 없음

        # DB 매장 정보 로드 (좌표 매칭용)
        # 전체 매장 수가 적으므로(59개) 전체를 가져와서 메모리에서 매칭
        db_stores = Store.objects.all()

        results = []
        for api_store in api_stores:
            # API가 주는 매장명 (예: "알라딘 중고서점 강남점")
            api_store_name = html.unescape(api_store.get('offName', ''))
            link = html.unescape(api_store.get('link', ''))
            off_code = api_store.get('offCode', '')

            # DB 매장 찾기 (이름 매칭)
            # 로직: DB의 매장명(예: "강남점")이 API 매장명에 포함되어 있는지 확인
            # 공백 제거 후 비교하면 적중률이 높음 ("강남점" in "알라딘중고서점강남점")
            matched_db_store = None
            for db_s in db_stores:
                if db_s.name.replace(' ', '') in api_store_name.replace(' ', ''):
                    matched_db_store = db_s
                    break

            # 매칭 성공 및 좌표 존재 시 거리 계산
            if matched_db_store and matched_db_store.lat is not None:
                store_coords = (matched_db_store.lat, matched_db_store.lon)

                # 거리 계산 (단위: km)
                distance = haversine(user_coords, store_coords, unit = 'km')

                results.append({
                    "name": api_store_name,
                    "branch_code": matched_db_store.branch_code,
                    "distance_km": round(distance, 1),
                    "link": link,
                    "off_code": off_code,
                    "lat": matched_db_store.lat,
                    "lon": matched_db_store.lon,
                    "stock_status": "재고 있음"  # API에서 왔으므로 항상 있음
                })
            else:
                # 좌표를 모르는 매장은 결과에서 제외
                pass

        # 거리순 오름차순 정렬 (가까운 매장이 먼저 나오도록)
        results.sort(key = lambda x: x['distance_km'])

        return results

    @classmethod
    def _fetch_off_store_list(cls, isbn):
        """
        알라딘 ItemOffStoreList API 호출 - 재고 보유 매장 리스트 반환
        """
        url = f"{cls.BASE_URL}/ItemOffStoreList.aspx"
        params = {
            'ttbkey': cls.TTB_KEY,
            'itemIdType': 'ISBN13',
            'ItemId': isbn,
            'output': 'js'  # JSON 포맷
        }

        try:
            response = requests.get(url, params = params, timeout = 5)

            print(f"\n[ALADIN API RAW RESPONSE] ISBN: {isbn}")
            print(response.text)  # <--- 이 줄을 추가하세요!
            print("--------------------------------------------------\n")

            response.raise_for_status()

            data = response.json()
            # itemOffStoreList 필드 추출
            return data.get('itemOffStoreList', [])

        except requests.exceptions.RequestException as e:
            print(f"[AladinStockService] API Request Error: {e}")
            return []
        except ValueError as e:  # JSON Decode Error
            print(f"[AladinStockService] JSON Parse Error: {e}")
            return []