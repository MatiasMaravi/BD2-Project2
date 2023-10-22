from flask import Flask

app = Flask(__name__)



# Importa las rutas después de crear la aplicación
from app import routes