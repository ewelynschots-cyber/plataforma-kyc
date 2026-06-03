import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Inicializar SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configurar banco de dados
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Para Render (production)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Para desenvolvimento local
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plataforma_kyc.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensões
    db.init_app(app)
    CORS(app)
    
    # Registrar blueprints
    from src.app import api_bp
    app.register_blueprint(api_bp)
    
    # Criar tabelas
    with app.app_context():
        db.create_all()
    
    return app