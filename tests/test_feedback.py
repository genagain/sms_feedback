from sms_feedback.app.server import app
import pytest

def test_feedback():
    test_client = app.test_client()
    # TODO: change the test for a random URL in the Media tags
    expected_response = u'<?xml version="1.0" encoding="UTF-8"?><Response><Message><Body>Thank you for your feedback! - Gen</Body><Media>https://demo.twilio.com/owl.png</Media></Message></Response>'
    response = test_client.get('/',data={'Body':'fjklafd'})
    assert expected_response == response.data
    
