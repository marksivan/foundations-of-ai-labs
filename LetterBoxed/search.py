from abc import ABC, abstractmethod
from queue import LifoQueue, Queue
from queue import PriorityQueue
import random
from tqdm import tqdm

random.seed(48)


class SearchSpace(ABC):

    @abstractmethod
    def get_start_state(self):
        """Returns the start state for the search space."""

    @abstractmethod
    def is_final_state(self, state):
        """Returns whether the provided state is a final state."""

    @abstractmethod
    def get_successors(self, state):
        """Returns the transitions from the current state.

        For a given state, this should return a list of triples of the form:
           (successor, action, step_cost)
        where:
        - `successor` is a successor state of the current state,
        - `action` is the action required to get to the successor state
        - `step_cost` is the cost of moving to the successor state.
        """


def search_template(
    space,
    container,
    heuristic_fn=lambda state, space: 0,
    memoize=False,
    show_progress=True,
):
    """General-purpose algorithmic template for search, e.g. DFS or BFS.

    Parameters
    ----------
    space : SearchSpace
        The search space
    container : queue.Queue or queue.LifoQueue or PriorityQueueWithFunction (defined below)
        The container for processing nodes of the search tree.
    heuristic_fn : function that takes a search state and a SearchSpace and returns a non-negative number
        The heuristic function (defaults to a function that always returns zero)
    """
    visited = set()
    initial_node = (space.get_start_state(), 0, 0, tuple())
    container.put(initial_node)
    count = 0
    if show_progress:
        progress_bar = tqdm()
    while not container.empty():
        (q, g, h, solution) = container.get()
        if q not in visited:
            count += 1
            if show_progress:
                progress_bar.update(1)
            if memoize:
                visited.add(q)
            if space.is_final_state(q):
                if show_progress:
                    progress_bar.close()
                print(f"Search nodes visited: {count}")
                return solution
            successors = space.get_successors(q)
            for next_state, action, cost in successors:
                h = heuristic_fn(next_state, space)
                successor_node = (next_state, g + cost, h, solution + (action,))
                container.put(successor_node)


def depth_first_search(problem, memoize=False, show_progress=True):
    return search_template(
        problem, LifoQueue(), memoize=memoize, show_progress=show_progress
    )


def breadth_first_search(problem, memoize=False, show_progress=True):
    return search_template(
        problem, Queue(), memoize=memoize, show_progress=show_progress
    )


class PriorityQueueWithFunction:
    def __init__(self, priority_fn):
        self.queue = PriorityQueue()
        self.priority_fn = priority_fn

    def put(self, item):
        prioritized_item = (self.priority_fn(item), item)
        self.queue.put((prioritized_item, item))

    def get(self):
        _, item = self.queue.get()
        return item

    def empty(self):
        return self.queue.empty()


def uniform_cost_search(problem, memoize=False, show_progress=True):
    return search_template(
        problem,
        PriorityQueueWithFunction(lambda x: x[1]),
        memoize=memoize,
        show_progress=show_progress,
    )


def a_star_search(problem, heuristic, memoize=False, show_progress=True):
    return search_template(
        problem,
        PriorityQueueWithFunction(lambda x: x[1] + x[2]),
        heuristic,
        memoize=memoize,
        show_progress=show_progress,
    )
