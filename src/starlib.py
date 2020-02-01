import pandas as pd
import numpy as np
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def storesByCity(ciudad):
    ds = pd.read_csv("./input/starbucks.csv")

    print(ds[ds['City']==ciudad])
    return True

def sendMail(correo):
    message = Mail(
        from_email='sergio.gomis@gmail.com',
        to_emails='sergio.gomis@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)