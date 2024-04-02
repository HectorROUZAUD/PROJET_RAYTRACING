from PIL import Image, ImageDraw
import numpy as np


import camera
import lumiere
import plan
import vecteur
import couleur
import objet
import sphere



class Scene:
    def __init__(self, camera, objets, lumieres, lumiere_ambiante, image):
        self.camera = camera
        self.objets = objets
        self.lumieres = lumieres
        self.lumiere_ambiante = lumiere_ambiante
        self.image = image

    def ajouter_camera(self, camera):
        pass


    def ajouter_scene(self):
        pass


    def ajouter_objets(self):
        pass

    def ajouter_lumieres(self):
        pass


    def trouve_intersection(self, rayon):
        pass

    def main(self):
        #AJOUT DE LA CAMERA
        ajouter_camera()

        #AJOUT DE LA SCENE
        ajouter_scene()

        #AJOUT DES OBJETS
        ajouter_objets()

        #AJOUT SOURCE LUMINEUSE
        ajouter_lumieres()
