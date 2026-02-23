import uuid

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from auth import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_google_id_token,
    verify_password,
)
from database import get_db
from exceptions import AppException
from models.user import User
from schemas.user_schema import (
    GoogleLoginRequest,
    LoginResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def _register_user(user: UserCreate, db: Session) -> User:
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise AppException(
            status_code=409,
            code="EMAIL_ALREADY_EXISTS",
            message="A user with this email already exists.",
        )

    db_user = User(
        id=uuid.uuid4(),
        full_name=f"{user.first_name} {user.last_name}".strip(),
        email=user.email,
        password_hash=hash_password(user.password),
        phone=user.phone,
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as exc:
        db.rollback()
        raise AppException(
            status_code=409,
            code="USER_CONFLICT",
            message="Could not create user due to conflicting data.",
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise AppException(
            status_code=500,
            code="DATABASE_ERROR",
            message="Unable to create user right now.",
        ) from exc


def _build_auth_response(user: User) -> LoginResponse:
    token = create_access_token(
        subject=str(user.id),
        extra_claims={"email": user.email},
    )
    return LoginResponse(access_token=token, user=user)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise AppException(
            status_code=401,
            code="INVALID_TOKEN",
            message="Token is missing subject.",
        )
    try:
        user_uuid = uuid.UUID(str(user_id))
    except ValueError as exc:
        raise AppException(
            status_code=401,
            code="INVALID_TOKEN",
            message="Token subject is invalid.",
        ) from exc

    try:
        user = db.query(User).filter(User.id == user_uuid).first()
    except SQLAlchemyError as exc:
        raise AppException(
            status_code=500,
            code="DATABASE_ERROR",
            message="Unable to fetch user from token.",
        ) from exc

    if not user:
        raise AppException(
            status_code=401,
            code="USER_NOT_FOUND",
            message="User associated with token was not found.",
        )
    return user


@router.post("/register", response_model=LoginResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    created_user = _register_user(user, db)
    return _build_auth_response(created_user)


@router.post("/", response_model=LoginResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    created_user = _register_user(user, db)
    return _build_auth_response(created_user)


@router.post("/login", response_model=LoginResponse)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == payload.email).first()
    except SQLAlchemyError as exc:
        raise AppException(
            status_code=500,
            code="DATABASE_ERROR",
            message="Unable to process login right now.",
        ) from exc

    if not user or not verify_password(payload.password, user.password_hash):
        raise AppException(
            status_code=401,
            code="INVALID_CREDENTIALS",
            message="Invalid email or password.",
        )

    return _build_auth_response(user)


@router.post("/login/google", response_model=LoginResponse)
def login_with_google(payload: GoogleLoginRequest, db: Session = Depends(get_db)):
    google_payload = verify_google_id_token(payload.id_token)
    email = google_payload.get("email")
    google_sub = google_payload.get("sub")
    full_name = (google_payload.get("name") or "").strip()

    if not email or not google_sub:
        raise AppException(
            status_code=401,
            code="GOOGLE_TOKEN_INVALID",
            message="Google token is missing required identity fields.",
        )

    if not full_name:
        given_name = (google_payload.get("given_name") or "").strip()
        family_name = (google_payload.get("family_name") or "").strip()
        full_name = f"{given_name} {family_name}".strip() or email.split("@")[0]

    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            if not user.google_Id:
                user.google_Id = google_sub
                db.commit()
                db.refresh(user)
            return _build_auth_response(user)

        user = User(
            id=uuid.uuid4(),
            full_name=full_name,
            google_Id=google_sub,
            email=email,
            password_hash=hash_password(uuid.uuid4().hex),
            phone="",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return _build_auth_response(user)
    except IntegrityError as exc:
        db.rollback()
        raise AppException(
            status_code=409,
            code="USER_CONFLICT",
            message="Google account is already linked with another user.",
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise AppException(
            status_code=500,
            code="DATABASE_ERROR",
            message="Unable to process Google login right now.",
        ) from exc


@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    try:
        return db.query(User).all()
    except SQLAlchemyError as exc:
        raise AppException(
            status_code=500,
            code="DATABASE_ERROR",
            message="Unable to fetch users right now.",
        ) from exc


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
