import numpy as np
from PIL import Image, ImageDraw

class Vecteur:
    def __init__(self, x, y, z):
        self.vecteur = np.array([x, y, z])

    def addition(self, autre):
        return Vecteur(*(self.vecteur + autre.vecteur))

    def soustraction(self, autre):
        return Vecteur(*(self.vecteur - autre.vecteur))

    def multiplication_scalaire(self, scalaire):
        return Vecteur(*(self.vecteur * scalaire))

    def produit_scalaire(self, autre):
        return np.dot(self.vecteur, autre.vecteur)

    def produit_vectoriel(self, autre):
        return Vecteur(*np.cross(self.vecteur, autre.vecteur))

    def normalisation(self):
        norme = np.linalg.norm(self.vecteur)
        return Vecteur(*(self.vecteur / norme if norme != 0 else self.vecteur))

    def norme(self):
        return np.linalg.norm(self.vecteur)

    def reflect(self, normal):
        n = normal.vecteur
        return Vecteur(*self.vecteur - 2 * self.produit_scalaire(normal) * n)

    def dessiner(self, image, couleur=(0, 0, 0), epaisseur=1):
        draw = ImageDraw.Draw(image)
        origine = (self.vecteur[0], self.vecteur[1])
        extremite = (self.vecteur[0] + self.vecteur[2], self.vecteur[1] + self.vecteur[2])
        draw.line(origine + extremite, fill=couleur, width=epaisseur)

    def normalisation(self):
        #Utilisation de np.linalg.norm qui nous calcule la norme directement
        norme = np.linalg.norm(self.extremite - self.origine)
        return Vecteur(self.origine, self.origine + (self.extremite - self.origine) / norme)


    def norme(self):
        #La norme calculer avec np
        return np.linalg.norm(self.extremite - self.origine)


    def normalize(self):
        norm = np.linalg.norm(self)
        if norm == 0: 
            return self
        return self / norm


    def dot(self, b):
        return np.dot(self, b)
