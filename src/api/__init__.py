"""
API Blueprint para a plataforma KYC
Importa todos os blueprints para facilitar o registro
"""

from src.api.customers import customers_bp
from src.api.kyc_processes import kyc_processes_bp

__all__ = ['customers_bp', 'kyc_processes_bp']