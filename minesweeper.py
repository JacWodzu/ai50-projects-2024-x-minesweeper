
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

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count
    
    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self, ai):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return set(self.cells)
        return set()

    def known_safes(self, ai):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        return set()

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

    def mark_mine(self, cell):
        """
        Updates internal knowledge given the fact that a cell is a known mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            
    
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
    def mark_safe(self, cell):
        """
        Updates internal knowledge given the fact that a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            

class MinesweeperAI():
    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []


    def mark_mine(self, cell):
        """
        Marks a cell as a mine and updates all knowledge accordingly.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
            

    def mark_safe(self, cell):
        """
        Marks a cell as safe and updates all knowledge accordingly.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Adds knowledge about the given cell, including its neighboring mine count.
        """
        # Mark the cell as a move made
        self.moves_made.add(cell)

        # Mark the cell as safe
        self.mark_safe(cell)

        # Get all neighbors of the cell
        neighbors = self.get_neighbors(cell)

        # Create a new sentence for the unexplored neighbors
        unexplored_neighbors = neighbors - self.safes - self.mines
        if unexplored_neighbors:
            new_sentence = Sentence(unexplored_neighbors, count)
            self.knowledge.append(new_sentence)

        # Update the knowledge base with inferences
        self.update_knowledge()       
   
   

    def get_neighbors(self, cell):
        """
        Returns the set of neighboring cells for a given cell.
        """
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) != cell and 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.add((i, j))
        return neighbors


    def infer_new_knowledge(self):
        
         updated = True
        while updated:
            updated = False

            # First pass: mark any known mines or safe cells
            for sentence in self.knowledge:
                mines = sentence.known_mines()
                safes = sentence.known_safes()

                if mines:
                    for mine in mines:
                        if mine not in self.mines:
                            self.mark_mine(mine)
                            updated = True

                if safes:
                    for safe in safes:
                        if safe not in self.safes:
                            self.mark_safe(safe)
                            updated = True

            # Second pass: infer new sentences
            new_knowledge = []
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence1 != sentence2 and sentence1.cells.issubset(sentence2.cells):
                        inferred_cells = sentence2.cells - sentence1.cells
                        inferred_count = sentence2.count - sentence1.count
                        new_sentence = Sentence(inferred_cells, inferred_count)
                        if new_sentence not in self.knowledge and new_sentence not in new_knowledge:
                            new_knowledge.append(new_sentence)
                            updated = True

            self.knowledge.extend(new_knowledge)


    def make_safe_move(self):
        """
        Returns a safe cell to choose, if one is known.
        """
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe
        return None
    
    

    def make_random_move(self):
        """
        Returns a random cell that has not been chosen and is not known to be a mine.
        """
        possible_moves = [(i, j) for i in range(self.height) for j in range(self.width)
                          if (i, j) not in self.moves_made and (i, j) not in self.mines]
        return random.choice(possible_moves) if possible_moves else None
