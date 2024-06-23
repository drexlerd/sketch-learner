% Optimization smallest sum over feature complexities
#minimize { C@2,complexity(F, C) : complexity(F, C), feature(F), select(F) }.

% Generate selected features
{ select(F) } :- feature(F).

% Generate good equivalence classes
{ good(C) } :- state_pair_class(C).

% Define R-reachable states, base and inductive case
r_reachable(S) :- initial(S).
r_reachable(S') :- D = D', r_reachable(S), good(S, S'), subgoal_distance(S, D), s_distance(S, S', D).

% Define a distance from which to pick at least one subgoal tuple for each R-reachable state
{ subgoal_distance(S, D) : t_distance(S, _, D) } != 0 :- r_reachable(S), nongoal(S).

% Require unsolvable state to not be R-reachable.
:- unsolvable(S), r_reachable(S).

% Define at least one subgoal tuple at the selected distance.
{ subgoal(S, T) : t_distance(S, T, D) } != 0 :- subgoal_distance(S, D), r_reachable(S).

% Require that all equivalence classes C underlying a tuple T of subproblem P[S] are good, effectively bounding the width of P[S]
:- not good(C), subgoal(S, T), contain(S, T, C).
% (Optimal-width): Require solvable states S' closer than subgoal to not be assigned to any rule.
:- D < D', r_distance(S, C, D), subgoal_distance(S, D'), good(C).

% Require D2-separation
% :- good(C), not good(C'), d2_separate(C, C'), state_pair_class(C), state_pair_class(C'), { feature(F) : select(F), feature_effect(C, F, V), feature_effect(C', F, V'), V != V' } = 0, { feature(F) : select(F), feature_condition(C, F, V), feature_condition(C', F, V'), V != V' } = 0.
:- good(C), not good(C'), state_pair_class(C), state_pair_class(C'), { feature(F) : select(F), feature_effect(C, F, V), feature_effect(C', F, V'), V != V' } = 0, { feature(F) : select(F), feature_condition(C, F, V), feature_condition(C', F, V'), V != V' } = 0.


% Define ``good`` pairs of state classes similar
good(S, S') :- good(C), cover(S, S', C).
% (Termination): Sketch must define strict partial order over R-reachable states
% Source of this formulation: https://users.aalto.fi/~rintanj1/papers/GebserJR14kr.pdf
order(S, S') :- r_reachable(S), r_reachable(S'), nongoal(S), good(S, S'), order(S').
order(S) :- r_reachable(S), order(S, S') : good(S, S'), r_reachable(S), r_reachable(S'), nongoal(S).
:- r_reachable(S), nongoal(S), not order(S).

% Display
#show select/1.
#show numerical/1.
#show boolean/1.
#show good/1.
#show feature_condition/3.
#show feature_effect/3.
