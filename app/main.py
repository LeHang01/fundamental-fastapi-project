from fastapi import FastAPI
from app.config import engine
from app.router import auth_router, pro_router
from app import model

# generate model to table postgresql
model.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
async def Home():
    return "Welcome Home"


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(pro_router, prefix="/product", tags=["product"])