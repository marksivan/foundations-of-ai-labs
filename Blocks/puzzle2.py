from search import SearchSpace, bfs


class BlockPuzzleSearchSpace(SearchSpace):

    def __init__(self, intervals, cube_width):
        super().__init__()
        self.intervals = intervals
        self.cube_width = cube_width
        self.num_blocks = cube_width ** 3
        self.moves = self.num_blocks - 1
        self.direction_values = direction_values = { "E" :(1, 0, 0), 
                          "W": (-1, 0, 0),
                           "N": (0, 1, 0),
                          "S": (0, -1, 0),
                           "U": (0, 0, 1),
                           "D": (0, 0, -1)
                           }
    

    def get_start_state(self):
        """Returns the start state.

        A state of this search space is a sequence of directions. The start state
        contains a single arbitrary initial direction ('E').

        Returns
        -------
        tuple[str]
            The start state
        """
        return ("E",)

    def is_final_state(self, state):
        """Checks whether a given state is a final state.

        To qualify as a final state, the state trajectory should visit all
        positions in a 3x3 cube (without visiting the same position twice).

        Parameters
        ----------
        state : tuple[str]
            A state of the search space, i.e. a sequence of directions
 
        Returns
        -------
        bool
            True iff the state is a final state

             2x2x2
            space.is_final_state(("E","N","W","U","E","S","W")) : RETURNS TRUE
            space.is_final_state(()"E","N","W","U","E","S","E")) : RETURNS FALSE

            3x3x3
            
        """

        def new_position(pos1, pos2):
            result = []
            for i in range(len(pos1)):
                result.append(pos1[i] + pos2[i])
            return tuple(result)
        
        direction_values = { "E" :(1, 0, 0), 
                             "W": (-1, 0, 0),
                             "N": (0, 1, 0),
                             "S": (0, -1, 0),
                             "U": (0, 0, 1),
                             "D": (0, 0, -1)
        }

        def is_valid_position(cube_width, position):
            for coord in position:
                if abs(coord) >= cube_width:
                    return False
            return True
        
        curr_post = (0,0,0)
        positions = set()
        positions.add(curr_post)

        for direction in state:
            curr_post = new_position(curr_post, direction_values[direction])
            if not is_valid_position(self.cube_width, curr_post):
                return False
            if curr_post in positions:
                return False
            positions.add(curr_post)
        if len(positions) != self.num_blocks:
            return False
        return True



    

    def get_successors(self, state):
        pivot_sums = set()
        curr_sum = 0
        for interval in self.intervals:
                curr_sum += interval
                pivot_sums.add(curr_sum)

        directions = ["E", "W", "N", "S", "U", "D"]
        opposites = {"E": "W", "W": "E", "N": "S", "S": "N", "D": "U", "U": "D"}

        curr_direction = state[-1]

        # Build visited positions and current position only once
        pos = (0, 0, 0)
        visited = {pos}
        for move in state:
            dx, dy, dz = self.direction_values[move]
            pos = (pos[0] + dx, pos[1] + dy, pos[2] + dz)
            visited.add(pos)

        successors = []

        # Continue straight if not pivot
        if len(state) not in pivot_sums:
            next_pos = (pos[0] + self.direction_values[curr_direction][0],
                        pos[1] + self.direction_values[curr_direction][1],
                        pos[2] + self.direction_values[curr_direction][2])
            if all(abs(c) < self.cube_width for c in next_pos) and next_pos not in visited:
                successors.append(state + (curr_direction,))
            return successors

        # Pivot: try all valid turns
        for d in directions:
            if d == curr_direction or d == opposites[curr_direction]:
                continue
            next_pos = (pos[0] + self.direction_values[d][0],
                        pos[1] + self.direction_values[d][1],
                        pos[2] + self.direction_values[d][2])
            if all(abs(c) < self.cube_width for c in next_pos) and next_pos not in visited:
                successors.append(state + (d,))

        return successors


        
        
      
        



def construct_search_space_for_2x2x2_puzzle():
    return BlockPuzzleSearchSpace(intervals=(1, 1, 1, 1, 1, 1, 1), cube_width=2)


def construct_search_space_for_3x3x3_puzzle():
    return BlockPuzzleSearchSpace(
        intervals=(2, 2, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 2), cube_width=3
    )


def small_solution():
    space = construct_search_space_for_2x2x2_puzzle()
    return bfs(space)


def puzzle_solution():
    space = construct_search_space_for_3x3x3_puzzle()
    return bfs(space)


def solution_b():
    """Computes a solution to block puzzle B from the assignment.

    The solution should be a trajectory, i.e. a sequence of directions
    from the set {'N', 'S', 'E', 'W', 'U', 'D'}. This trajectory should be
    consistent with the shape of the puzzle and should visit each subcube
    of a 3x3 cube exactly once.
    """
    

    intervals = (2,2,2,1,1,1,1,2,2,2,1,2,1,2,1,2)
    space = BlockPuzzleSearchSpace(intervals=intervals, cube_width=3)
    return bfs(space)


def solution_c():
    """Computes a solution to block puzzle C from the assignment.

    The solution should be a trajectory, i.e. a sequence of directions
    from the set {'N', 'S', 'E', 'W', 'U', 'D'}. This trajectory should be
    consistent with the shape of the puzzle and should visit each subcube
    of a 3x3 cube exactly once.
    """
    intervals = (1,1,1,2,2,1,2,2,1,1,1,1,2,2,1,2,1,2)
    space = BlockPuzzleSearchSpace(intervals=intervals, cube_width=3)
    return bfs(space)