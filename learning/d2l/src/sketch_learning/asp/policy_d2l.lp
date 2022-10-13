% Optimization smallest sum over feature complexities
#minimize { C,complexity(F, C) : complexity(F, C), feature(F), select(F) }.

% Generate selected features
{ select(F) } :- feature(F).

{ good(C) } :- state_pair_class(C).

% D2-separation
:- good(C), not good(C'), d2_separate(C, C'), state_pair_class(C), state_pair_class(C'), { feature(F) : select(F), feature_effect(F, C, V), feature_effect(F, C', V'), V != V' } = 0, { feature(F) : select(F), feature_condition(F, C, V), feature_condition(F, C', V'), V != V' } = 0.

% Goal-separation no possible with current pool, because decrement can mean 2->0, 2->1
% Hence one would need seed features that reflect feature change.
%:- nongoal_state_class(D), goal_state_class(D'), { feature(F) : select(F), value(D, F, V), value(D', F, V'), V != V' } = 0.

% Display
#show select/1.
#show numerical/1.
#show boolean/1.
#show good/1.
#show feature_condition/3.
#show feature_effect/3.
