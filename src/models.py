from src import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class KYCProcess(db.Model):
    __tablename__ = 'kyc_processes'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, approved, rejected
    document_type = db.Column(db.String(50))  # CPF, CNPJ, RG, etc
    document_number = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    customer = db.relationship('Customer', backref='kyc_processes')
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'status': self.status,
            'document_type': self.document_type,
            'document_number': self.document_number,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON

class AddressAlert(db.Model):
    """
    Modelo para armazenar alertas de endereços com múltiplos clientes associados.
    """
    __tablename__ = 'address_alerts'

    # Identificador único do alerta
    id = Column(Integer, primary_key=True)
    
    # Endereço para monitoramento, indexado para otimizar consultas de busca
    address = Column(String(255), nullable=False, index=True)
    
    # Contador de clientes vinculados a este endereço
    customer_count = Column(Integer, default=0)
    
    # Nível de risco associado ao endereço (LOW, MEDIUM, HIGH)
    risk_level = Column(String(20), default='LOW')
    
    # Lista de IDs de clientes que compartilham o mesmo endereço
    duplicate_customer_ids = Column(JSON, nullable=True)
    
    # Timestamps de criação e atualização automática
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Retorna uma representação em dicionário do objeto."""
        return {
            'id': self.id,
            'address': self.address,
            'customer_count': self.customer_count,
            'risk_level': self.risk_level,
            'duplicate_customer_ids': self.duplicate_customer_ids,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        """Representação para debug."""
        return f'<AddressAlert {self.address} (Risk: {self.risk_level})>'