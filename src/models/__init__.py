"""
Modelos de dados da plataforma KYC
Importa todos os modelos para facilitar o acesso
"""

from src.models.user import User, Role
from src.models.customer import Customer, CustomerType, RiskLevel, Status
from src.models.kyc_process import KycProcess, KycStatus

__all__ = [
    'User', 'Role',
    'Customer', 'CustomerType', 'RiskLevel', 'Status',
    'KycProcess', 'KycStatus'
]