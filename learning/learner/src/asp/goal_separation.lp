% Require Goal-separation
:- nongoal(I, S), goal(I', S'), { feature(F) : select(F), b_value(I, S, F, V), b_value(I', S', F, V'), V != V' } = 0.
