from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class Env:
    PORT = int(os.getenv("PORT", default=5000))
    DEBUG: bool = os.getenv("DEBUG", default=False)
    HOST: str = os.getenv("HOST", default="localhost")
