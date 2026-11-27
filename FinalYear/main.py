from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from .routers import analyze,auth,project,users,refactorEngine,fileref
from .models import Base
from .database import engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(analyze.router)
app.include_router(auth.router)
app.include_router(project.router)
app.include_router(users.router)
app.include_router(refactorEngine.router)
app.include_router(fileref.router)

#to allow CORS , requests from frontend temporarily
app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:5174",],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

@app.get("/health",status_code = status.HTTP_200_OK)
def get_health():
    return {"message": "we have all insights"}


