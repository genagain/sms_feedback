import os
import re
import random
import sys
import logging
import requests
import json

from flask import Flask, render_template, request, send_file
from flask.ext.sqlalchemy import SQLAlchemy

from twilio.twiml.messaging_response import MessagingResponse, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)

if 'DYNO' in os.environ:
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)

# TODO make own models file without circular imports
class Feedback(db.Model):
    __table__name = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120))

    def __init__(self, content):
        self.content = content

gif_media_urls = [
    'https://media.giphy.com/media/xUA7aN1MTCZx97V1Ic/giphy.gif',
    'https://media.giphy.com/media/3o6EhHMGNWQW1WEt7q/giphy.gif',
    'https://media.giphy.com/media/3oz8xIsloV7zOmt81G/giphy.gif',
    'https://media.giphy.com/media/6tHy8UAbv3zgs/giphy.gif'
]

# To suppress the warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

@app.route('/')
def hello_monkey():
    """Respond to incoming texts with a simple text message and store said text in a database."""
    content = request.values.get('Body', None)
    feedback = Feedback(content)
    db.session.add(feedback)
    db.session.commit()
    api_key = os.environ['API_KEY']
    response = requests.get('http://api.giphy.com/v1/gifs/search?api_key={}&q=thankyou'.format(api_key))
    data_dict = json.loads(response.text)
    random_gifs =[ gif['url'] for gif in data_dict['data'] ]
    gif = random_gifs.pop()
    url_end = re.search(r'\/gifs\/.+$', gif).group()
    slug = url_end.replace('/gifs/', '')
    media_url = 'http://media.giphy.com/media/{}'.format(slug)
    random_media_url = random.choice(gif_media_urls)
    resp = MessagingResponse()
    msg = Message().body('Thank you for your feedback! - Gen').media(random_media_url)
    resp.append(msg)
    return str(resp)

@app.route('/gif')
def get_gif():
    gif_number = random.randint(1, 8)
    gif_filepath = 'static/thank_you_{}.gif'.format(gif_number)
    return send_file(gif_filepath, mimetype='image/gif')



if __name__ == '__main__':
  app.run(debug=True)
