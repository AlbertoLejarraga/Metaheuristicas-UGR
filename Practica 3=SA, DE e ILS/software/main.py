__author__ = 'alberto'
import utilidades
import relief
import buscLocal
import aleatorio
import geneticos
import simulatedAnnealing
import random as randomPython
import numpy as np
import iterativeLocalSearch
import diferentialEvolution
def normalizar(lista):
    s=sum(lista)
    return map(lambda x:float(x)/s,lista)
if __name__ == '__main__':
    algoritmos=["ILS","SimulatedAnnealing","DiferentialEvolutionRand","DiferentialEvolutionCTB"]

    #obtengo las listas de atributos a partir de los datos normalizados
    ozono=utilidades.repartirClasesNormalizadas("ozono")
    parkinson=utilidades.repartirClasesNormalizadas("parkinson")
    corazon=utilidades.repartirClasesNormalizadas("corazon")


    #creo un generador de aleatorios a partir de la semilla 15041995 para utilizarlo en los algoritmos que se inicializara cada vez que se inicie un algoritmo
    semilla = input("Introduzca el valor de la semilla(numero)")
    #semilla = 15041995

    #si esta mejor la busqueda local corta, puede ser porque le vengan mejor los numeros aleatorios a eesta que a la larga(no en cada particion recibe los mismos numeros)

    #ejecuto los algoritmos colocando como particion de validacion una vez a cada particion, siendo
    # el resto particiones del conjunto de entrenamiento
    for algoritmo in algoritmos:
        generadorAleatorios=aleatorio.Random(semilla)
        randomPython.seed(semilla)
        np.random.seed(semilla)
        print "--------------------------------"
        print "Ejecucion de algoritmo ", algoritmo

        print "Ozono"
        for particion in range(ozono[1:].__len__()):
            print "Particion de validacion: ", particion
            if particion !=0:
                #a partir de la particion 1 intercambio el orden para dejar como particion de validacion
                # a la que toque en cada caso
                ozono[particion],ozono[5]=ozono[5],ozono[particion]
            if algoritmo=="Relief" : relief.lanzar(ozono)
            elif algoritmo=="1nn" : relief.lanzar(ozono, False)
            elif algoritmo=="BusquedaLocal" : buscLocal.lanzar(ozono,generadorAleatorios)
            elif algoritmo=="GeneticoGeneracionalBLX": geneticos.lanzar(ozono,"ozono",generadorAleatorios,"GeneticoGeneracionalBLX",semilla)
            elif algoritmo=="GeneticoGeneracionalArit": geneticos.lanzar(ozono,"ozono",generadorAleatorios,"GeneticoGeneracionalArit",semilla)
            elif algoritmo=="GeneticoEstacionarioBLX": geneticos.lanzar(ozono,"ozono",generadorAleatorios,"GeneticoEstacionarioBLX",semilla)
            elif algoritmo=="GeneticoEstacionarioArit": geneticos.lanzar(ozono,"ozono",generadorAleatorios,"GeneticoEstacionarioArit",semilla)
            elif algoritmo=="Memetico10-1": geneticos.lanzar(ozono,"ozono",generadorAleatorios,"Memetico10-1",semilla)
            elif algoritmo=="Memetico10-00.1": geneticos.lanzar(ozono,"ozono",generadorAleatorios,"Memetico10-0.1",semilla)
            elif algoritmo=="Memetico10-0.1n": geneticos.lanzar(ozono,"ozono",generadorAleatorios,"Memetico10-0.1n",semilla)
            elif algoritmo=="SimulatedAnnealing": simulatedAnnealing.lanzar(ozono,generadorAleatorios)
            elif algoritmo=="ILS": iterativeLocalSearch.lanzar(ozono,generadorAleatorios)
            elif algoritmo=="DiferentialEvolutionRand": diferentialEvolution.lanzar(ozono,"ozono",generadorAleatorios,"rand")
            elif algoritmo=="DiferentialEvolutionCTB": diferentialEvolution.lanzar(ozono,"ozono",generadorAleatorios,"CTB")
        print "*****************************"

        print "Parkinson"
        for particion in range(parkinson[1:].__len__()):
            print "Particion de validacion: ", particion
            if particion !=0:
                parkinson[particion],parkinson[5]=parkinson[5],parkinson[particion]
            if algoritmo=="Relief" : relief.lanzar(parkinson)
            elif algoritmo=="1nn" : relief.lanzar(parkinson, False)
            elif algoritmo=="BusquedaLocal" : buscLocal.lanzar(parkinson,generadorAleatorios)
            elif algoritmo=="GeneticoGeneracionalBLX": geneticos.lanzar(parkinson,"parkinson",generadorAleatorios,"GeneticoGeneracionalBLX",semilla)
            elif algoritmo=="GeneticoGeneracionalArit": geneticos.lanzar(parkinson,"parkinson",generadorAleatorios,"GeneticoGeneracionalArit",semilla)
            elif algoritmo=="GeneticoEstacionarioBLX": geneticos.lanzar(parkinson,"parkinson",generadorAleatorios,"GeneticoEstacionarioBLX",semilla)
            elif algoritmo=="GeneticoEstacionarioArit": geneticos.lanzar(parkinson,"parkinson",generadorAleatorios,"GeneticoEstacionarioArit",semilla)
            elif algoritmo=="Memetico10-1": geneticos.lanzar(parkinson,"parkinson",generadorAleatorios,"Memetico10-1",semilla)
            elif algoritmo=="Memetico10-00.1": geneticos.lanzar(parkinson,"parkinson",generadorAleatorios,"Memetico10-0.1",semilla)
            elif algoritmo=="Memetico10-0.1n": geneticos.lanzar(parkinson,"parkinson",generadorAleatorios,"Memetico10-0.1n",semilla)
            elif algoritmo=="SimulatedAnnealing": simulatedAnnealing.lanzar(parkinson,generadorAleatorios)
            elif algoritmo=="ILS": iterativeLocalSearch.lanzar(parkinson,generadorAleatorios)
            elif algoritmo=="DiferentialEvolutionRand": diferentialEvolution.lanzar(parkinson,"parkinson",generadorAleatorios,"rand")
            elif algoritmo=="DiferentialEvolutionCTB": diferentialEvolution.lanzar(parkinson,"parkinson",generadorAleatorios,"CTB")

        print "*****************************"

        print "Corazon"
        for particion in range(corazon[1:].__len__()):
            print "Particion de validacion: ", particion
            if particion !=0:
                corazon[particion],corazon[5]=corazon[5],corazon[particion]
            if algoritmo=="Relief" : relief.lanzar(corazon)
            elif algoritmo=="1nn" : relief.lanzar(corazon, False)
            elif algoritmo=="BusquedaLocal" : buscLocal.lanzar(corazon,generadorAleatorios)
            elif algoritmo=="GeneticoGeneracionalBLX": geneticos.lanzar(corazon,"corazon",generadorAleatorios,"GeneticoGeneracionalBLX",semilla)
            elif algoritmo=="GeneticoGeneracionalArit": geneticos.lanzar(corazon,"corazon",generadorAleatorios,"GeneticoGeneracionalArit",semilla)
            elif algoritmo=="GeneticoEstacionarioBLX": geneticos.lanzar(corazon,"corazon",generadorAleatorios,"GeneticoEstacionarioBLX",semilla)
            elif algoritmo=="GeneticoEstacionarioArit": geneticos.lanzar(corazon,"corazon",generadorAleatorios,"GeneticoEstacionarioArit",semilla)
            elif algoritmo=="Memetico10-1": geneticos.lanzar(corazon,"corazon",generadorAleatorios,"Memetico10-1",semilla)
            elif algoritmo=="Memetico10-00.1": geneticos.lanzar(corazon,"corazon",generadorAleatorios,"Memetico10-0.1",semilla)
            elif algoritmo=="Memetico10-0.1n": geneticos.lanzar(corazon,"corazon",generadorAleatorios,"Memetico10-0.1n",semilla)
            elif algoritmo=="SimulatedAnnealing": simulatedAnnealing.lanzar(corazon,generadorAleatorios)
            elif algoritmo=="ILS": iterativeLocalSearch.lanzar(corazon,generadorAleatorios)
            elif algoritmo=="DiferentialEvolutionRand": diferentialEvolution.lanzar(corazon,"corazon",generadorAleatorios,"rand")
            elif algoritmo=="DiferentialEvolutionCTB": diferentialEvolution.lanzar(corazon,"corazon",generadorAleatorios,"CTB")

        print "*****************************"







