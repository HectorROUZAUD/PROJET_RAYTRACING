from PIL import Image, ImageDraw
from PIL import Image 
import numpy as np



class Rayon:
    def __init__(self, origine, direction):
        self.origine = origine
        self.direction = direction


    def rayon_vue(self, t):
        """
           +---------+
          /         /|
         /         / |
        +---------+  |
        |         |  +
        |    O    | /
        |         |/
        +---------+
        

           (pixel)  
         \    |    /
          \   |   /
           \  |  /
            \ | /
             \|/
              +
           (Caméra)

        !!!! ÇA RETOURNE UN VECTEUR (x, y, z)
        """
       
        return self.origine + t * self.direction

    
