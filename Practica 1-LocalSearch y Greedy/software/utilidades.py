__author__ = 'alberto'
import arff
import sys
import math



ficheros={"ozono":"ozone-320.arff",
      "parkinson":"parkinsons.arff",
      "corazon":"spectf-heart.arff"}
def repartirClase(etiqueta, particiones=5):
    #devolvera una lista con <particiones>+1 listas, siendo la primera los nombres de los atributos
    #  y las demas las particiones de ejemplos balanceadas
    #obtengo los datos del fichero
    data = arff.load(open("data\\"+ficheros[etiqueta], "r"))
    atributos=data['attributes']
    datos=data['data']
    listaResul=[]
    lista=[]
    #anado a resul los atributos
    for i in range(atributos.__len__()):
        lista.append(atributos[i])
    listaResul.append(lista)
    #anado a resul <particiones> sublistas y las empiezo a rellenar de forma que se meta un ejemplo en cada particion
    # , teniendo en cuenta si son de una clase y otra
    numClases=atributos[-1][1].__len__()
    meterClase=[]#tendra el tamano del numero de clases e indicara para cada clase a que particion hay que meter el siguiente ejemplo
    for i in range(numClases):meterClase.append(0)
    for i in range(particiones):
        listaResul.append([])
    #random.shuffle(datos)
    for i in range(datos.__len__()):
        listaResul[meterClase[int(datos[i][-1])-1]+1].append(datos[i])
        meterClase[int(datos[i][-1])-1]=(meterClase[int(datos[i][-1])-1]+1)%particiones

    return listaResul

def normalizar(lista):
    #obtengo en minimos y maximos el minimo y maximo valor de cada valor de todo el conjunto de datos
    minimos=[sys.maxint for i in range(lista[1][1].__len__()-1)]
    maximos=[-sys.maxint-1 for i in range(lista[1][1].__len__()-1)]
    listaResul=[]
    listaResul.append(lista[0])

    for ejemplos in lista[1:]:
        for ejemplo in ejemplos:
            for i in range(ejemplo.__len__()-1):
                if ejemplo[i]>maximos[i]: maximos[i]=ejemplo[i]
                if ejemplo[i]<minimos[i]: minimos[i]=ejemplo[i]
    #a partir de los maximos valores normalizo con la formula [(ejemplo[i]-minimos[i])/(maximos[i]-minimos[i])]
    for ejemplos in lista[1:]:
        listado=[]
        for ejemplo in ejemplos:
            listaAux=[]
            for i in range(ejemplo.__len__()-1):
                listaAux.append((ejemplo[i]-minimos[i])/(maximos[i]-minimos[i]))
            listaAux.append(ejemplo[-1])
            listado.append(listaAux)
        listaResul.append(listado)
    return listaResul


#metodo que devuelve la distancia euclidea de dos elementos
def distanciaEuclidea(elemento1,elemento2):
    suma=0
    for i in range(elemento1.__len__()):
        suma+=pow(elemento1[i]-elemento2[i],2)
    return math.sqrt(suma)

#devuelve la distancia entre los elementos de elemento1 y 2 teniendo en cuenta el peso
def distPonderada(elemento1, elemento2, pesos):
    suma=0
    for i in range(elemento1.__len__()-1):
        if pesos[i]>=0.2:
            suma+= pesos[i] * pow(elemento1[i]-elemento2[i],2)
    return math.sqrt(suma)

#devuelve las tasas de clasificacion, reduccion y agregada en funcion de alfa
def evaluarSolucion(pesos, particion, conjuntoEntrenamiento, alfa=0.5):
    aciertos=0
    for ejemplo in particion:
        aciertos+=clasificador(pesos,ejemplo, conjuntoEntrenamiento)

    tasa_clas=100.0*aciertos/(particion.__len__())
    suma=0
    for valor in pesos:
        if valor<0.2:suma+=1
    tasa_red=100.0*suma/pesos.__len__()
    return [tasa_clas, tasa_red, alfa * tasa_clas + (1 - alfa) * tasa_red]

#recibido el vector de pesos, un ejemplo y un conjunto de entreno devuelve 1 si se acierta la clasificacion y 0 si se falla
def clasificador(vectorPesos, ejemploAClasificar, conjuntoEntrenamiento):
    distanciaMinima=sys.maxint
    #para cada ejempo del conjunto de entreno se busca el mas cercano al ejemplo a clasificar
    for particion in range(conjuntoEntrenamiento.__len__()):
        for ejemplo in range(conjuntoEntrenamiento[particion].__len__()):
            distancia=distPonderada(ejemploAClasificar, conjuntoEntrenamiento[particion][ejemplo][:-1],vectorPesos)
            if distancia < distanciaMinima:
                distanciaMinima=distancia
                ejemploMasCercano=conjuntoEntrenamiento[particion][ejemplo]
    if ejemploMasCercano[-1]==ejemploAClasificar[-1]: return 1
    else: return 0

