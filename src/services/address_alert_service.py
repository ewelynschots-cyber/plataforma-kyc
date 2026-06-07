import logging
import os
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from src import db
from src.models import Customer

logger = logging.getLogger(__name__)

class AddressAlert(db.Model):
    __tablename__ = 'address_alerts'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    address = Column(String(255), nullable=False)
    customer_count = Column(Integer, default=0)
    risk_level = Column(String(20), nullable=False)
    duplicate_customer_ids = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

MAX_CUSTOMERS_PER_ADDRESS = int(os.getenv('MAX_CUSTOMERS_PER_ADDRESS', 5))

def check_address_duplicates(address, exclude_customer_id=None):
    """Verifica se existem múltiplos clientes no mesmo endereço."""
    try:
        query = db.session.query(Customer).filter(Customer.address == address)
        if exclude_customer_id:
            query = query.filter(Customer.id != exclude_customer_id)
        return query.count() > 0
    except Exception as e:
        logger.error(f"Erro ao verificar duplicatas de endereço {address}: {e}")
        return False

def get_duplicate_customers(address, exclude_customer_id=None):
    """Retorna lista de IDs de clientes associados ao mesmo endereço."""
    try:
        query = db.session.query(Customer.id).filter(Customer.address == address)
        if exclude_customer_id:
            query = query.filter(Customer.id != exclude_customer_id)
        return [c.id for c in query.all()]
    except Exception as e:
        logger.error(f"Erro ao buscar IDs duplicados para {address}: {e}")
        return []

def calculate_risk_level(customer_count):
    """Calcula o nível de risco baseado na contagem de clientes."""
    if customer_count >= MAX_CUSTOMERS_PER_ADDRESS * 2:
        return "HIGH"
    elif customer_count >= MAX_CUSTOMERS_PER_ADDRESS:
        return "MEDIUM"
    return "LOW"

def create_alert(customer_id, risk_level, address=None):
    """Cria um novo registro de alerta de endereço."""
    try:
        alert = AddressAlert(
            customer_id=customer_id,
            address=address,
            risk_level=risk_level,
            created_at=datetime.utcnow()
        )
        db.session.add(alert)
        db.session.commit()
        logger.info(f"Alerta criado para o cliente {customer_id} com risco {risk_level}")
        return alert
    except Exception as e:
        db.session.rollback()
        logger.error(f"Falha ao criar alerta para cliente {customer_id}: {e}")
        raise