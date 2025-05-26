import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.auth.models.user import Base as AuthBase
from app.blog.models.blog import Base as BlogBase
from dotenv import load_dotenv
from app.core.base import Base

load_dotenv()

MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = urllib.parse.quote_plus(os.environ.get("MYSQL_PASSWORD", ""))
MYSQL_DB = os.environ.get("MYSQL_DB", "l4it_blog")
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_PORT = os.environ.get("MYSQL_PORT", "3306")

DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

engine = create_engine(
    DATABASE_URL, pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine) 