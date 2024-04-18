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

    def rayon_vue(self, pixel_courant_dessin, objet):
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
        x = pixel_courant_dessin[0]
        y = pixel_courant_dessin[1]

        for x_cam in range(self.position[0]):
            for y_cam in range(self.position[1]):
                new_posi = rayon.Rayon(self.position, [x_cam, y_cam, self.position[2]]).rayon_vue(self.distance_focale)
                ray = rayon.Rayon(new_posi, pixel_courant_dessin).rayon_vue(self.distance_focale)
        

                #S'il y a intersection alors j'allume le pixel
                if objet.find_intersection([ray[0], ray[1], ray[2]], [1, 1, 0]) != 0:
                    objet.dessiner_sphere(x, y)


    def in_window(self, x, y, dimension):
        """
        Vérifie si le pixel (x, y) est dans la vue de la caméra 
        donc sa vue window
        """
        a = self.position[0] -  dimension[0] <= x <= self.position[0] +  dimension[0]
        b = self.position[1] -  dimension[1] <= y <= self.position[1] +  dimension[1]
        
        if a and b:
            return True
        else:
            return False
                