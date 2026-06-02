from flask_restx import Resource, fields, Namespace
from src.database import db

kyc_processes_ns = Namespace('kyc-processes', description='Operações de processos KYC')

kyc_process_model = kyc_processes_ns.model('KYCProcess', {
    'id': fields.Integer(readonly=True, description='O identificador único do processo'),
    'customer_id': fields.Integer(required=True, description='ID do cliente associado'),
    'status': fields.String(required=True, description='Status do processo'),
    'risk_level': fields.String(required=True, description='Nível de risco'),
    'created_at': fields.String(description='Data de criação')
})

@kyc_processes_ns.route('/')
class KYCProcessList(Resource):
    @kyc_processes_ns.marshal_list_with(kyc_process_model)
    def get(self):
        """Lista todos os processos KYC"""
        return []

    @kyc_processes_ns.expect(kyc_process_model)
    @kyc_processes_ns.marshal_with(kyc_process_model, code=201)
    def post(self):
        """Cria um novo processo KYC"""
        return {}, 201

@kyc_processes_ns.route('/<int:id>')
@kyc_processes_ns.response(404, 'Processo não encontrado')
@kyc_processes_ns.param('id', 'O identificador do processo')
class KYCProcess(Resource):
    @kyc_processes_ns.marshal_with(kyc_process_model)
    def get(self, id):
        """Busca um processo por ID"""
        return {}

    @kyc_processes_ns.expect(kyc_process_model)
    @kyc_processes_ns.marshal_with(kyc_process_model)
    def put(self, id):
        """Atualiza um processo existente"""
        return {}

    @kyc_processes_ns.response(204, 'Processo deletado')
    def delete(self, id):
        """Deleta um processo"""
        return None, 204

kyc_processes_bp = kyc_processes_ns