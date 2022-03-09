from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from data.database import engine
from data import models
from routers import users, trips, auth


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(trips.router)
