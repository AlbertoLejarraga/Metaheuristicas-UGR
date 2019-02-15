#include "problemcec2014.h"
#include "problem.h"
#include "random.h"
#include "srandom.h"
#include "domain.h"
#include "SoccerGameOptimization.h"
#include <iostream>
#include <ctime>

using namespace realea;


int main(int argc, char *argv[]) {
  int dim = 10;
  int fun = 1;
  int maxevals = 0;
  const unsigned popsize = 5;
  // pop is only used by cmaes using neighborhood to get the delta
  vector<tChromosomeReal> pop;
  
  DomainRealPtr domain;
  // It is a vector value
  tChromosomeReal sol(dim);
  ProblemCEC2014 cec2014(dim);
  string type_ls="SGO";

  // Init the random with the seed
  int seed=time(NULL);
  Random random(new SRandom(seed));

	for(int i=1;i<=30;i++){
		cout << "Probando funcion f" << i<<endl;
			// Get the function fun for dimension dim
	  ProblemPtr problem = cec2014.get(i);
	  // Domain is useful for clipping solutions
	  domain = problem->getDomain();
	  // Get the maximum evaluations from the problem
	  unsigned max_evals = problem->getMaxEval();
	  SoccerGameOptimization *sgo = new SoccerGameOptimization(dim);
	  
		sgo->setM(0.3);
		sgo->setL(0.05);
		sgo->setK(0.1);
		sgo->setAlfa(0.5);
		sgo->setNumTitulares(dim);
		sgo->setNumSuplentes(5);
		sgo->setProblem(problem.get());
		sgo->setRandom(&random);
	  

	  cout <<"Applying the '" <<type_ls <<"' search" <<endl;
	  /*
	  // The following options are common for all LS methods
	  // Set the problem to allow the LS to eval solutions
	  ls->setProblem(problem.get());
	  // Set the random to generate mutations
	  ls->setRandom(&random);
	  // Get the initial parameters
	  ls_options = ls->getInitOptions(sol);
	  // Set the maximum and minimum delta for the LS
	  // (init with the maximum delta value
*/
	  // Test with 10% of evaluations
	  unsigned evals_ls = max_evals;

	  // Eval the initial solution
	  tFitness fitness = problem->eval(sol);
	  tFitness before, after, diff;

	  before = fitness;
	  
	  // sol and fitness are updated
	  //unsigned evals = ls->apply(ls_options, sol, fitness, evals_ls);
	  unsigned evals = sgo->apply(sol, fitness, evals_ls);
	  // evals should be equals to evals_ls
	  if (evals_ls != evals) {
		cout <<"Max Evals " <<evals_ls <<", real evals " <<evals <<endl;
	  }

	  after = fitness;
	  //assert(!problem->isBetter(before, after));
	  diff = before-after;
	  cout <<"Improvement: " <<std::scientific <<before <<"->" <<std::scientific <<after;
	  cout <<" [" <<std::scientific <<diff <<"]" <<endl;
	  
	  
	}
  return 0;
}

