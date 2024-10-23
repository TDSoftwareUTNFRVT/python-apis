import sys
import folium
import requests
import openrouteservice
from PyQt5 import QtWidgets, QtWebEngineWidgets

class MapApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Route Finder Map')
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout()

        # Campo de entrada para la localidad y la calle de origen
        self.origin_city_input = QtWidgets.QLineEdit(self)
        self.origin_city_input.setPlaceholderText('Enter origin city')
        layout.addWidget(self.origin_city_input)

        self.origin_street_input = QtWidgets.QLineEdit(self)
        self.origin_street_input.setPlaceholderText('Enter origin street')
        layout.addWidget(self.origin_street_input)

        # Campo de entrada para la localidad y la calle de destino
        self.dest_city_input = QtWidgets.QLineEdit(self)
        self.dest_city_input.setPlaceholderText('Enter destination city')
        layout.addWidget(self.dest_city_input)

        self.dest_street_input = QtWidgets.QLineEdit(self)
        self.dest_street_input.setPlaceholderText('Enter destination street')
        layout.addWidget(self.dest_street_input)

        # Botón para buscar la ruta
        self.search_btn = QtWidgets.QPushButton('Find Route', self)
        self.search_btn.clicked.connect(self.find_route)
        layout.addWidget(self.search_btn)

        # Crear un QWebEngineView y cargar el mapa
        self.web_view = QtWebEngineWidgets.QWebEngineView()
        layout.addWidget(self.web_view)

        self.setLayout(layout)

        # Crear el mapa inicial
        self.create_map(-33.74556, -61.96885)  # Venado Tuerto

    def create_map(self, lat, lon, route=None):
        # Crear el mapa
        m = folium.Map(location=[lat, lon], zoom_start=12)

        # Añadir un marcador en la ubicación
        folium.Marker([lat, lon], tooltip='Location').add_to(m)

        # Dibujar la ruta si existe
        if route:
            folium.PolyLine(route, color='blue', weight=5, opacity=0.7).add_to(m)

        # Guardar el mapa en un archivo HTML
        m.save('map.html')

        # Cargar el mapa en el QWebEngineView
        self.web_view.setHtml(open('map.html').read())

    def find_route(self):
        origin_city = self.origin_city_input.text()
        origin_street = self.origin_street_input.text()
        dest_city = self.dest_city_input.text()
        dest_street = self.dest_street_input.text()

        if origin_city and origin_street and dest_city and dest_street:
            # Obtener las coordenadas de origen y destino usando la API de Nominatim
            origin_query = f'{origin_street}, {origin_city}'
            dest_query = f'{dest_street}, {dest_city}'

            origin_coords = self.get_coordinates(origin_query)
            dest_coords = self.get_coordinates(dest_query)

            if origin_coords and dest_coords:
                # Obtener la ruta usando la API de OpenRouteService
                client = openrouteservice.Client(key='TU_CLAVE_API_OPENROUTESERVICE')  # Reemplaza con tu clave de API
                route = client.directions(coordinates=[origin_coords, dest_coords], profile='driving-car', format='geojson')

                # Extraer las coordenadas de la ruta
                route_coords = [(coord[1], coord[0]) for coord in route['features'][0]['geometry']['coordinates']]

                # Crear el mapa con la ruta
                self.create_map(origin_coords[1], origin_coords[0], route_coords)
            else:
                self.web_view.setHtml('<h1>Could not find coordinates for the given addresses</h1>')

    def get_coordinates(self, query):
        api_url = f'https://nominatim.openstreetmap.org/search?format=json&q={query}'
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return (lon, lat)
        return None

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = MapApp()
    ex.show()
    sys.exit(app.exec_())