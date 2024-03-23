from fastapi import FastAPI
from app.config import engine
from app import model
from app import router

# generate model to table postgresql
model.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
async def Home():
    return "Welcome Home"


app.include_router(router.router)