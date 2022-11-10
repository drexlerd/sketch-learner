% Optimization smallest sum over feature complexities
#minimize { C,complexity(F, C) : complexity(F, C), feature(F), select(F) }.

% Generate selected features
{ select(F) } :- feature(F).

% Generate exactly one subgoal for each solvable state for which the width exceeds.
{ subgoal(I, S, T) : tuple(I, S, T) } = 1 :- initial(I, S).
% Generate good equivalence classes
{ good(C) } :- state_pair_class(C).

% Require that all equivalence classes C underlying a tuple T of subproblem P[S] are good, effectively bounding the width of P[S]
:- not good(C), subgoal(I, S, T), contain(I, S, T, C).
% Require unsolvable states S' as close as subgoal to not be assigned to any rule.
:- D <= D', d_distance(I, S, C, D), t_distance(I, S, T, D'), subgoal(I, S, T), good(C).
% (Optimal-width): Require solvable states S' closer than subgoal to not be assigned to any rule.
:- D < D', r_distance(I, S, C, D), t_distance(I, S, T, D'), subgoal(I, S, T), good(C).
% Require that goal feature valuations are minimal
% :- good(C), cover(I, S, S', C), nongoal(I, S), goal(I, S).

% D2-separation
:- good(C), not good(C'), d2_separate(C, C'), state_pair_class(C), state_pair_class(C'), { feature(F) : select(F), feature_effect(F, C, V), feature_effect(F, C', V'), V != V' } = 0, { feature(F) : select(F), feature_condition(F, C, V), feature_condition(F, C', V'), V != V' } = 0.

% Goal-separation no possible with current pool, because decrement can mean 2->0, 2->1
% Hence one would need seed features that reflect feature change.
:- nongoal(I', S), goal(I, S'), { feature(F) : select(F), value(I', S, F, V), value(I, S', F, V'), V != V' } = 0.

% Define ``good`` pairs of state classes similar
good(I, S, S') :- good(C), cover(I, S, S', C).
% (Termination): Sketch must define strict partial order over R-reachable states
% Source of this formulation: https://users.aalto.fi/~rintanj1/papers/GebserJR14kr.pdf
order(I, S, S') :- good(I, S, S'), order(I, S'), state(I, S), state(I, S').
order(I, S) :- state(I, S), order(I, S, S') : good(I, S, S'), state(I, S), state(I, S').
:- state(I, S), not order(I, S).

% Display
#show select/1.
#show numerical/1.
#show boolean/1.
#show good/1.
#show feature_condition/3.
#show feature_effect/3.
