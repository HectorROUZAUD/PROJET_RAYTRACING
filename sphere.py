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


    def intersection(self, rayon_vue, origine, distance_focale=5):
      """
      a = t**2 * u
      b = t * 2 * OC * u
      c = OC**2 - r**2

      Delta = b**2 - 4 * a * c
        Si Delta == 0:
          PAS D'INTERSECTION
        Si Delta < 0:
          REGARDE LA TEANGEANTE ET LA SOLUTION EST: -b / 2 *a
        
        Si Delta > 0:
          t1 = -b - sqrt(Delta) / 2 * a
          t2 = -b + sqrt(Delta) / 2 * a
          
      """

      a = 1  #np.dot(rayon_vue, rayon_vue) #qui doit etre égal à 1 si normalisé
      b = 2 * np.dot(np.array(origine) - np.array(self.centre), np.array(rayon_vue)) #np.array(origine) - np.array(self.centre)
      c = np.dot(np.array(origine) - np.array(self.centre), np.array(origine) - np.array(self.centre)) - self.rayon * self.rayon   #np.array(origine) - np.array(self.centre)  - self.rayon * self.rayon


      delta = (b*b) - 4 * a * c
			
      #print(a, b, c, delta)

      if delta == 0:
        return 0
      else:
        t1 = (-b + np.sqrt(delta)) / (2 * a)
        t2 = (-b - np.sqrt(delta)) / (2 * a)

        i1 = origine + t1 * rayon_vue
        i2 = origine + t2 * rayon_vue

        if np.linalg.norm(i1 - origine) <= distance_focale or np.linalg.norm(i2 - origine) <= distance_focale:
          return i1, i2
        
        else:
          return 0

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