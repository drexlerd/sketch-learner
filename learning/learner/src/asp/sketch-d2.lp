% Optimization smallest sum over feature complexities
#minimize { C@2,complexity(F, C) : complexity(F, C), feature(F), select(F) }.

% Generate selected features
{ select(F) } :- feature(F).

% Generate good equivalence classes
{ good(C) } :- state_pair_class(C).

% Define R-reachable states, base and inductive case
r_reachable(I, S) :- initial(I, S).
r_reachable(I, S') :- D = D', r_reachable(I, S), good(I, S, S'), subgoal_distance(I, S, D), s_distance(I, S, S', D).

% Define a distance from which to pick at least one subgoal tuple for each R-reachable state
{ subgoal_distance(I, S, D) : t_distance(I, S, _, D) } != 0 :- r_reachable(I, S), nongoal(I, S).

% Require unsolvable state to not be R-reachable.
:- unsolvable(I, S), r_reachable(I, S).

% Define at least one subgoal tuple at the selected distance.
{ subgoal(I, S, T) : t_distance(I, S, T, D) } != 0 :- subgoal_distance(I, S, D), r_reachable(I, S).

% Require that all equivalence classes C underlying a tuple T of subproblem P[S] are good, effectively bounding the width of P[S]
:- not good(C), subgoal(I, S, T), contain(I, S, T, C).
% (Optimal-width): Require solvable states S' closer than subgoal to not be assigned to any rule.
:- D < D', r_distance(I, S, C, D), subgoal_distance(I, S, D'), good(C).

% Require D2-separation
:- good(C), not good(C'), d2_separate(C, C'), state_pair_class(C), state_pair_class(C'), { feature(F) : select(F), feature_effect(C, F, V), feature_effect(C', F, V'), V != V' } = 0, { feature(F) : select(F), feature_condition(C, F, V), feature_condition(C', F, V'), V != V' } = 0.


% Define ``good`` pairs of state classes similar
good(I, S, S') :- good(C), cover(I, S, S', C).
% (Termination): Sketch must define strict partial order over R-reachable states
% Source of this formulation: https://users.aalto.fi/~rintanj1/papers/GebserJR14kr.pdf
order(I, S, S') :- r_reachable(I, S), r_reachable(I, S'), nongoal(I, S), good(I, S, S'), order(I, S').
order(I, S) :- r_reachable(I, S), order(I, S, S') : good(I, S, S'), r_reachable(I, S), r_reachable(I, S'), nongoal(I, S).
:- r_reachable(I, S), nongoal(I, S), not order(I, S).

% Display
#show select/1.
#show numerical/1.
#show boolean/1.
#show good/1.
#show feature_condition/3.
#show feature_effect/3.
