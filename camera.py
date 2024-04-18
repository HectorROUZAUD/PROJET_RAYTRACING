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
        Retourne le rayon de vue si il est compris dans les dimensions de la caméra
        V = position + df * objet
            Si problème de compréhension regarder le TD "Raytracing exo 1


        SI vue_x <= dimension[0] and vue_y <= dimension[1]:
            ALORS ON PEUT FAIRE LE RESTE ET DESSINER LA PARTIE QU'ON VOIT 
        SINON 
            ON NE DESSINE RIEN
        """
        return  rayon.Rayon(self.position, objet).rayon_vue(self.distance_focale)

    
    def window(self):
        """
        C'est pour connaitre la taille de vue de notre caméra 
        en appliquant un ratio entre:

            les dimensions de la caméra et sa distance focale 
        SI dimensions = 100x100 et df = 0.01 => 1/100 ALORS:
            dimensions = dimensions - (dimensions * df)
        """
        return np.array(self.dimensions) - (np.array(self.dimensions) * self.distance_focale)
 

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
                