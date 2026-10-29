from sqlalchemy import Column, Integer, String
from database import Base #database.py에서 Base를 가져옴

class User(Base):
    __tablename__ = "users" # 테이블 이름 지정하기

    id = Column(Integer, primary_key=True, index=True) # id 정수형
    email = Column(String(255), unique=True, index=True, nullable=False) # email은 문자열로
    password = Column(String(255), nullable=False) # password도 문자열로