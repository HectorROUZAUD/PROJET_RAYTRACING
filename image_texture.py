from PIL import Image, ImageDraw
from PIL import Image 


class ImageTexture:
    def __init__(self, filename):
        """
        Il faut en premier exprimer les coordonnées d'un point P en coordonnées
        sphérique (theta, phi) et ensuite on les utlise pour calculer les 
        coordonnées de la texture (s, t)=(u, v)

        
        theta c'est la veleur de y mais en coordonnées sphérique car: 
            on part du principe que nous regardons notre sphère dans le repère de base (x, y, z)
                x qui va de gauche à droite
                y qui va de bas en haut
                z qui vient vers nous et recule

            Dans notre sphère y ne nous donne aucune info pour trouver la position du point P
            en coordonnée sphérique. Pour ça on "ramène" (avec de grosse guillemet) l'axe y en axe z
            Soit sur notre sphère on cherche le point y qui coresponde à un point en z.

            pour ça il existe une fonction appel arc-cos qui varie entre [0, pi] (angle de 180°) pour "ramener
            le point en y sur l'axe des z". Donc on fait venir le point y vers nous sur la sphère
                y = arc-cos(y)
            
            On a le point y en coordonnées sphérique, il nous faut maintenant connaitre la coordonnée phi 
            qui est l'angle entre l'axe x et z
            Or celui la est plus simple à comprendre et trouver car: c'est "le point" qui tourne autoure de la sphère en 360° 
            soit phi [0, 2pi]
                phi = arc_cos2(-z, x) + pi
                    on utilise arc-cos2 pour trouver directement l'angle entre x et z
        Ensuite il faut tout normaliser car nous venons de trouver les coordonnées sphérique 
        mais u et v sont dans l'intervale [O, 1]
        Pour ça comme:
                théta e[0, pi] on divise pas pi
                phi   e[0, 2pi] on divise par 2*pi
        
        Et nous avons nos coordonnées sphérique et la position du pixel sur nôtre image normalisé
            u et v 
        
        C'EST CE QUE FAIT LA FONCTION get_uv(P) #P:= on point 
        """
        self.image = Image.open(filename)
        self.largeur, self.hauteur = self.image.size

    def valeur(self, u, v):
        """
        Fonction qui s'occupe de retourner la couleur du pixel au point calculer
        sur la texture (u, v) mais à la bonne position et à la bonne échelle de l'image 
        si je suis en :
                0.5 je suis censée être au milieu de l'image donc c'est pour ça 
                    qu'on miltiplie par la taille de l'image c'est comme un produit en croix

        Il y a des vérification de u et v pour vérifier qu'ils ont bien étaient normalisé
        soit u et v e[0, 1] pour pouvoir faire la multiplication

        et même chose pour i et j mais normalement is doivent aussi être dans la plage de valeur 
        de la taille de nôtre image soit [0, largeur] et [0, hauteur]
        """
        #Vérifiction pour savoir si u et v sont bien compris entre [0, 1]
        u = max(0, min(1, u))
        v = 1.0 - max(0, min(1, v))

        #On remet u et v à la bonne échelle de nôtre image
        #   on appel ces nouvelles position i et j
        #   et on vérifie si ils sont dans la bonne plage de valeurs
        #           i e[0, largeur] et j e[0, hauteur]
        i = int(u * self.largeur)
        i = max(0, min(i, self.largeur - 1))


        j = int(v * self.hauteur)
        j = max(0, min(j, self.hauteur - 1))

        #On récupère la couleur du pixel à la position (i, j)
        pixel = self.image.getpixel((i, j))
        
        #Échelle de couleur "ratio" pour les mettre entre [0, 255]
        color_scale = 1.0 / 255.0

        #Normalisation des couleurs
        result = []
        for channel in pixel:
            result.append(color_scale * channel)

        return tuple(result)

       