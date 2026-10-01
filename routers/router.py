from fastapi import FastAPI, APIRouter,Request,UploadFile,File,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse,JSONResponse
from utils.dijkstra import chemin_plus_court,G1 ,get_temps_total, convertir_noms_en_int,create_graphe,convertir_chemin_en_noms
from utils.tracer import tracer, get_coordinates,coordonnees
from utils.parser import parser_fichier,convertir
from database import Base, engine,db
import models  
from models import Chemin,Ligne

Base.metadata.create_all(bind=engine)

api_router = APIRouter()

templates = Jinja2Templates(directory="templates")
api_router.mount("/static", StaticFiles(directory="static"), name="static")

@api_router.get("/accueil", name="accueil")
def accueil(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="accueil.html"
    )

@api_router.get("/itineraire")
def itineraire(
    request: Request,
    depart: str | None = None,
    arrivee: str | None = None
):

    lignes = db.query(Ligne).all()

    resultat = None
    temps = None

    if depart is not None and arrivee is not None:

        chemin = db.query(Chemin).filter(
            Chemin.depart == depart,
            Chemin.arrivee == arrivee
        ).first()

        if chemin:
            
            resultat = chemin.arrets
            temps = chemin.temps_total
            resultat = convertir_chemin_en_noms(
            resultat
            )

        else:

            depart_int = convertir_noms_en_int(
                [depart]
            )[0]

            arrivee_int = convertir_noms_en_int(
                [arrivee]
            )[0]
            resultat = chemin_plus_court(
                G1,
                depart_int,
                arrivee_int
            )

            resultat = convertir_chemin_en_noms(
                resultat
            )
            if resultat:

                temps = get_temps_total(
                    G1,
                    convertir_noms_en_int(resultat)
                )

            else:

                temps = None

            chemin = Chemin(
                depart=depart,
                arrivee=arrivee,
                arrets=resultat,
                temps_total=temps
            )

            db.add(chemin)

            db.commit()


        if resultat:
            tracer(
                get_coordinates(resultat)
            )


        if temps is not None:

            minutes = int(temps)

            secondes = int(
                (temps - minutes) * 60
            )

            temps = (
                f"{minutes} min "
                f"{secondes} s"
            )


    return templates.TemplateResponse(
        request=request,
        name="itinéraire.html",
        context={
            "resultat": resultat,
            "depart": depart,
            "arrivee": arrivee,
            "temps_total": temps if resultat else None,
            "image": "/static/images/resultat.png",
            "coordonnees": coordonnees,
            "lignes": lignes
        }
    )
contenu = ""

from pathlib import Path

@api_router.post("/upload")
async def upload_fichier(
    fichier: UploadFile = File(...)
):

    contenu = await fichier.read()

    contenu = contenu.decode("utf-8")

    sommets, aretes = parser_fichier(
        contenu
    )
    nom = Path(
        fichier.filename
    ).stem

    ligne = Ligne(
        nom=nom,
        sommets=sommets,
        aretes=aretes
    )

    db.add(ligne)
    db.commit()
    db.refresh(ligne)

    return RedirectResponse(
        url=f"/api/itineraire_bis?ligne_id={ligne.id}",
        status_code=303
    )


@api_router.get(
    "/itineraire_bis",
    name="itineraire_bis"
)
def itineraire_bis(
    request: Request,
    ligne_id: int,
    depart: str | None = None,
    arrivee: str | None = None
):

    lignes = db.query(Ligne).all()

    ligne = db.query(Ligne).filter(
        Ligne.id == ligne_id
    ).first()


    if ligne is None:

        raise HTTPException(
            status_code=404,
            detail="Ligne introuvable"
        )


    sommets = ligne.sommets
    aretes = ligne.aretes

    graphe, noms_vers_int, int_vers_noms = create_graphe(
        sommets,
        aretes
    )


    resultat = None
    temps_affichage = None

    if depart is not None and arrivee is not None:

        depart_converti = convertir(depart)
        arrivee_converti = convertir(arrivee)


        if depart_converti not in noms_vers_int:

            raise HTTPException(
                status_code=400,
                detail=f"Sommet de départ inconnu : {depart}"
            )

        if arrivee_converti not in noms_vers_int:

            raise HTTPException(
                status_code=400,
                detail=f"Sommet d'arrivée inconnu : {arrivee}"
            )

        depart_int = noms_vers_int[
            depart_converti
        ]


        arrivee_int = noms_vers_int[
            arrivee_converti
        ]


        resultat_int = chemin_plus_court(
            graphe,
            depart_int,
            arrivee_int
        )

        if resultat_int:

            resultat = [

                int_vers_noms[sommet]

                for sommet in resultat_int

            ]

            temps = get_temps_total(
                graphe,
                resultat_int
            )


            minutes = int(temps)


            secondes = int(
                (temps - minutes) * 60
            )


            temps_affichage = (
                f"{minutes} min "
                f"{secondes} s"
            )


        else:

            print(
                f"Aucun chemin trouvé entre "
                f"{depart_converti} et {arrivee_converti}"
            )

    return templates.TemplateResponse(
        request=request,
        name="itineraire_bis.html",
        context={

            "ligne": ligne,
            "lignes": lignes,
            "sommets": sommets,
            "aretes": aretes,
            "graphe": graphe,
            "resultat": resultat,
            "depart": depart_converti if depart is not None and arrivee is not None else None,
            "arrivee": arrivee_converti if depart is not None and arrivee is not None else None,
            "temps_total": temps_affichage,
            "int_vers_noms": int_vers_noms

        }
    )