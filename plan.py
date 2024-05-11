from PIL import Image, ImageDraw
import numpy as np
from objet import Objet

class Plan:
    def __init__(self, point, normal, couleur, reflection, texture = None, transparence = 0):
        self.point = np.array(point)  
        self.normal = np.array(normal)  
        self.couleur = couleur  
        self.reflection = reflection
        self.texture = texture
        self.transparence = transparence

    def find_intersection(self, ray_origin, ray_direction):
        """https://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection, utilisation de wiki pour le calcul du plan
        Puis au finale j'ai trouvé dans le TD, application du td pour cette fonction qui à pour but d'effectuer les calculs d'intersection
        """
        #self.normal = self.normal / np.linalg.norm(self.normal)
        denominateur = np.dot(self.normal, ray_direction)
        
        if denominateur != 0:#on vérifie qu'il n'est pas égale à zéro si il est égale à zéro ça veut dire que c'est parallèle  
            d = np.dot(self.normal, self.point - ray_origin) / denominateur
            if d >= 0:
                #le point d'intersection
                return ray_origin + d * ray_direction
        return None
    
    def get_couleur(self):
        return self.couleur
    
    def get_normal(self, point=None):#point None comme ça je peux l'appeler quand je veux sans avoir de type error
        return self.normal
    
    def get_uv(self, p):
        """https://physique.cmaisonneuve.qc.ca/svezina/nyc/note_nyc/NYC_XXI_Chap%206.7.pdf
        
            """
        # Utilisation de la position relative dans le plan pour déterminer u, v
        u = p[0] - np.floor(p[0])
        v = p[2] - np.floor(p[2])  
        return u, v