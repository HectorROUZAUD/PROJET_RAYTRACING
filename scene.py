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
        #PARTIE: CAMÉRA
        self.posi_cam = camera[0]
        self.dir_cam = camera[1]
        self.or_cam = camera[2]
        self.dim_cam = camera[3]
        self.df_cam = camera[4]


        self.objets = objets
        self.lumieres = lumieres
        self.lumiere_ambiante = lumiere_ambiante
        self.image = image


    def ajouter_camera(self, camera):
        camera_ = camera.Camera(self.posi_cam, self.dir_cam, self.or_cam, self.dim_cam, self.df_cam)



    def ajouter_objets(self):
        pass

    def ajouter_lumieres(self):
        pass


    def trouve_intersection(self, rayon):
        pass


