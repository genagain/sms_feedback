import os
import random

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

from twilio.twiml.messaging_response import MessagingResponse, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)

gif_urls = [
    'https://giphy.com/gifs/3oz8xIsloV7zOmt81G',
    'https://giphy.com/gifs/TlK63EXvLD0en57UJDa',
    'https://giphy.com/gifs/IcGkqdUmYLFGE',
    'https://giphy.com/gifs/26FPOogenQv5eOZHO'
]

# TODO make own models file without circular imports
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
    random_gif = random.choice(gif_urls)
    content = request.values.get('Body', None)
    feedback = Feedback(content)
    db.session.add(feedback)
    db.session.commit()
    resp = MessagingResponse()
    msg = Message().body('Thank you for your feedback! - Gen').media(random_gif)
    resp.append(msg)
    return str(resp)


if __name__ == '__main__':
  app.run(debug=True)
