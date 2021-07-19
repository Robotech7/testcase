from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    template_folder = Path(BASE_DIR / "templates")
