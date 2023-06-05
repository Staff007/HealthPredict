from app.models import Predict, Weather
from numpy import ndarray
from pandas.core.frame import DataFrame
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class TestClassificationManager:
    def __init__(self, data: DataFrame, cur_weather: Weather):
        self.data: DataFrame = data
        self.cur_weather: Weather = cur_weather
    
    def predict_is_head_hurts(self, model) -> int:
        pressure_arr: ndarray = self.data["pressure"].to_numpy()
        is_head_hurts_arr: ndarray = self.data["is_head_hurts"].to_numpy()
        magnetic_storms_arr: ndarray = self.data["magnetic_storms"].to_numpy()

        X = list(zip(pressure_arr, magnetic_storms_arr))
        y = is_head_hurts_arr

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

        model.fit(X_train, y_train)
        y_predicted = model.predict(X_test)

        print(f'{accuracy_score(y_test, y_predicted)} - результат для {model}')