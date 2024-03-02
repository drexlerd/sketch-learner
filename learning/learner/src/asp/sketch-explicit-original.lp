% Optimization for fewest number of rules, then smallest sum over feature complexities
#minimize {1,rule(R): rule(R)}.
#minimize { C,complexity(F, C) : complexity(F, C), feature(F), select(F) }.

%%%%%%%%%% C1 %%%%%%%%%%
% Generate selected features
{ select(F) } :- feature(F).
% Generate rules
{ rule(1..max_num_rules) }.

% Generate feature conditions and effects
{ c_eq(R, F); c_gt(R, F); c_unk(R, F) } = 1 :- rule(R), numerical(F).
{ c_pos(R, F); c_neg(R, F); c_unk(R, F) } = 1 :- rule(R), boolean(F).
{ e_dec(R, F); e_inc(R, F); e_unk(R, F); e_bot(R, F) } = 1 :- rule(R), numerical(F).
{ e_pos(R, F); e_neg(R, F); e_unk(R, F); e_bot(R, F) } = 1 :- rule(R), boolean(F).

% Define equivalence class C and rule R have same feature condition on F
c_satisfied(R, F, C) :- c_eq(R, F), c_eq_rule(C, F), numerical(F), rule(R), state_pair_class(C).
c_satisfied(R, F, C) :- c_gt(R, F), c_gt_rule(C, F), numerical(F), rule(R), state_pair_class(C).
c_satisfied(R, F, C) :- c_pos(R, F), c_pos_rule(C, F), boolean(F), rule(R), state_pair_class(C).
c_satisfied(R, F, C) :- c_neg(R, F), c_neg_rule(C, F), boolean(F), rule(R), state_pair_class(C).
c_satisfied(R, F, C) :- c_unk(R, F), feature(F), rule(R), state_pair_class(C).

e_satisfied(R, F, C) :- e_dec(R, F), e_dec_rule(C, F), numerical(F), rule(R), state_pair_class(C).
e_satisfied(R, F, C) :- e_inc(R, F), e_inc_rule(C, F), numerical(F), rule(R), state_pair_class(C).
e_satisfied(R, F, C) :- e_pos(R, F), e_pos_rule(C, F), boolean(F), rule(R), state_pair_class(C).
e_satisfied(R, F, C) :- e_neg(R, F), e_neg_rule(C, F), boolean(F), rule(R), state_pair_class(C).
e_satisfied(R, F, C) :- e_bot(R, F), e_bot_rule(C, F), feature(F), rule(R), state_pair_class(C).
e_satisfied(R, F, C) :- e_pos(R, F), c_pos_rule(C, F), e_bot_rule(C, F), feature(F), rule(R), state_pair_class(C).
e_satisfied(R, F, C) :- e_neg(R, F), c_neg_rule(C, F), e_bot_rule(C, F), feature(F), rule(R), state_pair_class(C).
e_satisfied(R, F, C) :- e_unk(R, F), feature(F), rule(R), state_pair_class(C).

%%%%%%%%%% C2.1 %%%%%%%%%%
% Generate subgoal distance and subgoal for r_reachable state.
{ sat_cond(I, S, R) : rule(R) } != 0 :- r_reachable(I, S), nongoal(I, S).

%%%%%%%%%% C2.2 %%%%%%%%%%
{ subgoal_distance(I, S, D, R) : t_distance(I, S, _, D) } != 0 :- sat_cond(I, S, R), r_reachable(I, S), nongoal(I, S).

%%%%%%%%%% C2.3 %%%%%%%%%%
% Define initial state to be r_reachable
r_reachable(I, S) :- initial(I, S).

%%%%%%%%%% C2.4 %%%%%%%%%%
% r_reachable(I, S') :- D = D', r_reachable(I, S), sat_pair(I, S, S', R), subgoal_distance(I, S, D, R), s_distance(I, S, S', D).
r_reachable(I, S') :- r_reachable(I, S), sat_pair(I, S, S', R).

%%% unable to bound width of unsolvable state.
:- unsolvable(I, S), r_reachable(I, S).

%%%%%%%%%% C3.1 %%%%%%%%%%
{ subgoal(I, S, T, R) : t_distance(I, S, T, D) } != 0 :- subgoal_distance(I, S, D, R), r_reachable(I, S).

%%%%%%%%%% C4.1 %%%%%%%%%%
% Require that all equivalence classes C underlying a tuple T of subproblem P[S] are good, effectively bounding the width of P[S]
:- not sat_rule(R, C), subgoal(I, S, T, R), contain(I, S, T, C), r_reachable(I, S).

%%%%%%%%%% C6.1 %%%%%%%%%%
% (Optimal-width): Require solvable states S' closer than subgoal to not be assigned to any rule.
:- D < D', r_distance(I, S, C, D), sat_rule(R, C), subgoal_distance(I, S, D', R), nongoal(I, S).

%%%%%%%%%% C7.1 %%%%%%%%%%
% Define state pair equivalences that are compatible with rules.
sat_rule(R, C) :- { feature(F) : not c_satisfied(R, F, C), select(F);
     feature(F) : not e_satisfied(R, F, C), select(F) } = 0, rule(R), state_pair_class(C).
% Define state pairs that are compatible with rules.
sat_pair(I, S, S', R) :- sat_rule(R, C), cover(I, S, S', C), nongoal(I, S).

%%%%%%%%%% C7.2 %%%%%%%%%%
sat_cond(I, S, R) :- { feature(F) : not c_satisfied(R, F, C), select(F) } = 0, rule(R), state_pair_class(C), cover(I, S, _, C), nongoal(I, S).

%%%%%%%%%% C8.1 %%%%%%%%%%
% (Termination): Sketch must define strict partial order over R-reachable states
% Source of this formulation: https://users.aalto.fi/~rintanj1/papers/GebserJR14kr.pdf
order(I, S, S') :- r_reachable(I, S), r_reachable(I, S'), nongoal(I, S), sat_pair(I, S, S', _), order(I, S').
order(I, S) :- r_reachable(I, S), order(I, S, S') : sat_pair(I, S, S', _), r_reachable(I, S), r_reachable(I, S'), nongoal(I, S).
:- r_reachable(I, S), nongoal(I, S), not order(I, S).

% Display
#show rule/1.
#show select/1.
#show numerical/1.
#show boolean/1.
#show sat_pair/4.
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
