#/src/views/Payment.py
import os
import paypalrestsdk
from flask import Flask, request, g, Blueprint, json, Response
from ..models.UserModel import UserModel, UserSchema
from ..shared.Authentication import Auth

app = Flask(__name__)
payment_api = Blueprint('payment_api', __name__)
user_schema = UserSchema()
env_name = os.getenv('FLASK_ENV')
pp_mode="live"
if env_name == 'development':
    pp_mode="sandbox"

paypalrestsdk.configure({
  "mode": pp_mode,
  "client_id": os.getenv('PAYPAL_ID'),
  "client_secret": os.getenv('PAYPAL_SECRET') 
})


@payment_api.route('/paypal/create', methods=['POST'])
@Auth.auth_required
def paypal_create():
    """
    Create Paypal payment
    """
    req_data = request.get_json()
    app.logger.info('llega siquiera blog--------------#'+json.dumps(req_data))
    quantity = req_data['quantity']

    if quantity < 1 :
        return custom_response('Quantity must be greater tnan zero.', 400)
    total = 99 * quantity
    app.logger.info('TOTAL DSE LA CUENTA#-------------'+str(total))
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:5000/api/v1/payment/paypal/execute",
            "cancel_url": "http://localhost:5000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Documento PDF a firma",
                    "sku": "MIFIEL_PDF_01",
                    "price": "99",
                    "currency": "MXN",
                    "quantity": quantity}]},
            "amount": {
                "total": total,
                "currency": "MXN"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        app.logger.info('Payment success!')
    else:
        app.logger.error(payment.error)

    return custom_response({'paymentID' : payment.id},200)

@payment_api.route('/paypal/execute', methods=['POST'])
@Auth.auth_required
def paypal_execute():
    req_data = request.get_json()
    quantity = req_data['quantity']
    app.logger.info('llega siquiera al execute--------------# '+str(quantity))
    success = False
    payment = paypalrestsdk.Payment.find(req_data['paymentID'])
    
    if payment.execute({'payer_id' : req_data['payerID']}):
        app.logger.info('Execute success!')
        success = True
        payer = UserModel.get_one_user(g.user.get('id'))
        payer.items_paid += quantity
        payer.save()
    else:
        app.logger.error(payment.error)
    return custom_response({'success' : success},200)

def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )