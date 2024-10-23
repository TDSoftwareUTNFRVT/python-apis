import sys
import folium
import requests
from PyQt5 import QtWidgets, QtWebEngineWidgets

class MapApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Street Search Map')
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout()

        # Campo de entrada para la localidad
        self.city_input = QtWidgets.QLineEdit(self)
        self.city_input.setPlaceholderText('Ingrese la localidad')
        layout.addWidget(self.city_input)

        # Campo de entrada para el nombre de la calle
        self.street_input = QtWidgets.QLineEdit(self)
        self.street_input.setPlaceholderText('Ingrese el nombre de la calle')
        layout.addWidget(self.street_input)

        # Botón para buscar la calle
        self.search_btn = QtWidgets.QPushButton('Buscar..', self)
        self.search_btn.clicked.connect(self.search_street)
        layout.addWidget(self.search_btn)

        # Crear un QWebEngineView y cargar el mapa
        self.web_view = QtWebEngineWidgets.QWebEngineView()
        layout.addWidget(self.web_view)

        self.setLayout(layout)

        # Crear el mapa inicial
        self.create_map(-33.74556, -61.96885)  # Coordenadas de Venado Tuerto

    def create_map(self, lat, lon):
        # Crear el mapa
        m = folium.Map(location=[lat, lon], zoom_start=15)

        # Añadir un marcador en la ubicación
        folium.Marker([lat, lon], tooltip='Street Location').add_to(m)

        # Guardar el mapa en un archivo HTML
        m.save('map.html')

        # Cargar el mapa en el QWebEngineView
        self.web_view.setHtml(open('map.html').read())

    def search_street(self):
        city_name = self.city_input.text()
        street_name = self.street_input.text()
        if city_name and street_name:
            # Concatenar la localidad y el nombre de la calle
            query = f'{city_name}, {street_name}'
            # Obtener las coordenadas de la calle usando la API de Nominatim
            api_url = f'https://nominatim.openstreetmap.org/search?format=json&q={query}'
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    lat = float(data[0]['lat'])
                    lon = float(data[0]['lon'])
                    self.create_map(lat, lon)
                else:
                    self.web_view.setHtml('<h1>Calle no encontrada</h1>')
            else:
                self.web_view.setHtml('<h1>Error retrieving street data</h1>')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = MapApp()
    ex.show()
    sys.exit(app.exec_())