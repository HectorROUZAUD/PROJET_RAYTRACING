from PIL import Image, ImageDraw
import numpy as np

class Lumiere:
    def __init__(self, position, couleur):
        self.position = position
        self.couleur = couleur

    def direction_from(self, point):
        return np.linalg.norm(self.position - point)
