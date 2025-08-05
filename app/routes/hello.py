from fastapi import APIRouter,HTTPException
from schema import UserRegister,UserLogin
from auth import hash_password,verify_password,create_access_token,decode_access_token
from database import fake_users_db
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/register")
def register(user: UserRegister):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash the password and save the user
    hashed_pw = hash_password(user.password)
    fake_users_db[user.username] = {
        "username": user.username,
        "password": hashed_pw
    }

    # Create JWT token after registration
    token = create_access_token({"sub": user.username})

    return {
        "msg": "User registered successfully",
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/login")
def login(form_data: OAuth2PasswordBearer = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid token")
    return {"msg": f"Welcome {username}, you are authenticated!"}
