# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]
import qrcode # allow make qrCode
import unittest
import stripe
import logging

from flask import Flask
from flask import request, make_response, redirect, session, url_for
from flask import render_template 
from flask import jsonify

from app import create_app

from app.common_functions import generarQR
from app.firestore_service import get_reservation, put_reservation, put_customer_into_reservation

app = create_app()

stripe.api_key = "sk_test_51IcKJFHn1TLFiHT2Z1W5PRfz8PxzdDigtAqyFaY2zcbmUB1RQ1z4M0c1dzwvWwFIskNQBboBfU5QbkLA0qYPlC6Q00xmL9uwpJ"

app = Flask(__name__)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


@app.route('/')
def index():
    # user__ip = request.remote_addr
    # session['user__ip'] = user__ip
    # response = make_response(redirect('/auth/login'))
    response = render_template('index.html')
    return response


@app.route('/masajes')
def masajes():
    return render_template('masajes.html')
    

@app.route('/kuoPartner')
def kuoPartner():
    return render_template('kuoPartner.html')
    

@app.route('/seleccion')
def seleccion():
    return render_template('seleccion.html')


@app.route('/unresolved')
def unresolved():
    return render_template('p.html')


@app.route('/reserva', methods=['GET','POST'])
def reserva():
    if request.method == 'POST':
        reservation__data   = {}
        formData            = request.form
        print(formData.to_dict())

        reservation = put_reservation(formData)
        print('reservation.id: ', reservation.id)
        # return redirect(url_for('pago', reservation=reservation.id))
        # return make_response(redirect('/pago', reservation=reservation.id))
        return redirect(url_for('datos', reservation=reservation.id))
    else:
        return render_template('reserva.html')


@app.route('/datos/<reservation>', methods=['POST','GET'])
def datos(reservation):
    if request.method == 'POST':
        reservation__data   = {}
        formData            = request.form.to_dict()
        print(formData)
        
        try:
            put_customer_into_reservation(reservation,formData)
            return redirect(url_for('pago', reservation=reservation.id))
        except Exception as e:
            print(type(e))
            print(e.args)
            print(e)          
        
            return redirect(url_for('datos', reservation=reservation.id))
    else:
        reservation__bd = get_reservation(reservation)
        price_id        = reservation__bd.to_dict()['products']
        print('price_id: ', price_id)

        price__strip = calculate_order_amount(price_id)
        print('price: ', price__strip)
        
        context = {
            'reservation'   :  reservation__bd,
            'price'         :  price__strip,
        }
        return render_template('datos.html', **context)


@app.route('/pago/<reservation>', methods=['POST','GET'])
def pago(reservation):
    print('reservation', reservation)
    context = {}

    if request.method == 'POST':
        print('POST')
        print('request.data', request.data)
        
        try:
            data = json.loads(request.data)
            print(data)
            
            intent = stripe.PaymentIntent.create(
                amount=calculate_order_amount(reservation),
                currency='usd'
            )

            return jsonify({
            'clientSecret': intent['client_secret']
            })
        except Exception as e:
            print(type(e))    # the exception instance
            print(e.args)     # arguments stored in .args
            print(e)          # __str__ allows args to be printed directly,
                            # but may be overridden in exception subclasses
            return jsonify(error=str(e)), 403


        # si todo resulta bien no deberia ir a pago sino a confirmacion.html
        return render_template('pago.html')


    else:
        print('GET')
        print(reservation)
        
        
        
        

        # context = {
        #     'reservation':  reservation__bd,
        #     'amount'    :   price__strip['unit_amount_decimal'],
        #     'currency'  :   price__strip['currency'],
        # }
        
        # comprobar el estado a pagar de la reserva
        # comprobar el price en stripe porque será necesario
        # comprobar el precio final para poder colocarselo por javascript

        return render_template('checkout.html',**context)


@app.route('/confirmacion/<reservation>', methods=['POST','GET'])
def confirmacion(reservation):
    reservation__bd = get_reservation(reservation)
    reservation__bd = reservation__bd.to_dict()
    
    date            = reservation__bd['date']
    hour            = reservation__bd['hour']
    address         = reservation__bd['address']
    customer_name   = reservation__bd['customer']
    customer_phone  = ""    ##reservation__bd['customer_phone']
    customer_email  = ""    ##reservation__bd['customer_email']
    context = {
        'reservation'   :  reservation__bd,
        'date'          :  date,
        'hour'          :  hour,
        'address'       :  address,
        'customer_name' :  customer_name,
        'customer_phone':  customer_phone,
        'customer_email':  customer_email,
    }
    return render_template('confirmacion.html',**context)


@app.route('/registro')
def registro():
    context = {}
    return render_template('registro.html',**context)


@app.route('/iniciarSesion')
def iniciarSesion():
    context = {}
    return render_template('iniciarSesion.html',**context)


"""
it is use in create_payment()
"""
def calculate_order_amount(price_id):
    # buscar API Stripe para buscar amount
    try:
        price = stripe.Price.retrieve(price_id)
    except Exception as e:
        print(e)
        price = {}
    # print(price)
    # print(price['unit_amount_decimal'])
    # print(price['currency'])

    return price


@app.route('/api/create-payment-intent', methods=['POST'])
def create_payment():
    """
        Procedure to checkout
        http://domain.com/api/create-payment-intent
    """
    try:
        data = json.loads(request.data)
        print(data)
        
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='usd'
        )

        return jsonify({
          'clientSecret': intent['client_secret']
        })
    except Exception as e:
        print(type(e))    # the exception instance
        print(e.args)     # arguments stored in .args
        print(e)          # __str__ allows args to be printed directly,
                          # but may be overridden in exception subclasses
        return jsonify(error=str(e)), 403


@app.route('/api/sandboxReset', methods=['GET'])
def sandboxReset():
    try:
        return {'message': 'Done' },200
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,
                             # but may be overridden in exception subclasses
        return {'message': 'Error importing or exporting data'},400


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]
