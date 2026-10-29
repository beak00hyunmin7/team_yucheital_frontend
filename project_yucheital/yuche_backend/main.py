from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
from schemas import UserCreate, UserResponse, UserLogin #schemas.py에서 함수? 가져오기
from auth import hash_password, verify_password #auth.py에서 함수? 가져오기
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI()

#CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발용, 모든 출처 허용
    allow_methods=["*"],
    allow_headers=["*"],
)

#회원가입
#post 요청 처리, 주소는 뒤에 /signup이 붙음, 
@app.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # 이미 같은 이메일로 가입된 사용자가 있는지를 확인
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if existing_user:
        # 이미 존재하면 에러 반환하기
        raise HTTPException(status_code=400, detail="User with this email already exists") 

    # 해싱한 값을 변수에 저장
    hashed_pw = hash_password(user.password)

    # 새 User 객체 (email은 요청받은 값, password는 해싱된 값)
    new_user = models.User(email=user.email, password=hashed_pw)

    db.add(new_user) # 저장 대기목록?에 올려라~
    db.commit() # 진짜로 db에 올려라~
    db.refresh(new_user) # db에 올린거 다시 정보 가져와라~ (commit하면 id값이 None이니깐 당연히..)

    return new_user

#로그인
#post 요청 처리, 주소는 뒤에 /login이 붙음
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    #이메일로 DB에서 사용자 조회하기
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    #사용자가 존재하지않으면?
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password") #에러메시지 던지기

    if not verify_password(user.password, db_user.password): #비밀번호 검증
        raise HTTPException(status_code=401, detail="Invalid email or password") #에러메시지 던지기

    return {"message": "Login successful"} #테스트용