import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QFont
from OpenGL.GL import *
from OpenGL.GLU import *


class Satellite:
    def __init__(self, name, pos, vel, scale):
        self.name = name
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel, dtype=float)
        self.scale = scale
        self.screen_pos = None

    def get_scaled_position(self):
        return np.array(self.pos) * self.scale

    def update_position(self, dt: float):
        mu = 398600.4418  # km^3/s^2
        r_vec = self.pos
        r_mag = np.linalg.norm(r_vec)
        a_vec = -mu / r_mag**3 * r_vec
        self.pos = self.pos + self.vel * dt + 0.5 * a_vec * dt**2
        r_vec_new = self.pos
        r_mag_new = np.linalg.norm(r_vec_new)
        a_vec_new = -mu / r_mag_new**3 * r_vec_new
        self.vel = self.vel + 0.5 * (a_vec + a_vec_new) * dt

    def render_satellite(self, modelview, projection, viewport):
        scaled_pos = self.get_scaled_position()
        glColor3f(0.0, 1.0, 0.0)
        glPointSize(4)
        glBegin(GL_POINTS)
        glVertex3f(*scaled_pos)
        glEnd()
        glColor3f(1.0, 1.0, 1.0)

        winX, winY, winZ = gluProject(scaled_pos[0], scaled_pos[1], scaled_pos[2], modelview, projection, viewport)

        self.screen_pos = (winX, viewport[3] - winY + 14)
