from fastapi import FastAPI
from backend.routes import auth,tasks
from backend.database.connection import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome! To start the App"}

app.include_router(auth.router)
app.include_router(tasks.router)
