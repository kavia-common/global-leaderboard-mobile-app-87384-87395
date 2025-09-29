import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()


@dataclass
class Config:
    """Application configuration loaded from environment variables."""

    # PUBLIC_INTERFACE
    def as_flask_config(self) -> dict:
        """Return a dict suitable for Flask app.config update."""
        return {
            "SQLALCHEMY_DATABASE_URI": self.SQLALCHEMY_DATABASE_URI,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "API_TITLE": self.API_TITLE,
            "API_VERSION": self.API_VERSION,
            "OPENAPI_VERSION": "3.0.3",
            "OPENAPI_URL_PREFIX": "/docs",
            "OPENAPI_SWAGGER_UI_PATH": "",
            "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
        }

    MYSQL_URL: str = os.getenv("MYSQL_URL", "")
    MYSQL_USER: str = os.getenv("MYSQL_USER", "appuser")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "dbuser123")
    MYSQL_DB: str = os.getenv("MYSQL_DB", "myapp")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT", "5000")
    API_TITLE: str = os.getenv("API_TITLE", "Game Leaderboard API")
    API_VERSION: str = os.getenv("API_VERSION", "v1")

    # Construct SQLAlchemy URI if MYSQL_URL not directly provided
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.MYSQL_URL:
            # Accept full DSN if provided (e.g., mysql+pymysql://user:pass@host:port/db)
            # If scheme is missing driver, add pymysql
            if self.MYSQL_URL.startswith("mysql://"):
                return self.MYSQL_URL.replace("mysql://", "mysql+pymysql://", 1)
            return self.MYSQL_URL
        # default: localhost with env vars
        user = self.MYSQL_USER
        pwd = self.MYSQL_PASSWORD
        host = "127.0.0.1"
        port = self.MYSQL_PORT
        db = self.MYSQL_DB
        return f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}?charset=utf8mb4"
