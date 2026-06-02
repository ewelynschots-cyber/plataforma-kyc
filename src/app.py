from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from src.config import Config
from src.database import db
from src.api.customers import customers_ns
from src.api.kyc_processes import kyc_processes_ns

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)

    api = Api(
        app,
        title='Plataforma KYC API',
        version='1.0.0',
        description='API para gerenciamento de processos KYC',
        doc='/api/docs'
    )

    api.add_namespace(customers_ns, path='/customers')
    api.add_namespace(kyc_processes_ns, path='/kyc-processes')

    return app