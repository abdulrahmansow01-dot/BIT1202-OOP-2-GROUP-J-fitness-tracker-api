import os
from pathlib import Path


def load_dotenv(dotenv_path: Path | str = None) -> None:
    path = Path(dotenv_path or Path(".env"))
    if not path.is_file():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


load_dotenv()


class Settings:
    secret_key: str = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY_CHANGE_ME")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/fitness_tracker",
    )
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


settings = Settings()
