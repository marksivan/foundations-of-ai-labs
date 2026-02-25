from search import SearchSpace, a_star_search
from tqdm import tqdm






class TrieNode:
   def __init__(self):
       self.children = [None] * 26
       self.is_terminal = False


class Trie:
   def __init__(self, words=None):
       self.root = TrieNode()


       if words:
           for word in words:
               self.insert(word)
      
  
   def insert(self, word):
       node = self.root


       for ch in word:
           index = ord(ch) - ord("a")
           child = node.children[index]


           if child is None:
               child = TrieNode()
               node.children[index] = child
          
           node = child
       node.is_terminal = True


   def is_valid_prefix(self, word1, word2):
       node = self.root
      
       for ch in word1:
           index = ord(ch) - ord("a")
           node = node.children[index]
           if node is None:
               return False
          
       for ch in word2:
           idx = ord(ch) - 97
           node = node.children[idx]
           if node is None:
               return False


       return True


class LetterBoxedSearchSpace(SearchSpace):




   def __init__(self, letters, words):
       self.letters = letters
       self.num_letters = len(self.letters)
       self.letters_index_map = {letter: i for i, letter in enumerate(letters)}
       self.words = self.filter_valid_words(words)
       self.trie = Trie(self.words)
  
   def get_directions(self):
       num_letters = self.num_letters
       first_quarter_end = num_letters//4
       second_quarter_end = num_letters//2
       third_quarter_end = int(self.num_letters * 0.75)


       top = set(i for i in range(first_quarter_end))
       right = set(i for i in range(first_quarter_end, second_quarter_end))
       down = set(i for i in range(second_quarter_end, third_quarter_end))
       left = set(i for i in range(third_quarter_end, num_letters))


       return [top, right, down, left]
  


   def filter_valid_words(self, words):
       side_sets = self.get_directions()
       valid_words = set()


       def same_side(x, y):
           return any(x in s and y in s for s in side_sets)


       for word in words:
           # must use only allowed letters
           if any(ch not in self.letters_index_map for ch in word):
               continue


           valid = True
           for i in range(len(word) - 1):
               idx1 = self.letters_index_map[word[i]]
               idx2 = self.letters_index_map[word[i+1]]
               if same_side(idx1, idx2):
                   valid = False
                   break


           if valid:
               valid_words.add(word)


       return valid_words










   def get_start_state(self):
       return ('', None, (0,) * self.num_letters)


   def is_final_state(self, state):
       current_word_so_far, last_letter_clicked_on, letters_clicked_on = state


       if len(current_word_so_far) != 1:
           return False
      
       return 0 not in letters_clicked_on
   
 




   def get_successors(self, state):
       current_word, last_idx, letters_clicked = state
       successors = []
       side_sets = self.get_directions()


       def same_side(x, y):
           return any(x in s and y in s for s in side_sets)


       for letter in self.letters:
           idx = self.letters_index_map[letter]


           if last_idx is not None and same_side(last_idx, idx):
               continue


           if not self.trie.is_valid_prefix(current_word, letter):
               continue


           temp_clicked = list(letters_clicked)
           temp_clicked[idx] = 1


           successors.append(
               ((current_word + letter, idx, tuple(temp_clicked)), letter, 0)
           )
       if current_word in self.words:
           successors.append(
               ((current_word[-1], self.letters_index_map[current_word[-1]], letters_clicked),
               "ENTER", 1)
           )


       return successors








def create_heuristic(letters, words):


   # letters_dict = {letter:i for i, letter in enumerate(letters)}


   max_length_of_word  = 0


   for word in words:
       max_length_of_word = max(len(word), max_length_of_word)
  
   def heuristic(state, space):
       curr_word, action, letters_clicked = state
       zero_count = sum(1 for num in letters_clicked if num == 0) # number of unused letters
       return (zero_count + max_length_of_word - 1)//max_length_of_word
  
      
   return heuristic
  
 


# if __name__ == "__main__":
#     from itertools import combinations


#     letters = list("hhhiitttccc")
#     words = []
#     with open("words.scrabble.txt") as reader:
#         for line in reader:
#             word = line.strip()
#             words.append(word)
  
#     space = LetterBoxedSearchSpace(letters, words)
#     solution = a_star_search(space, create_heuristic(letters, words, ))
#     print(solution)
#     # display_solution(solution)

