
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
        if len(self.cells) == self.count:
            return set(self.cells)
        return set()

    def known_safes(self, ai):
        """ Returns the set of all cells in self.cells known to be safe. """
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

#def mark_mine(self, ai, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1  # Decrement mine count
            
    
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
      

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
        """
        Called when the AI makes a move on a safe cell and knows how many mines surround it.
        """
        # Mark the cell as a safe move
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Get neighboring cells
        neighbors = self.get_neighbors(cell)
        new_sentence_cells = neighbors - self.safes - self.mines

        # Add new sentence based on the revealed cell's neighboring mine count
        if new_sentence_cells:
            new_sentence = Sentence(new_sentence_cells, count)
            self.knowledge.append(new_sentence)

        # Inference: Update knowledge based on new information
        self.infer_new_knowledge()
        
   
   

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
        
        """
        Loops through the knowledge base to infer safe cells, mines, or new sentences.
        """
        updated = True
        while updated:
            updated = False

            # First pass: Identify known mines and safes
            for sentence in self.knowledge:
                # Mark known mines
                mines = sentence.known_mines()
                if mines:
                    for mine in mines:
                        if mine not in self.mines:
                            self.mark_mine(mine)
                            updated = True

                # Mark known safes
                safes = sentence.known_safes()
                if safes:
                    for safe in safes:
                        if safe not in self.safes:
                            self.mark_safe(safe)
                            updated = True

            # Second pass: Check for subset inference
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence1 != sentence2 and sentence1.cells.issubset(sentence2.cells):
                        inferred_cells = sentence2.cells - sentence1.cells
                        inferred_count = sentence2.count - sentence1.count
                        if inferred_cells:
                            new_sentence = Sentence(inferred_cells, inferred_count)
                            if new_sentence not in self.knowledge:
                                self.knowledge.append(new_sentence)
                                updated = True

            # Remove any empty sentences
            self.knowledge = [sentence for sentence in self.knowledge if sentence.cells]


    def make_safe_move(self):
        """ Returns a safe cell to proceed in the Minesweeper board. """
        """ Returns a safe cell to proceed in the Minesweeper board. """
        safe_moves = self.safes - self.moves_made
        if safe_moves:
            return safe_moves.pop()  # Return one safe move
        return None  # No safe moves available
    
    

    def make_random_move(self):
        """
        Returns a random move to make on the board.
        It avoids cells that are known to be mines or have already been clicked.
        """
        all_possible_moves = set(itertools.product(range(self.height), range(self.width)))
        available_moves = list(all_possible_moves - self.moves_made - self.mines)

        if available_moves:
            return random.choice(available_moves)
        return None

