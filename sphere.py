from PIL import Image
import numpy as np
import math

class Sphere:
  def __init__(self, rayon, centre, couleur):
      """
      Une sphère est définie par :
        un <rayon> (entier)
        un <centre> (l, m, n)
        equation paramétrique: 
                    (P - C).(P - C) = r² <=> (x - l)² + (y - m)² + (z - n)² = r²
                    |
                    --> avec P = (x, y, z) le point du vecteur PC qui est un point du cercle
        Passage en paramètre de la classe de <draw> pour 
        pouvoir dessiner dans la bonne image de PIL
      """
      self.rayon = rayon
      self.centre = centre
      self.couleur = couleur

  def find_intersection(self, pixel_eval, rayon_vue):
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
      b = 2 * np.dot(rayon_vue, (Q - C))
      c = np.dot((Q - C), (Q - C)) - (r*r)

      delta = b*b  - 4 * a * c

      if delta < 0:
          return None
      elif delta == 0:
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

  def get_couleur(self):
      # Retourne la couleur de la sphère
      return self.couleur

  def get_normal(self, hit_point):
      return (hit_point - self.centre) / np.linalg.norm(hit_point - self.centre)

  def get_sphere_uv(self, p):
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

class ImageTexture:
  def __init__(self, filename):
      self.image = Image.open(filename)
      self.width, self.height = self.image.size

  def value(self, u, v):
      if self.height <= 0:
          return (0, 255, 255)  # Retourne une couleur cyan en cas de problème de chargement de l'image

      u = max(0, min(1, u))  # Clamp les coordonnées de texture dans la plage [0, 1]
      v = 1.0 - max(0, min(1, v))  # Inverse v pour les coordonnées de l'image

      i = int(u * self.width)
      j = int(v * self.height)
      pixel = self.image.getpixel((i, j))

      color_scale = 1.0 / 255.0
      return tuple(color_scale * channel for channel in pixel)

def earth():
    earth_texture = ImageTexture("earthmap.jpg")


if __name__ == "__main__":
    earth()
