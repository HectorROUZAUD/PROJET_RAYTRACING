from PIL import Image, ImageDraw
import numpy as np



class Couleur:
    #Constructeur
    def __init__(self, rouge, vert, bleu):
        #creation du vecteur couleur avec numpy
        self.couleur = np.array([rouge, vert, bleu])
    #Méthodes
    def addition(self, couleur2):
        # Utilisation de np.add() pour ajouter les composantes de couleur
        nouvelle_couleur = np.add(self.couleur,couleur2.couleur)
        return Couleur(nouvelle_couleur)#on remet la couleur à jour

    def multiplication(self, couleur2):
        nouvelle_couleur = self.couleur * couleur2.couleur
        #on retourne un vecteur
        return Couleur(nouvelle_couleur)
