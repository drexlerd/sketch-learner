% Optimization smallest sum over feature complexities
#minimize { C,complexity(F, C) : complexity(F, C), feature(F), select(F) }.

% Generate selected features
{ select(F) } :- feature(F).

{ good(C) } :- equivalence(C).
% All suboptimal transitions are bad
:- good(C), not_delta_optimal(I, C, S, _), expanded(I, S).
% At least one good optimal transiton
:- { good(C) : delta_optimal(I, C, S, _) } = 0, expanded(I, S).

% D2-separation
:- good(C), not good(C'), equivalence(C), equivalence(C'), { feature(F) : select(F), change(F, C, V), change(F, C', V'), V != V' } = 0.

% Goal-separation
:- nongoal(I, S), goal(I, S'), { feature(F) : select(F), value(I, S, F, V), value(I, S', F, V'), V != V' } = 0.

% Display
#show select/1.
#show numerical/1.
#show boolean/1.
#show good/1.
#show c_n_eq/2.
#show c_n_gt/2.
#show c_b_pos/2.
#show c_b_neg/2.
#show e_b_pos/2.
#show e_b_neg/2.
#show e_b_bot/2.
#show e_n_dec/2.
#show e_n_inc/2.
#show e_n_bot/2.
