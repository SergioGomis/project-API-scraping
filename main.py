import argparse
from src.starlib import (storesByCity, sendMail, createPDF, possibleResults, saveImage, composeMarkers)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ciudad", help="ciudad en la que quieres encontrar starbucks")
    #parser.add_argument("-e", "--email", help="correo al que enviar pdf-report")
    args = parser.parse_args()
    datos = storesByCity(args.ciudad)
    if datos.empty:
        possibleResults(args.ciudad)
    else:
        if(createPDF(datos,args.ciudad)):
            print('Report generado con éxito.')
            
            #status = sendMail(args.email,args.ciudad)
            #if status == 202:
            #    print('Email enviado correctamente.')
            #else:
            #    print('Oops, something went wrong.')
        else:6
            print('Error generando el fichero.')

