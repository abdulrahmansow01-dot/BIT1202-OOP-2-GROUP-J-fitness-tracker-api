from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=8, example="password123")


class UserBase(BaseModel):
    full_name: str = Field(..., example="Alex Carter")
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, example="strong_password123")


class UserRead(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime

    class Config:
        from_attributes = True


class WorkoutBase(BaseModel):
    title: str = Field(..., example="Leg day")
    description: Optional[str] = Field(None, example="Squats, lunges, and deadlifts")
    date: Optional[datetime] = None
    duration_minutes: int = Field(..., example=45)
    calories_burned: int = Field(..., example=500)


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    calories_burned: Optional[int] = None


class WorkoutRead(WorkoutBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class NutritionEntryBase(BaseModel):
    meal_type: str = Field(..., example="Lunch")
    description: Optional[str] = Field(None, example="Grilled chicken salad")
    calories: int = Field(..., example=650)
    protein_grams: float = Field(..., example=45.0)
    carbohydrates_grams: float = Field(..., example=60.0)
    fats_grams: float = Field(..., example=22.0)
    date: Optional[datetime] = None


class NutritionEntryCreate(NutritionEntryBase):
    pass


class NutritionEntryUpdate(BaseModel):
    meal_type: Optional[str] = None
    description: Optional[str] = None
    calories: Optional[int] = None
    protein_grams: Optional[float] = None
    carbohydrates_grams: Optional[float] = None
    fats_grams: Optional[float] = None
    date: Optional[datetime] = None


class NutritionEntryRead(NutritionEntryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProgressEntryBase(BaseModel):
    weight_kg: float = Field(..., example=78.5)
    body_fat_percentage: Optional[float] = Field(None, example=18.2)
    notes: Optional[str] = Field(None, example="Felt strong on squats")
    date: Optional[datetime] = None


class ProgressEntryCreate(ProgressEntryBase):
    pass


class ProgressEntryRead(ProgressEntryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
