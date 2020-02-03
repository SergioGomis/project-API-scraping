import argparse
from src.starlib import (storesByCity, sendMail, createPDF, possibleResults, saveImage, composeMarkers, showStats)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ciudad", help="Ciudad en la que quieres encontrar starbucks")
    #parser.add_argument("-h", "--help", help="Muestra este mensaje de ayuda.", action='help')
    parser.add_argument("-email", help="Correo al que enviar pdf-report")
    parser.add_argument("-s", "--stats", help="Muestra estadísticas globales del dataset.", action="store_true")
    parser.add_argument("-v", "--version", help="Muestra la versión actual del programa.", action='version', version='1.0')
    args = parser.parse_args()
    if not args.email:
        print('El email es requerido. Consulta la ayuda [-h] para más información.')
    else:
        if(args.stats):
            showStats()
        datos = storesByCity(args.ciudad)
        if datos.empty:
            possibleResults(args.ciudad)
        else:
            if(createPDF(datos,args.ciudad)):
                print('Report generado con éxito.')
                
                status = sendMail(args.email,args.ciudad)
                if status == 202:
                    print('Email enviado correctamente.')
                else:
                    print('Oops, something went wrong.')
            else:
                print('Error generando el fichero.')

