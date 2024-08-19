import sys
import logging
from app import app as application  # Importa la aplicación Flask desde app.py

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

if __name__ == "__main__":
    application.run()
