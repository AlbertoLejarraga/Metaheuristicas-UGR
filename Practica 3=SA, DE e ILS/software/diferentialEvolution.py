__author__ = 'alberto'
import os
import utilidades
import time
#para utilizar la misma poblacion inicial en los distintos algoritmos la guardo en un fichero y la extraigo de ahi
def generarPoblacionInicial(setEjemplos,nombreSet,random,tamanoPoblacion,particionValidacion, conjuntoEntrenamiento,alfa):
    if not os.path.isfile("data\\poblacionInicialDE"+nombreSet+".txt"):
        with open("data\\poblacionInicialDE"+nombreSet+".txt",'w') as fichero:
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
        with open("data\\poblacionInicialDE"+nombreSet+".txt",'r') as fichero:
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

def seleccionarPadres(prohibido,random,poblacion,tamanoPoblacion,tipo="Rand"):
    #selecciono los padres aleatoriamente verificando que no esten repetidos y no sean el actual
    indicePadre1=random.randInt(0,tamanoPoblacion-1)
    while(indicePadre1==prohibido): indicePadre1=random.randInt(0,tamanoPoblacion-1)

    indicePadre2=random.randInt(0,tamanoPoblacion-1)
    while(indicePadre2==prohibido or indicePadre2==indicePadre1): indicePadre2=random.randInt(0,tamanoPoblacion-1)

    if tipo=="Rand":
        indicePadre3=random.randInt(0,tamanoPoblacion-1)
        while(indicePadre3==prohibido or indicePadre3==indicePadre2 or indicePadre3==indicePadre1): indicePadre3=random.randInt(0,tamanoPoblacion-1)

        return poblacion[indicePadre1], poblacion[indicePadre2], poblacion[indicePadre3]
    else: return poblacion[indicePadre1], poblacion[indicePadre2]

def lanzarRand(particionValidacion,conjuntoEntrenamiento,poblacionInicial,random,tamanoPoblacion,numeroDeEvaluaciones,alfaTasas,sigmaDistNormal,F,probCruce):
    contador=tamanoPoblacion
    poblacionActual=poblacionInicial
    while(contador<numeroDeEvaluaciones):
        resultadoIteracion=[]
        for i in range(tamanoPoblacion):
            #selecciono los padres teniendo en cuenta las restricciones
            padre1,padre2,padre3=seleccionarPadres(i,random,poblacionActual,tamanoPoblacion)
            resultadoCruce=[]
            #se recorren todos los genes y se decide si se mutan
            for j in range(poblacionActual[i].__len__()-2):
                if random.rand()<probCruce:
                    resultadoCruce.append(padre1[j]+F*(padre2[j]-padre3[j]))
                    if resultadoCruce[j]>1:resultadoCruce[j]=1
                    elif resultadoCruce[j]<0:resultadoCruce[j]=0
                else:
                    resultadoCruce.append(poblacionActual[i][j])
            #anado marcas de no ser el mejor de la poblacion y su fitness
            resultadoCruce.append(False)
            resultadoCruce.append(utilidades.evaluarSolucion(resultadoCruce,particionValidacion,conjuntoEntrenamiento,alfaTasas)[2])
            #aumento el contador de numero de evaluaciones e incluyo el nuevo cromosoma en el resultado de la iteracion
            contador+=1
            resultadoIteracion.append(resultadoCruce)
        for i in range(tamanoPoblacion):
            if resultadoIteracion[i][-1]>poblacionActual[i][-1]:
                poblacionActual[i]=resultadoIteracion[i]
            contador+=2
    return poblacionActual

def obtenerMejorSolucion(poblacion,particionValidacion, conjuntoEntrenamiento, alfaTasas):
    mejorTasa=0
    mejorSolucion=[]
    #recorro la poblacion hasta encontrar la mejor solucion
    for solucion in poblacion:
        if(solucion[-1]>mejorTasa):
            mejorTasa= solucion[-1]
            mejorSolucion=solucion
    #vuelvo a evaluar la mejor solucion para obtener el resto de tasas
    return utilidades.evaluarSolucion(mejorSolucion,particionValidacion,conjuntoEntrenamiento,alfaTasas)

def lanzarCTB(particionValidacion,conjuntoEntrenamiento,poblacionInicial,random,tamanoPoblacion,numeroDeEvaluaciones,alfaTasas,sigmaDistNormal,F,probCruce):
    contador=tamanoPoblacion
    poblacionActual=poblacionInicial
    tasaMejorSol=0
    indMejorSol=1000
    #recorro la poblacion hasta encontrar la mejor solucion
    for solucion in range(tamanoPoblacion):
        if(poblacionActual[solucion][-1]>tasaMejorSol):
            tasaMejorSol= poblacionActual[solucion][-1]
            indMejorSol=solucion
    while(contador<numeroDeEvaluaciones):
        resultadoIteracion=[]
        for i in range(tamanoPoblacion):
            #selecciono los padres teniendo en cuenta las restricciones
            padre1,padre2=seleccionarPadres(i,random,poblacionActual,tamanoPoblacion,"CTB")
            resultadoCruce=[]
            #se recorren todos los genes y se decide si se mutan
            for j in range(poblacionActual[i].__len__()-2):
                aleatorio=random.rand()
                if aleatorio<probCruce:
                    resultadoCruce.append(poblacionActual[i][j]+F*(poblacionActual[indMejorSol][j]-poblacionActual[i][j])+F*(padre1[j]-padre2[j]))
                    if resultadoCruce[j]>1:resultadoCruce[j]=1
                    elif resultadoCruce[j]<0:resultadoCruce[j]=0
                else:
                    resultadoCruce.append(poblacionActual[i][j])

            #anado marcas de no ser el mejor de la poblacion y su fitness
            resultadoCruce.append(False)
            resultadoCruce.append(utilidades.evaluarSolucion(resultadoCruce,particionValidacion,conjuntoEntrenamiento,alfaTasas)[2])
            #aumento el contador de numero de evaluaciones e incluyo el nuevo cromosoma en el resultado de la iteracion
            contador+=1
            resultadoIteracion.append(resultadoCruce)
        tasaMejorSol=0
        indMejorSol=10000
        for i in range(tamanoPoblacion):
            if resultadoIteracion[i][-1]>poblacionActual[i][-1]:
                poblacionActual[i]=resultadoIteracion[i]
            if(poblacionActual[i][-1]>tasaMejorSol):
                tasaMejorSol= poblacionActual[i][-1]
                indMejorSol=i
            contador+=3
    return poblacionActual





def lanzar(setEjemplos,nombreSet,random,tipo,tamanoPoblacion=50,numeroDeEvaluaciones=15000,alfaTasas=0.5,sigmaDistNormal=0.3,F=0.5,probCruce=0.5):
    particionValidacion=setEjemplos[-1]
    conjuntoEntrenamiento=setEjemplos[1:-1]
    poblacionInicial=generarPoblacionInicial(setEjemplos,nombreSet,random,tamanoPoblacion,particionValidacion,conjuntoEntrenamiento,alfaTasas)
    #Dependiendo del tipo elegido se llama al metodo de evolucion diferencial seleccionando al mejor o uno aleatoriamente para cruzar en cada iteracion
    inicio=time.time()
    poblacionFinal=[]
    if tipo=="rand": poblacionFinal=lanzarRand(particionValidacion,conjuntoEntrenamiento,poblacionInicial,random,tamanoPoblacion,numeroDeEvaluaciones,alfaTasas,sigmaDistNormal,F,probCruce)
    else: poblacionFinal=lanzarCTB(particionValidacion,conjuntoEntrenamiento,poblacionInicial,random,tamanoPoblacion,numeroDeEvaluaciones,alfaTasas,sigmaDistNormal,F,probCruce)

    calidadMejorSolucion=obtenerMejorSolucion(poblacionFinal,particionValidacion,conjuntoEntrenamiento,alfaTasas)

    final=time.time()
    print "Tasa de clasificacion: ", calidadMejorSolucion[0]
    print "Tasa de reduccion: ", calidadMejorSolucion[1]
    print "Tasa agregada: ", calidadMejorSolucion[2]
    final=time.time()
    print "Tiempo de ejecucion: ",final-inicio
    print "*****************************"





























