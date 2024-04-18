from PIL import Image, ImageDraw
from PIL import Image 
import numpy as np
import math

#import scene
import camera
import sphere
WIDTH = 200
HEIGHT = 200


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
    df_cam = 20


    camera_ = camera.Camera(posi_cam, dir_cam, or_cam, dim_cam, df_cam)


    #Parcours de l'écran de la caméra
    for y in range(HEIGHT):
        for x in range(WIDTH):
            #il faut générer un rayon r(origine, direction)
            posi_x = x - WIDTH/2 + posi_cam[0]
            posi_y = y - HEIGHT/2 + posi_cam[1]
            posi_z = posi_cam[2] - df_cam
            pixel = np.array([posi_x, posi_y, posi_z])
            
            rayon = camera_.rayon_vue(pixel)
            #est-ce qu'il y a une intersection ? entre le rayon  et notre sphère
            if objet.find_intersection(rayon, pixel) is not None:
                draw.point((x, y), fill="red")
            


    image.show("sphere.png")



