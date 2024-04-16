from PIL import Image, ImageDraw
import numpy as np

class Camera:
    def __init__(self, dimensions, position, direction, orientation, distance_focale):
        self.dimensions = dimensions
        self.position = position
        self.direction = direction
        self.orientation = orientation
        self.distance_focale = distance_focale

    def rayon(self, vecteur_unitaire= [1, 1, 1]):
        """
        Retourne le rayon de vue
        V = position + df * vecteur unitaire
            Si problème de compréhension regarder le TD "Raytracing"
        """

        vue_x = self.position[0] + self.distance_focale * vecteur_unitaire[0]
        vue_y = self.position[1] + self.distance_focale * vecteur_unitaire[1]
        vue_z = self.position[2] + self.distance_focale * vecteur_unitaire[2]


        return np.array([vue_x, vue_y, vue_z])


    def rayon_vue(self, x, y):
        """
        Calcule la direction du rayon de vue pour un pixel donné (x, y) dans le plan de l'image.
        """
        # Calcul des vecteurs de la caméra
        camera_forward = np.array(self.direction)  # Vecteur de direction de la caméra
        camera_right = np.cross(camera_forward, self.orientation)  # Vecteur droit de la caméra
        camera_up = np.cross(camera_right, camera_forward)  # Vecteur haut de la caméra

        # Normalisation des vecteurs
        camera_forward = camera_forward / np.linalg.norm(camera_forward)
        camera_right = camera_right / np.linalg.norm(camera_right)
        camera_up = camera_up / np.linalg.norm(camera_up)

        # Calcul de la direction du rayon de vue
        ray_direction = (
            camera_forward
            + camera_right * (x - self.dimensions[0] / 2)
            + camera_up * (y - self.dimensions[1] / 2)
        )
        ray_direction = ray_direction / np.linalg.norm(ray_direction)

        return ray_direction

