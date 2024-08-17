from flask import Flask, request, Response
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Obtener credenciales de Twilio desde las variables de entorno
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/sms', methods=['POST'])
def sms_reply():
    # Obtenemos el mensaje de texto enviado
    incoming_msg = request.form.get('Body')
    from_number = request.form.get('From')

    # Imprime el mensaje y el número del remitente en la consola
    print(f"Mensaje recibido de {from_number}: {incoming_msg}")

    # Responder al mensaje SMS (esto es opcional)
    resp = MessagingResponse()
    resp.message("Tu OTP ha sido recibido.")
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)

