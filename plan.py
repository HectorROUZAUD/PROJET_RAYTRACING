from PIL import Image, ImageDraw
import numpy as np
from objet import Objet

class Plan:
    def __init__(self, point, normal, couleur):
        self.point = np.array(point)  
        self.normal = np.array(normal)  
        self.couleur = couleur  
        #self.reflection = reflection

    def find_intersection(self, ray_origin, ray_direction):
        """https://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection, utilisation de wiki pour le calcul du plan"""
        #self.normal = self.normal / np.linalg.norm(self.normal)
        denominateur = np.dot(self.normal, ray_direction)
        
        if denominateur != 0:#on vérifie qu'il n'est pas égale à zéro, pour vérifie  
            d = np.dot(self.normal, self.point - ray_origin) / denominateur
            if d >= 0:
                #le point d'intersection
                return ray_origin + d * ray_direction
        return None
    
    def get_couleur(self):
        return self.couleur
    
    def get_normal(self, point=None):#point None comme ça je peux l'appeler quand je veux sans avoir de type error
        return self.normal
    