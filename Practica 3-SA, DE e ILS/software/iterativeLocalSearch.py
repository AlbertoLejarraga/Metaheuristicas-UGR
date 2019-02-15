__author__ = 'alberto'
import utilidades
import buscLocal
import math
import numpy as np
import time

def lanzar(setEjemplos, random, alfa=0.5, sigmaMutacion=0.4,sigmaBuscLocal=0.3, iteraciones=10):
    inicio=time.time()

    #generar aleatoriamente la solucion inicial
    solucionInicial=[random.rand() for ejemplo in range(setEjemplos[0].__len__()-1)]
    particionValidacion=setEjemplos[-1]
    conjuntoEntrenamiento=setEjemplos[1:-1]

    #solucion sera una lista con la mejorSolucion como tal en la primera posicion y su calidad en la segunda(mejorSolucion[0],[1])
    mejorSolucion=buscLocal.lanzar(setEjemplos,random,alfa=alfa, sigma=sigmaBuscLocal,numeroDeEvaluaciones=500,solucionInicial=solucionInicial,particionValidar=particionValidacion,conjuntoEntrenar=conjuntoEntrenamiento)
    numCaracteristicas=mejorSolucion[0].__len__()

    #declaro cuantas caracteristicas se modificaran cada vez que se mute una solucion
    numCaractAMutar=math.trunc(0.1*numCaracteristicas)
    veces=1

    while veces<iteraciones:
        #modificar la solucionActual
        solucionModificada=mejorSolucion[0]
        for i in range(numCaractAMutar):
            solucionModificada=utilidades.generarVecino(solucionModificada,[np.random.normal(0,pow(sigmaMutacion,2))],random.randInt(0,numCaracteristicas-1))
        #realizar la busqueda local sobre esta solucion
        solucionModificadaMejorada=buscLocal.lanzar(setEjemplos,random,alfa=alfa, sigma=sigmaBuscLocal,numeroDeEvaluaciones=500,solucionInicial=solucionModificada,particionValidar=particionValidacion,conjuntoEntrenar=conjuntoEntrenamiento)
        #si la solucion obtenida es mejor se guarda, si no se deshecha
        if solucionModificadaMejorada[1]>mejorSolucion[1]:
            mejorSolucion=solucionModificadaMejorada
        veces+=1
        print veces, mejorSolucion[1]

    calidadMejorSolucion=utilidades.evaluarSolucion(mejorSolucion[0],particionValidacion,conjuntoEntrenamiento,alfa)
    print "Tasa de clasificacion: ", calidadMejorSolucion[0]
    print "Tasa de reduccion: ", calidadMejorSolucion[1]
    print "Tasa agregada: ", calidadMejorSolucion[2]
    final=time.time()
    print "Tiempo de ejecucion: ",final-inicio
    print "*****************************"
