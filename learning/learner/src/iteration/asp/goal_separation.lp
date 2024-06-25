% Require Goal-separation
:- nongoal(S), goal(S'), { feature(F) : select(F), b_value(S, F, V), b_value(S', F, V'), V != V' } = 0.
