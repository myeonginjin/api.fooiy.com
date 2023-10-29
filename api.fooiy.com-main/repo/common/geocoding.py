import requests
from common import index as Common

REVERSE_GEOCODING_URL = (
    "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc?coords="
)
GEOCODING_URL = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query="
CLIENT_ID = "oingm1h0rz"
CLIENT_SECRET = "Iljylcie23BNUM8r9y8WcweI78O6OX2fNYsTjZJt"
headers = {
    "X-NCP-APIGW-API-KEY-ID": CLIENT_ID,
    "X-NCP-APIGW-API-KEY": CLIENT_SECRET,
}
convert_depth1 = {
    "서울특별시": "서울",
    "부산광역시": "부산",
    "인천광역시": "인천",
    "대전광역시": "대전",
    "대구광역시": "대구",
    "광주광역시": "광주",
    "울산광역시": "울산",
    "서울시": "서울",
    "부산시": "부산",
    "인천시": "인천",
    "대전시": "대전",
    "대구시": "대구",
    "광주시": "광주",
    "울산시": "울산",
    "경기도": "경기",
    "강원도": "강원",
    "충청남도": "충남",
    "충청북도": "충북",
    "경상남도": "경남",
    "경상북도": "경북",
    "전라남도": "전남",
    "전라북도": "전북",
    "제주특별자치도": "제주",
    "제주도": "제주",
    "세종특별자치시": "세종",
    "세종시": "세종",
}


def convert_coordinate_to_address(longitude, latitude):
    """
    # 좌표를 주소로 변환하는 함수
    """
    try:
        response = requests.get(
            REVERSE_GEOCODING_URL + longitude + "," + latitude + "&output=json",
            headers=headers,
        )
        response = response.json()
        if response["status"].get("code", None) == 0:
            address_depth1 = response["results"][0]["region"]["area1"].get("alias")
            address_depth2 = response["results"][0]["region"]["area2"].get("name", None)
            address_depth3 = response["results"][0]["region"]["area3"].get("name", None)

            if address_depth2 == "":
                address_depth2 = address_depth1
            if address_depth3 == "":
                address_depth3 = address_depth2

            return address_depth1, address_depth2, address_depth3

        return None, None, None
    except Exception as e:
        Common.fooiy_standard_response(
            False, 5555, location="convert_coordinate_to_address error", error=e
        )
        return None, None, None


def convert_address_to_coordinate(address):
    """
    # 주소를 좌표로 변환하는 함수
    """
    try:
        response = requests.get(GEOCODING_URL + address, headers=headers)
        response = response.json()
        if response["status"] == "OK":
            response = response["addresses"]

            longitude = response[0].get("x", "")
            latitude = response[0].get("y", "")
            return longitude, latitude
        else:
            return None, None
    except Exception as e:
        Common.fooiy_standard_response(
            False,
            5555,
            location="convert_address_to_coordinate",
            address=address,
            error=e,
        )
        return None, None


def synchronize_address(address):
    """
    # 주소 동기화 함수
    """

    if address:
        for address_depth1, convert_address_depth1 in convert_depth1.items():
            address = address.replace(address_depth1, convert_address_depth1)

    return address
