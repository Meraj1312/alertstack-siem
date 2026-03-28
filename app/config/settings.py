import os
from pathlib import Path


class Settings:
    # ----------------------------
    # ENVIRONMENT
    # ----------------------------
    ENV: str = os.getenv("ENV", "development")

    # ----------------------------
    # DATABASE
    # ----------------------------
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DB_PATH: Path = Path(os.getenv("DB_PATH", BASE_DIR / "alertstack.db"))

    # ----------------------------
    # RISK ENGINE
    # ----------------------------
    POLICY_PATH: str = os.getenv(
        "POLICY_PATH",
        str(BASE_DIR / "app/risk/policy.json")
    )

    # ----------------------------
    # API DEFAULTS
    # ----------------------------
    DEFAULT_LIMIT: int = int(os.getenv("DEFAULT_LIMIT", 50))
    MAX_FETCH_LIMIT: int = int(os.getenv("MAX_FETCH_LIMIT", 10000))


# Singleton instance
settings = Settings()