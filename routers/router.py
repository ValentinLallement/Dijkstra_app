from fastapi import FastAPI, APIRouter,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from utils.dijkstra import chemin_plus_court,G1 ,get_temps_total, convertir_noms_en_int
from utils.tracer import tracer, get_coordinates

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

    resultat = None

    if depart is not None and arrivee is not None:
        resultat = chemin_plus_court(G1, depart, arrivee)
        tracer(get_coordinates(resultat))
        temps = get_temps_total(
            G1,
            convertir_noms_en_int(resultat)
        ) if resultat else None

        if temps is not None:
            minutes = int(temps)
            secondes = int((temps - minutes) * 60)
            temps = f"{minutes} min {secondes} s"

    return templates.TemplateResponse(
        request=request,
        name="itinéraire.html",
        context={
            "resultat": resultat,
            "depart": depart,
            "arrivee": arrivee,
            "temps_total": temps if resultat else None,
            "image": "/static/images/resultat.png",
            "coordonnees": get_coordinates(resultat) if resultat else None

        }
    )
