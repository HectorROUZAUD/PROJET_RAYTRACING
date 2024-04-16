from PIL import Image, ImageDraw
import numpy as np
import math


class Sphere:
    def __init__(self, rayon, centre):
            self.rayon = rayon
            self.centre = centre

    def renvoie_centre(self):
      res = []
      res.append(self.centre[0])
      res.append(self.centre[1])
      res.append(self.centre[2])

      return res

    def intersection(self, rayon_vue, origine, distance_focale):
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

      a = np.dot(rayon_vue, rayon_vue) #qui doit etre égal à 1 si normalisé
      b = 2 * np.dot(np.array(origine) - np.array(self.centre), np.array(rayon_vue)) #np.array(origine) - np.array(self.centre)
      c = np.dot(np.array(origine) - np.array(self.centre), np.array(origine) - np.array(self.centre)) - self.rayon * self.rayon   #np.array(origine) - np.array(self.centre)  - self.rayon * self.rayon


      delta = (b*b) - 4 * a * c

      #print(a, b, c, delta)

      if delta == 0:
        return False
    
      t1 = (-b + np.sqrt(delta)) / (2 * a)
      t2 = (-b - np.sqrt(delta)) / (2 * a)

      i1 = origine + t1 * rayon_vue
      i2 = origine + t2 * rayon_vue
      
      if np.linalg.norm(i1 - origine) <= distance_focale or np.linalg.norm(i2 - origine) <= distance_focale:
         return True
      
      else:
        return False

    def intersection2(self, camera_position, rayon_vue, distance_focale):
            """
            CELUI DE CHATGPT
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

            a = np.dot(rayon_vue, rayon_vue)  # qui doit être égal à 1 si normalisé
            b = 2 * np.dot(rayon_vue, camera_position - self.centre)
            c = np.dot(camera_position - self.centre, camera_position - self.centre) - self.rayon * self.rayon

            delta = (b * b) - 4 * a * c

            if delta == 0:
                return False

            t1 = (-b + np.sqrt(delta)) / (2 * a)
            t2 = (-b - np.sqrt(delta)) / (2 * a)

            i1 = camera_position + t1 * rayon_vue
            i2 = camera_position + t2 * rayon_vue

            if np.linalg.norm(i1 - camera_position) <= distance_focale or np.linalg.norm(i2 - camera_position) <= distance_focale:
                return True
            else:
                return False