import argparse
from src.starlib import (storesByCity, sendMail, createPDF, possibleResults, saveImage, composeMarkers, showStats)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ciudad", help="ciudad en la que quieres encontrar starbucks")
    #parser.add_argument("-e", "--email", help="correo al que enviar pdf-report")
    #parser.add_argument("-s", "--stats", help="Muestra estadísticas globales del dataset.", action="store_true")
    args = parser.parse_args()
    #if(args.stats):
    #    showStats()
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
        else:
            print('Error generando el fichero.')

