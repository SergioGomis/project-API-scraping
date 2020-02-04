import pandas as pd
import numpy as np
import os
import base64
from dotenv import load_dotenv
load_dotenv()
import re
from fpdf import FPDF
import requests


ver = FPDF()


def composeMarkers(datos):
    s = ''
    for _,row in datos.iterrows():
        s += '&markers=color:green%7C'+str(row['Latitude'])+','+str(row['Longitude'])
    return s



def saveImage(url):
    try:
        MAPS_API_KEY = os.getenv("MAPS_API_KEY")
        url = f'{url}&key={MAPS_API_KEY}'
        r = requests.get(url, allow_redirects=True, stream=True)
        f = open('./output/temp_map.png', 'wb')
        f.write(r.content)
        f.close()
        return True
    except:
        return False

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
        # url de imagen con el mapa
        puntos = composeMarkers(datos)
        baseURL = 'https://maps.googleapis.com/maps/api/staticmap?size=750x350&maptype=roadmap'
        

        # Create FPDF object
        # FPDF(orientation, unit, format)
        pdf = FPDF('L','mm','A4')
        #210 x 297 mm P
        #297 x 210 mm L

        pdf.add_page()
        #df = pd.DataFrame(data)
        pdf.image('./src/starbucks-logo-small.png', 250, 10, link='https://www.starbucks.com/')

        # Defining parameters
        num_col = len(datos.columns)
        w,h=277,190
        font_type = ('Arial', 'B', 16)
        pdf.set_font(*font_type)
        pdf.set_text_color(0)
        pdf.set_draw_color(0)

        # Title
        pdf.cell(w,50,'',0,1,'C')
        pdf.cell(w,10,f'Stores from {ciudad}',1,1,'C')

        # Column names
        pdf.set_line_width(0.1)
        #for col in datos.columns:
        #    pdf.cell(w/num_col,10,col,1,0,'C')
        pdf.cell(27,10,'Brand',1,0,'C')
        pdf.cell(34,10,'#',1,0,'C')
        pdf.cell(44,10,'Name',1,0,'C')
        pdf.cell(54,10,'Address',1,0,'C')
        pdf.cell(34,10,'City',1,0,'C')
        pdf.cell(25,10,'Lat.',1,0,'C')
        pdf.cell(25,10,'Long.',1,0,'C')
        pdf.cell(34,10,'Country',1,0,'C')
        pdf.ln()


        # Data
        pdf.set_fill_color(121, 181, 161)
        font_type = ('Arial', '', 12)
        pdf.set_font(*font_type)
        # iteration rows
        for _,row in datos.iterrows():
            pdf.cell(27,10,fit_word(str(row['Brand']),27,font_type),1,0,'C',1)
            pdf.cell(34,10,fit_word(str(row['Store Number']),34,font_type),1,0,'C',1)
            pdf.cell(44,10,fit_word(str(row['Store Name']),44,font_type),1,0,'C',1)
            pdf.cell(54,10,fit_word(str(row['Street Address']),54,font_type),1,0,'C',1)
            pdf.cell(34,10,fit_word(str(row['City']),34,font_type),1,0,'C',1)
            pdf.cell(25,10,fit_word(str(row['Latitude']),25,font_type),1,0,'C',1)
            pdf.cell(25,10,fit_word(str(row['Longitude']),25,font_type),1,0,'C',1)
            pdf.cell(34,10,fit_word(str(row['Pais']),34,font_type),1,0,'C',1)
            # iterating columns
            #for value in datos.columns:
            #    pdf.cell(w/num_col,10,fit_word(str(row[value]),w/num_col,font_type),1,0,'C',1)
            pdf.ln()
        if(saveImage(f'{baseURL}{puntos}')):
            pdf.add_page()
            #df = pd.DataFrame(data)

            pdf.image('./src/starbucks-logo-small.png', 250, 10, link='https://www.starbucks.com/')
            pdf.image('./output/temp_map.png', 10, 60)

        # Exporting file
        pdf.output('./output/stores_from_{}.pdf'.format(ciudad),'F')
        return True
    except:
        return False
