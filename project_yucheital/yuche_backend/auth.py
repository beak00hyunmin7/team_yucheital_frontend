from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #bcrypt를 사용하여 비밀번호를 해싱하고 검증하는 데 사용되는 CryptContext 객체를 생성
#bcrypt는 salt를 이용해서 항상 다른 해시값이 나옴
def hash_password(plain_password: str) -> str: #주어진 평문 비밀번호를 해싱하여 반환하는 함수
    return pwd_context.hash(plain_password) 

def verify_password(plain_password: str, hashed_password: str) -> bool: #주어진 평문 비밀번호와 해시된 비밀번호를 비교하여 일치 여부를 반환하는 함수
    return pwd_context.verify(plain_password, hashed_password)