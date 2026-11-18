from fastapi import FastAPI,HTTPException
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


@app.get("/health",status_code = status.HTTP_200_OK)
def get_health():
    return {"message": "we have all insights"}


