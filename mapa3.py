import sys
import folium
import requests
from PyQt5 import QtWidgets, QtWebEngineWidgets

class MapApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Map with Location')
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout()

        # Campo de entrada para la localidad
        self.location_input = QtWidgets.QLineEdit(self)
        self.location_input.setPlaceholderText('Enter location')
        layout.addWidget(self.location_input)

        # Menú desplegable para seleccionar el tipo de mapa
        self.map_type_combo = QtWidgets.QComboBox(self)
        self.map_type_combo.addItems([
            'OpenStreetMap', 
            'CartoDB positron', 
            'CartoDB dark_matter', 
            'Esri Satellite'
        ])
        layout.addWidget(self.map_type_combo)

        # Botón para actualizar el mapa
        self.update_map_btn = QtWidgets.QPushButton('Update Map', self)
        self.update_map_btn.clicked.connect(self.update_map)
        layout.addWidget(self.update_map_btn)

        # Crear un QWebEngineView y cargar el mapa
        self.web_view = QtWebEngineWidgets.QWebEngineView()
        layout.addWidget(self.web_view)

        self.setLayout(layout)

        # Crear el mapa inicial
        self.create_map(-33.74556, -61.96885, 'OpenStreetMap')  # Coordenadas de Venado Tuerto

    def create_map(self, lat, lon, tiles):
        # Crear el mapa con el tileset seleccionado
        if tiles == 'Esri Satellite':
            m = folium.Map(location=[lat, lon], zoom_start=12, tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri')
        else:
            m = folium.Map(location=[lat, lon], zoom_start=12, tiles=tiles)

        # Añadir un marcador en la ubicación
        folium.Marker([lat, lon], tooltip=self.location_input.text()).add_to(m)

        # Guardar el mapa en un archivo HTML
        m.save('map.html')

        # Cargar el mapa en el QWebEngineView
        self.web_view.setHtml(open('map.html').read())

    def update_map(self):
        location = self.location_input.text()
        tiles = self.map_type_combo.currentText()
        if location:
            # Obtener las coordenadas de la localidad usando una API de geocodificación
            api_url = f'https://nominatim.openstreetmap.org/search?format=json&q={location}'
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    lat = float(data[0]['lat'])
                    lon = float(data[0]['lon'])
                    self.create_map(lat, lon, tiles)
                else:
                    self.web_view.setHtml('<h1>Location not found</h1>')
            else:
                self.web_view.setHtml('<h1>Error retrieving location data</h1>')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = MapApp()
    ex.show()
    sys.exit(app.exec_())