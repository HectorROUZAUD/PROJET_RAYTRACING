from PIL import Image, ImageDraw
import numpy as np
import math 


from camera import Camera
from sphere import Sphere
from plan import Plan
from lumiere import Lumiere
from image_texture import ImageTexture
from scene import Scene

def main(self):
    image = Image.new("RGB", (self.largeur, self.hauteur), "white")
    draw = ImageDraw.Draw(image)
    #Boucle principale
    for y in range(self.hauteur):
        for x in range(self.largeur):
            rayon = self.calculer_rayon(x, y)
            couleur = self.tracer_rayon(self.camera.position, rayon, 0)
            draw.point((x, y), fill=tuple(couleur.astype(int)))
    image.save("Images/scene1.png")
    image.show()
    """
    # Appliquez la correction gamma ici
    corrected_image = self.apply_gamma_correction(image)
    corrected_image.save("Images/corrected_scene.png")
    corrected_image.show()
    """

def scene1(self):
    """
    Image avec: ombres
                ombre portées
                plan
    """
    #dimensions de la scène
    largeur, hauteur = 1080, 600

    #Initialisation de la scène
    scene = Scene(largeur, hauteur)
    earth = ImageTexture('Texture_image/earthmap.jpg')
    sol = ImageTexture('Texture_image/sol2.jpg')
    texture_bois = ImageTexture('Texture_image/bois.png')

    sphere1 = Sphere(1, [0, 1, 0], [255, 255, 255], 0, earth, 0)
    #sphere2 = Sphere(0.5, [0, 1, 2], [0, 255, 0], 0, None, 1.5)
    sphere3 = Sphere(1, [2, 1, 0], [255, 255, 255], 1.0, None, 0)
    sphere4 = Sphere(1, [-2, 1, 0], [255, 255, 255], 0, None, 0)
    plan_horizontal = Plan([0, 0, 0], [0, 1, 0], [255, 255, 255], 0.2, sol, 0)
    #plan_vertical = Plan([0, 0, -10], [0, 0, 1], [0, 0, 0], 0, None,0)
    #plan_vertical1 = Plan([0, 0, 10], [0, 0, 1], [255, 255, 255], 0, None)

    #Ajout 
    scene.ajouter_objet(sphere1)
    #scene.ajouter_objet(sphere2)
    scene.ajouter_objet(sphere3)
    scene.ajouter_objet(sphere4)
    scene.ajouter_objet(plan_horizontal)
    #scene.ajouter_objet(plan_vertical)
    #scene.ajouter_objet(plan_vertical1)

    #configuration de la caméra
    camera = Camera(np.array([0, 1, 5]), np.array([0, 0, -1]), [0, 1, 0], [largeur, hauteur], largeur/2)
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
    earth = ImageTexture('Texture_image/earthmap.jpg')

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
    earth = ImageTexture('Texture_image/earthmap.jpg')

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
    scene1()