import sys
import folium
import requests
from PyQt5 import QtWidgets, QtWebEngineWidgets

class MapApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Mapa')
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout()

        # Campo de entrada para la localidad
        self.location_input = QtWidgets.QLineEdit(self)
        self.location_input.setPlaceholderText('Ingresa una localidad')
        layout.addWidget(self.location_input)

        # Botón para actualizar el mapa
        self.update_map_btn = QtWidgets.QPushButton('Buscar..', self)
        self.update_map_btn.clicked.connect(self.update_map)
        layout.addWidget(self.update_map_btn)

        # Crear un QWebEngineView y cargar el mapa
        self.web_view = QtWebEngineWidgets.QWebEngineView()
        layout.addWidget(self.web_view)

        self.setLayout(layout)

        # Crear el mapa inicial
        self.create_map(-33.74556, -61.96885)  # Coordenadas de Venado Tuerto

    def create_map(self, lat, lon):
        # Crear el mapa
        m = folium.Map(location=[lat, lon], zoom_start=12)

        # Añadir un marcador en la ubicación
        folium.Marker([lat, lon], tooltip=self.location_input.text()).add_to(m)

        # Guardar el mapa en un archivo HTML
        m.save('map.html')

        # Cargar el mapa en el QWebEngineView
        self.web_view.setHtml(open('map.html').read())

    def update_map(self):
        location = self.location_input.text()
        if location:
            # Obtener las coordenadas de la localidad usando una API de geocodificación
            api_url = f'https://nominatim.openstreetmap.org/search?format=json&q={location}'
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    lat = float(data[0]['lat'])
                    lon = float(data[0]['lon'])
                    self.create_map(lat, lon)
                else:
                    self.web_view.setHtml('<h1>Localidad no encontrada</h1>')
            else:
                self.web_view.setHtml('<h1>Error al recibir datos..</h1>')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = MapApp()
    ex.show()
    sys.exit(app.exec_())