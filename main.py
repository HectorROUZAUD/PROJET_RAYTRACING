from PIL import Image, ImageDraw
from PIL import Image 
import numpy as np

import scene
import camera
import sphere
WIDTH= 100
HEIGHT = 100


if __name__ == "__main__":
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    #draw.point((100, 100), fill="red")

    objet = sphere.Sphere(1, [0, 0, 0])
          
    for x in range(WIDTH):
        for y in range(HEIGHT):
            camera_ = camera.Camera([WIDTH, HEIGHT], [0, 0, 10], [x, y, 10], [0, 0, 1], 0.1)

            rayon_vue = camera_.rayon([x, y, 0]) #ça balaye bien tous les pixels
            print(x, y)
            #print(f"rayon de vue: {rayon_vue}\n")
            if objet.intersection(rayon_vue, [0, 0, 0], 2) == True:
                pass
                #draw.point((x, y), fill="red")
                #image.putpixel((x, y), (0, 0, 0))

    image.show("sphere.png")


"""
    #AJOUT DE LA SCENE
    ajouter_scene()

    #AJOUT DES OBJETS
    ajouter_objets()

    #AJOUT SOURCE LUMINEUSE
    ajouter_lumieres()
"""
