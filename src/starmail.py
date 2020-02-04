import pandas as pd
import numpy as np
import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
from dotenv import load_dotenv
load_dotenv()
import re
from fpdf import FPDF
import requests



def sendMail(correo,ciudad):
    pattern = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    #print(os.getcwd())
    MAIL_SENDER = os.getenv("MAIL_SENDER")
    if(re.search(pattern,correo)): 
        message = Mail(
            from_email=MAIL_SENDER,
            to_emails=correo,
            subject='Starbucks report',
            html_content='Your requested data is ready.')
        file_path = './output/stores_from_{}.pdf'.format(ciudad)
        with open(file_path, 'rb') as f:
            data = f.read()
            f.close()
        encoded = base64.b64encode(data).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        #attachment.file_content = FileContent(data)
        attachment.file_type = FileType('application/pdf')
        attachment.file_name = FileName('stores_from_{}.pdf'.format(ciudad))
        attachment.disposition = Disposition('attachment')
        message.attachment = attachment
        try:
            token = os.getenv("SENDGRID_API_KEY")
            sg = SendGridAPIClient(token)
            response = sg.send(message)
            return response.status_code
            #print(response.body)
            #print(response.headers)
        except Exception as e:
            print(e.message)
    else:
        print("La dirección de email no es correcta")
        return 0
