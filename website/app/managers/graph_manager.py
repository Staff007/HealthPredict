import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from app.managers.network_manager import NetworkManager
from pandas.core.frame import DataFrame

class GraphManager:
    def __init__(self, data: DataFrame):
        self.data: DataFrame = data
        self.graph = self.save_graph() 
    
    def save_graph(self):    
        plt.switch_backend('Agg') 
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        user_id = NetworkManager().get_user_id()
        id = NetworkManager().get_id()

        cursor.execute(f'SELECT well_being FROM data WHERE user_id={user_id} ORDER BY id DESC LIMIT 10;')
        well_being = cursor.fetchall()
        cursor.execute(f'SELECT pressure FROM data WHERE user_id={user_id} ORDER BY id DESC LIMIT 10;')
        pressure = cursor.fetchall()
        cursor.execute(f'SELECT magnetic_storms FROM data WHERE user_id={user_id} ORDER BY id DESC LIMIT 10;')
        magnetic_storms = cursor.fetchall()

        conn.close()

        def to_mass(mass):
            for i in range(len(mass)):
                mass[i] = list(mass[i])
            for i in range(len(mass)):
                mass[i][0] = int(mass[i][0])
            for i in range(len(mass)):
                mass[i] = int(mass[i][0])
            return mass

        def scaling(param):
            param = [(n - min(param)) / (max(param) - min(param)) for n in param]
            return param

        x = np.arange(0, 10, 1)

        if not self.data.empty and self.data.shape[0] > 10:    
            fig = plt.figure()
            plt.plot(x, scaling(to_mass(pressure)), linewidth = 3, color = '#FFB6C1', label='pressure')
            plt.plot(x, scaling(to_mass(magnetic_storms)), linewidth = 3, color = '#F08080', label='magnetic storms')
            plt.plot(x, scaling(to_mass(well_being)), linewidth = 3, color = '#87CEFA', label='well being')
            plt.box(False)
            plt.yticks([])
            plt.xlabel('Days')
            fig.savefig('/Users/kirillkoskarev/HealthAndWeather/website/app/static/images/graph.png', transparent=True, bbox_inches='tight')