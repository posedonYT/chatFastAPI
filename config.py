import os

from dotenv import load_dotenv

load_dotenv()
DataBase_URL = os.getenv('DATABASE_URL')
print(f"url={DataBase_URL}")
