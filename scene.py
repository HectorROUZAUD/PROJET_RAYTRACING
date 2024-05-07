from PIL import Image, ImageDraw
import numpy as np


from camera import Camera
from sphere import Sphere
from sphere import ImageTexture
from plan import Plan
from lumiere import Lumiere


class Scene:
    def __init__(self, largeur, hauteur):
        self.objets = []
        self.camera = None
        self.lumiere = None
        self.largeur = largeur 
        self.hauteur = hauteur
        self.earth_texture = ImageTexture("earthmap.jpg")

    def ajouter_objet(self, objet):
        self.objets.append(objet)

    def configurer_camera(self, camera):
        self.camera = camera

    def ajouter_lumiere(self, lumiere):
        self.lumiere = lumiere

    def calculer_rayon(self, x, y):
    #calcul du rayon sortant de la caméra
        pixel = np.array([x - self.largeur / 2 + self.camera.position[0], 
                          self.hauteur / 2 - y + self.camera.position[1], 
                          self.camera.position[2] - self.camera.distance_focale])
        rayon = self.camera.rayon_vue(pixel)
        rayon /= np.linalg.norm(rayon)
        return rayon

    def rendre(self):
        image = Image.new("RGB", (self.largeur, self.hauteur), "black")
        draw = ImageDraw.Draw(image)

        for y in range(self.hauteur):
            for x in range(self.largeur):
                rayon = self.calculer_rayon(x, y)
                couleur = self.tracer_rayon(self.camera.position, rayon)
                #draw.point((x, y), fill=tuple(couleur.astype(int)))
                draw.point((x, y), fill=tuple(int(component) for component in couleur))

        image.save("scene.png")
        image.show()

    def tracer_rayon(self, origine, direction):
        objet_proche, point_proche = self.trouver_intersection_la_plus_proche(origine, direction)
        if objet_proche is None:
            return np.array([0, 0, 0])

        if self.est_dans_ombre(point_proche, objet_proche):
            return np.array([0, 0, 0]) * 0.1  # Assombrir pour l'ombre

        return self.calculer_couleur(objet_proche, point_proche, self.lumiere, direction)

    def trouver_intersection_la_plus_proche(self, origine, direction):
        distance_min = float('inf')
        objet_proche = None
        point_proche = None

        for objet in self.objets:
            point = objet.find_intersection(origine, direction)
            if point is not None:
                distance = np.linalg.norm(point - origine)
                if distance < distance_min:
                    distance_min = distance
                    objet_proche = objet
                    point_proche = point

        return objet_proche, point_proche

    def calculer_couleur(self, objet, point, lumiere, rayon):
        normale = np.array(objet.get_normal(point))
        # envoyer la lumière sur ce point d'intersection
        lumi = np.array(lumiere.direction_from(point))
        # à ce point on calcule la lumière 
        Ia = np.array([0.7, 0.7, 0.7]) # Intensité lumière ambiante
        ka = 0.4  # Coefficient ambiant
        kd = 0.5  # Coefficient de diffusion
        ks = 0.1  # Coefficient spéculaire
        r_reflechi = np.array(2 * (np.dot(-lumi, normale) * normale + lumi))
        r_reflechi /= np.linalg.norm(r_reflechi)
        #V = np.array(rayon)
        I = Ia * ka + kd * np.dot(lumi, normale) + ks * (np.dot(r_reflechi, rayon) ** 100)
        
        # Vérifie si l'objet est une sphère pour appliquer la texture
        if not isinstance(objet, Plan):
            # Conversion de la normale en coordonnées sphériques
            u, v = objet.get_sphere_uv(normale)
            col = self.earth_texture.value(u, v)

            couleur = np.array(objet.couleur) * I * col
            couleur = np.clip(couleur, 0, 255)
        else:
            #return couleur
            couleur = np.array(objet.couleur) * I
            couleur = np.clip(couleur, 0, 255)

        #return couleur.astype(int)
        return couleur

    def est_dans_ombre(self, intersection, objet_ignore):
        direction_lumiere = self.lumiere.direction_from(intersection)
        distance_lumiere = np.linalg.norm(self.lumiere.position - intersection)
        point_de_depart = intersection + direction_lumiere * 0.001

        for objet in self.objets:
            if objet != objet_ignore:
                intersection_ombre = objet.find_intersection(point_de_depart, direction_lumiere)
                if intersection_ombre is not None:
                    distance_intersection = np.linalg.norm(intersection_ombre - point_de_depart)
                    if distance_intersection < distance_lumiere:
                        return True
        return False
    
    def main(self):
        # Dimensions de la scène
        largeur, hauteur = 500, 500

        # Initialisation de la scène
        scene = Scene(largeur, hauteur)

        sphere1 = Sphere(1, [0, 1, 0], [255, 255, 255])
        sphere2 = Sphere(0.5, [0, 1, 4], [255, 255, 255])
        plan = Plan([0, 0, 0], [0, 1, 0], [255, 255, 0])

        #Ajout 
        scene.ajouter_objet(sphere1)
        scene.ajouter_objet(sphere2)
        scene.ajouter_objet(plan)

        #configuration de la caméra
        camera = Camera(np.array([0, 3, 5]), np.array([0, 0, -1]), [0, 1, 0], [largeur, hauteur], 350)
        scene.configurer_camera(camera)

        #configuration de la lumière
        lumiere = Lumiere([2, 5, 5], [1, 1, 1])
        scene.ajouter_lumiere(lumiere)

        # Rendu de la scène
        scene.rendre()

if __name__ == "__main__":
    largeur, hauteur = 500, 500

    #Initialisation de la scène
    scene = Scene(largeur, hauteur)
    scene.main()