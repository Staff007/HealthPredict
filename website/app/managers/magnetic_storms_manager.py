import time

from typing import Optional
from requests import get


class MagneticStormsManager:
    def __init__(self):
        self.api_key = "pSHEACFndRX7pJ5FivlPWt4eRkalFdCYy94jiUKO"

    def get_magnetic_storms(self) -> Optional[int]:
        request_string = "https://api.nasa.gov/DONKI/GST?startDate=yyyy-MM-dd&endDate=yyyy-MM-dd&api_key=DEMO_KEY"
        try:
            start_date = time.strftime("%Y-%m-%d")
            result = get(
                request_string,
                params={
                    "startDate": start_date,
                    "location": "Earth",
                    "catalog": "SWRC_CATALOG",
                    "api_key": self.api_key,
                },
            )

            if not result.content:
                return 0

            data = result.json()

            return int(data[-1]["allKpIndex"][-1]["kpIndex"])
        except Exception as e:
            print(f"Ошибка при получении магнитных бурь {e}")

            return None
