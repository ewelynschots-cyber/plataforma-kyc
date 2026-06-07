import logging
from flask import request
from flask_restx import Namespace, Resource, fields
from src.services.address_alert_service import (
    check_address_duplicates,
    get_all_alerts,
    get_alerts_by_address,
    get_alerts_by_customer,
    delete_alert
)

logger = logging.getLogger(__name__)

api = Namespace('alerts', description='Operações relacionadas a alertas de endereço')

alert_model = api.model('Alert', {
    'id': fields.String(readOnly=True, description='ID do alerta'),
    'address': fields.String(required=True, description='Endereço do alerta'),
    'customer_id': fields.String(required=True, description='ID do cliente'),
    'created_at': fields.DateTime(description='Data de criação')
})

@api.route('')
class AlertList(Resource):
    @api.doc('list_alerts')
    @api.marshal_list_with(alert_model)
    def get(self):
        """Lista todos os alertas"""
        try:
            return get_all_alerts(), 200
        except Exception as e:
            logger.error(f"Erro ao listar alertas: {e}")
            api.abort(500, "Erro interno ao buscar alertas")

@api.route('/address/<string:address>')
class AlertByAddress(Resource):
    @api.doc('get_alerts_by_address')
    @api.marshal_list_with(alert_model)
    def get(self, address):
        """Filtra alertas por endereço"""
        try:
            return get_alerts_by_address(address), 200
        except Exception as e:
            logger.error(f"Erro ao buscar alertas por endereço {address}: {e}")
            api.abort(500, "Erro interno ao buscar alertas por endereço")

@api.route('/customer/<string:customer_id>')
class AlertByCustomer(Resource):
    @api.doc('get_alerts_by_customer')
    @api.marshal_list_with(alert_model)
    def get(self, customer_id):
        """Filtra alertas por cliente"""
        try:
            return get_alerts_by_customer(customer_id), 200
        except Exception as e:
            logger.error(f"Erro ao buscar alertas para o cliente {customer_id}: {e}")
            api.abort(500, "Erro interno ao buscar alertas por cliente")

@api.route('/<string:alert_id>')
class AlertDetail(Resource):
    @api.doc('delete_alert')
    def delete(self, alert_id):
        """Deleta um alerta pelo ID"""
        try:
            success = delete_alert(alert_id)
            if not success:
                api.abort(404, f"Alerta {alert_id} não encontrado")
            return {'message': 'Alerta deletado com sucesso'}, 200
        except Exception as e:
            logger.error(f"Erro ao deletar alerta {alert_id}: {e}")
            api.abort(500, "Erro interno ao deletar alerta")