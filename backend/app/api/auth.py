from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserLogin, User, Token
from app.services.user_service import create_user, authenticate_user
from app.core.security import create_access_token, get_current_user

router = APIRouter()


@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate):
    """Register a new user."""
    try:
        user = create_user(user_data.email, user_data.password)
        return {
            "id": user["id"],
            "email": user["email"],
            "created_at": user["created_at"]
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/signin", response_model=Token)
def signin(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signin-json", response_model=Token)
def signin_json(credentials: UserLogin):
    """Login with JSON body (alternative to form data)."""
    user = authenticate_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user information."""
    return current_user
