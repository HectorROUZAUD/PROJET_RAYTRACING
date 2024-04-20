from PIL import Image, ImageDraw
from PIL import Image 
import numpy as np
import math

#import scene
from camera import Camera
from sphere import Sphere
WIDTH = 1000
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
    """

    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    #PARTIE: SPHÈRE
    x_centre = 100
    y_centre = 100
    z_centre = 0
    couleur = "red"
    rayon = 100

    x_centre1 = 300
    y_centre1 = 100
    z_centre1 = 0
    couleur1 = "green"
    rayon1 = 100
    
    x_centre2 = -100
    y_centre2 = 100
    z_centre2 = 0
    couleur2 = "blue"
    rayon2 = 100

    sphere = Sphere(rayon, [x_centre, y_centre, z_centre], couleur, draw)
    sphere1 = Sphere(rayon1, [x_centre1, y_centre1, z_centre1], couleur1, draw)
    sphere2 = Sphere(rayon2, [x_centre2, y_centre2, z_centre2], couleur2, draw)

    #PARTIE: CAMÉRA
    """
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
    """
    posi_cam = np.array([100, 100, 100])
    dir_cam =  np.array([0, 0, -1]) #regarde la viewport 
    or_cam = [0, 0, -1] 
    dim_cam = [WIDTH, HEIGHT] #la caméra à une window de taille 100x100 pixel
    df_cam = 150

    objets = [
        sphere, sphere1, sphere2
    ]

    camera_ = Camera(posi_cam, dir_cam, or_cam, dim_cam, df_cam)


    # À l'intérieur de la boucle principale dans main.py
    for y in range(HEIGHT):
        for x in range(WIDTH):
            pixel = np.array([x - WIDTH/2 + posi_cam[0], y - HEIGHT/2 + posi_cam[1], posi_cam[2] - df_cam])
            rayon = camera_.rayon_vue(pixel)
            
            # Initialisation de la variable pour conserver la sphère la plus proche
            closest_sphere = None
            closest_distance = float('inf')

            # Recherchez l'intersection la plus proche pour chaque sphère
            for sphere in objets:
                point = sphere.find_intersection(rayon, pixel)
                if point is not None:
                    distance = np.linalg.norm(point - camera_.position)
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_sphere = sphere

            # Dessinez le point seulement si la sphère la plus proche a été trouvée
            if closest_sphere is not None:
                draw.point((x, y), fill=closest_sphere.couleur)
        

    image.show()  # Vous pouvez aussi sauvegarder l'image si nécessaire avec image.save("output.png")