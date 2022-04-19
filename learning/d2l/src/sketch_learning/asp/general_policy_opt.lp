% Optimization for fewest number of rules, then smallest sum over feature complexities
#minimize { 1,rule(R) : rule(R) }.
#minimize { C,complexity(F, C) : complexity(F, C), feature(F), select(F) }.

% Generate selected features
{ select(F) } :- feature(F).
% Generate rules
{ rule(1..max_sketch_rules) }.

% Generate feature conditions and effects
{ c_eq(R, F); c_gt(R, F); c_unk(R, F) } = 1 :- rule(R), numerical(F).
{ c_pos(R, F); c_neg(R, F); c_unk(R, F) } = 1 :- rule(R), boolean(F).
{ e_dec(R, F); e_inc(R, F); e_unk(R, F); e_bot(R, F) } = 1 :- rule(R), numerical(F).
{ e_pos(R, F); e_neg(R, F); e_unk(R, F); e_bot(R, F) } = 1 :- rule(R), boolean(F).

% Define satisfied feature conditions
c_satisfied(R, F, I, S) :- { c_eq(R, F) : V = 0; c_gt(R, F) : V > 0; c_pos(R, F) : V = 1; c_neg(R, F) : V = 0; c_unk(R, F) } = 1,
    rule(R), feature_valuation(F, I, S, V), transition(I, S, S').
% Define satisfied feature effects
e_satisfied(R, F, I, S, S') :- { e_dec(R, F) : V > V'; e_inc(R, F) : V < V'; e_pos(R, F) : V' = 1; e_neg(R, F) : V' = 0; e_bot(R, F) : V = V'; e_unk(R, F) } = 1,
    rule(R), feature_valuation(F, I, S, V), feature_valuation(F, I, S', V'), transition(I, S, S').

% Generate assignment of state pair to rule.
{ assign(R, I, S, S') } :- rule(R), transition(I, S, S').
% Require that good state pair satisfies all feature conditions and effects of the assigned rule
:- { not c_satisfied(R, F, I, S); not e_satisfied(R, F, I, S, S') } != 0, select(F), assign(R, I, S, S').
% Require that bad state pair has at least one unsatisfied feature condition or feature effect for every rule.
:- { not c_satisfied(R, F, I, S) : select(F); not e_satisfied(R, F, I, S, S') : select(F) } = 0, rule(R), transition(I, S, S'), not assign(R, I, S, S').

% Define subgoal for each solvable state for which the width exceeds.
:- { assign(R, I, S, S') } = 0, solvable(I, S), exceed(I, S).

% Require transition to unsolvable state to be bad.
:- assign(R, I, S, S'), solvable(I, S), unsolvable(I, S').

% (Termination): Sketch must define strict partial order over R-reachable states
% Source of this formulation: https://users.aalto.fi/~rintanj1/papers/GebserJR14kr.pdf
order(I, S, S') :- solvable(I, S), solvable(I, S'), assign(_, I, S, S'), order(I, S').
order(I, S) :- solvable(I, S), order(I, S, S') : assign(_, I, S, S'), solvable(I, S), solvable(I, S').
:- solvable(I, S), not order(I, S).

% Display
#show rule/1.
#show select/1.
#show numerical/1.
#show boolean/1.
#show c_eq/2.
#show c_gt/2.
#show c_unk/2.
#show c_pos/2.
#show c_neg/2.
#show e_pos/2.
#show e_neg/2.
#show e_dec/2.
#show e_inc/2.
#show e_bot/2.
#show e_unk/2.
