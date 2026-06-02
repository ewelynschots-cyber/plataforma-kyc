"""
Pacote src da plataforma KYC
Inicializa a aplicação e extensões
"""

from flask_sqlalchemy import SQLAlchemy

# Inicializar db aqui para evitar circular imports
db = SQLAlchemy()