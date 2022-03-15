import uvicorn
from fastapi import FastAPI, status

from data.database import engine
from data import models
from routers import users, trips, auth


app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(trips.router)


@app.get("/", status_code=status.HTTP_200_OK)
async def index_get():
    return {"template": "index.html"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
