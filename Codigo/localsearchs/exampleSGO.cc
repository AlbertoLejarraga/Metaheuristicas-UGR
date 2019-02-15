#include "problemcec2014.h"
#include "problem.h"

#include "random.h"
#include "srandom.h"
#include "domain.h"
#include "assert.h"
#include "SoccerGameOptimization.h"
#include <iostream>

using namespace realea;

void getInitRandom(Random *random, DomainRealPtr domain, tChromosomeReal &crom) {
  tReal min, max;
    
  for (unsigned i = 0; i < crom.size(); ++i) {
      domain->getValues(i, &min, &max, true);
      crom[i] = random->randreal(min, max);
  }

}

int main(int argc, char *argv[]) {
  int fun;
  
  DomainRealPtr domain;

  // It is a vector value
  
  int dim=10;

  // Init the random with the seed
  int seed=time(NULL);
  Random random(new SRandom(seed));

  if (argc > 1) {
     dim = atoi(argv[1]);
	 cout << dim;
     assert(dim == 10 || dim == 30 || dim == 50);
  }
  tChromosomeReal sol(dim);
  ProblemCEC2014 cec2014(dim);
	int veces=25;
  
	for(int i=1;i<=20;i++){
		double suma=0;
		cout << "Funcion " << i<<endl;
		for(int j =0;j<veces;j++){
			
			
		  // Get the function fun for dimension dim
		  ProblemPtr problem = cec2014.get(i);
		  // Domain is useful for clipping solutions
		  domain = problem->getDomain();
		  // Init the initial solution (for LS)
		  getInitRandom(&random, domain, sol);
		  // Get the maximum evaluations from the problem
		  unsigned max_evals = problem->getMaxEval();
		  SoccerGameOptimization *sgo = new SoccerGameOptimization(dim);
		sgo->setMIni(0.8);
		sgo->setMFin(0.4);//0.4
		sgo->setLIni(0.1);
		sgo->setLFin(0.3);//0.3
		sgo->setK(0.15);
		sgo->setAlfa(0.2);
		sgo->setNumTitulares(1.1*dim);
		sgo->setNumSuplentes(0.4*dim);
		sgo->setProblem(problem.get());
		sgo->setRandom(&random);
		  
			unsigned evals_ls = max_evals;
			tFitness before, after, diff,fitness;
			double valor = sgo->apply(sol, fitness, evals_ls);
			suma += valor/veces;
		}
		cout << "Media de " << veces << " ejecuciones: " << suma <<endl;
	}  
	

	  
  return 0;
}

