from typing import Optional

from app.models import Predict, Weather
from numpy import ndarray
from pandas.core.frame import DataFrame
from sklearn.naive_bayes import GaussianNB


class GaussianNBManager:
    def __init__(self, data: DataFrame, cur_weather: Weather):
        self.data: DataFrame = data
        self.cur_weather: Weather = cur_weather

    def get_predict(self) -> Optional[Predict]:
        if not self.data.empty and self.data.shape[0] > 7:
            is_high_pressure = self.predict_is_high_pressure()
            is_head_hurts = self.predict_is_head_hurts()
            well_being = self.predict_well_being(
                is_high_pressure=is_high_pressure, is_head_hurts=is_head_hurts
            )
            predict = Predict(
                is_high_pressure=is_high_pressure,
                is_head_hurts=is_head_hurts,
                well_being=well_being,
            )
            return predict
        return None

    def predict_is_head_hurts(self) -> int:
        model = GaussianNB()
        pressure_arr: ndarray = self.data["pressure"].to_numpy()
        is_head_hurts_arr: ndarray = self.data["is_head_hurts"].to_numpy()
        magnetic_storms_arr: ndarray = self.data["magnetic_storms"].to_numpy()

        features = list(zip(pressure_arr, magnetic_storms_arr))
        labels = is_head_hurts_arr

        model.fit(features, labels)
        result: int = model.predict(
            [(self.cur_weather.pressure, self.cur_weather.magnetic_storms)]
        ).tolist()[0]
        return result

    def predict_is_high_pressure(self) -> int:
        model = GaussianNB()
        pressure_arr: ndarray = self.data["pressure"].to_numpy()
        magnetic_storms_arr: ndarray = self.data["magnetic_storms"].to_numpy()
        is_high_pressure_arr: ndarray = self.data["is_high_pressure"].to_numpy()

        features = list(zip(pressure_arr, magnetic_storms_arr))
        labels = is_high_pressure_arr

        model.fit(features, labels)
        result: int = model.predict(
            [(self.cur_weather.pressure, self.cur_weather.magnetic_storms)]
        ).tolist()[0]
        return result

    def predict_well_being(self, is_high_pressure: int, is_head_hurts: int) -> int:
        model = GaussianNB()
        is_head_hurts_arr: ndarray = self.data["is_high_pressure"].to_numpy()
        is_high_pressure_arr: ndarray = self.data["is_high_pressure"].to_numpy()
        well_being_arr: ndarray = self.data["well_being"].to_numpy()

        features = list(zip(is_high_pressure_arr, is_head_hurts_arr))
        labels = well_being_arr

        model.fit(features, labels)
        result: int = model.predict([(is_high_pressure, is_head_hurts)]).tolist()[0]
        return result
