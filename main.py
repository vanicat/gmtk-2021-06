from ursina import *

app = Ursina()

camera.orthographic = True
camera.fov = 1

window.borderless = True

if __name__ == '__main__':
    app.run()