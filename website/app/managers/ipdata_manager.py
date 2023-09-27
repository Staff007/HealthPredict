from typing import Dict, Optional, Tuple

from ipdata import ipdata


class IpdataManager:
    def __init__(self, ip: str):
        self.api_key = "bc859e6746afa069cbac1b77e5504837ad48b90701b405148b595e79"
        self.response = self.get_response(ip=ip)

    def get_response(
        self, ip: str
    ) -> (Optional[Dict[str, int]] or Optional[Dict[str, str or int]]):
        try:
            ip_data = ipdata.IPData(self.api_key)
            response = ip_data.lookup(fields=["latitude", "longitude", "city"])
            print(response)
            return response
        except Exception as e:
            print(f"Ошибка при попытке получить ответ IPData: {e}")
            return None

    def get_lat_and_lon(self) -> Optional[Tuple[float, float]]:
        try:
            lat = float(self.response["latitude"])
            lon = float(self.response["longitude"])
            answer = (lat, lon)
            return answer
        except Exception as e:
            print(f"Ошибка при попытке определения широты и долготы: {e}")
            return None

    def get_city(self) -> Optional[str]:
        try:
            city = self.response["city"]
            return city
        except Exception as e:
            print(f"Ошибка при попытке определения города: {e}")
            return None
