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


ver = FPDF()

def possibleResults(ciudad):
    ds = pd.read_csv("./input/starbucks_updt.csv")
    busqueda = ciudad[:-1]
    alternativas = ds[ds['City'].str.contains(busqueda, case=False, na=False)].City.unique()
    while not alternativas.any() and len(busqueda) > 1:
        #print(busqueda)
        busqueda = busqueda[:-1]
        alternativas = ds[ds['City'].str.contains(busqueda, case=False, na=False)].City.unique()
    print('Ciudad no encontrada. Prueba con estas posibles coincidencias:')
    for elem in alternativas:
        print('- ',elem)
    #df[df['A'].str.contains("hello")]


def storesByCity(ciudad):
    ds = pd.read_csv("./input/starbucks_updt.csv")

    #print(ds[ds['City']==ciudad])
    return ds[ds['City'].str.lower()==ciudad]


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


def fit_word(string,cell_w,font_type):
    ver.set_font(*font_type)
    # if string fits, return it unchanged
    if ver.get_string_width(string)<cell_w:
        return string
    # cut string until it fits
    while ver.get_string_width(string)>=cell_w:
        string = string[:-1]
    # replace last 3 characters with "..."
    string = string[:-3] + "..."
    return string


def createPDF(datos,ciudad):
    try:
        # Create FPDF object
        # FPDF(orientation, unit, format)
        pdf = FPDF('L','mm','A4')

        pdf.add_page()
        #df = pd.DataFrame(data)

        # Defining parameters
        num_col = len(datos.columns)
        w,h=190,277
        font_type = ('Arial', 'B', 16)
        pdf.set_font(*font_type)
        pdf.set_text_color(0)
        pdf.set_draw_color(0)

        # Title
        pdf.cell(w,10,'Datos Personales',1,1,'C')

        # Column names
        pdf.set_line_width(0.2)
        for col in datos.columns:
            pdf.cell(w/num_col,10,col,1,0,'C')
        pdf.ln()

        # Data
        pdf.set_fill_color(243,95,95)
        font_type = ('Arial', '', 12)
        pdf.set_font(*font_type)
        # iteration rows
        for _,row in datos.iterrows():
            # Adding conditional
            #fill = 0
            #if row["country"] in european_countries:
            #    fill = 1
            # iterating columns
            for value in datos.columns:
                pdf.cell(w/num_col,10,fit_word(str(row[value]),w/num_col,font_type),1,0,'C',1)
            pdf.ln()
            
        # Exporting file
        #numfile = int(os.getenv("PDFNAME"),base=16)
        #print(numfile)
        pdf.output('./output/stores_from_{}.pdf'.format(ciudad),'F')
        #os.environ['PDFNAME'] = str(numfile+1)
        return True
    except:
        return False