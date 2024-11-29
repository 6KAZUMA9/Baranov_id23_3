import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer, QRectF, QPointF
import math

class AsteroidSizeControl(QWidget):
    def __init__(self, min_size, max_size, simulation):
        super().__init__()
        self.simulation = simulation
        layout = QVBoxLayout()
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setMinimum(min_size)
        self.size_slider.setMaximum(max_size)
        self.size_slider.setValue(simulation.asteroid_size)
        print(3)
        self.size_slider.valueChanged.connect(self.slider_changed)
        label = QLabel(f"Размер астероида ({min_size}-{max_size})")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        layout.addWidget(self.size_slider)
        self.setLayout(layout)
        print(2)
    def slider_changed(self):
        print(1)
        self.simulation.asteroid_size = self.size_slider.value()
        print(1)
        self.simulation.update()
        print(1)

class SolarSystemWithStars(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Солнечная система со звёздами")
        self.setGeometry(100, 100, 1000, 1000)
        self.timer = QTimer(self)  # Timer is created here
        self.timer.timeout.connect(self.update_planets) # Connection is here
        self.is_running = True
        self.timer.start(25)
        self.asteroid_size = 10

        self.planets = self.create_planets()
        self.num_stars = 500
        self.stars = self.generate_stars()
        self.center_x = self.width() // 2
        self.center_y = self.height() // 2
        self.asteroids = []

        controls = AsteroidSizeControl(5, 25, self)
        main_layout = QVBoxLayout()
        main_layout.addWidget(controls)
        main_layout.addWidget(self)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setLayout(main_layout)

    def create_planets(self):
        planets = [
            {"name": "Солнце", "radius": 100, "orbit_radius": 0, "color": Qt.yellow, "angle": 0, "speed": 0,
             "satellites": []},
            {"name": "Меркурий", "radius": 20, "orbit_radius": 140, "color": Qt.gray, "angle": 0, "speed": 5,
             "satellites": self.create_satellites(1, 20)},
            {"name": "Венера", "radius": 30, "orbit_radius": 260, "color": Qt.white, "angle": 0, "speed": 3,
             "satellites": []},
            {"name": "Земля", "radius": 30, "orbit_radius": 340, "color": Qt.blue, "angle": 0, "speed": 2,
             "satellites": self.create_satellites(1, 48)},
            {"name": "Марс", "radius": 24, "orbit_radius": 455, "color": Qt.red, "angle": 0, "speed": 1,
             "satellites": self.create_satellites(2, 24)},
        ]
        return planets

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.is_running = not self.is_running
            if self.is_running:
                self.timer.start(25)
            else:
                self.timer.stop()

    def create_satellites(self, num_satellites, planet_radius):
        satellites = []
        for i in range(num_satellites):
            radius = planet_radius / 2  # Satellite radius is 1/4 of planet radius
            orbit_radius = planet_radius + 10 + radius  # Small orbit
            angle = random.uniform(0, 360)
            speed = random.uniform(10, 20)
            satellites.append({"radius": radius, "orbit_radius": orbit_radius, "angle": angle, "speed": speed,
                               "color": QColor(200, 200, 200)})
        return satellites

    def generate_stars(self):
        stars = []
        for _ in range(self.num_stars):
            x = random.randint(0, self.width())
            y = random.randint(0, self.height())
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            stars.append({"x": x, "y": y, "size": size, "brightness": brightness})
        return stars

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(0, 0, 40))
        painter.drawRect(0, 0, self.width(), self.height())
        for star in self.stars:
            color = QColor(star["brightness"], star["brightness"], star["brightness"])
            painter.setBrush(color)
            painter.drawEllipse(QRectF(star["x"], star["y"], star["size"], star["size"]))

        for planet in self.planets:
            x = self.center_x + planet["orbit_radius"] * math.cos(math.radians(planet["angle"]))
            y = self.center_y + planet["orbit_radius"] * math.sin(math.radians(planet["angle"]))
            painter.setBrush(planet["color"])
            painter.drawEllipse(x - planet["radius"], y - planet["radius"], 2 * planet["radius"], 2 * planet["radius"])

            for satellite in planet["satellites"]:
                sat_x = x + satellite["orbit_radius"] * math.cos(math.radians(satellite["angle"]))
                sat_y = y + satellite["orbit_radius"] * math.sin(math.radians(satellite["angle"]))
                painter.setBrush(satellite["color"])
                painter.drawEllipse(sat_x - satellite["radius"], sat_y - satellite["radius"], 2 * satellite["radius"],
                                    2 * satellite["radius"])

        for asteroid in self.asteroids:
            painter.setBrush(asteroid["color"])
            painter.drawEllipse(asteroid["position"].x() - asteroid["radius"], asteroid["position"].y() - asteroid["radius"], 2 * asteroid["radius"], 2 * asteroid["radius"])


    def update_planets(self):
        if self.is_running:  # Only update if running
            for planet in self.planets:
                planet["angle"] = (planet["angle"] + planet["speed"]) % 360
                for satellite in planet["satellites"]:
                    satellite["angle"] = (satellite["angle"] + satellite["speed"]) % 360
            for asteroid in self.asteroids:
                asteroid["position"] = QPointF(asteroid["position"].x() + asteroid["velocity"].x(), asteroid["position"].y() + asteroid["velocity"].y())
                #Keep asteroids within the window
                asteroid["position"].setX(max(asteroid["radius"], min(asteroid["position"].x(), self.width() - asteroid["radius"])))
                asteroid["position"].setY(max(asteroid["radius"], min(asteroid["position"].y(), self.height() - asteroid["radius"])))
            self.repaint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.create_asteroid(event.x(), event.y())

    def create_asteroid(self, x, y):
        radius = self.asteroid_size
        speed_x = random.uniform(-2, 2)
        speed_y = random.uniform(-2, 2)
        color = QColor(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.asteroids.append({"radius": radius, "position": QPointF(x, y), "velocity": QPointF(speed_x, speed_y), "color": color})
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.is_running = not self.is_running
            if self.is_running:
                self.timer.start(25)
            else:
                self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    simulation = SolarSystemWithStars()
    simulation.show()
    sys.exit(app.exec_())