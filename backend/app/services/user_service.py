from datetime import datetime
from typing import List, Optional
from passlib.context import CryptContext

# In-memory storage (like printers/jobs)
USERS: List[dict] = []
USER_ID_SEQ = 1

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_user(email: str, password: str) -> dict:
    """Create a new user with hashed password."""
    global USER_ID_SEQ
    
    # Check if user already exists
    if get_user_by_email(email):
        raise ValueError(f"User with email {email} already exists")
    
    user = {
        "id": USER_ID_SEQ,
        "email": email,
        "hashed_password": hash_password(password),
        "created_at": datetime.utcnow()
    }
    
    USERS.append(user)
    USER_ID_SEQ += 1
    
    return user


def authenticate_user(email: str, password: str) -> Optional[dict]:
    """Authenticate a user by email and password."""
    user = get_user_by_email(email)
    if not user:
        return None
    
    if not verify_password(password, user["hashed_password"]):
        return None
    
    # Return user without password hash
    return {
        "id": user["id"],
        "email": user["email"],
        "created_at": user["created_at"]
    }


def get_user_by_email(email: str) -> Optional[dict]:
    """Get a user by email."""
    for user in USERS:
        if user["email"] == email:
            return user
    return None


def get_user_by_id(user_id: int) -> Optional[dict]:
    """Get a user by ID."""
    for user in USERS:
        if user["id"] == user_id:
            return {
                "id": user["id"],
                "email": user["email"],
                "created_at": user["created_at"]
            }
    return None
