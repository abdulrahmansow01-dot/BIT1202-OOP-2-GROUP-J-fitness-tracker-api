from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    workouts = relationship("Workout", back_populates="owner", cascade="all, delete-orphan")
    nutrition_entries = relationship("NutritionEntry", back_populates="owner", cascade="all, delete-orphan")
    progress_entries = relationship("ProgressEntry", back_populates="owner", cascade="all, delete-orphan")


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    calories_burned = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    owner = relationship("User", back_populates="workouts")


class NutritionEntry(Base):
    __tablename__ = "nutrition_entries"

    id = Column(Integer, primary_key=True, index=True)
    meal_type = Column(String(60), nullable=False)
    description = Column(Text, nullable=True)
    calories = Column(Integer, nullable=False)
    protein_grams = Column(Float, nullable=False)
    carbohydrates_grams = Column(Float, nullable=False)
    fats_grams = Column(Float, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    owner = relationship("User", back_populates="nutrition_entries")


class ProgressEntry(Base):
    __tablename__ = "progress_entries"

    id = Column(Integer, primary_key=True, index=True)
    weight_kg = Column(Float, nullable=False)
    body_fat_percentage = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    owner = relationship("User", back_populates="progress_entries")
