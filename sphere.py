from PIL import Image, ImageDraw
from PIL import Image 
import numpy as np
import math

from image_texture import ImageTexture

class Sphere:
    def __init__(self, rayon, centre, couleur, reflection, texture, transparence):
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
      self.centre = centre
      self.couleur = couleur
      self.reflection = reflection
      self.texture = texture if texture else None
      self.transparence = transparence 
      
    def find_intersection(self,pixel_eval,rayon_vue):
      """
      
      P -  <=> t²*B*B - 2*t*B * (C - Q) + (C - Q) * (C - Q) - r² = 0
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
      C = self.centre 
      Q = np.array(pixel_eval)
      r = self.rayon

      a = np.dot(rayon_vue, rayon_vue)
      b = 2 * np.dot(rayon_vue,  (Q - C))
      c = np.dot((Q - C), (Q - C)) - (r*r)

      delta = b*b  - 4 * a * c
      #print(a, b, c, delta)

      if delta < 0:
         return None
      
      elif delta == 0:
        if a == 0:
            return None
        else:
          return -b/(2*a)
      
      else:
        t1 = (-b + math.sqrt(delta)) / (2 * a)
        t2 = (-b - math.sqrt(delta)) / (2 * a)

        # Retourne le point d'intersection le plus proche devant le rayon
        if t1 >= 0 and t2 >= 0:
            return pixel_eval + min(t1, t2) * rayon_vue
        elif t1 >= 0:
            return pixel_eval + t1 * rayon_vue
        elif t2 >= 0:
            return pixel_eval + t2 * rayon_vue
        else:
            return None
    """
    def draw_sphere(self, intersections):
        for (x, y), _ in intersections.items():
            self.draw.point((x, y), fill=self.couleur)
    """
    def get_couleur(self):
       # Retourne la couleur de la sphère
       return self.couleur
    
    def get_normal(self, hit_point):
        return (hit_point - self.centre)/np.linalg.norm(hit_point - self.centre)
    
    def get_couleur(self, hit_point):
        if self.texture:
            #conversion du point d'impact en coordonnées UV de la sphère
            u, v = self.get_sphere_uv((hit_point - self.centre) / self.rayon)
            return self.texture.valeur(u, v)
        return self.couleur
    
    def get_uv(self, p):
      """
      p: un point donné sur la sphère de rayon un, centrée à l'origine.
      u: valeur retournée [0,1] de l'angle autour de l'axe Y à partir de X=-1.
      v: valeur retournée [0,1] de l'angle de Y=-1 à Y=+1.
          <1 0 0> donne <0.50 0.50>       <-1  0  0> donne <0.00 0.50>
          <0 1 0> donne <0.50 1.00>       < 0 -1  0> donne <0.50 0.00>
          <0 0 1> donne <0.25 0.50>       < 0  0 -1> donne <0.75 0.50>
      """
      y = max(-1.0, min(1.0, -p[1]))  # Clamp la valeur de -p[1] dans l'intervalle [-1, 1]
      theta = math.acos(y)
      phi = math.atan2(-p[2], p[0]) + math.pi

      u = phi / (2 * math.pi)
      v = theta / math.pi

      return u, v
    
    
