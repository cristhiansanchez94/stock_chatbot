from flask import Flask, request
from twilio.rest import Client
from marketstack import get_stock_price
import os 


app = Flask(__name__)

ACCOUNT_ID = os.environ.get('tw_account')
TOKEN = os.environ.get('tw_token')
TWILIO_NUMBER='whatsapp:+14155238886'
tw_client = Client(ACCOUNT_ID, TOKEN)

def process_msg(msg): 
    response = ""
    if msg == "hola mi prro": 
        response ='Qué se cuenta. Escoger el ticker:'
        response+='Escribir sym:ticker'
    elif 'sym' in msg: 
        stock_symbol = msg.split(':')[-1]
        stock_price = get_stock_price(stock_symbol)
        last_price_str = str(stock_price['last_price'])
        response = f"El precio de {stock_symbol} es ${last_price_str}"
    else: 
        response = 'Escribir hola mi prro'
    return response

def send_msg(msg, recipient):
    tw_client.messages.create(from_=TWILIO_NUMBER,
                             body=msg, 
                             to=recipient)
    

@app.route("/webhook", methods=["POST"])
def webhook():
    form = request.form
    msg = form['Body']
    sender = form['From']
    response = process_msg(msg)
    send_msg(response,sender)
    return "OK", 200
