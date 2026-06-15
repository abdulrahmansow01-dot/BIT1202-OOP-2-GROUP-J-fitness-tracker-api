from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, Workout, NutritionEntry, ProgressEntry
from schemas import UserCreate, WorkoutCreate, WorkoutUpdate, NutritionEntryCreate, NutritionEntryUpdate, ProgressEntryCreate


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    from auth import get_password_hash

    hashed_password = get_password_hash(user_in.password)
    user = User(full_name=user_in.full_name, email=user_in.email, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def get_workouts_for_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(Workout).where(Workout.owner_id == user_id).order_by(Workout.date.desc()))
    return result.scalars().all()


async def create_workout(db: AsyncSession, user_id: int, workout_in: WorkoutCreate) -> Workout:
    workout = Workout(owner_id=user_id, **workout_in.dict(exclude_unset=True))
    db.add(workout)
    await db.commit()
    await db.refresh(workout)
    return workout


async def get_workout_by_id(db: AsyncSession, workout_id: int, user_id: int):
    result = await db.execute(select(Workout).where(Workout.id == workout_id, Workout.owner_id == user_id))
    return result.scalars().first()


async def update_workout(db: AsyncSession, workout_id: int, user_id: int, workout_in: WorkoutUpdate):
    stmt = (
        update(Workout)
        .where(Workout.id == workout_id, Workout.owner_id == user_id)
        .values(**workout_in.dict(exclude_unset=True))
        .execution_options(synchronize_session="fetch")
        .returning(Workout)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalars().first()


async def delete_workout(db: AsyncSession, workout_id: int, user_id: int) -> bool:
    stmt = delete(Workout).where(Workout.id == workout_id, Workout.owner_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def get_nutrition_entries_for_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(NutritionEntry).where(NutritionEntry.owner_id == user_id).order_by(NutritionEntry.date.desc()))
    return result.scalars().all()


async def create_nutrition_entry(db: AsyncSession, user_id: int, entry_in: NutritionEntryCreate) -> NutritionEntry:
    entry = NutritionEntry(owner_id=user_id, **entry_in.dict(exclude_unset=True))
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry


async def get_nutrition_entry_by_id(db: AsyncSession, nutrition_id: int, user_id: int):
    result = await db.execute(select(NutritionEntry).where(NutritionEntry.id == nutrition_id, NutritionEntry.owner_id == user_id))
    return result.scalars().first()


async def update_nutrition_entry(db: AsyncSession, nutrition_id: int, user_id: int, entry_in: NutritionEntryUpdate):
    stmt = (
        update(NutritionEntry)
        .where(NutritionEntry.id == nutrition_id, NutritionEntry.owner_id == user_id)
        .values(**entry_in.dict(exclude_unset=True))
        .execution_options(synchronize_session="fetch")
        .returning(NutritionEntry)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalars().first()


async def delete_nutrition_entry(db: AsyncSession, nutrition_id: int, user_id: int) -> bool:
    stmt = delete(NutritionEntry).where(NutritionEntry.id == nutrition_id, NutritionEntry.owner_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def get_progress_entries_for_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(ProgressEntry).where(ProgressEntry.owner_id == user_id).order_by(ProgressEntry.date.desc()))
    return result.scalars().all()


async def create_progress_entry(db: AsyncSession, user_id: int, entry_in: ProgressEntryCreate) -> ProgressEntry:
    entry = ProgressEntry(owner_id=user_id, **entry_in.dict(exclude_unset=True))
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry
