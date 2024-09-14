#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import itertools
import os
import random

from tarski.fstrips import create_fstrips_problem, language, DelEffect, AddEffect
from tarski.io import FstripsWriter
from tarski.theories import Theory
from tarski.syntax import forall, implies, exists, land, Tautology

_CURRENT_DIR_ = os.path.dirname(os.path.realpath(__file__))


def create_noop(problem):
    # A hackish no-op, to prevent the planner from detecting that the action is useless and pruning it
    lang = problem.language
    cell_t, at = lang.get("cell", "at")
    x = lang.variable("x", cell_t)
    problem.action(name='noop', parameters=[x], precondition=at(x), effects=[AddEffect(at(x))])


def create_single_action_version(problem):
    lang = problem.language
    cell_t, at, reward, unblocked, picked, adjacent = lang.get("cell", "at", "reward", "unblocked", "picked", "adjacent")
    from_ = lang.variable("from", cell_t)
    to = lang.variable("to", cell_t)
    c = lang.variable("c", cell_t)
    problem.action(name='move', parameters=[from_, to],
                   precondition=land(adjacent(from_, to), at(from_), unblocked(to), exists(c, reward(c)), flat=True),
                   effects=[DelEffect(at(from_)),
                            AddEffect(at(to)),
                            # AddEffect(visited(to)),
                            DelEffect(reward(to))])


def create_two_action_version(problem):
    lang = problem.language
    cell_t, at, reward, unblocked, picked, adjacent = lang.get("cell", "at", "reward", "unblocked", "picked", "adjacent")
    from_ = lang.variable("from", cell_t)
    to = lang.variable("to", cell_t)
    c = lang.variable("c", cell_t)
    problem.action(name='move', parameters=[from_, to],
                   precondition=land(adjacent(from_, to), at(from_), unblocked(to), flat=True),
                   effects=[DelEffect(at(from_)),
                            AddEffect(at(to))])

    x = lang.variable("x", cell_t)
    problem.action(name='pick-reward', parameters=[x],
                   precondition=at(x) & reward(x),
                   effects=[DelEffect(reward(x)),
                            AddEffect(picked(x))])


def generate_propositional_domain(h, w, num_rewards, num_blocked_cells, add_noop=False):
    lang = language(theories=[Theory.EQUALITY])
    problem = create_fstrips_problem(domain_name='reward-strips',
                                     problem_name=f"reward-{h}x{w}",
                                     language=lang)
    cell_t = lang.sort('cell')
    at = lang.predicate('at', cell_t)
    reward = lang.predicate('reward', cell_t)
    unblocked = lang.predicate('unblocked', cell_t)
    picked = lang.predicate('picked', cell_t)
    adjacent = lang.predicate('adjacent', cell_t, cell_t)
    # visited = lang.predicate('visited', cell_t)

    # Create the actions
    # create_single_action_version(problem)
    create_two_action_version(problem)
    if add_noop:
        create_noop(problem)

    h_rng = range(0, h)
    w_rng = range(0, w)
    coordinates = list(itertools.product(h_rng, w_rng))

    def cell_name(x, y):
        return f"c_{x}_{y}"

    # Declare the constants:
    coord_objects = [lang.constant(cell_name(x, y), cell_t) for x, y in coordinates]

    # Declare the adjacencies:
    adjacent_coords = [(a, b, c, d) for (a, b), (c, d) in itertools.combinations(coordinates, 2)
                       if abs(a-c) + abs(b-d) == 1]

    for a, b, c, d in adjacent_coords:
        problem.init.add(adjacent, cell_name(a, b), cell_name(c, d))
        problem.init.add(adjacent, cell_name(c, d), cell_name(a, b))

    # The initial position is already visited, by definition
    # problem.init.add(visited, initial_position)
    problem.init.add(at, cell_name(0, 0))
    problem.init.add(unblocked, cell_name(0, 0))

    # Set some random rewards and cell blocks:
    if num_rewards + num_blocked_cells > len(coordinates) - 1:
        raise RuntimeError("Number of rewards and blocks higher than total number of available cells!")

    cd = coordinates[1:]  # Clone the list of coordinates excluding the initial position
    random.shuffle(cd)

    num_unblocked = len(cd) - num_blocked_cells
    for x, y in cd[0:num_unblocked]:
        problem.init.add(unblocked, cell_name(x, y))

    cells_with_reward = list()
    for x, y in cd[0:num_rewards]:
        problem.init.add(reward, cell_name(x, y))
        cells_with_reward.append(cell_name(x, y))

    # Set the problem goal
    c = lang.variable("c", cell_t)
    # problem.goal = forall(c, ~reward(c))

    # This one's good, and doesn't require a "picked" predicate, but cannot be parsed by Pyperplan:
    # problem.goal = land(*[~reward(c) for c in coord_objects], flat=True)

    problem.goal = land(*[picked(lang.get(c)) for c in cells_with_reward], flat=True)

    return problem


def main():
    # training
    for h in range(1,4):
        for w in range(1,4):
            gridsize = h * w
            if gridsize < 2:
                # need to place robot and at least one reward in separate cells
                continue
            run = 0
            while run != 30:
                num_blocks = random.randint(0, gridsize-1)
                num_rewards = random.randint(1, gridsize)
                if num_rewards + num_blocks <= gridsize - 1:
                    print(h, w, num_blocks, num_rewards)
                    problem = generate_propositional_domain(h, w, num_rewards, num_blocks, False)
                    writer = FstripsWriter(problem)
                    writer.write(domain_filename=os.path.join(_CURRENT_DIR_, "domain.pddl"),  # We can overwrite the domain
                                instance_filename=os.path.join(_CURRENT_DIR_, f"instance_{h}x{w}_{run}.pddl"))
                    run += 1
    # testing
    #for gridsize in [5, 7, 10, 15, 20, 25]:
    #    for run in range(0, 5):
    #        num_blocks = random.randint(0, gridsize-1)
    #        num_rewards = random.randint(1, gridsize)
    #        problem = generate_propositional_domain(gridsize, num_rewards, num_blocks, False)
    #        writer = FstripsWriter(problem)
    #        writer.write(domain_filename=os.path.join(_CURRENT_DIR_, "domain.pddl"),  # We can overwrite the domain
    #                     instance_filename=os.path.join(_CURRENT_DIR_, f"instance_{gridsize}x{gridsize}_{run}.pddl"))


if __name__ == "__main__":
    main()
