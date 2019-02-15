__author__ = 'alberto'
import utilidades
import time
import os.path
import random as randomPython
import math
import random
import aleatorio
import numpy as np
import sys
import buscLocal
#para utilizar la misma poblacion inicial en los distintos algoritmos la guardo en un fichero y la extraigo de ahi
def generarPoblacionInicial(setEjemplos,nombreSet,random,tamanoPoblacion,particionValidacion, conjuntoEntrenamiento,alfa):
    if not os.path.isfile("data\\poblacionInicialGeneticos"+nombreSet+".txt"):
        with open("data\\poblacionInicialGeneticos"+nombreSet+".txt",'w') as fichero:
            numeroDeGenes=setEjemplos[1][0].__len__()-1
            fichero.write(str(tamanoPoblacion)+'\n')
            fichero.write(str(numeroDeGenes)+'\n')
            poblacion=[]
            for i in range(tamanoPoblacion):
                cromosoma=[]
                for j in range(numeroDeGenes):
                    cromosoma.append(random.rand())
                    fichero.write(str(cromosoma[j])+'\n')
                cromosoma.append(False)#anado este marcador para facilitar que el mejor cromosoma sobreviva en cada iteracion
                cromosoma.append(utilidades.evaluarSolucion(cromosoma,particionValidacion, conjuntoEntrenamiento,alfa)[2])#anado el valor de la solucion
                fichero.write(str(cromosoma[-1])+'\n')
                poblacion.append(cromosoma)
    else:
        with open("data\\poblacionInicialGeneticos"+nombreSet+".txt",'r') as fichero:
            tamanoPoblacionF=int(fichero.readline())
            numeroDeGenesF=int(fichero.readline())
            if tamanoPoblacion!=tamanoPoblacionF: print "tamanos de poblacion distintos"
            if numeroDeGenesF!=setEjemplos[1][0].__len__()-1: print "numero de genes distintos"
            poblacion=[]
            for i in range(tamanoPoblacionF):
                cromosoma=[]
                for j in range(numeroDeGenesF):
                    cromosoma.append(float(fichero.readline()))
                cromosoma.append(False)#anado este marcador para facilitar que el mejor cromosoma sobreviva en cada iteracion
                cromosoma.append(float(fichero.readline()))
                poblacion.append(cromosoma)
    fichero.close()
    return poblacion
#devuelve la poblacion modificada con el marcador del mejor y el cromosoma con mayor fitness(mejor individuo de la poblacion)
def mejorCromosoma(poblacion):
    calidadMejorSolucion=-1.0
    mejorCromosoma=1000
    poblacionAux=poblacion
    for i in range(poblacion.__len__()):
        poblacionAux[i][-2]=False
        calidadActual=poblacionAux[i][-1]
        if calidadActual > calidadMejorSolucion:
            calidadMejorSolucion=calidadActual
            mejorCromosoma=i
    poblacionAux[mejorCromosoma][-2]=True

    return poblacionAux,poblacionAux[mejorCromosoma]

#devuelve la poblacion resultante de hacer un torneo binario entre los miembros de la poblacion anterior
#la aleatoriedad de los padres seleccionados viene de "barajar" la poblacion para despues hacer 0vs1,1vs2,2vs3,etc.
def seleccionGeneracional(poblacion):
    poblacionResul=[]
    randomPython.shuffle(poblacion)
    for i in range(-1,poblacion.__len__()-1):
        calidadPadre=poblacion[i][-1]
        calidadMadre=poblacion[i+1][-1]
        if calidadMadre>calidadPadre:
            poblacionResul.append(poblacion[i+1])
        else:
            poblacionResul.append(poblacion[i])
    return poblacionResul,poblacion.__len__()

def seleccionEstacionario(poblacion,random):
    padres=[]
    #selecciono 4 candidatos aleatorios
    candidatos=[poblacion[random.randInt(0,poblacion.__len__()-1)] for valor in range(4)]
    #hago el torneo entre los dos primeros y los dos segundos
    if candidatos[0][-1]>candidatos[1][-1]:padres.append(candidatos[0])
    else: padres.append(candidatos[1])
    if candidatos[2][-1]>candidatos[1][3]:padres.append(candidatos[2])
    else: padres.append(candidatos[3])
    return padres,4



def cruceBLX(poblacion,alfaBLX,probCruce,random,particionValidacion,conjuntoEntrenamiento,alfaTasas):
    #introduzco la probabilidad de cruce decidiendo a priori cuantos cruces se haran en base a la esperanza de que dos padres crucen
    #este numero viene de la probabilidad de cruce por el numero de parejas a cruzar
    #cruzaran los numeroDeCruces primeras parejas, al ser ya aleatoria la seleccion
    numeroDeCruces=math.trunc(probCruce*poblacion.__len__()/2)
    poblacionResul=[]
    #introduzco la parte de la poblacion que cruza
    for i in range(numeroDeCruces):
        cromosoma1=poblacion[2*i][:-2]
        cromosoma2=poblacion[2*i+1][:-2]
        cromosomaAIntroducir1=[]
        cromosomaAIntroducir2=[]
        for j in range(cromosoma1.__len__()):
            if cromosoma1[j]>cromosoma2[j]:
                CMax=cromosoma1[j]
                CMin=cromosoma2[j]
            else:
                CMax=cromosoma2[j]
                CMin=cromosoma1[j]
            I=CMax-CMin
            cromosomaAIntroducir1.append(random.randFloat(CMin-I*alfaBLX,CMax+I*alfaBLX))
            cromosomaAIntroducir2.append(random.randFloat(CMin-I*alfaBLX,CMax+I*alfaBLX))
        #anado las marcas de mejorSolucion y valor de solucion aunque sean invalidas
        cromosomaAIntroducir1.append(False)
        cromosomaAIntroducir2.append(False)
        cromosomaAIntroducir1.append(utilidades.evaluarSolucion(cromosomaAIntroducir1,particionValidacion,conjuntoEntrenamiento,alfaTasas)[2])
        cromosomaAIntroducir2.append(utilidades.evaluarSolucion(cromosomaAIntroducir2,particionValidacion,conjuntoEntrenamiento,alfaTasas)[2])
        poblacionResul.append(cromosomaAIntroducir1)
        poblacionResul.append(cromosomaAIntroducir2)
    if probCruce!=1: poblacionResul.extend(poblacion[2*numeroDeCruces:])
    return poblacionResul,numeroDeCruces*2

def cruceAritmetico(poblacion, probCruce,particionValidacion,conjuntoEntrenamiento,alfaTasas):
    #similar al anterior pero realizando el cruce aritmetico(cromosoma1[i]+cromosoma2[i]/2
    numeroDeCruces=math.trunc(probCruce*poblacion.__len__()/2)
    poblacionResul=[]
    #introduzco la parte de la poblacion que cruza
    for i in range(numeroDeCruces):
        cromosoma1=poblacion[2*i][:-2]
        cromosoma2=poblacion[2*i+1][:-2]
        cromosomaAIntroducir=[]
        for j in range(cromosoma1.__len__()):
            cromosomaAIntroducir.append((cromosoma1[j]+cromosoma2[j])/2)
        #anado las marcas de mejorSolucion y valor de solucion aunque sean invalidas
        cromosomaAIntroducir.append(False)
        cromosomaAIntroducir.append(utilidades.evaluarSolucion(cromosomaAIntroducir,particionValidacion,conjuntoEntrenamiento,alfaTasas)[2])
        poblacionResul.append(cromosomaAIntroducir)
        poblacionResul.append(cromosomaAIntroducir)
    poblacionResul.extend(poblacion[2*numeroDeCruces:])
    return poblacionResul,numeroDeCruces

#realiza la mutacion de un numero de genes escogiendo aleatoriamente un cromosoma y un gen
def mutacion(poblacion,random,probMut,sigmaDistNormal,particionValidacion,conjuntoEntrenamiento,alfaTasas):
    numeroMutaciones=math.trunc((poblacion[0].__len__()-2)*poblacion.__len__()*probMut)
    poblacionAux=poblacion
    for i in range(numeroMutaciones):
        cromosomaAMutar=random.randInt(0,poblacion.__len__()-1)
        genAMutar=random.randInt(0,poblacion[0].__len__()-3)
        poblacionAux[cromosomaAMutar]=utilidades.generarVecino(poblacion[cromosomaAMutar],[np.random.normal(0,pow(sigmaDistNormal,2))],genAMutar)
        poblacionAux[cromosomaAMutar][-2]=False
        poblacionAux[cromosomaAMutar][-1]=utilidades.evaluarSolucion(poblacionAux[cromosomaAMutar],particionValidacion,conjuntoEntrenamiento,alfaTasas)[2]
    return poblacionAux,numeroMutaciones

def BLMemeticos(poblacion,proporcionCromosomas,particionValidacion,conjuntoEntrenamiento,random,tamanoPoblacion):
    #reconstruyo el setEjemplos para mandarlo a la busqueda local
    evaluaciones=0
    poblacionResul=[]
    if(proporcionCromosomas==1):
        for i in range(tamanoPoblacion):
            resulBuscLocal=buscLocal.lanzar([],random,numeroDeEvaluaciones=2*tamanoPoblacion,solucionInicial=poblacion[i][:-2],particionValidar=particionValidacion,conjuntoEntrenar=conjuntoEntrenamiento)
            poblacionResul.append(resulBuscLocal[0])
            poblacionResul[i].append(False)
            poblacionResul[i].append(resulBuscLocal[1])
            evaluaciones+=resulBuscLocal[2]
    elif(proporcionCromosomas==0.1):
        numCromosomasAMandar=math.trunc(0.1*tamanoPoblacion)
        introducidos=[]
        for i in range(numCromosomasAMandar):
            numAleatorio=random.randInt(0,tamanoPoblacion-1)
            introducidos.append(numAleatorio)
            resulBuscLocal=buscLocal.lanzar([],random,numeroDeEvaluaciones=2*tamanoPoblacion,solucionInicial=poblacion[numAleatorio][:-2],particionValidar=particionValidacion,conjuntoEntrenar=conjuntoEntrenamiento)
            poblacionResul.append(resulBuscLocal[0])
            evaluaciones+=resulBuscLocal[2]
            poblacionResul[numAleatorio].append(False)
            poblacionResul[numAleatorio].append(resulBuscLocal[1])
        for i in range(tamanoPoblacion):
            if i not in introducidos: poblacionResul.append(poblacion[i])
    else:
        poblacion.sort(key=lambda x: x[poblacion[0].__len__()-2])
        numCromosomasAMandar=math.trunc(0.1*tamanoPoblacion)
        for i in range(numCromosomasAMandar):
            resulBuscLocal=buscLocal.lanzar([],random,numeroDeEvaluaciones=2*tamanoPoblacion,solucionInicial=poblacion[i][:-2],particionValidar=particionValidacion,conjuntoEntrenar=conjuntoEntrenamiento)
            poblacionResul.append(resulBuscLocal[0])
            evaluaciones+=resulBuscLocal[2]
            poblacionResul[i].append(False)
            poblacionResul[i].append(resulBuscLocal[1])
        for i in range(tamanoPoblacion-numCromosomasAMandar):
            poblacionResul.append(poblacion[numCromosomasAMandar+i])
    return poblacionResul,evaluaciones




def generacionalBLX(poblacionInicial,particionValidacion, conjuntoEntrenamiento,random,tamanoPoblacion,numeroDeEvaluaciones,alfaBLX,probCruceGeneracional,probMut,alfaTasas,sigmaDistNormal,cromosomasBusqLocal):
    evaluaciones=poblacionInicial.__len__()
    poblacionActual=poblacionInicial
    iteraciones=11.0
    while(evaluaciones<numeroDeEvaluaciones):
        #obtengo el mejor cromosoma para introducirlo en caso de que no aparezca en la poblacion final y modifico
        #la poblacion actual para que solo tenga el marcador del mejor el que es realmente el mejor

        resulMejorCromosoma=mejorCromosoma(poblacionActual)
        poblacionActual=resulMejorCromosoma[0]
        mejorCromosomaPoblacion=resulMejorCromosoma[1]
        evaluaciones+=poblacionActual.__len__()
        #realizo la seleccion por torneo binario
        resulSeleccion=seleccionGeneracional(poblacionActual)
        poblacionActual=resulSeleccion[0]
        evaluaciones+=resulSeleccion[1]
        #realizo el cruce BLX

        resulCruce=cruceBLX(poblacionActual,alfaBLX,probCruceGeneracional,random,particionValidacion,conjuntoEntrenamiento,alfaTasas)
        poblacionActual=resulCruce[0]
        evaluaciones+=resulCruce[1]
        #mutacion en base a una probabilidad(probMut)

        resulMutacion=mutacion(poblacionActual,random,probMut,sigmaDistNormal,particionValidacion,conjuntoEntrenamiento,alfaTasas)
        poblacionActual=resulMutacion[0]
        evaluaciones+=resulMutacion[1]
        #realizo la busqueda local indicada si es necesario
        if cromosomasBusqLocal!=0:
            if(iteraciones%10==0.0):
                resulBusqLocal=BLMemeticos(poblacionActual,cromosomasBusqLocal,particionValidacion,conjuntoEntrenamiento,random,tamanoPoblacion)
                poblacionActual=resulBusqLocal[0]
                evaluaciones+=resulBusqLocal[1]
                print evaluaciones

        #comprobar si sobrevive el mejor individuo de la poblacion anterior

        encontrado=False
        i=0
        posicionPeor=-1
        peor=sys.maxint
        while(i<tamanoPoblacion and not encontrado):
            if poblacionActual[i][-2]==True: encontrado=True
            else:
                valorSolucion=poblacionActual[i][-1]
                if valorSolucion<peor:
                    peor = valorSolucion
                    posicionPeor=i
            i+=1
        if not encontrado:
            poblacionActual[posicionPeor]=mejorCromosomaPoblacion
        evaluaciones+=1
        iteraciones+=1
    mejorSolucion=mejorCromosoma(poblacionActual)[1]
    calidadMejorSolucion=utilidades.evaluarSolucion(mejorSolucion,particionValidacion,conjuntoEntrenamiento,alfaTasas)
    return calidadMejorSolucion

def generacionalArit(poblacionInicial,particionValidacion,conjuntoEntrenamiento,random,tamanoPoblacion,numeroDeEvaluaciones,probCruceGeneracional,probMut,alfaTasas, sigmaDistNormal):
    evaluaciones=poblacionInicial.__len__()
    poblacionActual=poblacionInicial

    while(evaluaciones<numeroDeEvaluaciones):
        #obtengo el mejor cromosoma para introducirlo en caso de que no aparezca en la poblacion final y modifico
        #la poblacion actual para que solo tenga el marcador del mejor el que es realmente el mejor

        resulMejorCromosoma=mejorCromosoma(poblacionActual)
        poblacionActual=resulMejorCromosoma[0]
        mejorCromosomaPoblacion=resulMejorCromosoma[1]
        evaluaciones+=poblacionActual.__len__()

        #realizo la seleccion por torneo binario
        resulSeleccion=seleccionGeneracional(poblacionActual)
        poblacionActual=resulSeleccion[0]
        evaluaciones+=resulSeleccion[1]

        #realizo el cruce BLX

        resulCruce=cruceAritmetico(poblacionActual,probCruceGeneracional,particionValidacion,conjuntoEntrenamiento,alfaTasas)
        poblacionActual=resulCruce[0]
        evaluaciones+=resulCruce[1]

        #mutacion en base a una probabilidad(probMut

        resulMutacion=mutacion(poblacionActual,random,probMut,sigmaDistNormal,particionValidacion,conjuntoEntrenamiento,alfaTasas)
        poblacionActual=resulMutacion[0]
        evaluaciones+=resulMutacion[1]

        #comprobar si sobrevive el mejor individuo de la poblacion anterior

        encontrado=False
        i=0
        posicionPeor=-1
        peor=sys.maxint
        while(i<tamanoPoblacion and not encontrado):
            if poblacionActual[i][-2]==True: encontrado=True
            else:
                valorSolucion=poblacionActual[i][-1]
                if valorSolucion<peor:
                    peor = valorSolucion
                    posicionPeor=i
            i+=1
        if not encontrado:
            poblacionActual[posicionPeor]=mejorCromosomaPoblacion
        evaluaciones+=1
    mejorSolucion=mejorCromosoma(poblacionActual)[1]
    calidadMejorSolucion=utilidades.evaluarSolucion(mejorSolucion,particionValidacion,conjuntoEntrenamiento,alfaTasas)
    return calidadMejorSolucion

def valorarHijos(hijosNuevosMutados,poblacion,tamanoPoblacion,random):
    poblacionActual=poblacion
    posicionPeor = 1000
    peor=sys.maxint
    i=0
    evaluaciones=0
    while(i<tamanoPoblacion):
        valorSolucion=poblacionActual[i][-1]
        if valorSolucion<peor:
            peor=valorSolucion
            posicionPeor=i
        i+=1
    evaluaciones+=tamanoPoblacion
    poblacionActual[posicionPeor]=hijosNuevosMutados[random.randInt(0,1)]
    cambio=True

    return poblacionActual,evaluaciones

def estacionarioBLX(poblacionInicial,particionValidacion,conjuntoEntrenamiento,random,tamanoPoblacion,numeroDeEvaluaciones,alfaBLX,probMut,alfaTasas,sigmaDistNormal):
    evaluaciones=poblacionInicial.__len__()
    poblacionActual=poblacionInicial
    numGenes=poblacionActual[0].__len__()-2
    while(evaluaciones<numeroDeEvaluaciones):
        #obtengo el mejor cromosoma para introducirlo en caso de que no aparezca en la poblacion final y modifico
        #la poblacion actual para que solo tenga el marcador del mejor el que es realmente el mejor

        #realizo la seleccion por torneo binario
        resulSeleccion=seleccionEstacionario(poblacionActual,random)
        cromSeleccionados=resulSeleccion[0]
        evaluaciones+=resulSeleccion[1]

        #realizo el cruce BLX

        resulCruce=cruceBLX(cromSeleccionados,alfaBLX,1,random,particionValidacion,conjuntoEntrenamiento,alfaTasas)
        hijosNuevos=resulCruce[0]
        evaluaciones+=resulCruce[1]

        #mutacion en base a una probabilidad(probMut)
        aMutar=random.randFloat(0,1)
        if aMutar<=0.001:
            probMutacion=1/(2*numGenes)
        else: probMutacion=probMut

        resulMutacion=mutacion(hijosNuevos,random,probMutacion,sigmaDistNormal,particionValidacion,conjuntoEntrenamiento,alfaTasas)
        hijosNuevosMutados=resulMutacion[0]
        evaluaciones+=resulMutacion[1]

        #determinar en que posicion entran los hijos nuevos
        resulValoracion=valorarHijos(hijosNuevosMutados,poblacionActual,tamanoPoblacion,random)
        poblacionActual=resulValoracion[0]
        evaluaciones+=resulValoracion[1]

    mejorSolucion=mejorCromosoma(poblacionActual)[1][:-1]
    calidadMejorSolucion=utilidades.evaluarSolucion(mejorSolucion,particionValidacion,conjuntoEntrenamiento,alfaTasas)
    return calidadMejorSolucion

def estacionarioArit(poblacionInicial,particionValidacion,conjuntoEntrenamiento,random,tamanoPoblacion,numeroDeEvaluaciones,probMut,alfaTasas,sigmaDistNormal):
    evaluaciones=poblacionInicial.__len__()
    poblacionActual=poblacionInicial
    numGenes=poblacionActual[0].__len__()-2
    while(evaluaciones<numeroDeEvaluaciones):
        #obtengo el mejor cromosoma para introducirlo en caso de que no aparezca en la poblacion final y modifico
        #la poblacion actual para que solo tenga el marcador del mejor el que es realmente el mejor

        #realizo la seleccion por torneo binario
        resulSeleccion=seleccionEstacionario(poblacionActual,random)
        cromSeleccionados=resulSeleccion[0]
        evaluaciones+=resulSeleccion[1]

        #realizo el cruce aritmetico

        resulCruce=cruceAritmetico(cromSeleccionados,1,particionValidacion,conjuntoEntrenamiento,alfaTasas)
        hijosNuevos=resulCruce[0]
        evaluaciones+=resulCruce[1]

        #mutacion en base a la probMut. La funcion recibira 1/2*numGenes si debe mutar o probMut en otro caso(no muta ningun gen)
        aMutar=random.randFloat(0,1)
        if aMutar<=probMut:
            probMutacion=1/(2*numGenes)
        else: probMutacion=probMut

        resulMutacion=mutacion(hijosNuevos,random,probMutacion,sigmaDistNormal,particionValidacion,conjuntoEntrenamiento,alfaTasas)
        hijosNuevosMutados=resulMutacion[0]
        evaluaciones+=resulMutacion[1]

        #determinar en que posicion entran los hijos nuevos
        resulValoracion=valorarHijos(hijosNuevosMutados,poblacionActual,tamanoPoblacion,random)
        poblacionActual=resulValoracion[0]
        evaluaciones+=resulValoracion[1]

    mejorSolucion=mejorCromosoma(poblacionActual)[1]
    calidadMejorSolucion=utilidades.evaluarSolucion(mejorSolucion,particionValidacion,conjuntoEntrenamiento,alfaTasas)
    return calidadMejorSolucion

def lanzar(setEjemplos,nombreSet,randomG,tipo,semilla,tamanoPoblacion=30,numeroDeEvaluaciones=15000,alfaBLX=0.3,probCruceGeneracional=0.7,probMut=0.001,alfaTasas=0.5,sigmaDistNormal=0.3):
    particionValidacion=setEjemplos[-1]
    conjuntoEntrenamiento=setEjemplos[1:-1]
    poblacionInicial=generarPoblacionInicial(setEjemplos,nombreSet,randomG,tamanoPoblacion,particionValidacion,conjuntoEntrenamiento,alfaTasas)
    if tipo=="Memetico10-1" or tipo=="Memetico10-0.1" or tipo=="Memetico10-0.1n":
        random=aleatorio.Random(semilla)
        randomPython.seed(semilla)
        np.random.seed(semilla)
    inicio=time.time()
    #los algoritmos devolveran todos una lista con la tasa de clasificacion, reduccion y agregada de la mejor solucion de la poblacion final
    if tipo=="GeneticoGeneracionalBLX":
        calidadMejorSolucion=generacionalBLX(poblacionInicial,particionValidacion,conjuntoEntrenamiento,randomG,tamanoPoblacion,numeroDeEvaluaciones,alfaBLX,probCruceGeneracional,probMut,alfaTasas,sigmaDistNormal,0)
    elif tipo=="GeneticoGeneracionalArit":
        calidadMejorSolucion=generacionalArit(poblacionInicial,particionValidacion,conjuntoEntrenamiento,randomG,tamanoPoblacion,numeroDeEvaluaciones,probCruceGeneracional,probMut,alfaTasas,sigmaDistNormal)
    elif tipo=="GeneticoEstacionarioBLX":
        calidadMejorSolucion=estacionarioBLX(poblacionInicial,particionValidacion,conjuntoEntrenamiento,randomG,tamanoPoblacion,numeroDeEvaluaciones,alfaBLX,probMut,alfaTasas,sigmaDistNormal)
    elif tipo=="GeneticoEstacionarioArit":
        calidadMejorSolucion=estacionarioArit(poblacionInicial,particionValidacion,conjuntoEntrenamiento,randomG,tamanoPoblacion,numeroDeEvaluaciones,probMut,alfaTasas,sigmaDistNormal)
    elif tipo=="Memetico10-1":
        calidadMejorSolucion=generacionalBLX(poblacionInicial,particionValidacion,conjuntoEntrenamiento,random,tamanoPoblacion,numeroDeEvaluaciones,alfaBLX,probCruceGeneracional,probMut,alfaTasas,sigmaDistNormal,1)
    elif tipo=="Memetico10-0.1":
        calidadMejorSolucion=generacionalBLX(poblacionInicial,particionValidacion,conjuntoEntrenamiento,random,tamanoPoblacion,numeroDeEvaluaciones,alfaBLX,probCruceGeneracional,probMut,alfaTasas,sigmaDistNormal,0.1)
    elif tipo=="Memetico10-0.1n":
        calidadMejorSolucion=generacionalBLX(poblacionInicial,particionValidacion,conjuntoEntrenamiento,random,tamanoPoblacion,numeroDeEvaluaciones,alfaBLX,probCruceGeneracional,probMut,alfaTasas,sigmaDistNormal,-1)

    print "Tasa de clasificacion: ", calidadMejorSolucion[0]
    print "Tasa de reduccion: ", calidadMejorSolucion[1]
    print "Tasa agregada: ", calidadMejorSolucion[2]
    final=time.time()
    print "Tiempo de ejecucion: ",final-inicio
    print "*****************************"



























