from PIL import Image, ImageDraw
import numpy as np

class Camera:
    def __init(self, dimensions, position, direction, orientation, distance_focale):
        self.dimensions = dimensions
        self.position = position
        self.orientation = orientation
        self.distance_focale = distance_focale

    def rayon(self, vecteur_unitaire):
        """
        Retourne le rayon de vue
        V = position + df * vecteur unitaire
            Si problème de compréhension regarder le TD "Raytracing"
        """

        vue_x = self.position[0] + self.distance_focale * vecteur_unitaire
        vue_y = self.position[1] + self.distance_focale * vecteur_unitaire
        vue_z = self.position[2] + self.distance_focale * vecteur_unitaire


        return np.array(vue_x, vue_y, vue_z)
