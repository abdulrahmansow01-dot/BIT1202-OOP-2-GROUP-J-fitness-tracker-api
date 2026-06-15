from contextlib import asynccontextmanager
import traceback
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import engine, async_session
from models import Base, User
from schemas import (
    Token,
    LoginRequest,
    UserCreate,
    UserRead,
    WorkoutCreate,
    WorkoutRead,
    WorkoutUpdate,
    NutritionEntryCreate,
    NutritionEntryRead,
    NutritionEntryUpdate,
    ProgressEntryCreate,
    ProgressEntryRead,
)
from auth import create_access_token, authenticate_user
from crud import (
    create_user,
    get_user_by_email,
    get_workouts_for_user,
    create_workout,
    get_workout_by_id,
    update_workout,
    delete_workout,
    get_nutrition_entries_for_user,
    create_nutrition_entry,
    get_nutrition_entry_by_id,
    update_nutrition_entry,
    delete_nutrition_entry,
    get_progress_entries_for_user,
    create_progress_entry,
)
from deps import get_db, get_current_active_user

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Fitness Tracker API", version="1.0.0", lifespan=lifespan)


@app.post("/users/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        existing = await get_user_by_email(db, user_in.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        user = await create_user(db, user_in)
        return user
    except HTTPException:
        raise
    except Exception as exc:
        log_path = Path("register_error.log")
        tb = traceback.format_exc()
        log_path.write_text(tb, encoding="utf-8")
        print(f"Registration error: {exc}")
        print(f"Traceback: {tb}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Registration failed: {str(exc)}") from exc


@app.post("/users/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    try:
        # form_data.username contains the email for this API
        user = await authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Incorrect email or password. Please ensure you're using form-data with 'username' (email) and 'password' fields.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as exc:
        log_path = Path("login_error.log")
        tb = traceback.format_exc()
        log_path.write_text(tb, encoding="utf-8")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from exc


@app.post("/users/login-json", response_model=Token, tags=["Authentication"])
async def login_with_json(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Alternative login endpoint that accepts JSON instead of form data.
    
    Send as JSON body:
    {
        "email": "user@example.com",
        "password": "password123"
    }
    """
    user = await authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/workouts", response_model=List[WorkoutRead])
async def list_workouts(current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await get_workouts_for_user(db, current_user.id)


@app.post("/workouts", response_model=WorkoutRead, status_code=status.HTTP_201_CREATED)
async def add_workout(workout_in: WorkoutCreate, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await create_workout(db, current_user.id, workout_in)


@app.get("/workouts/{workout_id}", response_model=WorkoutRead)
async def read_workout(workout_id: int, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    workout = await get_workout_by_id(db, workout_id, current_user.id)
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    return workout


@app.put("/workouts/{workout_id}", response_model=WorkoutRead)
async def edit_workout(workout_id: int, workout_in: WorkoutUpdate, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    workout = await update_workout(db, workout_id, current_user.id, workout_in)
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found or not owned by current user")
    return workout


@app.delete("/workouts/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_workout(workout_id: int, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    deleted = await delete_workout(db, workout_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found or not owned by current user")
    return None


@app.get("/nutrition", response_model=List[NutritionEntryRead])
async def list_nutrition_entries(current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await get_nutrition_entries_for_user(db, current_user.id)


@app.post("/nutrition", response_model=NutritionEntryRead, status_code=status.HTTP_201_CREATED)
async def add_nutrition_entry(entry_in: NutritionEntryCreate, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await create_nutrition_entry(db, current_user.id, entry_in)


@app.put("/nutrition/{nutrition_id}", response_model=NutritionEntryRead)
async def edit_nutrition_entry(nutrition_id: int, entry_in: NutritionEntryUpdate, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    entry = await update_nutrition_entry(db, nutrition_id, current_user.id, entry_in)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nutrition entry not found or not owned by current user")
    return entry


@app.delete("/nutrition/{nutrition_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_nutrition_entry(nutrition_id: int, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    deleted = await delete_nutrition_entry(db, nutrition_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nutrition entry not found or not owned by current user")
    return None


@app.get("/progress", response_model=List[ProgressEntryRead])
async def list_progress_entries(current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await get_progress_entries_for_user(db, current_user.id)


@app.post("/progress", response_model=ProgressEntryRead, status_code=status.HTTP_201_CREATED)
async def add_progress_entry(entry_in: ProgressEntryCreate, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await create_progress_entry(db, current_user.id, entry_in)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
