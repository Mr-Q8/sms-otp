from flask import Flask, request, Response
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import re

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Obtener credenciales de Twilio desde las variables de entorno
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/')
def index():
    return "La aplicación Flask está funcionando correctamente."

@app.route('/sms', methods=['POST'])
def sms_reply():
    # Obtenemos el mensaje de texto enviado
    incoming_msg = request.form.get('Body')
    from_number = request.form.get('From')

    # Imprime el mensaje y el número del remitente en la consola
    print(f"Mensaje recibido de {from_number}: {incoming_msg}")

    # Buscar un código OTP en el mensaje entrante (ejemplo: 6 dígitos numéricos)
    otp_match = re.search(r'\b\d{6}\b', incoming_msg)
    
    if otp_match:
        otp_code = otp_match.group(0)
        response_text = f"Hemos recibido tu código OTP: {otp_code}"
        # Muestra el OTP en la consola
        print(f"OTP detectado: {otp_code}")
    else:
        response_text = "No se encontró ningún código OTP en tu mensaje."
        print("No se encontró OTP en el mensaje.")

    # Responder al mensaje SMS con el resultado de la búsqueda de OTP
    resp = MessagingResponse()
    resp.message(response_text)
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)

