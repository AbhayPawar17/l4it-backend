import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.auth.routes import user as user_routes
from app.blog.routes import blog as blog_routes
from app.services.routes.mspservices import router as msp_services_routes
from app.whatwedo.routes.info import router as info_routes
from app.contact.routes.routes import router as contact_router
from app.casestudy.routes.route import router as case_study_routes
from app.core.logging import LoggingMiddleware
from app.images.routes import images as img_routes

load_dotenv()

APP_HOST = os.environ["APP_HOST"]
APP_PORT = int(os.environ["APP_PORT"])

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
# app = FastAPI(lifespan=lifespan, root_path="/api")

origins = [
    "http://ai.l4it.net",
    "https://ai.l4it.net",
    "https://ai.l4it.net/",
    "http://ai.l4it.net:4000",
    "https://ai.l4it.net:4000",
    "http://ai.l4it.net:8000",
    "https://ai.l4it.net:8000",
    "http://ai.l4it.net:5000",
    "https://ai.l4it.net:5000",
    "http://localhost:4000",
    "http://localhost:8000",
]

app.include_router(user_routes.router, prefix="/auth", tags=["auth"])
app.include_router(blog_routes.router, prefix="/blog", tags=["blog"])
app.include_router(msp_services_routes, prefix="/msp-services", tags=["msp-services"])
app.include_router(info_routes, prefix="/info", tags=["info"])
app.include_router(contact_router, prefix="/contact", tags=["contact"])
app.include_router(case_study_routes, prefix="/case-studies", tags=["case-studies"])
app.include_router(img_routes.router, prefix="/img", tags=["img"])

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
    uvicorn.run("app.main:app", host=APP_HOST, port=APP_PORT, reload=True)
