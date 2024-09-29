
import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()
@@ -34,10 +31,6 @@ def __init__(self, height=8, width=8, mines=8):
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
@@ -53,43 +46,21 @@ def is_mine(self, cell):
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines

class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

class Sentence():
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
@@ -100,46 +71,27 @@ def __eq__(self, other):
    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self, ai):
        """ Returns the set of all cells in self.cells known to be mines. """
        return {cell for cell in self.cells if cell in self.mines}

    def known_safes(self, ai):
        """ Returns the set of all cells in self.cells known to be safe. """
        return {cell for cell in self.cells if cell in self.safes}

    def count_mines(self, ai):
        """ Returns a set of known mines in the sentence. """
        return self.cells.intersection(ai.mines)
    def known_mines(self):
        if len(self.cells) == self.count:
            return set(self.cells)
        return set()

    def count_safes(self, ai):
        """ Returns a set of known safe cells in the sentence. """
        return self.cells.intersection(ai.safes)
    def known_safes(self):
        if self.count == 0:
            return set(self.cells)
        return set()

#def mark_mine(self, ai, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            
        #if cell in self.cells:
         #   self.cells.remove(cell)
          #  self.count -= 1  # Decrease count of mines by 1
           # self.count -= 1

  #  def mark_safe(self, ai, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            # No need to decrease count for safe
        #if cell in self.cells:
         #   self.cells.remove(cell)
        # No decrement on count as a safe does not affect mine count
        # No decrement on count as a safe does not affect mine count

#class MinesweeperAI():
    """
    Minesweeper game player
    """

class MinesweeperAI():
    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []
#@@ -150,103 +102,85 @@ def __init__(self, height=8, width=8):
        #self.knowledge = []

    def mark_mine(self, cell):
        """ Mark a cell as a mine and update all sentences accordingly. """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """ Mark a cell as safe and update all sentences accordingly. """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """ Updates knowledge based on the cell clicked and the count of mines around it. """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        neighbors = self.get_neighbors(cell)
        new_sentence_cells = neighbors - self.safes - self.mines

        # Create a new sentence only if it has undetermined neighbors
        if new_sentence_cells:
            new_sentence = Sentence(new_sentence_cells, count)
            self.knowledge.append(new_sentence)

        # Inference loop to update knowledge
        self.infer_new_knowledge()
        
        #self.moves_made.add(cell)  # Mark the cell as moved
        #self.mark_safe(cell)  # Mark the clicked cell as safe
        # Get neighboring cells
        #neighbors = self.get_neighbors(cell)
        #new_sentence_cells = neighbors - self.safes - self.mines  # Exclude known safes and mines
         # Create a new sentence if there are still undetermined neighbors
        #if new_sentence_cells:
         #   new_sentence = Sentence(new_sentence_cells, count)
          #  self.knowledge.append(new_sentence)  # Add it to knowledge

            # Check for new inferences immediately after adding the knowledge
           # self.infer_new_knowledge()


        # Get neighboring cells
       # neighbors = self.get_neighbors(cell)
        #new_sentence_cells = neighbors - self.safes - self.mines  # Exclude known safes and mines
        #neighbors = neighbors - self.safes - self.mines

        # Create a new sentence representing the current cell's neighbors and count
        #new_sentence = Sentence(new_sentence_cells, count)
        #self.knowledge.append(new_sentence)  # Add it to knowledge
        #if len(neighbors) > 0:
         #   self.knowledge.append(Sentence(neighbors, count))

        # Check for new inferences
        #self.infer_new_knowledge()

    def get_neighbors(self, cell):
        """ Returns the set of neighboring cells for the given cell. """
        """ Returns the set of neighboring cells for the given cell. """
        neighbors = set()
        for i in range(-1, 2):  # -1, 0, 1
            for j in range(-1, 2):  # -1, 0, 1
                if (i, j) != (0, 0):  # Exclude the cell itself
                    ni, nj = cell[0] + i, cell[1] + j
                    if 0 <= ni < self.height and 0 <= nj < self.width:
                        neighbors.add((ni, nj))
      #  return neighbors
       # neighbors = set()
        #for i in range(-1, 2):  # -1, 0, 1
         #   for j in range(-1, 2):  # -1, 0, 1
          #      if (i, j) != (0, 0):  # Exclude the cell itself
        #for i in range(-1, 2):
         #   for j in range(-1, 2):
          #      if (i, j) != (0, 0):
           #         ni, nj = cell[0] + i, cell[1] + j
            #        if 0 <= ni < self.height and 0 <= nj < self.width:
             #           neighbors.add((ni, nj))
       # return neighbors

    def infer_new_knowledge(self):
        
        """ Check knowledge base for new safe cells or mines and add sentences. """
        updated = True
        while updated:
            updated = False

            for sentence in self.knowledge:
                # Check for known mines
                mines = sentence.known_mines()
                for mine in mines:
                    self.mark_mine(mine)
                    updated = True

                # Check for known safes
                safes = sentence.known_safes()
                for safe in safes:
                    self.mark_safe(safe)
                    updated = True

            # Infer new sentences from subsets
            for i in range(len(self.knowledge)):
                for j in range(len(self.knowledge)):
                    if i != j:
                        sentence1 = self.knowledge[i]
                        sentence2 = self.knowledge[j]
                        if sentence1.cells.issubset(sentence2.cells):
                            new_cells = sentence2.cells - sentence1.cells
                            new_count = sentence2.count - sentence1.count
                            if new_count >= 0 and new_cells:
                                new_sentence = Sentence(new_cells, new_count)
                                if new_sentence not in self.knowledge:
                                    self.knowledge.append(new_sentence)
                                    updated = True


    def make_safe_move(self):
        """ Returns a safe cell to proceed in the Minesweeper board. """
        """ Returns a safe cell to proceed in the Minesweeper board. """
        safe_moves = self.safes - self.moves_made
        if safe_moves:
            return safe_moves.pop()  # Return one safe move
        return None  # No safe moves available
    
    

    def make_random_move(self):
        """ Returns a random move that hasn't been made already and isn't a known mine. """
        all_possible_moves = {(i, j) for i in range(self.height) for j in range(self.width)}
        valid_moves = all_possible_moves - self.moves_made - self.mines
        if valid_moves:
            return random.choice(list(valid_moves))
        return None  # No moves possible

