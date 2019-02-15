#include "SoccerGameOptimization.h"
using namespace realea;
SoccerGameOptimization :: SoccerGameOptimization(int dimension){
	dim=dimension;
}
SoccerGameOptimization :: ~SoccerGameOptimization(){
	delete [] jugSuplentes;
	delete [] jugTitulares;
}
void SoccerGameOptimization :: setMIni(float parM){
	mIni=parM;
}
void SoccerGameOptimization :: setMFin(float parM){
	mFin=parM;
}
void SoccerGameOptimization :: setLIni(float parL){
	lIni=parL;
}
void SoccerGameOptimization :: setLFin(float parL){
	lFin=parL;
}
void SoccerGameOptimization :: setK(float parK){
	k=parK;
}
void SoccerGameOptimization :: setAlfa(float parAlfa){
	alfa=parAlfa;
}

void SoccerGameOptimization :: setNumTitulares(int n){
	numTitulares=n;
	jugTitulares = new jugadorTitular[numTitulares];
}
void SoccerGameOptimization :: setNumSuplentes(int n){
	numSuplentes=n;
	jugSuplentes = new jugadorSuplente[numSuplentes];
}

void SoccerGameOptimization :: setRandom(Random *random){
	m_random = random;
}
void SoccerGameOptimization :: setEval(IEval *eval){
	m_eval = eval;
}
void SoccerGameOptimization :: setProblem(Problem *problem){
	m_problem = problem;
	setEval(problem);
}


void SoccerGameOptimization :: obtenerJugAleatorio(DomainRealPtr domain, tChromosomeReal &crom){
	tReal min, max;
	for (unsigned i = 0; i < crom.size(); ++i) {
		domain->getValues(i, &min, &max, true);
		crom[i] = m_random->randreal(min, max);
	}
}
//genera array de titulares y suplentes aleatoriamente y devuelve el indice del mejor titular
void SoccerGameOptimization :: generarEquipoInicial() {
	DomainRealPtr domain = m_problem->getDomain();//dominio del problema
	tChromosomeReal sol(dim);//jugador
	std::vector<tChromosomeReal> jugadores(numSuplentes+numTitulares);//array con todos los jugadores, despues se decidirán titulares y suplentes
	std::vector<tFitness> fitnessJug(numSuplentes+numTitulares);//array con fitness de los jugadores
	
	for(int i=0;i<numSuplentes+numTitulares;i++){//se rellena el array a partir de soluciones aleatorias
		obtenerJugAleatorio(domain,sol);
		jugadores[i]=sol;
		fitnessJug[i] = m_eval->eval(sol);
	}
	//creo un vector auxiliar igual que el del fitness de los jugadores
	std::vector<tFitness> fitnessAux(fitnessJug);
	//ordeno el vector de fitness de jugadores
	sort(fitnessJug.begin(),fitnessJug.end());
	//declaro un umbral para decidir los numTitulares titulares y numSuplentes suplentes
	tFitness umbral=fitnessJug[numTitulares];
	int introducidosTitulares=0;
	int introducidosSuplentes=0;
	//ahora introduzco cada jugador en su respectivo array en función de si son titulares o suplentes por su fitness7
	for(int i=0;i<jugadores.size();i++){
		if(m_problem->isBetter(fitnessAux[i], umbral)){
			jugadorTitular aux;
			aux.posicion=jugadores[i];
			aux.mejorPosEncontrada=jugadores[i];
			aux.fitness=fitnessAux[i];
			aux.fitnessMejorEnc=fitnessAux[i];
			jugTitulares[introducidosTitulares]=aux;
			introducidosTitulares++;
		}
		else{
			jugadorSuplente aux;
			aux.posicion=jugadores[i];
			aux.fitness=fitnessAux[i];
			jugSuplentes[introducidosSuplentes]=aux;
			introducidosSuplentes++;
		}
	}
}
int SoccerGameOptimization :: obtenerMejorJugador(){
	return 0;	
}
double SoccerGameOptimization :: distanciaEuclidea(tChromosomeReal crom1, tChromosomeReal crom2){
	double suma=0;
	for(int i=0;i<crom1.size();i++){
		suma+=pow(crom1[i]-crom2[i],2);
	}
	return sqrt(suma);
}
void SoccerGameOptimization :: hacerMoveForward(int pos,tChromosomeReal &poseedorDelBalon){
	double nuevoValor;
	for (int i = 0; i < dim; ++i) {
		nuevoValor= jugTitulares[pos].posicion[i];
		nuevoValor+= jugTitulares[pos].mejorPosEncontrada[i];
		nuevoValor+= poseedorDelBalon[i];
		jugTitulares[pos].posicion[i]= nuevoValor/3;
	}

	
}
void SoccerGameOptimization :: hacerMoveOff(int pos,int evaluaciones, unsigned maxEval, DomainRealPtr domain){
	tReal min, max;
	for (int i = 0; i < dim; i++) {
		domain->getValues(i, &min, &max, true);
		double aleatorio = m_random->randreal(0,1);
		double nuevoValor=jugTitulares[pos].posicion[i];
		double aleatorio2 = m_random->randreal(0,1);
		if(aleatorio<0.5)
			nuevoValor += (((float)max-jugTitulares[pos].posicion[i]) * (1-pow(aleatorio2,pow(1-(evaluaciones/maxEval),alfa))));
		else
			nuevoValor -= ((jugTitulares[pos].posicion[i]-(float)min) * (1-pow(aleatorio2,pow(1-(evaluaciones/maxEval),alfa))));
		jugTitulares[pos].posicion[i]=nuevoValor;
		if (jugTitulares[pos].posicion[i]>max) jugTitulares[pos].posicion[i] =max;
		else if (jugTitulares[pos].posicion[i] < min) jugTitulares[pos].posicion[i] = min;
		//cout << jugTitulares[pos].posicion[i] << "  ";
	}
}
void SoccerGameOptimization :: realizarSustituciones(){
	int indiceSup=0;
	int indiceTit=numTitulares-1;
	while(indiceSup<numSuplentes and indiceTit>=0){
		if(m_problem->isBetter(jugSuplentes[indiceSup].fitness, jugTitulares[indiceTit].fitness)){
			if (m_random->randreal(0,1)<=k){
				jugadorTitular auxTit;
				auxTit.posicion=jugSuplentes[indiceSup].posicion;
				auxTit.mejorPosEncontrada=jugSuplentes[indiceSup].posicion;
				auxTit.fitness=jugSuplentes[indiceSup].fitness;
				auxTit.fitnessMejorEnc=jugSuplentes[indiceSup].fitness;
				
				jugadorSuplente auxSup;
				auxSup.posicion = jugTitulares[indiceTit].mejorPosEncontrada;
				auxSup.fitness = jugTitulares[indiceTit].fitnessMejorEnc;
				
				jugTitulares[indiceTit]=auxTit;
				jugSuplentes[indiceSup]=auxSup;
				indiceSup++;
				indiceTit=numTitulares-1;
			}
			else indiceTit--;
		}
		else{
			indiceSup++;
			indiceTit=numTitulares-1;
		}
	}
}
void SoccerGameOptimization :: actualizarSuplentes(){
	int indiceSup=numSuplentes-1;
	int indiceTit=0;
	//se van comparando mejor titular con peor suplente, segundo mejor titular con segundo peor suplente,...
	//se modifican los suplentes si son mejores hasta que no haya titulares mejores==>salir
	while(indiceTit<numTitulares and indiceSup>=0){
		if(m_problem->isBetter(jugTitulares[indiceTit].fitness, jugSuplentes[indiceSup].fitness)){
			jugSuplentes[indiceSup].posicion= jugTitulares[indiceTit].posicion;
			jugSuplentes[indiceSup].fitness= jugTitulares[indiceTit].fitness;
			indiceSup--;
			indiceTit++;
		}
		else break;
	}
		
}
void SoccerGameOptimization :: ordenarJugadores(){
	std::sort(jugTitulares,jugTitulares+numTitulares);
	std::sort(jugSuplentes,jugSuplentes+numSuplentes);
}

double SoccerGameOptimization :: apply(tChromosomeReal &sol, tFitness &fitness, unsigned maxEval){
	//inicializar jugadores titulares y suplentes
	generarEquipoInicial();
	DomainRealPtr domain = m_problem->getDomain();//dominio del problema
	//determino el poseedor del balón como el índice del mejor jugador titular, al estar ordenado==>0
	ordenarJugadores();
	int poseedorDelBalon=0;
	tChromosomeReal cromPoseedor=jugTitulares[poseedorDelBalon].posicion;
	float m=mIni;
	float reduccion = (mIni-mFin)/(0.7*maxEval);
	float l=lIni;
	float aumentoL = (lFin-lIni)/(0.7*maxEval);
	int evaluaciones = numTitulares+numSuplentes;
	int totalEvaluaciones=0.7*maxEval;
	while(evaluaciones < totalEvaluaciones){
		for(int i=0;i<numTitulares;i++){//para cada jugador

			if(m_random->randreal(0, 1)<=m){//probabilidad de hacer moveOff
				hacerMoveOff(i,evaluaciones,maxEval,domain);
				if(m_random->randreal(0,1)<=l){ //probabilidad de hacer moveForward
					hacerMoveForward(i,cromPoseedor);
				}
			}
			else{
				hacerMoveForward(i,cromPoseedor);
			}
			jugTitulares[i].fitness= m_eval->eval(jugTitulares[i].posicion);
			
			
			evaluaciones++;
		}
		ordenarJugadores();
		
		
		realizarSustituciones();
		ordenarJugadores();
		//actualizar conocimiento de jugadores titulares
		for(int i=0;i<numTitulares;i++){
			if(m_problem->isBetter(jugTitulares[i].fitness, jugTitulares[i].fitnessMejorEnc)){
				jugTitulares[i].fitnessMejorEnc=jugTitulares[i].fitness;
				jugTitulares[i].mejorPosEncontrada=jugTitulares[i].posicion;
			}
		}
		cromPoseedor=jugTitulares[poseedorDelBalon].mejorPosEncontrada;
		//actualizar conocimiento de jugadores suplentes
		actualizarSuplentes();
		m-=(totalEvaluaciones/evaluaciones)*reduccion;
		l+=(totalEvaluaciones/evaluaciones)*aumentoL;
	}

	//ahora aplico localSearch
	ILocalSearch *ls;
	ILSParameters *ls_options;
	tFitness evaluacion;
	CMAESHansen *cmaes = new CMAESHansen("cmaesinit.par");
	cmaes->searchRange(0.1);
	ls = cmaes;
	ls->setProblem(m_problem);
	ls->setRandom(m_random);
	ls_options = ls->getInitOptions(jugTitulares[0].posicion); 
	unsigned evals = ls->apply(ls_options, jugTitulares[0].posicion, jugTitulares[0].fitness, maxEval-evaluaciones);
	//cout << "Despues: " << jugTitulares[0].fitness<<endl;
	
	return jugTitulares[0].fitness;
	/*fitness = jugTitulares[poseedorDelBalon].fitness;
	sol = jugTitulares[poseedorDelBalon].posicion;
	after = fitness;
	diff = before-after;
	cout <<"Improvement: " <<std::scientific <<before <<" -> " <<std::scientific <<after;
	cout <<" [" <<std::scientific <<diff <<"]" <<endl;
	return evaluaciones;*/
}



















