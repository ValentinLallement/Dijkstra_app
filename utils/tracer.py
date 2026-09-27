from PIL import Image, ImageDraw
from starlette.responses import FileResponse
coordonnees = {
    "A1": (63,  100),
    "A2": (160, 100),
    "A3": (240, 182),
    "A4": (317, 250),
    "A5": (454, 251),
    "A6": (565, 167),
    "A7": (622, 204),
    "A8": (689, 314),
    "B1": (155, 403),
    "B2": (258, 379),
    "B3": (250, 312),
    "B4": (378, 113),
    "B5": (447, 44),
    "B6": (650, 40),
    "C1": (59, 195),
    "C2": (220, 40),
    "C3": (325, 38),
    "C4": (559, 274),
    "C5": (559, 376),
    "C6": (414, 376),
    "C7": (155, 290),
}

def get_coordinates(node_names):
    print(node_names)
    
    return [coordonnees[name] for name in node_names]

from PIL import Image, ImageDraw
from fastapi.responses import FileResponse


def tracer(liste_points):
    print("tracé !")

    image = Image.open("static/images/Graphe.png").convert("RGBA")
    dessin = ImageDraw.Draw(image)

    # Points supplémentaires uniquement pour les 3 cassures
    points_intermediaires = {
        (coordonnees["A2"], coordonnees["A3"]): (160, 180),
        (coordonnees["A5"], coordonnees["A6"]): (455, 168),
        (coordonnees["A6"], coordonnees["A7"]): (565, 205)

    
    }

    # Tracé du chemin
    for i in range(len(liste_points) - 1):

        point1 = liste_points[i]
        point2 = liste_points[i + 1]

        
        if (point1, point2) in points_intermediaires:

            point_intermediaire = points_intermediaires[(point1, point2)]

            dessin.line(
                [point1, point_intermediaire, point2],
                fill="lightcoral",
                width=5
            )

        else:
            dessin.line(
                [point1, point2],
                fill="lightcoral",
                width=5
            )

    x, y = liste_points[-1]

    pointeur = Image.open(
        "static/images/pointeur.png"
    ).convert("RGBA")

    taille = 40
    pointeur = pointeur.resize(
        (taille, taille),
        Image.Resampling.LANCZOS
    )
    position = (
        x - taille // 2,
        y - taille
    )
    image.paste(
        pointeur,
        position,
        pointeur
    )

    image.save("static/images/resultat.png")

    return FileResponse("static/images/resultat.png")