from PIL import Image, ImageDraw
import numpy as np


import camera
#import lumiere
#import plan
import vecteur
import couleur
#import objet
import sphere

class Scene:
    def __init__(self, camera, image, objets, lumieres = 0, lumiere_ambiante = 0):
        self.camera = camera
        self.objets = objets
        self.lumieres = lumieres
        self.lumiere_ambiante = lumiere_ambiante
        self.image = image
        self.matrice = []


    def ajouter_camera(self, camera):
        self.camera=camera


    def ajouter_objets(self):
        pass

    def ajouter_lumieres(self):
        pass


    def trouve_intersection(self, rayon):
        pass
