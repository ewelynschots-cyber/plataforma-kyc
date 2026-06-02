from src.app import db
from enum import Enum

class KycStatus(Enum):
    INICIADO = 'iniciado'
    EM_ANALISE = 'em_analise'
    APROVADO = 'aprovado'
    REJEITADO = 'rejeitado'

class KycProcess(db.Model):
    __tablename__ = 'kyc_processes'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    status = db.Column(db.Enum(KycStatus), nullable=False, default=KycStatus.INICIADO)
    risk_assessment = db.Column(db.String(50), nullable=True)
    documents_submitted = db.Column(db.JSON, nullable=True)
    analyst_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    completed_at = db.Column(db.DateTime, nullable=True)

    customer = db.relationship('Customer', backref=db.backref('kyc_processes', lazy=True))
    analyst = db.relationship('User', backref=db.backref('kyc_processes', lazy=True))

    def __repr__(self):
        return f'<KycProcess {self.id} - Customer {self.customer_id} - Status {self.status.value}>'