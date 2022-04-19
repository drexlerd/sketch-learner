% Optimization for fewest number of rules, then smallest sum over feature complexities
#minimize { C,complexity(F, C) : complexity(F, C), select(F) }.

% Generate selected features
{ select(F) } :- feature(F).

% Features are goal separating
:- { select(F) : V = V', f_value(I, F, S, V), f_value(I, F, S', V'), select(F) } = 0, nongoal(S), goal(S').

% Define subgoal for each solvable state for which the width exceeds.
{ subgoal(I, S, T) : tuple(I, S, T) } = 1 :- solvable(I, S), exceed(I, S).

% Generate potentially good feature changes equivalence classes
{ good(I, X) } :- equivalence(I, X).

% Require that all equivalence classes underlying subgoal tuple are good
:- { not good(I, X) : contain(I, S, T, X) } != 0, subgoal(I, S, T).

% Require unsolvable states S' as close as subgoal to not be assigned to any rule.
:- D <= D', good(I, X), unsolvable_distance(I, S, X, D), unsolvable(I, S, X), t_distance(I, S, T, D'), solvable(I, S).

% (Termination): Sketch must define strict partial order over R-reachable states
% Source of this formulation: https://users.aalto.fi/~rintanj1/papers/GebserJR14kr.pdf
order(I, S, S') :- solvable(I, S), solvable(I, S'), good(I, X), contain(I, S, S', X), order(I, S').
order(I, S) :- solvable(I, S), order(I, S, S') : good(I, X), contain(I, S, S', X), solvable(I, S), solvable(I, S').
:- solvable(I, S), not order(I, S).

% Display
#show select/1.
#show good/2.

% unsolvable(I, S, X) denotes that selected equivalence class X leads to deadend in tuple graph rooted as S.
% unsolvable_distance(I, S, X, D) denotes that selected equivalence class X leads to deadend in in tuple graph rooted at S with distance d.
