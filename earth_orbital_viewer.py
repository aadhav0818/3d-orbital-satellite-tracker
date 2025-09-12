import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QFont
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from norad_satellite_data import TLEFetcher, SatelliteManager
from satellite import Satellite

class OpenGL_Window(QOpenGLWidget):

    def __init__(self, earth: str, starmap: str, parent: QMainWindow = None) -> None:
       
        super(OpenGL_Window, self).__init__(parent)
        self.angle = 0.0  # Angle for sphere rotation
        self.earth_texture = None  # Texture ID for the sphere
        self.earth_projection: str = earth  # texture image
        self.starmap_texture: int = None  # Texture ID for the background
        self.starmap_projection: str = starmap  # background image

        self.mouse_pos_v0 = np.array([0, 0, 0])
        self.rotation_matrix = np.identity(4, dtype=float)

        self.zoom = -20
        self.sensitivity = 0.05
        self.refresh_rate = 8 # ms

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(self.refresh_rate)

        self.tle_fetcher = TLEFetcher()

        CURRENT_GROUP = "active" # remove and re implement later)

        self.sat_manager = SatelliteManager(self.tle_fetcher, CURRENT_GROUP)
        self.sat_manager.load_tles()
        

    def initializeGL(self) -> None:

        glClearColor(0.0, 0.0, 0.0, 1.0)  # Set background color to black
        glEnable(GL_DEPTH_TEST)  # Enable depth testing for 3D rendering
        glEnable(GL_TEXTURE_2D)  # Enable texture mapping
        self.earth_texture = self.load_texture(self.earth_projection)  # Load the texture image
        self.starmap_texture = self.load_texture(self.starmap_projection)

    def resizeGL(self, w: int, h: int) -> None:

        glViewport(0, 0, w, h)  # Set the viewport to cover the whole widget
        glMatrixMode(GL_PROJECTION)  # Set up the projection matrix
        glLoadIdentity()
        gluPerspective(45.0, w / h if h != 0 else 1.0, 0.1, 100.0)  # Set perspective projection
        glMatrixMode(GL_MODELVIEW)  # Switch back to the model view matrix

    def paintGL(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        self.render_background()

        glScalef(1.0, 1.0, 1.0)

        # Starmap
        glPushMatrix()
        glTranslatef(0.0, 0.0, self.zoom * 0.05)
        glMultMatrixf(self.rotation_matrix.T)
        self.draw_textured_sphere(30, 32, 32, self.starmap_texture, True)
        glPopMatrix()

        # Earth
        glPushMatrix()
        glTranslatef(0.0, 0.0, self.zoom)
        glMultMatrixf(self.rotation_matrix.T)
        self.draw_textured_sphere(1.5, 32, 32, self.earth_texture, False)

        # Satellites
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)

        for sat in self.sat_manager.satellites:
            sat.render_satellite(modelview, projection, viewport)

        glPopMatrix()

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 10))

        for sat in self.sat_manager.satellites:
            if sat.screen_pos:
                x, y = sat.screen_pos
                painter.drawText(int(x), int(y), sat.name)

        painter.end()

    def mousePressEvent(self, event):
        mouse_x = event.x()
        mouse_y = event.y()

        nx0 = mouse_x/self.width() * 2 - 1
        ny0 = 1 - 2*mouse_y/self.height()
        nz0 = 0.01
        if 1 - (nx0**2 + ny0**2) >= 0:
            nz0 = np.sqrt(1 - (nx0**2 + ny0**2))

        self.mouse_pos_v0 = np.array([nx0, ny0, nz0])
        

    def mouseMoveEvent(self, event):
        mouse_x = event.x()
        mouse_y = event.y()

        nx1 = mouse_x/self.width() * 2 - 1
        ny1 = 1 - 2*mouse_y/self.height()
        nz1 = 0.01
        if 1 - (nx1**2 + ny1**2) >= 0:
            nz1 = np.sqrt(1 - (nx1**2 + ny1**2))

        mouse_pos_v1 = np.array([nx1, ny1, nz1])

        rotation_axis = np.cross(self.mouse_pos_v0, mouse_pos_v1)
        rotation_axis_norm = np.linalg.norm(rotation_axis)
        rotation_axis = rotation_axis / rotation_axis_norm

        rotation_angle = np.arccos(np.dot(self.mouse_pos_v0, mouse_pos_v1)) * self.sensitivity

        c = np.cos(rotation_angle)
        s = np.sin(rotation_angle)
        t = 1 - c
        x = rotation_axis[0]
        y = rotation_axis[1]
        z = rotation_axis[2]

        self.rotation_matrix = np.array([
            [t*x*x + c,   t*x*y - s*z, t*x*z + s*y, 0],
            [t*x*y + s*z, t*y*y + c,   t*y*z - s*x, 0],
            [t*x*z - s*y, t*y*z + s*x, t*z*z + c,   0],
            [0, 0, 0, 1]
        ], dtype=float) @ self.rotation_matrix


        # self.update()  # redraw with new rotation

    def wheelEvent(self, event):
        angle = event.angleDelta().y()
        if(angle > 0):
            if(self.zoom + 0.2 <= -1.7):
                self.zoom += 0.2
        else:
            self.zoom -= 0.2
        # self.update()

    def render_background(self) -> None:

        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.width(), 0, self.height())
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()


        # Draw a quad that covers the entire window
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(0.0, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(self.width(), 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(self.width(), self.height())
        glTexCoord2f(0.0, 1.0)
        glVertex2f(0.0, self.height())
        glEnd()

        # Restore the previous projection and modelview matrices
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        glEnable(GL_DEPTH_TEST)

    def load_texture(self, image_file: str) -> int:

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        image = Image.open(image_file)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Flip the image vertically for OpenGL
        img_data = image.convert("RGBA").tobytes()

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return texture_id

    def draw_textured_sphere(self, radius: float, slices: int, stacks: int, sphere_texture: int, inverted: bool) -> None:

        glBindTexture(GL_TEXTURE_2D, sphere_texture)  # Bind the texture

        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)  # Enable texturing for the sphere
        gluSphere(quadric, radius, slices, stacks)  # Draw the sphere

        if(inverted):
            gluQuadricOrientation(quadric, GLU_INSIDE)

        gluDeleteQuadric(quadric)  # Clean up the quadric object
    

    def update_frame(self):
        for sat in self.sat_manager.satellites:
            sat.update_position(self.refresh_rate * 0.001)
        
        self.update()

class MainWindow(QMainWindow):

    def __init__(self) -> None:

        super().__init__()
        self.setWindowTitle('OpenGL with PyQt5: Textured Sphere')
        self.setGeometry(100, 100, 800, 600)

        # Add the OpenGL widget to the window
        # Planet Earth Day Map without background
        # self.opengl_widget = OpenGLWindow("8k_earth_daymap.jpg", "", self)
        # Planet Earth Day Map with a background
        self.opengl_widget = OpenGL_Window("./assets/earth_textured_2d_projection.png", "./assets/earth_starmap_2d_projection_dim.jpg", self)
        self.setCentralWidget(self.opengl_widget)


def main() -> None:

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()