from PIL import Image, ImageDraw
import numpy as np




class Camera:
    def __init__(self, position=[50, 50, 50], direction=[0, 0, 50], orientation=[0, 0, 1], dimensions=[100, 100], distance_focale=1.0):
        self.dimensions = np.array(dimensions)
        self.position = np.array(position)
        self.direction = np.array(direction)
        self.orientation = np.array(orientation)
        self.distance_focale = distance_focale

    def rayon_vue(self, pixel_courant):
        """
        Retourne le rayon de vue si il est compris dans les dimensions de la caméra
        V = position + df * objet
            Si problème de compréhension regarder le TD "Raytracing exo 1


        SI vue_x <= dimension[0] and vue_y <= dimension[1]:
            ALORS ON PEUT FAIRE LE RESTE ET DESSINER LA PARTIE QU'ON VOIT 
        SINON 
            ON NE DESSINE RIEN


        Il faut d'abord connaitre la position du pixel de la caméra dans le plan 3D et on part de ce pixel pour le lancer sur 
        l'écran de dessin 
        """
        return pixel_courant - self.position

