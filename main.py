import argparse
from src.starlib import (storesByCity, sendMail, createPDF)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ciudad", help="ciudad en la que quieres encontrar starbucks")
    #parser.add_argument("-e", "--email", help="correo al que enviar pdf-report")
    args = parser.parse_args()
    datos = storesByCity(args.ciudad)
    createPDF(datos)
    #sendMail(args.e)

