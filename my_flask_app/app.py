from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

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
