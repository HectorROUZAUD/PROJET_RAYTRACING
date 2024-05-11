from PIL import Image, ImageDraw
import numpy as np
import math 


from camera import Camera
from sphere import Sphere
from plan import Plan
from lumiere import Lumiere
from image_texture import ImageTexture


class Scene:
    def __init__(self, largeur, hauteur):
        self.objets = []
        self.camera = None
        self.lumiere = None
        self.largeur = largeur 
        self.hauteur = hauteur
        self.max_profondeur = 3

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
    
    
    def refraction(self, ray_direction, normal):
        """https://www.alloprof.qc.ca/fr/eleves/bv/physique/la-loi-de-snell-descartes-sur-la-refraction-p1034
            La loi de Snell-Descartes est déterminée par l'équation suivante : n1sin(teta_i) = n2sin(teta_r)
            n1 = l'indice de réfraction du milieu traversé par le rayon incident
            teta_i = l'angle incident
            n2 = l'indice de réfraction du milieu traversé par le rayon réfléchi
            teta_r = représente l'angle de réfraction.
        """
        cos_i = -np.dot(normal, ray_direction)
        sin_i2 = 1.0 - cos_i * cos_i
        sin_r2 = (1 / 1.52) ** 2 * sin_i2
        if sin_r2 > 1.0:
            return None  # Total internal reflection
        cos_r = math.sqrt(1.0 - sin_r2)
        return (1 / 1.52) * ray_direction + (1 / 1.52 * cos_i - cos_r) * normal
      

        


    def apply_gamma_correction(self, image, gamma=2.2):
        """
        Applique une correction gamma à une image.
        
        Args:
        image (Image): L'objet Image PIL.
        gamma (float): Le facteur de correction gamma. Typiquement, 2.2 pour les images destinées à être affichées sur des écrans classiques.
        
        Returns:
        Image: L'image corrigée.
        """
        # Convertir l'image en un array numpy
        img_array = np.array(image)
        
        # Normaliser les données pour être entre 0 et 1
        normalized_array = img_array / 255.0
        
        # Appliquer la correction gamma
        corrected_array = np.power(normalized_array, 1/gamma)
        
        # Convertir de nouveau en valeurs de pixels [0, 255]
        corrected_array = np.clip(corrected_array * 255, 0, 255).astype('uint8')
        
        # Créer une nouvelle image à partir du résultat
        new_image = Image.fromarray(corrected_array)
        
        return new_image
    
    
    def tracer_rayon(self, origine, direction, profondeur):
        """Tracer_rayon sera à déterminer les ombres, ombres portés, la réflexion avec la récursivité"""
        #Si on dépasse ou égale c'est noir
        if profondeur >= self.max_profondeur:
            return np.array([255, 255, 255])

        #Si aucun objet est détecté on affiche en blanc, exemple le fond vue dans le mirroir
        objet_proche, point_proche, couleur_directe = self.trouver_intersection_la_plus_proche(origine, direction)
        if objet_proche is None:
            return np.array([255, 255, 255])

        #Si on est dans l'ombre on met noir
        if self.est_dans_ombre(point_proche, objet_proche):
            return np.array([0, 0, 0]) * 0.1 

        #J'initialise la couleur qui sera reflechie avec la récursivité
        couleur_reflechie = np.array([0, 0, 0])
        couleur_refraction = np.array([0, 0, 0])

        #Calcule de la normale 
        normale = np.array(objet_proche.get_normal(point_proche))
        #print(objet_proche.transparence)
        
        
        #Gérer la réflexion
        if objet_proche.reflection > 0:
            #Calcule du rayon reflechi vue en TD
            direction_reflechie = direction + 2 * np.dot(-direction, normale) * normale
            direction_reflechie /=np.linalg.norm(direction_reflechie)#Normalisation important
            premier_reflect = point_proche + normale * 0.001#Le 0.001 est très important pour éviter les erreurs, les auto-intersections 
            couleur_reflechie = self.tracer_rayon(premier_reflect, direction_reflechie, profondeur)


        # Réfraction
        if objet_proche.transparence > 0:
            rayon_refraction = self.refraction(direction, normale)
            if rayon_refraction is not None:
                premiere_refraction = point_proche + normale * 0.001
                couleur_refraction = self.tracer_rayon(premiere_refraction, rayon_refraction, profondeur + 1)
                #print(couleur_refraction)
        
                        #(1-k)* C1 + C2 * k
        #couleur_totale = (1 - objet_proche.reflection - objet_proche.transparence) * np.array(couleur_directe) + objet_proche.reflection * np.array(couleur_reflechie) + objet_proche.transparence * np.array(couleur_refraction)
        k_refl = objet_proche.reflection
        k_trans = objet_proche.transparence
        k_direct = 1 - k_refl - k_trans
        couleur_totale = k_direct * couleur_directe + k_refl * couleur_reflechie + k_trans * couleur_refraction
        if(couleur_totale[0]>255):
            #print(couleur_totale)
            couleur_totale/=2
        return np.clip(couleur_totale, 0, 255)

    def trouver_intersection_la_plus_proche(self, origine, direction):
        """Cette fonction permet de vérifie si il y a des objets avant etc pour éviter les erreurs"""
        distance_min = float('inf')#Valeur par defaut
        couleur_min = np.array([255, 255, 255])#Couleur par defaut pour le fond
        objet_proche = None
        point_proche = None

        for objet in self.objets:
            point = objet.find_intersection(origine, direction)
            if point is not None:
                #la norme pour obtenir la distance
                distance = np.linalg.norm(point - origine)
                #on met a jour la distance minimale, l'objet le plus proche et le point d'intersection
                if distance < distance_min:
                    distance_min = distance
                    objet_proche = objet
                    point_proche = point
                    couleur_min = self.calculer_couleur(objet, point, self.lumiere, direction)

        return objet_proche, point_proche, couleur_min

    def calculer_couleur(self, objet, point, lumiere, rayon):
        """Méthode qui a pour but de faire de l'ombre avec la méthode de Phong"""

        normale = np.array(objet.get_normal(point))
        lumi = np.array(lumiere.direction_from(point))


        Ia = np.array([0.7, 0.7, 0.7]) #intensité lumiere ambiante
        ka = 0.4 #coefficient ambiant
        kd = 0.5 #coefficient de diffusion
        ks = 0.1 #coefficient spéculaire

        #calcule du rayon reflechi vue en TD
        r_reflechi = np.array(2 * (np.dot(-lumi, normale) * normale + lumi))
        r_reflechi /= np.linalg.norm(r_reflechi)
        I = Ia * ka + kd * np.dot(lumi, normale) + ks * (np.dot(r_reflechi, rayon) ** 100)
        
        if objet.texture and isinstance(objet, Sphere):
            u, v = objet.get_uv(normale)
            #print(u, v)
            texture_color = objet.texture.valeur(u, v)
            couleur = (np.array(objet.couleur) * np.array(texture_color)) * I
        elif objet.texture and isinstance(objet, Plan):
            u, v = objet.get_uv(point)
            #print(u, v)
            texture_color = objet.texture.valeur(u, v)
            couleur = (np.array(objet.couleur) * np.array(texture_color)) * I

        else:
            # Pour les objets sans texture, utiliser la couleur de base de l'objet
            couleur = np.array(objet.couleur) * I

        return np.clip(couleur, 0, 255).astype(int)
    
    def trouver_ombre_par_objets(self, objet_ignore, point_de_depart, direction_lumiere, distance_lumiere):
        for objet in self.objets:
            #on verifie si c'est le bonne objet si c'est le bon
            if objet != objet_ignore:
                    #on peut chopper notre nouvelle intersection de notre objet
                    intersection_ombre = objet.find_intersection(point_de_depart, direction_lumiere)
                    if intersection_ombre is not None:
                        #une fois ça on peut obtenir notre distance 
                        distance_intersection = np.linalg.norm(intersection_ombre - point_de_depart)
                        #si oui ça veut dire qu'on tracer l'ombre
                        if distance_intersection < distance_lumiere:
                            return True
        return False
        
    

    def est_dans_ombre(self, intersection, objet_ignore):
        """Fonction qui pour but de déterminer si on dans l'ombre de l'objet en question"""
        #recuperation de la lumiere et normalisation
        direction_lumiere = self.lumiere.direction_from(intersection)
        distance_lumiere = np.linalg.norm(self.lumiere.position - intersection)
        point_de_depart = intersection + direction_lumiere * 0.001#on obtient un point de depart toujours avec l'espsilon pour eviter l'erreur
        return self.trouver_ombre_par_objets(objet_ignore, point_de_depart, direction_lumiere, distance_lumiere)

    def main(self):

        image = Image.new("RGB", (self.largeur, self.hauteur), "white")
        draw = ImageDraw.Draw(image)
        #Boucle principale
        for y in range(self.hauteur):
            for x in range(self.largeur):
                rayon = self.calculer_rayon(x, y)
                couleur = self.tracer_rayon(self.camera.position, rayon, 0)
                draw.point((x, y), fill=tuple(couleur.astype(int)))
        image.save("scene1.png")
        image.show()
        """
        # Appliquez la correction gamma ici
        corrected_image = self.apply_gamma_correction(image)
        corrected_image.save("corrected_scene.png")
        corrected_image.show()
        """


    def scene1(self):
        #dimensions de la scène
        largeur, hauteur = 1080, 600

        #Initialisation de la scène
        scene = Scene(largeur, hauteur)
        earth = ImageTexture('earthmap.jpg')
        sol = ImageTexture('sol2.jpg')
        texture_bois = ImageTexture('bois.png')

        sphere1 = Sphere(1, [0, 1, 0], [255, 255, 255], 0,earth,0)
        #sphere2 = Sphere(0.5, [0, 1, 2], [0, 255, 0], 0, None, 1.5)
        #sphere3 = Sphere(1, [2, 1, 0], [255, 255, 255], 1.0, None,0)
        #sphere4 = Sphere(1, [-2, 1, 0], [255, 255, 255], 0, None, 0)
        plan_horizontal = Plan([0, 0, 0], [0, 1, 0], [255, 255, 255],0.2, sol,0)
        #plan_vertical = Plan([0, 0, -10], [0, 0, 1], [0, 0, 0], 0, None,0)
        #plan_vertical1 = Plan([0, 0, 10], [0, 0, 1], [255, 255, 255], 0, None)

        #Ajout 
        scene.ajouter_objet(sphere1)
        #scene.ajouter_objet(sphere2)
        #scene.ajouter_objet(sphere3)
        #scene.ajouter_objet(sphere4)
        scene.ajouter_objet(plan_horizontal)
        #scene.ajouter_objet(plan_vertical)
        #scene.ajouter_objet(plan_vertical1)

        #configuration de la caméra
        camera = Camera(np.array([0, 3, 7]), np.array([0, 0, -1]), [0, 1, 0], [largeur, hauteur], largeur/2)
        scene.configurer_camera(camera)

        #configuration de la lumière
        lumiere = Lumiere([-2, 5, 1], [1, 1, 1])
        scene.ajouter_lumiere(lumiere)

        #Rendu de la scène
        scene.main()

    def test_1080(self):
        #dimensions de la scène
        largeur, hauteur = 500, 500

        #Initialisation de la scène
        scene = Scene(largeur, hauteur)
        earth = ImageTexture('earthmap.jpg')

        sphere1 = Sphere(1, [0, 1, 0], [255, 255, 255], 0, earth)
        scene.ajouter_objet(sphere1)
       
        #configuration de la caméra
        camera = Camera(np.array([0, 3, 7]), np.array([0, 0, -1]), [0, 1, 0], [largeur, hauteur], largeur/1.5)
        scene.configurer_camera(camera)

        #configuration de la lumière
        lumiere = Lumiere([2, 5, 5], [1, 1, 1])
        scene.ajouter_lumiere(lumiere)

        #Rendu de la scène
        scene.main()

    def test_transparent(self):
            #dimensions de la scène
            largeur, hauteur = 500, 500

            #Initialisation de la scène
            scene = Scene(largeur, hauteur)
            earth = ImageTexture('earthmap.jpg')

            sphere1 = Sphere(1, [0, 1, 0], [255, 255, 255], 0,earth,0)
            sphere2 = Sphere(0.5, [0, 1, 2], [0, 255, 0], 0, None, 1.5)
            scene.ajouter_objet(sphere1)
            scene.ajouter_objet(sphere2)

            #configuration de la caméra
            camera = Camera(np.array([0, 3, 5]), np.array([0, 0, -1]), [0, 1, 0], [largeur, hauteur], largeur/1.5)
            scene.configurer_camera(camera)

            #configuration de la lumière
            lumiere = Lumiere([2, 5, 5], [1, 1, 1])
            scene.ajouter_lumiere(lumiere)

            #Rendu de la scène
            scene.main()

if __name__ == "__main__":
    #Initialisation de la scène
    scene = Scene(None, None)
    scene.scene1()