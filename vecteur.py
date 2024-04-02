from PIL import Image, ImageDraw
import numpy as np

class Vecteur:
    def __init__(self, origine, extremite):
        self.origine = np.array(origine)
        self.extremite = np.array(extremite)

    def addition(self, vecteur2):
        return Vecteur(self.origine, self.extremite + vecteur2.extremite)

    def soustraction(self, vecteur2):
        return Vecteur(self.origine, self.extremite - vecteur2.extremite)

    def multiplication_scalaire(self, scalaire):
        return Vecteur(self.origine, self.extremite * scalaire)

    def produit_scalaire(self, vecteur2):
        """fait le produit scalaire avec dot"""
        return np.dot(self.extremite - self.origine, vecteur2.extremite - vecteur2.origine)

    def produit_vectoriel(self, vecteur2):
        return np.cross(self.extremite - self.origine, vecteur2.extremite - vecteur2.origine)

    def normalisation(self):
        norme = np.linalg.norm(self.extremite - self.origine)
        return Vecteur(self.origine, self.origine + (self.extremite - self.origine) / norme)

    def norme(self):
        return np.linalg.norm(self.extremite - self.origine)

    def dessiner(self, image, couleur=(0, 0, 0), epaisseur=1):
        draw = ImageDraw.Draw(image)
        draw.line((self.origine[0], self.origine[1], self.extremite[0], self.extremite[1]), fill=couleur, width=epaisseur)


"""
# Exemple d'utilisation
origine_vecteur1 = (50, 50)
extremite_vecteur1 = (100, 100)
vecteur1 = Vecteur(origine_vecteur1, extremite_vecteur1)

origine_vecteur2 = (100, 100)
extremite_vecteur2 = (200, 150)
vecteur2 = Vecteur(origine_vecteur2, extremite_vecteur2)

# Création d'une image
image = Image.new("RGB", (300, 200), "white")

# Dessiner les vecteurs sur l'image
vecteur1.dessiner(image, couleur=(255, 0, 0), epaisseur=2)
vecteur2.dessiner(image, couleur=(0, 0, 255), epaisseur=2)

# Afficher l'image
image.show()
"""
