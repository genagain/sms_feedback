from flask import Flask, render_template
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/')
def hello_monkey():
    """Respond to incoming texts with a simple text message and store said text in a database."""

    resp = MessagingResponse()
    resp.message("Hello, Mobile Monkey")
    return str(resp)


if __name__ == '__main__':
  app.run(debug=True)
