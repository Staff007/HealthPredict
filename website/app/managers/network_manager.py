from typing import Dict, Optional, Tuple

import flask_login
from app.managers.ipdata_manager import IpdataManager
from app.managers.weather_manager import WeatherManager
from app.models import User, Weather, Data
from flask import request


class NetworkManager:
    def __init__(self):
        self.ipdata_manager = IpdataManager(ip=self.get_ip())
        self.current_user: User = flask_login.current_user
        self.current_user_data: Data = flask_login.current_user

    def get_ip(self):
        # return request.remote_addr # для реального сервера
        return "178.68.70.67"  # для теста

    def get_user_answer(self) -> Dict[str, str]:
        return request.form
    
    def get_user_id(self) -> int:
        return self.current_user.id
    
    def get_id(self) -> int:
        return self.current_user_data.id
    
    def get_user_username(self) -> str:
        return self.current_user.username

    def get_user_avatar(self):
        return self.current_user.avatar()

    def get_lat_and_lon(self) -> Optional[Tuple[float, float]]:
        return self.ipdata_manager.get_lat_and_lon()

    def get_cur_weather(self) -> Optional[Weather]:
        lat_lon = self.get_lat_and_lon()
        if lat_lon is None:
            return None
        lat, lon = lat_lon
        weather_manager = WeatherManager(lat=lat, lon=lon)
        weather = weather_manager.get_weather()
        return weather

    def get_city(self) -> str:
        city = self.ipdata_manager.get_city()
        if city is None:
            city = "Город N"
        return city
