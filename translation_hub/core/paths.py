from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent

CONFIG_FILE = Path.home() / "TranslateHubConfig.json"
ENV_FILE = PROJECT_DIR / ".env"
