from flask import Flask, render_template, request
from twilio.twiml.messaging_response import MessagingResponse, Message

app = Flask(__name__)

@app.route('/')
def hello_monkey():
    """Respond to incoming texts with a simple text message and store said text in a database."""
    body = request.values.get('Body', None).lower()
    resp = MessagingResponse()
    # TODO have a number of GIFs that are selected randomly for the media part
    msg = Message().body('Thank you for your feedback! - Gen').media("https://demo.twilio.com/owl.png")
    resp.append(msg)
    return str(resp)


if __name__ == '__main__':
  app.run(debug=True)
