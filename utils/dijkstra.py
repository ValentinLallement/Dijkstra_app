G1 = [
    [0,     0.700, 0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0    ],  # A1
    [0.700, 0,     0.920, 0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     1.590, 1.170, 0,     0,     0,     0,     0    ],  # A2
    [0,     0.920, 0,     0.780, 0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0    ],  # A3
    [0,     0,     0.780, 0,     1.200, 0,     0,     0,     0,     0,     0.686, 0.994, 0,     0,     0,     0,     0,     0,     0,     0,     0    ],  # A4
    [0,     0,     0,     1.200, 0,     1.060, 0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0    ],  # A5
    [0,     0,     0,     0,     1.060, 0,     0.780, 0,     0,     0,     0,     0,     2.040, 0,     0,     0,     0,     1.350, 0,     0,     0    ],  # A6
    [0,     0,     0,     0,     0,     0.780, 0,     1.080, 0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0    ],  # A7
    [0,     0,     0,     0,     0,     0,     1.080, 0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0    ],  # A8
    [0,     0,     0,     0,     0,     0,     0,     0,     0,     0.771, 0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0    ],  # B1
    [0,     0,     0,     0,     0,     0,     0,     0,     0.771, 0,     0.429, 0,     0,     0,     0,     0,     0,     0,     0,     1.800, 1.695],  # B2
    [0,     0,     0,     0.686, 0,     0,     0,     0,     0,     0.429, 0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0    ],  # B3
    [0,     0,     0,     0.994, 0,     0,     0,     0,     0,     0,     0,     0,     0.857, 0,     0,     0,     0,     0,     0,     0,     0    ],  # B4
    [0,     0,     0,     0,     0,     2.040, 0,     0,     0,     0,     0,     0.857, 0,     1.200, 0,     0,     1.500, 0,     0,     0,     0    ],  # B5
    [0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     1.200, 0,     0,     0,     0,     0,     0,     0,     0    ],  # B6
    [0,     1.590, 0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     1.590],  # C1
    [0,     1.170, 0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     1.350, 0,     0,     0,     0    ],  # C2
    [0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     1.500, 0,     0,     1.350, 0,     0,     0,     0,     0    ],  # C3
    [0,     0,     0,     0,     0,     1.350, 0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     1.500, 0,     0    ],  # C4
    [0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     1.500, 0,     1.800, 0    ],  # C5
    [0,     0,     0,     0,     0,     0,     0,     0,     0,     1.800, 0,     0,     0,     0,     0,     0,     0,     0,     1.800, 0,     0    ],  # C6
    [0,     0,     0,     0,     0,     0,     0,     0,     0,     1.695, 0,     0,     0,     0,     1.590, 0,     0,     0,     0,     0,     0    ],  # C7
]

def initialisation(G, s_init) :
  result={}
  for i in range(len(G)):
    result[i]=[i,'infini',None]
  result[s_init][1]=0
  return result


def recherche_sommet_min(D):
    if len(D) == 0:
        return False

    min = None
    result = None

    for sommet in D:
        if D[sommet][1] != 'infini' and (min is None or D[sommet][1] < min):
            min = D[sommet][1]
            result = D[sommet][0]

    return result



def retirer_sommet(D, sommet) :
  D.pop(sommet)
  return D

def ajouter_sommet(S, sommet, D):
    S[sommet] = D[sommet]
    return S

def get_sommets_voisins(G, liste_sommet, sommet) :
  liste=[]
  for j in range(len(G[sommet])):
    if G[sommet][j] != 0 and j in liste_sommet :
      liste.append(j)
  return liste


def maj_poids(G, sommet1, sommet2, D):

    poids_1 = D[sommet1][1]
    poids_2 = D[sommet2][1]

    poids_chemin = G[sommet1][sommet2]
    if poids_1 != "infini":
        nouveau_poids = poids_1 + poids_chemin
        if poids_2 == "infini" or poids_1 + poids_chemin < poids_2:
            D[sommet2][1] = nouveau_poids
            D[sommet2][2] = sommet1

    return D

def dijkstra(G, s_init):
    S = {}
    D = initialisation(G, s_init)

    while len(D) > 0:

        sommet_min = recherche_sommet_min(D)

        sommets_voisins = get_sommets_voisins(G, D, sommet_min)

        for voisin in sommets_voisins:
            maj_poids(G, sommet_min, voisin, D)

        S = ajouter_sommet(S, sommet_min,D)
        D = retirer_sommet(D, sommet_min)


    return S

def convertir_chemin_en_noms(chemin):
    noms = []
    for sommet in chemin:
        noms.append(f"A{sommet + 1}" if sommet < 8 else f"B{sommet - 7}" if sommet < 14 else f"C{sommet - 13}")
    return noms

def convertir_noms_en_int(noms):
    sommets = []
    for nom in noms:
        if nom.startswith("A"):
            sommets.append(int(nom[1:]) - 1)
        elif nom.startswith("B"):
            sommets.append(int(nom[1:]) + 7)
        elif nom.startswith("C"):
            sommets.append(int(nom[1:]) + 13)
    return sommets
    

def chemin_plus_court(G,sommet1,sommet2):
    a=convertir_noms_en_int([sommet1,sommet2])
    sommet1=a[0]
    sommet2=a[1]
    D=dijkstra(G,sommet1)
    i=sommet2
    chemin=[sommet2]
    while D[i][2]!= None :
        sommet=D[i][2]
        chemin.append(sommet)
        i=sommet
    chemin.reverse()
    chemin = convertir_chemin_en_noms(chemin)
    return chemin


def get_temps_total(G, chemin):
    temps_total = 0
    for i in range(len(chemin) - 1):
        sommet1 = chemin[i]
        sommet2 = chemin[i + 1]
        poids = G[sommet1][sommet2]
        temps_total += poids
    return temps_total