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


WIDTH = 500
HEIGHT = 500


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
    

    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    #PARTIE: SPHÈRE
    x_centre = 100
    y_centre = 100
    z_centre = 0
    couleur = [255, 0, 0]
    rayon = 100

    x_centre1 = 300
    y_centre1 = 100
    z_centre1 = 0
    couleur1 = [0, 255, 0]
    rayon1 = 100
    
    x_centre2 = -100
    y_centre2 = 100
    z_centre2 = 0
    couleur2 = [0, 0, 255]
    rayon2 = 100

    sphere = Sphere(rayon, [x_centre, y_centre, z_centre], couleur, draw)
    sphere1 = Sphere(rayon1, [x_centre1, y_centre1, z_centre1], couleur1, draw)
    sphere2 = Sphere(rayon2, [x_centre2, y_centre2, z_centre2], couleur2, draw)

    #PARTIE: CAMÉRA
    """"""
    Pour voir une différence sur l'angle de vue, copie-colle ce qu'il y a en dessous 
    et le remplacer par tout le reste pour la caméra:

                    posi_cam = [100, 100, 150]
                    dir_cam =  [0, 0, -1] #regarde la viewport 
                    or_cam = [0, 0, -1] 
                    dim_cam = [50, 50] #la caméra à une window de taille 100x100 pixel
                    df_cam = 0 #PLUS LA DISTANCE FOCALE EST GRANDE, PLUS L'OUVERTURE DE LA CAM SERA PETITE

    La distance focale sert juste à dire si on zoom ou si on ne zoom pas la scène


    VOICI UN SCHÉMA DE COMMENT EST REPRÉSENTÉ LA CAMÉRA 
        |
        |
        -----> x:= centre de la caméra c'est posi_cam
        Ça nous sert pour dire si le pixel courant est dans le champ de vision 
        de la caméra ou pas 


                    dim_cam[0] / 2                  
                    ------|------
                    |           |
                    |           |
                    |           |
   dim_cam[1] / 2  ---    x     |
                    |           |
                    |           |
                    |           |
                    ------|------
    
    posi_cam = np.array([100, 100, 500])
    dir_cam =  np.array([0, 0, -1]) #regarde la viewport 
    or_cam = [0, 0, -1] 
    dim_cam = [WIDTH, HEIGHT] #la caméra à une window de taille 100x100 pixel
    df_cam = 150

    objets = [
        sphere, sphere1, sphere2
    ]

    camera_ = Camera(posi_cam, dir_cam, or_cam, dim_cam, df_cam)

    #PARTIE: LUMIÈRE
    posi_lumi = [100, -1000, 0]
    lumiere_ = lumiere.Lumiere(posi_lumi, [1, 1, 1])

    plan = Plan([100,300,0],[0,-1,0],[255,0,0])

    # À l'intérieur de la boucle principale dans main.py

    for y in range(HEIGHT):
        for x in range(WIDTH):
            pixel = np.array([x - WIDTH/2 + posi_cam[0], y - HEIGHT/2 + posi_cam[1], posi_cam[2] - df_cam])
            rayon = camera_.rayon_vue(pixel)
            rayon /= np.linalg.norm(rayon)
            
            # Recherchez l'intersection la plus proche pour chaque sphère
            for sphere in objets:
                point = sphere.find_intersection(rayon, pixel)
                if point is not None:
                    #il faut en premier trouver la normale au point d'intersection
                    normale = np.array(sphere.get_normal(point))
                    
                    #envoyer la lumière sur ce point d'intersection
                    lumi = np.array(lumiere_.direction_from(point))
                    
                    #à ce point on calcule la lumière 
                    Ia = np.array([0.7, 0.7, 0.7])
                    ka = 0.4
                    kd = 0.5
                    ks = 0.1
                    r_reflechi = np.array(2 * (np.dot(-lumi, normale) * normale + lumi))
                    r_reflechi/=np.linalg.norm(r_reflechi)
                    V = np.array(rayon)
                    I = Ia * ka + kd * (np.dot(lumi, normale)) + ks * (np.dot(r_reflechi, rayon)**100)
                    #I /=  np.linalg.norm(I)
                
                    
                    couleur = np.array(sphere.couleur) * I
                    
                    #couleur /= np.linalg.norm(couleur)
                    #couleur = np.clip(couleur,0,1)*255
                    print(couleur)
                    couleur = couleur.astype(int)  # Convertir en entiers
                    #print("couleur\n",couleur)
                    draw.point((x, y), fill=tuple(couleur))

            plan=plan.find_intersection(rayon, pixel)
            if plan is not None:
                #il faut en premier trouver la normale au point d'intersection
                    normale = np.array([0,-1,0])
                    
                    #envoyer la lumière sur ce point d'intersection
                    lumi = np.array(lumiere_.direction_from(plan))
                    
                    #à ce point on calcule la lumière 
                    Ia = np.array([0.7, 0.7, 0.7])
                    ka = 0.4
                    kd = 0.5
                    ks = 0.1
                    r_reflechi = np.array(2 * (np.dot(-lumi, normale) * normale + lumi))
                    r_reflechi/=np.linalg.norm(r_reflechi)
                    V = np.array(rayon)
                    I = Ia * ka + kd * (np.dot(lumi, normale)) + ks * (np.dot(r_reflechi, rayon)**100)
                    #I /=  np.linalg.norm(I)
                
                    
                    couleur = np.array(plan.couleur) * I
                    
                    #couleur /= np.linalg.norm(couleur)
                    #couleur = np.clip(couleur,0,1)*255
                    print(couleur)
                    couleur = couleur.astype(int)  # Convertir en entiers
                    #print("couleur\n",couleur)
                    draw.point((x, y), fill=tuple(couleur))
"""



    def calculer_couleur(objet, point, lumiere_, rayon, camera_):
        # il faut en premier trouver la normale au point d'intersection
        normale = np.array(objet.get_normal(point))
        
        # envoyer la lumière sur ce point d'intersection
        lumi = np.array(lumiere_.direction_from(point))
        
        # à ce point on calcule la lumière 
        Ia = np.array([0.7, 0.7, 0.7]) # Intensité lumière ambiante
        ka = 0.5  # Coefficient ambiant
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
        direction_lumiere = lumiere_.direction_from(intersection)
        distance_lumiere = np.linalg.norm(lumiere_.position - intersection)
        point_de_depart = intersection + direction_lumiere * 0.001  # Un petit offset pour éviter l'intersection avec l'objet lui-même

        for objet in objets:
            if objet is not objet_ignore:
                intersection_ombre = objet.find_intersection(point_de_depart, direction_lumiere)
                if intersection_ombre is not None:
                    distance_intersection = np.linalg.norm(intersection_ombre - point_de_depart)
                    if distance_intersection < distance_lumiere:
                        return True  # Une intersection plus proche que la lumière a été trouvée
        return False   # Aucune intersection trouvée, donc le point est éclairé


    # Initialisation de la scène avec les sphères et le plan
    #WIDTH, HEIGHT = 500, 500
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    
    # Création des objets de la scène
    spheres = [
        Sphere(100, [100, 100, 0], [255, 0, 0], draw),
        Sphere(100, [300, 100, 0], [0, 255, 0], draw),
        Sphere(100, [-100, 100, 0], [0, 0, 255], draw),
    ]
    plan = Plan([0, 0, 0], [0, 1, 0], [255, 255, 0])  # Un plan jaune pour le sol

    # Ajouter les objets dans une liste
    objets_scene = spheres + [plan]

    # Configuration de la caméra
    camera_ = Camera(np.array([100, 100, 500]), np.array([0, 0, -1]), [0, 1, 0], [WIDTH, HEIGHT], 150)

    # Configuration de la lumière
    lumiere_ = Lumiere([0, 500, 0], [1, 1, 1])


    # Boucle principale du ray tracing
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # Calcul du rayon sortant de la caméra
            pixel = np.array([x - WIDTH / 2 + camera_.position[0], HEIGHT / 2 - y + camera_.position[1], camera_.position[2] - camera_.distance_focale])
            rayon = camera_.rayon_vue(pixel)
            rayon /= np.linalg.norm(rayon)
            
            couleur_min = np.array([255, 255, 255])  # On part d'une couleur blanche par défaut
            distance_min = float('inf')  # Distance initiale infinie pour trouver le minimum
            objet_proche = None
            intersection_proche = None
            
            # Vérifier l'intersection avec tous les objets
            for objet in objets_scene:
                intersection = objet.find_intersection(rayon, camera_.position)
                if intersection is not None:
                    distance = np.linalg.norm(intersection - camera_.position)
                    if distance < distance_min:
                        distance_min = distance
                        couleur_min = calculer_couleur(objet, intersection, lumiere_, rayon, camera_)
                        objet_proche = objet
                        intersection_proche = intersection

            
            # Vérifiez si le point est dans l'ombre et calculez la couleur
            if intersection_proche is not None and objet_proche is not None:
                if est_dans_ombre(intersection_proche, lumiere_, objets_scene, objet_proche):
                    # Utiliser une couleur plus sombre pour simuler l'ombre
                    couleur = (couleur_min * 0.1)  # Assombrir la couleur pour l'ombre
                else:
                    # Calculer la couleur normalement si le point n'est pas dans l'ombre
                    couleur = couleur_min

                # Assurez-vous que la couleur est un tableau d'entiers avant de dessiner
                couleur = np.clip(couleur, 0, 255)  # S'assurer que la couleur reste dans les limites valides
                couleur = couleur.astype(int)  # Convertir en entier après l'arrondissement

                draw.point((x, y), fill=tuple(couleur))

    # Enregistrement et affichage de l'image finale
    image.save("scene.png")
    image.show()