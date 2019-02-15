__author__ = 'alberto'
import utilidades
import numpy as np
import time



def elegirCaracteristica(caracteristicasModificadas,random):
    return caracteristicasModificadas.pop(random.randInt(0,caracteristicasModificadas.__len__()-1))

def lanzar(setEjemplos, random, alfa=0.5, sigma=0.3,numeroDeEvaluaciones=15000, solucionInicial=[],particionValidar=[],conjuntoEntrenar=[]):
    inicio=time.time()
    #Genero un vector de pesos aleatorio que sera la solucion inicial e inicializo las variables necesarias
    if solucionInicial==[]:mejorSolucion=[random.rand() for ejemplo in range(setEjemplos[0].__len__()-1)]
    else: mejorSolucion=solucionInicial
    contador=0#evaluaciones de la funcion objetivo
    vecinosExplorados=0#vecinos explorados para una solucion seleccionada como mejor que la anterior
    if particionValidar==[]:
        particionValidacion=setEjemplos[-1]
        conjuntoEntrenamiento=setEjemplos[1:-1]
    else:
        particionValidacion=particionValidar
        conjuntoEntrenamiento=conjuntoEntrenar
    calidadMejorSolucion=utilidades.evaluarSolucion(mejorSolucion, particionValidacion, conjuntoEntrenamiento, alfa)#calidad de la mejor solucion encontrada
    numCaracteristicas=solucionInicial.__len__()
    #genero una lista de numeros que sigan una distribucion normal de media 0 y desviacion tipica sigma
    distNormalNP=np.random.normal(0,pow(sigma,2),15000)
    distNormal=distNormalNP.tolist()
    evaluadas=1

    while(contador<numeroDeEvaluaciones and vecinosExplorados < (20*numCaracteristicas)):
        mejora=False
        quedanPorModificar=[i for i in range(numCaracteristicas)]#caracteristicas que no se han modificado para una solucion encontrada
        modificadas=0#caracteristicas modificadas para una solucion encontrada(numero de caract. eliminadas de quedanPorModificar)
        #mientras no haya mejora y no se hayan modificado todas las caracteristicas
        while(not mejora and modificadas<numCaracteristicas):
            contador+=1
            modificadas+=1
            vecinosExplorados+=1
            if contador==3000 or contador==6000 or contador==9000:
                print calidadMejorSolucion

            caractAModificar=elegirCaracteristica(quedanPorModificar, random)
            solucionActual = utilidades.generarVecino(mejorSolucion,distNormal,caractAModificar)
            calidadSolActual = utilidades.evaluarSolucion(solucionActual, particionValidacion, conjuntoEntrenamiento, alfa)
            evaluadas+=1

            #[2] devuelve la tasa agregada, [0] la de clasificacion y [1]la de reduccion, se tiene en cuenta la agregada
            if(calidadSolActual[2]>calidadMejorSolucion[2]):
                mejorSolucion=solucionActual
                calidadMejorSolucion=calidadSolActual
                mejora=True
                vecinosExplorados=0
    if(numeroDeEvaluaciones==15000):
        print "Tasa de clasificacion: ", calidadMejorSolucion[0]
        print "Tasa de reduccion: ", calidadMejorSolucion[1]
        print "Tasa agregada: ", calidadMejorSolucion[2]
        final=time.time()
        print "Tiempo de ejecucion: ",final-inicio
        print "*****************************"
        return calidadMejorSolucion
    else:
        return mejorSolucion,calidadMejorSolucion[2],evaluadas


