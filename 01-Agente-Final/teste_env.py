import os
from dotenv import load_dotenv

# Caminho absoluto para o .env dentro da pasta do script
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")

print("Procurando .env em:", env_path)

load_dotenv(env_path)

print("GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))
