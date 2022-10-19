% Optimization smallest sum over feature complexities
#minimize { C,complexity(F, C) : complexity(F, C), feature(F), select(F) }.

% Generate selected features Phi from F
{ select(F) } :- feature(F).
% Generate selected rules over F
{ good(C) } :- state_pair_class(C).
% Generate R-reachable states
{ r_reachable(I, S) } :- state(I, S).

% initial state is R-reachable
:- not r_reachable(I, S), initial(I, S).
% require at least one outgoing good for each alive R-reachable state.
:- { good(C) : cover(I, S, _, C) } = 0, r_reachable(I, S), alive(I, S).
% require S' to be R-reachable if there is good state pair (S,S') from R-reachable state S.
:- not r_reachable(I, S'), r_reachable(I, S), good(C), cover(I, S, S', C).

% D2-separation
:- good(C), not good(C'), d2_separate(C, C'), state_pair_class(C), state_pair_class(C'), { feature(F) : select(F), feature_effect(F, C, V), feature_effect(F, C', V'), V != V' } = 0, { feature(F) : select(F), feature_condition(F, C, V), feature_condition(F, C', V'), V != V' } = 0.

% Goal-separation no possible with current pool, because decrement can mean 2->0, 2->1
% Hence one would need seed features that reflect feature change.
%:- nongoal(I, S), goal(I, S'), { feature(F) : select(F), value(I, S, F, V), value(I, S', F, V'), V != V' } = 0.

% Define ``good`` pairs of state classes similar
good(I, S, S') :- good(C), cover(I, S, S', C).
% (Termination): Sketch must define strict partial order over R-reachable states
% Source of this formulation: https://users.aalto.fi/~rintanj1/papers/GebserJR14kr.pdf
order(I, S, S') :- good(I, S, S'), order(I, S'), state(I, S), state(I, S').
order(I, S) :- state(I, S), order(I, S, S') : good(I, S, S'), state(I, S), state(I, S').
:- state(I, S), not order(I, S).

% Display
#show good/1.
#show select/1.
#show numerical/1.
#show boolean/1.
#show good/1.
#show feature_condition/3.
#show feature_effect/3.
