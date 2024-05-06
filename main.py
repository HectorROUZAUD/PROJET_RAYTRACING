from PIL import Image, ImageDraw
from PIL import Image 
import numpy as np
import math

#import scene
from camera import Camera
from sphere import Sphere
from plan import Plan
from lumiere import Lumiere
from scene import Scene





if __name__ == "__main__":
    """
    Schéma pour s'aider sur la position et la dimension de la caméra
   300
   / \---------------------------
    |                            |
    |                            |
    |                            |
    |         ----------         |
    |         |        |         |
    |         |   X    |         | 150
    |         |        |         |
    |         ----------         |
    |                            |
    |                            |
    |                            |
    ------------------------------> 300
                 150    
    
"""
    #initialisation
    WIDTH, HEIGHT = 500, 500
    image = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(image)

    
    #création des objets de la scène
    spheres = [
        Sphere(1, [0, 1, 0], [255, 0, 0], draw),
        Sphere(0.5, [0, 1, -2], [0, 255, 0], draw),
        #Sphere(100, [-100, 100, 0], [0, 0, 255], draw),
    ]
    
    #je créer un plan horizontal, et en jaune
    plan = Plan([0, 0, 0], [0, 1, 0], [255, 255, 0])  

    #Ajouter les objets dans une liste
    objets_scene = spheres + [plan]

    #configuration de la caméra
    camera_ = Camera(np.array([0, 3, 5]), np.array([0, 0, -1]), [0, 1, 0], [WIDTH, HEIGHT], 350)

    #configuration de la lumière
    lumiere_ = Lumiere([2, 5, 5], [1, 1, 1])



    def calculer_phong(objet, point, lumiere_, rayon, camera_):
        # il faut en premier trouver la normale au point d'intersection
        normale = np.array(objet.get_normal(point))
        
        # envoyer la lumière sur ce point d'intersection
        lumi = np.array(lumiere_.direction_from(point))
        
        # à ce point on calcule la lumière 
        Ia = np.array([0.7, 0.7, 0.7]) # Intensité lumière ambiante
        ka = 0.4  # Coefficient ambiant
        kd = 0.5  # Coefficient de diffusion
        ks = 0.1  # Coefficient spéculaire
        r_reflechi = np.array(2 * (np.dot(-lumi, normale) * normale + lumi))
        r_reflechi /= np.linalg.norm(r_reflechi)
        V = np.array(rayon)
        I = Ia * ka + kd * np.dot(lumi, normale) + ks * (np.dot(r_reflechi, rayon) ** 100)
        
        couleur = np.array(objet.couleur) * I
        couleur = np.clip(couleur, 0, 255)
        return couleur.astype(int)

    def est_dans_ombre(intersection, lumiere_, objets, objet_ignore):
        
        #print(direction_lumiere)
        distance_lumiere = np.linalg.norm(lumiere_.position - intersection)
        for objet in objets:
            point_de_depart = intersection + objet.get_normal(intersection) * 0.001#0.001 pour éviter d'avoir l'intersection avec l'objet lui même
            direction_lumiere = lumiere_.direction_from(point_de_depart)
            if objet != objet_ignore:
                intersection_ombre = objet.find_intersection(point_de_depart, direction_lumiere)
                if intersection_ombre is not None:
                    distance_intersection = np.linalg.norm(intersection_ombre - point_de_depart)
                    if distance_intersection < distance_lumiere:
                        return True  # Une intersection plus proche que la lumière a été trouvée
        return False   # Aucune intersection trouvée, donc le point est éclairé


    def calculer_rayon(x,y):
        #calcul du rayon sortant de la caméra
            pixel = np.array([x - WIDTH / 2 + camera_.position[0], HEIGHT / 2 - y + camera_.position[1], camera_.position[2] - camera_.distance_focale])
            rayon = camera_.rayon_vue(pixel)
            rayon /= np.linalg.norm(rayon)
            return rayon


    #Code principale
    for y in range(HEIGHT):
        for x in range(WIDTH):
            rayon=calculer_rayon(x,y)
            
            couleur_min = np.array([255, 255, 255])  # On part d'une couleur blanche par défaut
            distance_min = float('inf')  # Distance initiale infinie pour trouver le minimum
            objet_proche = None
            intersection_proche = None
            
            #Vérifier l'intersection avec tous les objets
            for objet in objets_scene:
                intersection = objet.find_intersection(camera_.position,rayon)
                if intersection is not None:
                    distance = np.linalg.norm(intersection - camera_.position)
                    if distance < distance_min:
                        distance_min = distance
                        couleur_min = calculer_phong(objet, intersection, lumiere_, rayon, camera_)
                        objet_proche = objet
                        intersection_proche = intersection

            
            # Vérifiez si le point est dans l'ombre et calculez la couleur
            if intersection_proche is not None and objet_proche is not None:
                if est_dans_ombre(intersection_proche, lumiere_, objets_scene, objet_proche):
    
                    couleur = np.array([0,0,0])*0.1  # Assombrir la couleur pour l'ombre
                else:
                    
                    couleur = calculer_phong(objet_proche, intersection_proche, lumiere_, rayon, camera_)

                couleur = np.clip(couleur, 0, 255)  #Pour s'assurer que la couleur reste dans les limites valides
                couleur = couleur.astype(int)  # Convertir en entier après l'arrondissement

                draw.point((x, y), fill=tuple(couleur))

    # Enregistrement et affichage de l'image finale
    image.save("scene.png")
    image.show()