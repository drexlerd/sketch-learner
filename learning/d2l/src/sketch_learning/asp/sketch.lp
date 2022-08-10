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

% Define equivalence class C and rule R have same feature condition on F
c_satisfied(R, F, C) :- c_eq(R, F), c_eq_fixed(C, F), numerical(F), rule(R), equivalence(C).
c_satisfied(R, F, C) :- c_gt(R, F), c_gt_fixed(C, F), numerical(F), rule(R), equivalence(C).
c_satisfied(R, F, C) :- c_pos(R, F), c_pos_fixed(C, F), boolean(F), rule(R), equivalence(C).
c_satisfied(R, F, C) :- c_neg(R, F), c_neg_fixed(C, F), boolean(F), rule(R), equivalence(C).
c_satisfied(R, F, C) :- c_unk(R, F), feature(F), rule(R), equivalence(C).

e_satisfied(R, F, C) :- e_dec(R, F), e_dec_fixed(C, F), numerical(F), rule(R), equivalence(C).
e_satisfied(R, F, C) :- e_inc(R, F), e_inc_fixed(C, F), numerical(F), rule(R), equivalence(C).
e_satisfied(R, F, C) :- e_pos(R, F), e_pos_fixed(C, F), boolean(F), rule(R), equivalence(C).
e_satisfied(R, F, C) :- e_neg(R, F), e_neg_fixed(C, F), boolean(F), rule(R), equivalence(C).
e_satisfied(R, F, C) :- e_bot(R, F), e_bot_fixed(C, F), feature(F), rule(R), equivalence(C).
e_satisfied(R, F, C) :- e_pos(R, F), c_pos_fixed(C, F), e_bot_fixed(C, F), feature(F), rule(R), equivalence(C).
e_satisfied(R, F, C) :- e_neg(R, F), c_neg_fixed(C, F), e_bot_fixed(C, F), feature(F), rule(R), equivalence(C).
e_satisfied(R, F, C) :- e_unk(R, F), feature(F), rule(R), equivalence(C).

% Define assignment of equivalence class to rule
good(C) :- { feature(F) : not c_satisfied(R, F, C), select(F);
     feature(F) : not e_satisfied(R, F, C), select(F) } = 0, rule(R), equivalence(C).

% Define exactly one subgoal for each solvable state for which the width exceeds.
{ subgoal(I, S, T) : tuple(I, S, T) } = 1 :- exceed(I, S).

% Require that all equivalence classes C underlying a tuple T of subproblem P[S] are good, effectively bounding the width of P[S]
:- not good(C), subgoal(I, S, T), contain(I, S, T, C).
% Require unsolvable states S' as close as subgoal to not be assigned to any rule.
:- D <= D', d_distance(I, S, C, D), t_distance(I, S, T, D'), subgoal(I, S, T), good(C).
% (Optimal-width): Require solvable states S' closer than subgoal to not be assigned to any rule.
:- D < D', r_distance(I, S, C, D), t_distance(I, S, T, D'), subgoal(I, S, T), good(C).

% Define ``good`` state pairs similar to equivalence classes
good(I, S, S') :- good(C), equivalence_contains(I, C, S, S').

subgoal(I, S', T) :- subgoal(I, S, T), subgoal_implication(I, S, S', T).

% (Termination): Sketch must define strict partial order over R-reachable states
% Source of this formulation: https://users.aalto.fi/~rintanj1/papers/GebserJR14kr.pdf
order(I, S, S') :- solvable(I, S), solvable(I, S'), good(I, S, S'), order(I, S').
order(I, S) :- solvable(I, S), order(I, S, S') : good(I, S, S'), solvable(I, S), solvable(I, S').
:- solvable(I, S), not order(I, S).

% Display
#show subgoal_implication/4.
#show subgoal/3.
#show rule/1.
#show select/1.
#show numerical/1.
#show boolean/1.
#show good/3.
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
