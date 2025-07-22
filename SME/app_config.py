# config.py

import os
from dotenv import load_dotenv

load_dotenv()

# Database config
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "sme_db")

# Folder paths
TEMPLATE_FOLDER = "templates_docs"
GENERATED_FOLDER = os.path.join("static", "generated_docs")
