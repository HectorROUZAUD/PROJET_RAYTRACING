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

      a = rayon_vue * rayon_vue
      b = -2 * rayon_vue * C - Q
      c = (C - Q) * (C - Q) - (r*r)

      delta = np.dot(b, b)  - 4 * np.dot(a, c)

      print(a, b, c, delta)
    
    def ray_sphere_intersection(self, Q, d):
        """
        Calcule l'intersection entre un rayon et la sphère.
        Renvoie les valeurs de t pour lesquelles le rayon intersecte la sphère.
        """
        # Calcul des composantes du vecteur entre le centre de la sphère et le point Q
        dx = Q[0] - self.x_centre
        dy = Q[1] - self.y_centre
        dz = Q[2] - self.z_centre

        # Calcul des coefficients pour l'équation quadratique
        a = d[0]**2 + d[1]**2 + d[2]**2
        b = 2 * (dx * d[0] + dy * d[1] + dz * d[2])
        c = dx**2 + dy**2 + dz**2 - self.rayon**2

        # Calcul du discriminant
        discriminant = b**2 - 4*a*c

        print(a, b, c, discriminant)

        if discriminant == 0:
            return 0  # Pas de solution réelle
        elif discriminant < 0:
            t = -b / (2*a)
            return t, t  # Une solution réelle
        else:
            t1 = (-b + math.sqrt(discriminant)) / (2*a)
            t2 = (-b - math.sqrt(discriminant)) / (2*a)
            return t1, t2  # Deux solutions réelles