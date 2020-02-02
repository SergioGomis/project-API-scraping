import pandas as pd
import numpy as np
import os
#import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
from dotenv import load_dotenv
load_dotenv()
import re

def storesByCity(ciudad):
    ds = pd.read_csv("./input/starbucks.csv")

    print(ds[ds['City']==ciudad])
    return True

def sendMail(correo):
    pattern = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    #print(os.getcwd())
    if(re.search(pattern,correo)): 
        message = Mail(
            from_email='realender@gmail.com',
            to_emails=correo,
            subject='Sending with Twilio SendGrid is Fun',
            html_content='<strong>and easy to do anywhere, even with Python</strong>')
        file_path = './output/adjunto_prueba.txt'
        with open(file_path, 'r') as f:
            data = f.read()
            f.close()
        #encoded = base64.b64encode(data).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(data)
        attachment.file_type = FileType('txt')
        attachment.file_name = FileName('adjunto_prueba.txt')
        message.attachment = attachment
        try:
            token = os.getenv("SENDGRID_API_KEY")
            sg = SendGridAPIClient(token)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)
    else:
        print("El email no es correcto")