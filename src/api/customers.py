from flask_restx import Resource, fields, Namespace
from src.database import db

customers_ns = Namespace('customers', description='Operações de clientes')

customer_model = customers_ns.model('Customer', {
    'id': fields.Integer(readonly=True, description='O identificador único do cliente'),
    'name': fields.String(required=True, description='Nome do cliente'),
    'email': fields.String(required=True, description='Email do cliente'),
    'status': fields.String(required=True, description='Status do cliente')
})

@customers_ns.route('/')
class CustomerList(Resource):
    @customers_ns.marshal_list_with(customer_model)
    def get(self):
        """Lista todos os clientes"""
        return []

    @customers_ns.expect(customer_model)
    @customers_ns.marshal_with(customer_model, code=201)
    def post(self):
        """Cria um novo cliente"""
        return customers_ns.payload, 201

@customers_ns.route('/<int:id>')
@customers_ns.response(404, 'Cliente não encontrado')
@customers_ns.param('id', 'O identificador do cliente')
class Customer(Resource):
    @customers_ns.marshal_with(customer_model)
    def get(self, id):
        """Busca um cliente por ID"""
        return {'id': id, 'name': 'Exemplo', 'email': 'exemplo@email.com', 'status': 'ativo'}

    @customers_ns.expect(customer_model)
    @customers_ns.marshal_with(customer_model)
    def put(self, id):
        """Atualiza um cliente"""
        return customers_ns.payload

    @customers_ns.response(204, 'Cliente deletado')
    def delete(self, id):
        """Deleta um cliente"""
        return '', 204

customers_bp = customers_ns