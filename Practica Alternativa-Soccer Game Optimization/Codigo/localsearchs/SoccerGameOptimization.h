#ifndef _SOCCERGAMEOPTIMIZATION_H
#define _SOCCERGAMEOPTIMIZATION_H

#include "problem.h"
#include "random.h"
#include "define.h"
#include <vector>
#include <limits>
#include <algorithm>
#include <math.h>
#include "localsearch.h"
#include "cmaeshan.h"

namespace realea {
	
	class SoccerGameOptimization {
		struct jugadorTitular{
			tChromosomeReal posicion;
			tChromosomeReal mejorPosEncontrada;
			tFitness fitness;
			tFitness fitnessMejorEnc;
			const bool operator < ( const jugadorTitular &jug ) const{
				return ( fitness < jug.fitness );
			}
			
		};
		struct jugadorSuplente{
			tChromosomeReal posicion;
			tFitness fitness;
			const bool operator < ( const jugadorSuplente &jug ) const{
				return ( fitness < jug.fitness );
			}
		};
		protected:
			Random *m_random; /**< The current randomgeneration numbers */
			IEval *m_eval; /** The current evaluation function */
			Problem *m_problem; /**< The current problem */
			float mIni; //parametro que discrimina entre realizar move off o forward
			float mFin;
			float lIni; //parametro que indica si se realizara move forward despues de move off
			float lFin;
			float k; //parametro que indica si se realizara o no la sustitucion de un jugador
			float alfa; //parametro de no uniformidad para el movimiento move off
			int numTitulares;
			int numSuplentes;
			int dim;

			jugadorTitular *jugTitulares;
			jugadorSuplente *jugSuplentes;//arrays de jugadores titulares y suplentes
			
		public:
			SoccerGameOptimization(int dimension);
			~SoccerGameOptimization();
			void setMIni(float parM); 
			void setMFin(float parM);
			void setLIni(float parL);
			void setLFin(float parL);
			void setK(float parK);
			void setAlfa(float parAlfa);
			void setNumTitulares(int n);
			void setNumSuplentes(int n);
			
			void setRandom(Random *random);
			void setEval(IEval *eval);
			void setProblem(Problem *problem);
			
			void generarEquipoInicial();
			double apply(tChromosomeReal &sol, tFitness &fitness, unsigned maxEval);
			void obtenerJugAleatorio(DomainRealPtr domain, tChromosomeReal &crom);
			int obtenerMejorJugador();
			double distanciaEuclidea(tChromosomeReal crom1, tChromosomeReal crom2);
			
			void hacerMoveOff(int posicion,int evaluaciones, unsigned maxEval, DomainRealPtr domain);//hecho
			void hacerMoveForward(int posicion,tChromosomeReal &poseedorDelBalon);//hecho
			void realizarSustituciones();
			void actualizarSuplentes();
			void ordenarJugadores();
			bool compararMenorT(jugadorTitular jug1, jugadorTitular jug2);
			bool compararMenorS(jugadorSuplente jug1, jugadorSuplente jug2);
			

	};
}



#endif //SOCCERGAMEOPTIMIZATION_H