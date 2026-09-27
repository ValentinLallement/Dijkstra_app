from fastapi import FastAPI
from routers.router import api_router
from PIL import Image, ImageDraw
from fastapi.responses import FileResponse, RedirectResponse

app = FastAPI()
app.include_router(api_router,prefix="/api")

@app.get("/")
def root():
        return RedirectResponse("/api/accueil")

