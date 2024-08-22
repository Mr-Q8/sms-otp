import os

class Config:
    # Configuración básica
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    
    # Configuración de la base de datos
   

#class Config:
    #SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://u673267152_dmorales:Marisel-7@127.0.0.1/u673267152_dmoralesllc'
   # SQLALCHEMY_TRACK_MODIFICATIONS = False

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Usar una base de datos en memoria para pruebas
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# Definir qué configuración usar por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

