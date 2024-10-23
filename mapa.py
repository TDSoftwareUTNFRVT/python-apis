import sys
import folium
from PyQt5 import QtWidgets, QtWebEngineWidgets

class MapApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Vista Mapa')
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout()

        # Crear el mapa con folium
        self.create_map()

        # Crear un QWebEngineView y cargar el mapa
        self.web_view = QtWebEngineWidgets.QWebEngineView()
        self.web_view.setHtml(open('map.html').read())
        layout.addWidget(self.web_view)

        self.setLayout(layout)

    def create_map(self):
        # Ubicación fija (puedes usar una API para obtener la ubicación actual)
        lat, lon = -33.74556, -61.96885  # Coordenadas de Venado Tuerto

        # Crear el mapa
        m = folium.Map(location=[lat, lon], zoom_start=12)

        # Añadir un marcador en la ubicación
        folium.Marker([lat, lon], tooltip='estas acá').add_to(m)

        # Guardar el mapa en un archivo HTML
        m.save('map.html')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = MapApp()
    ex.show()
    sys.exit(app.exec_())