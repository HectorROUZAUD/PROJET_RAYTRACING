from PIL import Image, ImageDraw
from PIL import Image 
import numpy as np
import math

#import scene
import camera
import sphere
WIDTH= 500
HEIGHT = 500


if __name__ == "__main__":
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    #PARTIE: SPHÈRE
    x_centre = 250
    y_centre = 250
    z_centre = 0
    rayon = 50
    
    objet = sphere.Sphere(rayon, [x_centre, y_centre, z_centre], draw)

    #PARTIE: CAMÉRA
    posi_cam = [250, 250, 250]
    dir_cam =  [0, 0, -1] #regarde la viewport 
    or_cam = [0, 0, -1] 
    dim_cam = [100, 100] #la caméra à une window de taille 100x100 pixel
    df_cam = 0.5

    camera_ = camera.Camera(posi_cam, dir_cam, or_cam, dim_cam, df_cam)

    for y in range(HEIGHT):
        for x in range(WIDTH):
            """
            Il faut vérifier que pour chaque objet qui se trouve dans la 
            viewport, on la voit bien dans la window de notre caméra

            C'est pour ça qu'on a definie une taille de caméra

            C'est comme pour les premier TP on avait une viewport et une window à définir
            """


            objet.dessiner_sphere(x, y)


    image.show("sphere.png")



