# dpll

A simple implementation of DPLL. Input data is required to be in disjunctive normal form.
The dpll algorithm returns True if we found values that makes that satisfy every clause, False in the other cases. 

dpll() uses Depth First Search and alternate between three tactics:

--> Look for unitary clauses (clauses of one element)
--> Look for pure lits variable
--> Randomly assign boolean value to the variables. 

Bactracking is used when a dead end is found (i.e the clauses are unsatisfiable)

All the test inputs are in .cnf format
