% Optimization smallest sum over feature complexities
#minimize { C,complexity(F, C) : complexity(F, C), feature(F), select(F) }.

% Generate selected features
{ select(F) } :- feature(F).

{ good(C) } :- equivalence(C).
% All suboptimal transitions are bad
:- good(C), not_delta_optimal(I, C, S, _), alive(I, S).
% At least one good optimal transiton
:- { good(C) : delta_optimal(I, C, S, _) } = 0, alive(I, S).

% D2-separation
:- good(C), not good(C'), d2_separate(C, C'), equivalence(C), equivalence(C'), { feature(F) : select(F), feature_effect(F, C, V), feature_effect(F, C', V'), V != V' } = 0, { feature(F) : select(F), feature_condition(F, C, V), feature_condition(F, C', V'), V != V' } = 0.

% Goal-separation
:- nongoal(I, S), goal(I, S'), { feature(F) : select(F), value(I, S, F, V), value(I, S', F, V'), V != V' } = 0.

% Display
#show select/1.
#show numerical/1.
#show boolean/1.
#show good/1.
#show feature_condition/3.
#show feature_effect/3.
