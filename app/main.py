from app.auth.routes import user as user_routes
from app.blog.routes import blog as blog_routes
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import init_db
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import LoggingMiddleware

@asynccontextmanager
async def lifespan(app):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_routes.router, prefix="/auth", tags=["auth"])
app.include_router(blog_routes.router, prefix="/blog", tags=["blog"])
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 