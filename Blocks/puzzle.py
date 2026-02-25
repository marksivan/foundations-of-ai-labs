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
      """Determines the possible successors of a state.




      A state is a sequence of directions. To generate its successor, we append a direction
      that forces the puzzle to make a 90-degree turn along some axis. In other words,
      one cannot append the direction in which the puzzle is already heading, nor can one
      append the completely opposite direction.




      For instance, if the state is (U, N, W), then we cannot append directions "W" (the
      direction in which the puzzle is currently going) or "E" (the opposite direction)
      to derive a successor.








      Parameters
      ----------
      state : tuple[str]
          A state of the search space, i.e. a sequence of directions




      Returns
      -------
      list[tuple[str]]
          The list of valid successor states.
      """
    
      # keep track of the pivot positions  
      pivot_sums = set()




      curr_sum = 0
      for interval in self.intervals:
          curr_sum += interval
          pivot_sums.add(curr_sum)




      directions = ["E", "W", "N", "S", "U", "D"]




      opposites = {"E": "W",
                   "W": "E",
                   "N": "S",
                   "S":"N",
                   "D":"U",
                   "U":"D"}
      result = []
    
      curr_direction = state[-1]






       # check if it at a pivot position
      if len(state) not in pivot_sums:
      
          new_tuple = state + (curr_direction,)
          result.append(new_tuple)
      else:


         
          for direction in directions:
              if direction != curr_direction and opposites[curr_direction] != direction:
                  new_tuple = state + (direction,)
                  result.append(new_tuple)




      def has_valid_positions(state):
    




          pos = (0, 0, 0)
          visited = {pos}  # start position is already occupied
          for direction in state:
              dx, dy, dz = self.direction_values[direction]
              pos = (pos[0] + dx, pos[1] + dy, pos[2] + dz)




              x_values = [tup[0] for tup in visited]
              y_values = [tup[1] for tup in visited]
              z_values = [tup[2] for tup in visited]




              if pos in visited:
                  return False


              # check bounds
              
              if (max(x_values) - min(x_values) >= self.cube_width) or (max(y_values) - min(y_values) >= self.cube_width) or (max(z_values) - min(z_values) >= self.cube_width):
                  return False
              if any(abs(c) >= self.cube_width for c in pos):
                  return False
              # check overlap
          
              visited.add(pos)
          return True
      # keep track of the pruned states
      pruned_states = []
      for state in result:
          if has_valid_positions(state):
              pruned_states.append(state)




        




      return pruned_states
 




    
    
  
    












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




  intervals = (2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 2 )
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





