from flask import Flask, render_template
from twilio.twiml.messaging_response import MessagingResponse, Message

app = Flask(__name__)

@app.route('/')
def hello_monkey():
    """Respond to incoming texts with a simple text message and store said text in a database."""
    resp = MessagingResponse()
    msg = Message().body("Hello, Mobile Monkey").media("https://demo.twilio.com/owl.png")
    resp.append(msg)
    return str(resp)


if __name__ == '__main__':
  app.run(debug=True)
