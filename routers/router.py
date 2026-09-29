from fastapi import FastAPI, APIRouter,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from utils.dijkstra import chemin_plus_court,G1 ,get_temps_total, convertir_noms_en_int
from utils.tracer import tracer, get_coordinates,coordonnees
from database import Base, engine,db
import models  
from models import Chemin

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
        else :  
            resultat = chemin_plus_court(G1, depart, arrivee)
            if temps==None :
                temps = get_temps_total(
                    G1,
                    convertir_noms_en_int(resultat)
                ) if resultat else None
            chemin = Chemin(
                depart=depart,
                arrivee=arrivee,
                arrets=resultat,
                temps_total=temps
            )

            db.add(chemin)
            db.commit()
        
        
        tracer(get_coordinates(resultat))
        

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
            "coordonnees": coordonnees

        }
    )
