import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 기본값은 기존과 동일. 다른 PC/계정이면 서버 실행 전에 환경변수로만 바꾸면 된다.
#   PowerShell : $env:DB_PASSWORD = "비밀번호"
#   cmd        : set DB_PASSWORD=비밀번호
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "yuche_db")


SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal() #DB 세션 생성
    try:
        yield db
    finally:
        db.close()