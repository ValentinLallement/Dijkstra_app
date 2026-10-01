def convertir(valeur):
    try:
        return int(valeur)
    except ValueError:
        try:
            return float(valeur)
        except ValueError:
            return valeur


def parser_fichier(contenu):
    sommets = set()
    aretes = []

    for ligne in contenu.splitlines():

        ligne = ligne.strip()

        if not ligne:
            continue

        depart, arrivee, poids = ligne.split()

        depart = convertir(depart)
        arrivee = convertir(arrivee)
        poids = convertir(poids)

        sommets.add(depart)
        sommets.add(arrivee)

        aretes.append({
            "depart": depart,
            "arrivee": arrivee,
            "poids": poids
        })

    sommets = sorted(
        sommets,
        key=str
    )

    return sommets, aretes