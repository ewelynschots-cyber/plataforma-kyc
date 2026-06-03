from flask import request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from src import db
from src.models import Customer, KYCProcess

# Criar namespace
api_ns = Namespace('api', description='KYC Platform API')

# Definir modelos Swagger
customer_model = api_ns.model('Customer', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'email': fields.String(required=True),
    'phone': fields.String(),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True)
})

kyc_model = api_ns.model('KYCProcess', {
    'id': fields.Integer(readonly=True),
    'customer_id': fields.Integer(required=True),
    'status': fields.String(required=True),
    'document_type': fields.String(),
    'document_number': fields.String(),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True)
})

# ============ CUSTOMERS ============

@api_ns.route('/customers')
class CustomerList(Resource):
    @api_ns.doc('list_customers')
    def get(self):
        """Listar todos os clientes"""
        customers = Customer.query.all()
        return {'customers': [c.to_dict() for c in customers]}, 200
    
    @api_ns.expect(customer_model)
    @api_ns.marshal_with(customer_model, code=201)
    def post(self):
        """Criar novo cliente"""
        data = request.get_json()
        
        # Validar email único
        if Customer.query.filter_by(email=data['email']).first():
            return {'error': 'Email já existe'}, 400
        
        customer = Customer(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone')
        )
        db.session.add(customer)
        db.session.commit()
        return customer.to_dict(), 201

@api_ns.route('/customers/<int:id>')
class CustomerDetail(Resource):
    @api_ns.doc('get_customer')
    def get(self, id):
        """Obter cliente por ID"""
        customer = Customer.query.get_or_404(id)
        return customer.to_dict(), 200
    
    @api_ns.expect(customer_model)
    def put(self, id):
        """Atualizar cliente"""
        customer = Customer.query.get_or_404(id)
        data = request.get_json()
        
        customer.name = data.get('name', customer.name)
        customer.email = data.get('email', customer.email)
        customer.phone = data.get('phone', customer.phone)
        
        db.session.commit()
        return customer.to_dict(), 200
    
    def delete(self, id):
        """Deletar cliente"""
        customer = Customer.query.get_or_404(id)
        db.session.delete(customer)
        db.session.commit()
        return {'message': 'Cliente deletado'}, 200

# ============ KYC PROCESSES ============

@api_ns.route('/kyc-processes')
class KYCProcessList(Resource):
    @api_ns.doc('list_kyc_processes')
    def get(self):
        """Listar todos os processos KYC"""
        processes = KYCProcess.query.all()
        return {'kyc_processes': [p.to_dict() for p in processes]}, 200
    
    @api_ns.expect(kyc_model)
    @api_ns.marshal_with(kyc_model, code=201)
    def post(self):
        """Criar novo processo KYC"""
        data = request.get_json()
        
        # Validar se cliente existe
        customer = Customer.query.get(data['customer_id'])
        if not customer:
            return {'error': 'Cliente não encontrado'}, 404
        
        kyc = KYCProcess(
            customer_id=data['customer_id'],
            status=data.get('status', 'pending'),
            document_type=data.get('document_type'),
            document_number=data.get('document_number')
        )
        db.session.add(kyc)
        db.session.commit()
        return kyc.to_dict(), 201

@api_ns.route('/kyc-processes/<int:id>')
class KYCProcessDetail(Resource):
    @api_ns.doc('get_kyc_process')
    def get(self, id):
        """Obter processo KYC por ID"""
        kyc = KYCProcess.query.get_or_404(id)
        return kyc.to_dict(), 200
    
    @api_ns.expect(kyc_model)
    def put(self, id):
        """Atualizar processo KYC"""
        kyc = KYCProcess.query.get_or_404(id)
        data = request.get_json()
        
        kyc.status = data.get('status', kyc.status)
        kyc.document_type = data.get('document_type', kyc.document_type)
        kyc.document_number = data.get('document_number', kyc.document_number)
        
        db.session.commit()
        return kyc.to_dict(), 200
    
    def delete(self, id):
        """Deletar processo KYC"""
        kyc = KYCProcess.query.get_or_404(id)
        db.session.delete(kyc)
        db.session.commit()
        return {'message': 'Processo KYC deletado'}, 200

# Criar blueprint
from flask import Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Registrar API
api = Api(api_bp, version='1.0.0', title='Plataforma KYC API',
          description='API para gerenciamento de processos KYC')
api.add_namespace(api_ns)