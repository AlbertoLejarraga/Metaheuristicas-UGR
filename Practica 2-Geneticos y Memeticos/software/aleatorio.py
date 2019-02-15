__author__ = 'adaptacion generador aleatorio C++ de sci2s'

class Random:
    #inicializar la semilla  con el valor dado y las constantes necesarias
    def __init__(self, semilla):
        self.__mascara=2147483647
        self.__primo=65539
        self.__escala=0.4656612875e-9
        self.__semilla=long(semilla)
    #devuelve el valor de la semilla
    def get_random(self):
        return self.__semilla
    #generar un aleatorio real en el intervalo [0,1)
    def rand(self):
        self.__semilla=(self.__semilla * self.__primo) & self.__mascara
        return self.__semilla * self.__escala
    #genera un aleatorio entero en el intervalo [x,y]
    def randInt(self, x,y):
        return int(x + ((y-x+1) * self.rand()))
    #genera un aleatorio real en el intervalo [x,y)
    def randFloat(self,x,y):
        return x + ((y-x) * self.rand())