import os.path
import sqlite3
from sqlite3.dbapi2 import Connection
from typing import Dict

from app import db
from app.models import Data, User, Weather
from pandas import read_sql_query
from pandas.core.frame import DataFrame


class DBManager:
    def __init__(self):
        self.connection: Connection = self.create_connection()

    def create_connection(self) -> Connection:
        BASE_DIR: bytes = os.path.dirname(os.path.abspath(__file__))
        db_path: bytes = os.path.join(BASE_DIR, "./../../app.db")
        connection: Connection = sqlite3.connect(db_path)
        return connection

    def get_data(self, user_id: int) -> DataFrame:
        query: str = f"""
        select well_being, is_head_hurts, is_high_pressure, pressure, magnetic_storms
        from "data" 
        where user_id={user_id}
        """
        data: DataFrame = read_sql_query(query, self.connection)
        return data

    def save_data(
        self, user_id: int, time: str, user_answer: Dict[str, str], weather: Weather
    ):
        data = Data(
            user_id=user_id,
            time=time,
            well_being=user_answer.get("radio1"),
            is_head_hurts=user_answer.get("radio2"),
            is_high_pressure=user_answer.get("radio3"),
            temperature=weather.temperature,
            pressure=weather.pressure,
            magnetic_storms=weather.magnetic_storms,
        )
        db.session.add(data)
        db.session.commit()

    def get_user(self, email: str) -> User:
        return User.query.filter_by(email=email).first()

    def save_user(self, username: str, email: str, password: str):
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
