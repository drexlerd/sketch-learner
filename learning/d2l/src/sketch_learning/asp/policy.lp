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

% Require one good equivalence class for each expanded state in G of P
:- { good(C) : optimal_equivalence(I, G, C, S, _) } = 0, expanded(I, G, S).

% Require suboptimal transitions to be bad, that includes those to deadends
:- good(C), suboptimal_equivalence(I, G, C, S, _), expanded(I, G, S).

% Display
#show rule/1.
#show select/1.
#show numerical/1.
#show boolean/1.
#show good/1.
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
