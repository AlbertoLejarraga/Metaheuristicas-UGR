En la carpeta data se encuentran las poblaciones iniciales, que se pueden borrar para generarlas de nuevo, aunque siempre ser�n las mismas como se detalla en el documento


aleatorio.py: en este fichero creo una clase �Random� que es una adaptaci�n a Python de la clase �Random� para C++ colgada en la web de la asignatura. El nombre de las funciones es pr�cticamente el mismo y simplemente he �traducido� este c�digo original para poder utilizarlo con este lenguaje. 

utilidades.py: aqu� introduzco los m�todos que aparecen en el apartado 3 de este documento, es decir, los m�todos comunes a los distintos algoritmos como pueden ser el c�lculo de distancias, el clasificador o el evaluador de una soluci�n, as� como los m�todos necesarios para leer los ficheros en el �main� e inicializar las listas de datos.

relief.py: en este archivo est�n implementados los m�todos necesarios para ejecutar desde el �main� el algoritmo �Relief� y el algoritmo 1-NN simple.

buscLocal.py: en este caso los m�todos los m�todos que aparecen son los utilizados para lanzar el algoritmo de b�squeda local.

main.py: es el programa principal desde el que se llama a los m�todos antes descritos, preguntar� por la semilla utilizada. Yo he utilizado mi fecha de nacimiento 15041995

geneticos.py: archivo con los distintos algoritmos gen�ticos realizados