from PIL import Image, ImageDraw
from PIL import Image 
import numpy as np
import math

#import scene
import camera
import sphere
WIDTH= 300
HEIGHT = 300


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
    x_centre = 150
    y_centre = 150
    z_centre = 0
    rayon = 50
    
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

                    Avec ses dimentions on voit le demi cercle pourquoi ? 
                                ----> Voir le shcéma du dessous


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
    posi_cam = [150, 150, 150]
    dir_cam =  [0, 0, -1] #regarde la viewport 
    or_cam = [0, 0, -1] 
    dim_cam = [100, 100] #la caméra à une window de taille 100x100 pixel
    df_cam = 0


    camera_ = camera.Camera(posi_cam, dir_cam, or_cam, dim_cam, df_cam)

    window = camera_.window()
    print(df_cam, window)
    
    for y in range(HEIGHT):
        for x in range(WIDTH):
            """
            Il faut vérifier que pour chaque objet qui se trouve dans la 
            viewport, on la voit bien dans la window de notre caméra

            C'est pour ça qu'on a definie une taille de caméra

            C'est comme pour les premier TP on avait une viewport et une window à définir
            """
            x_ray, y_ray, z_ray = camera_.rayon_vue([x, y, 0]) #récupère le rayon de vue de la caméra à pixel courant
        
            if camera_.in_window(x, y, window):
                #S'il y a intersection alors j'allume le pixel
                if objet.find_intersection([x_ray, y_ray, z_ray], [1, 1, 0]) != 0:
                    objet.dessiner_sphere(x, y)


    image.show("sphere.png")



