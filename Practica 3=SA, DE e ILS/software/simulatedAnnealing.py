__author__ = 'alberto'
import utilidades
import math
import numpy as np
import time

def aceptarSolucionPeor(calidadSolActual,calidadSolNueva,tempActual,random):
    aleatorio=random.rand()
    diferenciaCalidad=calidadSolNueva-calidadSolActual
    return aleatorio <= math.exp(diferenciaCalidad/tempActual)

def enfriar(temperaturaActual,beta):
    return temperaturaActual/(1+beta*temperaturaActual)

def lanzar(setEjemplos,random,phi=0.3,mu=0.3,sigma=0.3,tempFinal=0.001):
    inicio=time.time()

    #generar aleatoriamente la solucion inicial y evaluarla
    mejorSolucion=[random.rand() for ejemplo in range(setEjemplos[0].__len__()-1)]
    particionValidacion=setEjemplos[-1]

    conjuntoEntrenamiento=setEjemplos[1:-1]
    calidadMejorSolucion=utilidades.evaluarSolucion(mejorSolucion,particionValidacion,conjuntoEntrenamiento)[2]
    solucionActual=mejorSolucion
    calidadSolucionActual=calidadMejorSolucion

    #determinar la temperatura inicial
    tempActual=mu*calidadMejorSolucion/(-math.log(phi))
    numCaracteristicas=solucionActual.__len__()

    #determinar numero maximo de vecinos y exitos para continuar en el bucle interno
    maxVecinos=10*numCaracteristicas
    maxExitos=0.1*maxVecinos
    numEvaluaciones=1
    numExitos=1

    #determinar beta para utilizarlo en el esquema de enfriamiento
    numIteracionesMaximas=15000/maxVecinos
    beta=(tempActual-tempFinal)/(numIteracionesMaximas*tempFinal*tempActual)

    #mientras no se cumplan las condiciones de parada
    while(numEvaluaciones<15000 and numExitos>0 and tempActual>tempFinal):
        iteraciones=0
        numExitos=0
        while(iteraciones<maxVecinos and numExitos<maxExitos):
            #genero una solucion vecina y la evaluo
            solucionNueva = utilidades.generarVecino(solucionActual,[np.random.normal(0,pow(sigma,2))],random.randInt(0,numCaracteristicas-1))
            calidadSolucionNueva = utilidades.evaluarSolucion(solucionNueva,particionValidacion,conjuntoEntrenamiento)[2]

            #si la solucion es mejor o se decide aceptar la solucion aunque sea peor se coge esta solucion
            if(calidadSolucionNueva>calidadSolucionActual or aceptarSolucionPeor(calidadSolucionActual,calidadSolucionNueva,tempActual,random)):
                solucionActual=solucionNueva
                calidadSolucionActual=calidadSolucionNueva
                numExitos+=1

                #si la solucion mejora a la mejor solucion global se guarda
                if calidadSolucionActual > calidadMejorSolucion:
                    mejorSolucion=solucionActual
                    calidadMejorSolucion=calidadSolucionActual
            iteraciones+=1
        numEvaluaciones+=iteraciones
        tempActual=enfriar(tempActual,beta)

    calidadMejorSolucion=utilidades.evaluarSolucion(mejorSolucion,particionValidacion,conjuntoEntrenamiento)
    print "Tasa de clasificacion: ", calidadMejorSolucion[0]
    print "Tasa de reduccion: ", calidadMejorSolucion[1]
    print "Tasa agregada: ", calidadMejorSolucion[2]
    final=time.time()
    print "Tiempo de ejecucion: ",final-inicio
    print "*****************************"
    return calidadMejorSolucion
