% Optimization for fewest number of rules, then smallest sum over feature complexities
#minimize { C@2,complexity(F, C) : complexity(F, C), feature(F), select(F) }.
#minimize { 1@1,rule(R): rule(R)}.

%%%%%%%%%% C1 %%%%%%%%%%
% Generate selected features
{ select(F) } :- feature(F).
% Generate rules
{ rule(1..max_num_rules) }.

% Generate feature conditions and effects
{ c_n_eq(R, F); c_n_gt(R, F); c_n_unk(R, F) } = 1 :- rule(R), numerical(F).
{ c_b_pos(R, F); c_b_neg(R, F); c_b_unk(R, F) } = 1 :- rule(R), boolean(F).
{ e_n_dec(R, F); e_n_inc(R, F); e_n_unk(R, F); e_n_bot(R, F) } = 1 :- rule(R), numerical(F).
{ e_b_pos(R, F); e_b_neg(R, F); e_b_unk(R, F); e_b_bot(R, F) } = 1 :- rule(R), boolean(F).

% Define equivalence class C and rule R have same feature condition on F
c_satisfied(R, F, C) :- c_n_eq(R, F), feature_condition(C, F, "c_n_eq"), numerical(F), rule(R), state_pair_class(C).
c_satisfied(R, F, C) :- c_n_gt(R, F), feature_condition(C, F, "c_n_gt"), numerical(F), rule(R), state_pair_class(C).
c_satisfied(R, F, C) :- c_b_pos(R, F), feature_condition(C, F, "c_b_pos"), boolean(F), rule(R), state_pair_class(C).
c_satisfied(R, F, C) :- c_b_neg(R, F), feature_condition(C, F, "c_b_neg"), boolean(F), rule(R), state_pair_class(C).
c_satisfied(R, F, C) :- c_n_unk(R, F), numerical(F), rule(R), state_pair_class(C).
c_satisfied(R, F, C) :- c_b_unk(R, F), boolean(F), rule(R), state_pair_class(C).

e_satisfied(R, F, C) :- e_n_dec(R, F), feature_effect(C, F, "e_n_dec"), numerical(F), rule(R), state_pair_class(C).
e_satisfied(R, F, C) :- e_n_inc(R, F), feature_effect(C, F, "e_n_inc"), numerical(F), rule(R), state_pair_class(C).
e_satisfied(R, F, C) :- e_b_pos(R, F), feature_effect(C, F, "e_b_pos"), boolean(F), rule(R), state_pair_class(C).
e_satisfied(R, F, C) :- e_b_neg(R, F), feature_effect(C, F, "e_b_neg"), boolean(F), rule(R), state_pair_class(C).
e_satisfied(R, F, C) :- e_b_bot(R, F), feature_effect(C, F, "e_b_bot"), boolean(F), rule(R), state_pair_class(C).
e_satisfied(R, F, C) :- e_n_bot(R, F), feature_effect(C, F, "e_n_bot"), numerical(F), rule(R), state_pair_class(C).
e_satisfied(R, F, C) :- e_b_pos(R, F), feature_effect(C, F, "e_b_bot"), feature_condition(C, F, "c_b_pos"), boolean(F), rule(R), state_pair_class(C).
e_satisfied(R, F, C) :- e_b_neg(R, F), feature_effect(C, F, "e_b_bot"), feature_condition(C, F, "c_b_neg"), boolean(F), rule(R), state_pair_class(C).
e_satisfied(R, F, C) :- e_n_unk(R, F), numerical(F), rule(R), state_pair_class(C).
e_satisfied(R, F, C) :- e_b_unk(R, F), boolean(F), rule(R), state_pair_class(C).

%%%%%%%%%% C2.1 %%%%%%%%%%
% Generate subgoal distance and subgoal for r_reachable state.
{ sat_cond(S, R) : rule(R) } != 0 :- r_reachable(S), nongoal(S).

%%%%%%%%%% C2.2 %%%%%%%%%%
{ subgoal_distance(S, D, R) : t_distance(S, _, D) } != 0 :- sat_cond(S, R), r_reachable(S), nongoal(S).

%%%%%%%%%% C2.3 %%%%%%%%%%
% Define initial state to be r_reachable
r_reachable(S) :- initial(S).

%%%%%%%%%% C2.4 %%%%%%%%%%
r_reachable(S') :- D = D', r_reachable(S), sat_pair(S, S', R), subgoal_distance(S, D, R), s_distance(S, S', D).
%r_reachable(S') :- r_reachable(S), sat_pair(S, S', R).

%%% unable to bound width of unsolvable state.
:- unsolvable(S), r_reachable(S).

%%%%%%%%%% C3.1 %%%%%%%%%%
{ subgoal(S, T, R) : t_distance(S, T, D) } != 0 :- subgoal_distance(S, D, R), r_reachable(S).

%%%%%%%%%% C4.1 %%%%%%%%%%
% Require that all equivalence classes C underlying a tuple T of subproblem P[S] are good, effectively bounding the width of P[S]
:- not sat_rule(R, C), subgoal(S, T, R), contain(S, T, C), r_reachable(S).

%%%%%%%%%% C6.1 %%%%%%%%%%
% (Optimal-width): Require solvable states S' closer than subgoal to not be assigned to any rule.
:- D < D', r_distance(S, C, D), sat_rule(R, C), subgoal_distance(S, D', R), nongoal(S).

%%%%%%%%%% C7.1 %%%%%%%%%%
% Define state pair equivalences that are compatible with rules.
sat_rule(R, C) :- { feature(F) : not c_satisfied(R, F, C), select(F);
     feature(F) : not e_satisfied(R, F, C), select(F) } = 0, rule(R), state_pair_class(C).
% Define state pairs that are compatible with rules.
sat_pair(S, S', R) :- sat_rule(R, C), cover(S, S', C), nongoal(S).

%%%%%%%%%% C7.2 %%%%%%%%%%
sat_cond(S, R) :- { feature(F) : not c_satisfied(R, F, C), select(F) } = 0, rule(R), state_pair_class(C), cover(S, _, C), nongoal(S).

%%%%%%%%%% C8.1 %%%%%%%%%%
% (Termination): Sketch must define strict partial order over R-reachable states
% Source of this formulation: https://users.aalto.fi/~rintanj1/papers/GebserJR14kr.pdf
order(S, S') :- r_reachable(S), r_reachable(S'), nongoal(S), sat_pair(S, S', _), order(S').
order(S) :- r_reachable(S), order(S, S') : sat_pair(S, S', _), r_reachable(S), r_reachable(S'), nongoal(S).
:- r_reachable(S), nongoal(S), not order(S).

% Display
#show rule/1.
#show select/1.

#show c_n_eq/2.
#show c_n_gt/2.
#show c_n_unk/2.

#show e_n_dec/2.
#show e_n_inc/2.
#show e_n_bot/2.
#show e_n_unk/2.

#show c_b_pos/2.
#show c_b_neg/2.
#show c_b_unk/2.

#show e_b_pos/2.
#show e_b_neg/2.
#show e_b_bot/2.
#show e_b_unk/2.

