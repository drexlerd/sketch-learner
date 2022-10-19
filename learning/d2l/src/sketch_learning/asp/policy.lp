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
%:- nongoal(S), goal(S'), { feature(F) : select(F), value(S, F, V), value(S', F, V'), V != V' } = 0.

% TODO: depending on select features, state pair classes of multiple states fall together
% effectively undirecte
% Define ``good`` pairs of state classes similar
good(D, D') :- good(C), state_pair_class_contains(C, D, D').
% (Termination): Sketch must define strict partial order over R-reachable states
% Source of this formulation: https://users.aalto.fi/~rintanj1/papers/GebserJR14kr.pdf
order(D, D') :- state_class(D), state_class(D'), good(D, D'), order(D').
order(D) :- state_class(D), order(D, D') : good(D, D'), state_class(D), state_class(D').
:- state_class(D), not order(D).

% Display
#show good/1.
#show select/1.
#show numerical/1.
#show boolean/1.
#show good/1.
#show feature_condition/3.
#show feature_effect/3.
