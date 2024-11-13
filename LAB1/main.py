from math import cos, sin, radians, pi
from tkinter import *

window = Tk()


# функция движения точки
def moving(a):
    if a >= 360:
        a = 0
    x = cos(radians(a)) * (oval_r * pi) / 180
    y = sin(radians(a)) * (oval_r * pi) / 180 * direction
    a += 1
    canvas.move(point, x, y)
    canvas.after(speed, moving, a)


# данные для постройки круга и точки
size = 600
x0 = size / 2
y0 = size / 2
oval_r = 200
point_r = 10

# создание поля и круга с точкой
canvas = Canvas(window, width=size, height=size)
canvas.create_oval(x0 - oval_r, y0 - oval_r, x0 + oval_r, y0 + oval_r, fill='#61F5FF')
point = canvas.create_oval(x0 + oval_r - point_r, y0 - point_r,
                           x0 + oval_r + point_r, y0 + point_r, fill='#4174FF')
canvas.pack()
# скорость и направление точки
speed = 6
direction = -1

window.after(speed, moving, 90)
window.mainloop()
