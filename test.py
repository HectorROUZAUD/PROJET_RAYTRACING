import numpy as np

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction / np.linalg.norm(direction)

class HitRecord:
    def __init__(self, t, point, normal, material):
        self.t = t
        self.point = point
        self.normal = normal
        self.material = material

class Material:
    def __init__(self, color, reflectivity):
        self.color = color
        self.reflectivity = reflectivity

class Sphere:
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, ray, t_min, t_max):
        # Calcul de l'intersection entre le rayon et la sphère
        # Retourne le point d'intersection, la normale et le matériau
        ...

def ray_color(ray, scene, depth):
    if depth <= 0:
        return np.zeros(3)  # Retourne du noir pour éviter la récursion infinie
    
    # Intersection avec les objets de la scène
    hit_record = intersect_scene(ray, scene)

    if hit_record is not None:
        scattered_ray = scatter_ray(ray, hit_record)
        if scattered_ray is not None:
            return hit_record.material.color * ray_color(scattered_ray, scene, depth - 1)
        else:
            return np.zeros(3)  # Pas de réflexion, retourne du noir
    else:
        # Pas d'intersection, couleur de fond
        return np.array([0.5, 0.7, 1.0])  # Exemple de couleur de fond

def scatter_ray(ray, hit_record):
    # Réflexion spéculaire
    if hit_record.material.reflectivity > 0:
        reflected_direction = reflect(ray.direction, hit_record.normal)
        return Ray(hit_record.point, reflected_direction)
    else:
        return None

def reflect(v, n):
    return v - 2 * np.dot(v, n) * n

def intersect_scene(ray, scene):
    closest_t = float('inf')
    closest_hit_record = None

    for object in scene:
        hit_record = object.hit(ray, 0.001, closest_t)
        if hit_record is not None and hit_record.t < closest_t:
            closest_t = hit_record.t
            closest_hit_record = hit_record

    return closest_hit_record

# Exemple de scène avec une sphère réfléchissante
scene = [Sphere(np.array([0, 0, -1]), 0.5, Material(np.array([0.8, 0.8, 0.8]), reflectivity=0.5))]

# Code principal pour générer une image
image_width = 200
image_height = 100

# Exemple de code pour générer l'image pixel par pixel
for j in range(image_height):
    for i in range(image_width):
        u = i / image_width
        v = j / image_height
        ray = Ray(origin=np.array([0, 0, 0]), direction=np.array([-1 + 2*u, -1 + 2*v, -1]))
        color = ray_color(ray, scene, depth=50)  # Profondeur maximale de récursion
        # Afficher la couleur du pixel (i, j)

