from PIL import Image, ImageDraw
from PIL import Image 
import numpy as np
import math

#import scene
import camera
import sphere
WIDTH = 70
HEIGHT = 70


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
    x_centre = WIDTH // 2
    y_centre = HEIGHT // 2
    z_centre = 0
    rayon = 5
    
    objet = sphere.Sphere(rayon, [x_centre, y_centre, z_centre], draw)

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
    posi_cam = [WIDTH // 2, HEIGHT // 2, WIDTH // 2]
    dir_cam =  [0, 0, -1] #regarde la viewport 
    or_cam = [0, 0, -1] 
    dim_cam = [8, 8] #la caméra à une window de taille 100x100 pixel
    df_cam = 50


    camera_ = camera.Camera(posi_cam, dir_cam, or_cam, dim_cam, df_cam)


    for y in range(HEIGHT):
        print(y)
        for x in range(WIDTH):
            """
            Il faut vérifier que pour chaque objet qui se trouve dans la 
            viewport, on la voit bien dans la window de notre caméra

            C'est pour ça qu'on a definie une taille de caméra

            C'est comme pour les premier TP on avait une viewport et une window à définir
            """
            print("\t", x)
            pixel_courant_dessin = [x, y, 0]
            camera_.rayon_vue(pixel_courant_dessin, objet)
            


    image.show("sphere.png")



