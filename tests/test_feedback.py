import os
import re

from app.server import app
from app.server import Feedback

import pytest

os.environ['DATABASE_URL'] = 'postgres://localhost/sms_feedback_test'

def test_thank_you():
    test_client = app.test_client()
    # TODO: change the test for a random URL in the Media tags
    expected_response = r"<\?xml version=\"1.0\" encoding=\"UTF-8\"\?><Response><Message><Body>Thank you for your feedback! - Gen</Body><Media>https://giphy.com/gifs/.*</Media></Message></Response>"
    response = test_client.get('/',data={'Body':'fjklafd'})
    assert re.match(expected_response, response.data)
    
# TODO: test for feedback in database
def test_feedback_db():
    test_client = app.test_client()
    expected_feedback_content = 'It was dope food'
    response = test_client.get('/', data={'Body':'It was dope food'})
    # TODO change this to getting just one feedback in query
    stored_feedback = Feedback.query.filter_by(content='It was dope food').first()
    stored_content = stored_feedback.content
    assert expected_feedback_content == stored_content
