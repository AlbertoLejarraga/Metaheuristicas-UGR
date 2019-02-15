__author__ = 'alberto'
import utilidades
import sys
import time

def obtenerPeso(lista):
    #creo una lista del tamano del numero de parametros de los ejemplos llena de ceros
    W=[0 for i in range(lista[0].__len__()-1)]
    #creo una lista con los ejemplos de entrenamiento(particiones 1,2,3,4)
    ejemplosEntreno=[]
    for particion in lista[1:-1]:
        for ejemplo in particion:
            ejemplosEntreno.append(ejemplo)
    #para cada ejemplo del conjunto de entreno busco el amigo y enemigo mas cercano
    for ejemplo in range(ejemplosEntreno.__len__()):
        distanciaMinEnemigo=sys.maxint
        distanciaMinAmigo=sys.maxint
        for ejemploOtraVez in range(ejemplosEntreno.__len__()):
            if ejemploOtraVez!=ejemplo:
                distancia=utilidades.distanciaEuclidea(ejemplosEntreno[ejemplo][:-1],ejemplosEntreno[ejemploOtraVez][:-1])
                #si son de la misma clase(amigos)
                if(ejemplosEntreno[ejemplo][-1]==ejemplosEntreno[ejemploOtraVez][-1]):
                    if distancia<distanciaMinAmigo:
                        amigoMasCercano=ejemplosEntreno[ejemploOtraVez]
                        distanciaMinAmigo=distancia
                else:#distinta clase
                    if distancia<distanciaMinEnemigo:
                        enemigoMasCercano=ejemplosEntreno[ejemploOtraVez]
                        distanciaMinEnemigo=distancia
        #encontrados amigo y enemigo actualizo vector W
        for i in range(W.__len__()):
            W[i] += abs(ejemplosEntreno[ejemplo][i]-enemigoMasCercano[i]) - abs(ejemplosEntreno[ejemplo][i]-amigoMasCercano[i])
    #normalizo W en funcion del maximo valor de W
    maxValW=max(W)
    for dato in range(W.__len__()):
        if(W[dato]<0): W[dato]=0
        else:          W[dato]=W[dato]/maxValW
    return W


def lanzar(setEjemplos, conPesos=True):
    inicio=time.time()

    #obtengo el vector de pesos, con la funcion para el metodo relief con con vector de "unos" si el metodo es 1nn
    if conPesos: WSet=obtenerPeso(setEjemplos)
    else: WSet=[1 for ejemplo in range(setEjemplos[0].__len__()-1)]

    #Evaluo la solucion obtenida y muestro las tasas resultantes
    tasas=utilidades.evaluarSolucion(WSet, setEjemplos[-1],setEjemplos[1:-1])

    print "Tasa de clasificacion: ", tasas[0]
    print "Tasa de reduccion: ", tasas[1]
    print "Tasa agregada: ", tasas[2]

    final=time.time()
    print "Tiempo de ejecucion: ",final-inicio
    print "*****************************"
    return WSet

