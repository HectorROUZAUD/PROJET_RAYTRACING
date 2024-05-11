from PIL import Image, ImageDraw
from PIL import Image 


class ImageTexture:
    def __init__(self, filename):
        self.image = Image.open(filename)
        self.largeur, self.hauteur = self.image.size

    def valeur(self, u, v):
        u = max(0, min(1, u))
        v = 1.0 - max(0, min(1, v))
        i = int(u * self.largeur)
        j = int(v * self.hauteur)
        i = max(0, min(i, self.largeur - 1))
        j = max(0, min(j, self.hauteur - 1))
        pixel = self.image.getpixel((i, j))
        color_scale = 1.0 / 255.0
        return tuple(color_scale * channel for channel in pixel)

        """
        if isinstance(pixel, int):  # Si le pixel est un entier, c'est probablement une image en niveaux de gris
            color_scale = 1.0 / 255.0
            return (color_scale * pixel, color_scale * pixel, color_scale * pixel)  # Retourne un tuple RGB normalisé
        else:
            color_scale = 1.0 / 255.0
            return tuple(color_scale * channel for channel in pixel)
        """