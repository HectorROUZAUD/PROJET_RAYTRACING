from PIL import Image, ImageDraw
from PIL import Image 
import numpy as np



class Rayon:
    def __init__(self, origine, direction):
        self.origine = origine
        self.direction = direction


    def rayon_vue(self, t):
        """
        P(t) = A + t*B
            A:= Point d'origine 
            B:= Point sur lequel le rayon est envoyé

                        A-----------------------B
                        t=0       t=1/2       t= 1

        on lance une "droite" (ici un rayon de vue) entre A et B 
        et en fesant varier t entre [0, 1] on se rapproche soit du point A ou B


        !!!! ÇA RETOURNE UN VECTEUR (x, y, z)




        """
        x_ray = self.origine[0] + t * self.direction[0]
        y_ray = self.origine[1] + t * self.direction[1]
        z_ray = self.origine[2] + t * self.direction[2]

        ray = [x_ray, y_ray, z_ray]

        return ray

    
