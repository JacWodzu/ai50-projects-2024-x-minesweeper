import itertools
import random

class Sentence:
    """
    Logical statement about a Minesweeper game.
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells that are known to be mines.
        """
        return self.cells if len(self.cells) == self.count else set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells that are known to be safe.
        """
        return self.cells if self.count == 0 else set()

    def mark_mine(self, cell):
        """
        Updates the sentence when a cell is confirmed as a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates the sentence when a cell is confirmed as safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI:
    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()    # Track all moves made
        self.mines = set()         # Track cells that are mines
        self.safes = set()         # Track cells that are safe
        self.knowledge = []        # Knowledge base of sentences about the game

        # Define self.cells as all cells in the grid
        self.cells = set((i, j) for i in range(self.height) for j in range(self.width))

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
        self.moves_made.add(cell)  # Mark the move as made
        self.safes.add(cell)       # The cell is safe since we just revealed it

    # Create a new sentence based on the neighboring cells
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) != cell and 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.add((i, j))
    
    # Add the new sentence to the knowledge base
        new_sentence = Sentence(neighbors, count)
        self.knowledge.append(new_sentence)

    # Try to infer any new information after adding this knowledge
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
        # Example logic for inferring new knowledge
        for sentence in self.knowledge:
            if len(sentence.cells) == sentence.count:  # All cells in sentence are mines
                for cell in sentence.cells:
                    self.mines.add(cell)
            elif sentence.count == 0:  # All cells in sentence are safe
                    for cell in sentence.cells:
                        self.safes.add(cell)

    # Now check for new safe cells across all cells on the board
        for cell in self.cells:
            if cell not in self.mines and cell not in self.safes:
                # Add your logic for checking if this cell is safe or not
                if self.is_safe(cell):  # Assume this is defined elsewhere
                    self.safes.add(cell)



    def is_safe(self, cell):
        # Your logic to determine if the cell is safe
        # For example:
            return (
                # Check surrounding cells and the knowledge base to determine if this cell can be considered safe
                )





    def make_safe_move(self):
        """
        Returns a move (i, j) that is known to be safe.
        The move returned must be known to be safe, and not a move already made.
        """
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe
        return None

    def make_random_move(self):
        """
        Returns a random move (i, j).
        This function will be called if a safe move is not possible.
        The move must not be a move that has already been made.
        """
        all_possible_moves = {(i, j) for i in range(self.height) for j in range(self.width)}
        valid_moves = all_possible_moves - self.moves_made - self.mines
        if valid_moves:
            return random.choice(list(valid_moves))
        return None
