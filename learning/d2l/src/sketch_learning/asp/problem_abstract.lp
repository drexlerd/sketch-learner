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

% equivalence class C and rule R have same feature condition on F
c_satisfied(R, C, F) :- { c_eq(R, F), c_unk(R, F) } = 1, c_eq(C, F), numerical(F), rule(R), equivalence(C).
c_satisfied(R, C, F) :- { c_gt(R, F), c_unk(R, F) } = 1, c_gt(C, F), numerical(F), rule(R), equivalence(C).

% assign equivalence class to rule if for all selected features the feature conditions and effects are equivalent
assign(R, C) :- { feature(F) : not c_satisfied(C, R, F), select(F) } = 0, rule(R), equivalence(C).

% Define subgoal for each solvable state for which the width exceeds.
{ subgoal(I, S, T) : tuple(I, S, T) } = 1 :- solvable(I, S), exceed(I, S).

% Require that all states S' underlying a tuple T are a subgoal states in the subproblem P[S], effectively bounding the width of P[S]
:- { assign(R, C) : rule(R) } = 0, subgoal(I, S, T), contain(I, S, T, C).
% Require unsolvable states S' as close as subgoal to not be assigned to any rule.
:- D <= D', d_distance(I, S, C, D), t_distance(I, S, T, D'), subgoal(I, S, T), assign(_, C).

% (Termination): Sketch must define strict partial order over R-reachable states
% Source of this formulation: https://users.aalto.fi/~rintanj1/papers/GebserJR14kr.pdf
order(I, C, C') :- termination_node(I, C), termination_node(I, C'), assign(_, C), order(I, C').
order(I, C) :- termination_node(I, C), order(I, C, C') : assign(_, C), termination_edge(C, C').
:- termination_node(I, C), not order(I, C).

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
