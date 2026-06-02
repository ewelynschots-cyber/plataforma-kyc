"""
Configuração da aplicação Flask
Carrega variáveis de ambiente e define configurações por ambiente
"""

import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()


class Config:
    """Configuração base (aplicável a todos os ambientes)"""
    
    # Segurança
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    # Banco de Dados
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('DATABASE_ECHO', 'False') == 'True'
    
    # JWT (Autenticação)
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-dev-key-change-in-production')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', '24'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')


class DevelopmentConfig(Config):
    """Configuração para ambiente de desenvolvimento"""
    
    DEBUG = True
    TESTING = False
    
    # Banco de dados (SQLite para desenvolvimento local)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'sqlite:///kyc_dev.db'  # Cria arquivo local se não houver PostgreSQL
    )


class ProductionConfig(Config):
    """Configuração para ambiente de produção"""
    
    DEBUG = False
    TESTING = False
    
    # Banco de dados (PostgreSQL obrigatório em produção)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError(
            "DATABASE_URL não configurada em produção! "
            "Defina a variável de ambiente DATABASE_URL."
        )


class TestingConfig(Config):
    """Configuração para testes automatizados"""
    
    DEBUG = True
    TESTING = True
    
    # Banco de dados em memória para testes (rápido e isolado)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Dicionário com todas as configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """
    Retorna a configuração apropriada baseada no ambiente
    
    Args:
        env (str): Nome do ambiente ('development', 'production', 'testing')
        
    Returns:
        Config: Classe de configuração apropriada
    """
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    
    return config.get(env, config['default'])