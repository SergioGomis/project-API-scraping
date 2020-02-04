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


ver = FPDF()

def showStats():
    ds = pd.read_csv("./input/starbucks_updt.csv")
    # print(ds.describe())
    print('==== STATS ====')
    print('- El dataset contiene '+str(len(ds))+' tiendas')
    print('- De las cuales el '+str(int(len(ds[ds['Latitude']>0])*100/len(ds)))+'% están ubicadas en el hemisferio norte.')
    print('- Y están en Estados Unidos el '+str(int(len(ds[ds['Pais']=='United States'])*100/len(ds)))+'% del total.')
    # Top 10 countries
    print('\n')




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
    salida = ds[ds['City'].str.lower()==ciudad.lower()]
    if not salida.empty:
        paises = salida.groupby(['Pais'])['Pais'].unique().shape[0]
        if paises > 1:
            print('Hay varios posibles países para esta ciudad:')
            lista = [a for a in ds[ds['City'].str.lower()==ciudad.lower()].groupby(['Pais'])['Pais'].unique().keys()]
            for a in range(len(lista)):
                print('['+str(a)+'] '+lista[a])
            while True:
                try:
                    pais_elegido = int(input('Introduce el numero del cual quieres los datos: '))
                    if(pais_elegido in range(paises)):
                        break
                except:
                    print('Valor no válido')
            salida = ds[(ds['City'].str.lower()==ciudad.lower()) & (ds['Pais']==lista[pais_elegido])]
    #print(ds[ds['City']==ciudad])
    return salida


