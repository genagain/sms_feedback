from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

from twilio.twiml.messaging_response import MessagingResponse, Message

app = Flask(__name__)
# TODO: create app based on environment specific configurations for dev, testing and production
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/sms_feedback_development'

db = SQLAlchemy(app)

class Feedback(db.Model):
    __table__name = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120))

    def __init__(self, content):
        self.content = content


# To suppress the warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Make this a POST route instead
@app.route('/')
def hello_monkey():
    """Respond to incoming texts with a simple text message and store said text in a database."""
    content = request.values.get('Body', None)
    feedback = Feedback(content)
    db.session.add(feedback)
    db.session.commit()
    resp = MessagingResponse()
    # TODO have a number of GIFs that are selected randomly for the media part
    msg = Message().body('Thank you for your feedback! - Gen').media('https://demo.twilio.com/owl.png')
    resp.append(msg)
    return str(resp)


if __name__ == '__main__':
  app.run(debug=True)
