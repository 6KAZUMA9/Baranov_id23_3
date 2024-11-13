from tkinter import *
from math import cos, sin, radians
import random
import json


class PlanetarySystem:
    def __init__(self, canvas):
        self.canvas = canvas
        self.planets = []

    def add_planet(self, planet):
        self.planets.append(planet)

    def update(self):
        for planet in self.planets:
            planet.update_position()
            planet.update_satellite_position()
        self.canvas.after(10, self.update)


class Planet:
    def __init__(self, canvas, sun_x, sun_y, orbit_radius, planet_size, orbit_speed, d, name):
        self.canvas = canvas
        self.sun_x = sun_x
        self.sun_y = sun_y
        self.orbit_radius = orbit_radius
        self.planet_size = planet_size
        self.orbit_speed = orbit_speed
        self.color = density(d)
        self.name = name
        self.angle = 0
        self.planet = canvas.create_oval(0, 0, 0, 0, fill=self.color, outline="")

        self.satellite_orbit_radius = planet_size * 2
        self.satellite_size = planet_size // 3
        self.satellite_angle = 0
        self.satellite = canvas.create_oval(0, 0, 0, 0, fill='white', outline="")

    def update_position(self):
        x = self.sun_x + cos(radians(self.angle)) * self.orbit_radius
        y = self.sun_y + sin(radians(self.angle)) * self.orbit_radius

        self.canvas.coords(self.planet,
                           x - self.planet_size, y - self.planet_size,
                           x + self.planet_size, y + self.planet_size)

        self.angle += self.orbit_speed

    def update_satellite_position(self):
        planet_x = self.sun_x + cos(radians(self.angle)) * self.orbit_radius
        planet_y = self.sun_y + sin(radians(self.angle)) * self.orbit_radius

        x = planet_x + cos(radians(self.satellite_angle)) * self.satellite_orbit_radius
        y = planet_y + sin(radians(self.satellite_angle)) * self.satellite_orbit_radius

        self.canvas.coords(self.satellite,
                           x - self.satellite_size, y - self.satellite_size,
                           x + self.satellite_size, y + self.satellite_size)

        self.satellite_angle += self.orbit_speed * 2


def density(rand_seed):
    random.seed(rand_seed)
    return "#%02X%02X%02X" % (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))


def add_stars(canvas, canvas_size, num_stars=100):
    for _ in range(num_stars):
        x = random.randint(0, canvas_size)
        y = random.randint(0, canvas_size)
        star_size = random.randint(1, 3)  # Размер звезды случайный
        canvas.create_oval(x, y, x + star_size, y + star_size, fill='white', outline='')


def create_planetary_system():
    window = Tk()
    window.title("Planetary System")

    canvas_size = 600
    canvas = Canvas(window, width=canvas_size, height=canvas_size, bg='black')
    canvas.pack()

    add_stars(canvas, canvas_size)

    sun_x, sun_y = canvas_size / 2, canvas_size / 2
    sun_radius = 50
    sun = canvas.create_oval(sun_x - sun_radius, sun_y - sun_radius, sun_x + sun_radius, sun_y + sun_radius,
                             fill='yellow')

    system = PlanetarySystem(canvas)

    with open('planets_data.json', 'r') as json_file:
        planets_data = json.load(json_file)

    for pdata in planets_data:
        planet = Planet(canvas, sun_x, sun_y, pdata["orbit_radius"], pdata["planet_size"], pdata["orbit_speed"],
                        pdata["density"], pdata["name"])
        system.add_planet(planet)

    system.update()
    window.mainloop()


if __name__ == "__main__":
    create_planetary_system()
