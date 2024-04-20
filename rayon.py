from vecteur import Vecteur

class Rayon:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalize()

    def at(self, t):
        return self.origin + t * self.direction