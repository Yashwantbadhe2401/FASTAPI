from fastapi import FastAPI
from app.routes import hello


app = FastAPI()

# Register routes
app.include_router(hello.router)

