from PIL import Image, ImageDraw
import numpy as np

import rayon 


class Camera:
    def __init__(self, position=[50, 50, 50], direction=[0, 0, 50], orientation=[0, 0, 1], dimensions=[100, 100], distance_focale=1.0):
        self.dimensions = dimensions
        self.position = position
        self.direction = direction
        self.orientation = orientation
        self.distance_focale = distance_focale

    def rayon_vue(self, objet):
        """
        Retourne le rayon de vue
        V = position + df * objet
            Si problème de compréhension regarder le TD "Raytracing exo 1"
        """
        vue = rayon.Rayon(self.position, objet).rayon_vue(self.distance_focale)
        vue_x = vue[0]
        vue_y = vue[1]
        vue_z = vue[2]

        return np.array([vue_x, vue_y, vue_z])
    




