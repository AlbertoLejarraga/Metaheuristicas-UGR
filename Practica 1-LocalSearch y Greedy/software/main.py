__author__ = 'alberto'
import utilidades
import relief
import buscLocal
import aleatorio
if __name__ == '__main__':
    algoritmos=["1nn","Relief","BusquedaLocal"]

    #obtengo las listas de atributos a partir de los datos
    ozono=utilidades.repartirClase("ozono")
    parkinson=utilidades.repartirClase("parkinson")
    corazon=utilidades.repartirClase("corazon")

    #normalizo los ejemplos, haciendo que cada valor este en [0,1]
    ozonoNormalizado=utilidades.normalizar(ozono)
    parkinsonNormalizado=utilidades.normalizar(parkinson)
    corazonNormalizado=utilidades.normalizar(corazon)
    #creo un generador de aleatorios a partir de la semilla 15041995 para utilizarlo en los algoritmos
    semilla = input("Introduzca el valor de la semilla(numero)")
    generadorAleatorios=aleatorio.Random(semilla)

    #ejecuto los algoritmos colocando como particion de validacion una vez a cada particion, siendo
    # el resto particiones del conjunto de entrenamiento
    for algoritmo in algoritmos:
        print "--------------------------------"
        print "Ejecucion de algoritmo ", algoritmo

        print "Ozono"
        for particion in range(ozonoNormalizado[1:].__len__()):
            print "Particion de validacion: ", particion
            if particion !=0:
                #a partir de la particion 1 intercambio el orden para dejar como particion de validacion
                # a la que toque en cada caso
                ozonoNormalizado[particion],ozonoNormalizado[5]=ozonoNormalizado[5],ozonoNormalizado[particion]
            if algoritmo=="Relief" : relief.lanzar(ozonoNormalizado)
            elif algoritmo=="1nn" : relief.lanzar(ozonoNormalizado, False)
            elif algoritmo=="BusquedaLocal" : buscLocal.lanzar(ozonoNormalizado,generadorAleatorios)
        print "*****************************"

        print "Parkinson"
        for particion in range(parkinsonNormalizado[1:].__len__()):
            print "Particion de validacion: ", particion
            if particion !=0:
                parkinsonNormalizado[particion],parkinsonNormalizado[5]=parkinsonNormalizado[5],parkinsonNormalizado[particion]
            if algoritmo=="Relief" : relief.lanzar(parkinsonNormalizado)
            elif algoritmo=="1nn" : relief.lanzar(parkinsonNormalizado, False)
            elif algoritmo=="BusquedaLocal" : buscLocal.lanzar(parkinsonNormalizado,generadorAleatorios)
        print "*****************************"

        print "Corazon"
        for particion in range(corazonNormalizado[1:].__len__()):
            print "Particion de validacion: ", particion
            if particion !=0:
                corazonNormalizado[particion],corazonNormalizado[5]=corazonNormalizado[5],corazonNormalizado[particion]
            if algoritmo=="Relief" : relief.lanzar(corazonNormalizado)
            elif algoritmo=="1nn" : relief.lanzar(corazonNormalizado, False)
            elif algoritmo=="BusquedaLocal" : buscLocal.lanzar(parkinsonNormalizado,generadorAleatorios)
        print "*****************************"







