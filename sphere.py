from PIL import Image, ImageDraw
from PIL import Image 
import numpy as np
import math


class Sphere:
    def __init__(self, rayon, centre, draw):
      """

      #==========================================================================================#
      Une sphère est definie par:
        un <rayon> (entier)
        un <centre> (l, m, n)
        equation paramétrique: 
                      (P - C).(P - C) = r² <=> (x - l)² + (y - m)² + (z - n)² = r²
                      |
                      --> avec P = (x, y, z) le point du vecteur PC qui est un point du cercle
      #==========================================================================================#
      Passage en paramètre de la classe de <draw> pour 
      pouvoir dessiner dans la bonne image de PIL

      """
      self.rayon = rayon

      self.x_centre = centre[0]
      self.y_centre = centre[1]
      self.z_centre = centre[2]
      
      self.draw = draw

    def dessiner_sphere(self, x, y):
      """
      Ici pour le moment on veut savoir si notre point en (x, y)
      se trouve dans le cercle ou pas

      Donc on cherche à savoir si la distance entre le point
      (x, y) et le centre du cercle est INF au rayon.
      
      Pour ça on calcul la norme soit:
              sqrt [(x - x_centre)**2 + (y - y_centre)**2] <= rayon
      """
      a = (x - self.x_centre) * (x - self.x_centre)
      b = (y - self.y_centre) * (y - self.y_centre)
      pixel= math.sqrt(a+b)

      if pixel<= self.rayon:
          self.draw.point((x, y), fill="red")

    def find_intersection(self, rayon_vue, pixel_eval):
      """
      t²*B*B - 2*t*B * (C - Q) + (C - Q) * (C - Q) - r² = 0
      Il faut résoudre cette équation qui est de la forme:
            ax² + bx + c = 0
      Donc on doit trouver t qui est notre point d'intersection
            DELTA = b² - 4ac
            |
            |
            ------> a = t²*B*B => Doit être égal à 1
                    b = -2*t*B * (C - Q)
                    c = (C - Q) * (C - Q) - r²
            |
            |
            ------> C:= Centre de la sphère
                    B:= Rayon de vue
                    Q:= Pixel évalué
            
                    SI DELTA = 0:
                      PAS D'INTERSECTION 
                    SI DELTA < 0:
                      t = -b / 2*a
                    SI DELTA > 0:
                      t1 = b² + sqrt(DELTA) / 2*a
                      t2 = b² - sqrt(DELTA) / 2*a             
      """
      C = np.array([self.x_centre, self.y_centre, self.z_centre])  
      Q = np.array(pixel_eval)
      r = self.rayon

      a = np.dot(rayon_vue, rayon_vue)
      b = 2 * np.dot(rayon_vue,  (Q - C))
      c = np.dot((Q - C), (Q - C)) - (r*r)

      delta = b*b  - 4 * a * c
      #print(a, b, c, delta)

      if delta == 0:
         return 0
      
      elif delta < 0:
        t = -b / (2 * a)
        return t, t
      
      elif delta > 0:
        t1 = -b + math.sqrt(delta) / (2 * a)
        t2 = -b - math.sqrt(delta) / (2 * a)
        return t1, t2
    
    