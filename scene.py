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
        """
        calcul du rayon sortant de la caméra
        """
        x = x - self.largeur / 2 + self.camera.position[0]
        y = self.hauteur / 2 - y + self.camera.position[1]
        z = self.camera.position[2] - self.camera.distance_focale
        
        pixel = np.array([x, y, z])
        

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


        #Total internal reflection
        if sin_r2 > 1.0:
            return None  
        
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


        #Réfraction
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
        """
        if(couleur_totale[0]>255):
            #print(couleur_totale)
            couleur_totale/=2
        """
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

