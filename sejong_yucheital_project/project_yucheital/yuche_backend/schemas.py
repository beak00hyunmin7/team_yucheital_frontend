from pydantic import BaseModel

class UserCreate(BaseModel): # 회원가입 요청으로 들어올 데이터 형태를 정의하는 클래스.
    email: str
    password: str


class UserResponse(BaseModel):
    # 회원가입 성공 후 응답으로 돌려줄 데이터 형태.
    id: int
    email: str

    class Config:
        from_attributes = True  # SQLAlchemy 객체 → Pydantic 객체로 변환 허용

class UserLogin(BaseModel): # 로그인 요청으로 들어올 데이터 형태를 정의하는 클래스
    email: str
    password: str