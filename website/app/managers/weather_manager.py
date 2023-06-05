from typing import Optional

from app.managers.magnetic_storms_manager import MagneticStormsManager
from app.managers.openweather_manager import OpenweatherManager
from app.models import Weather


class WeatherManager:
    def __init__(self, lat: float, lon: float):
        self.lat = (lat,)
        self.lon = lon
        self.openweather_manager = OpenweatherManager(lat, lon)
        self.magnetic_storms_managers = MagneticStormsManager()

    def get_weather(self) -> Optional[Weather]:
        temperature = self.openweather_manager.get_temperature()
        pressure = self.openweather_manager.get_pressure()
        magnetic_storms = self.magnetic_storms_managers.get_magnetic_storms()
        if (
            temperature is not None
            and pressure is not None
            and magnetic_storms is not None
        ):
            weather = Weather(
                pressure=pressure,
                temperature=temperature,
                magnetic_storms=magnetic_storms,
            )
            return weather
        return None
