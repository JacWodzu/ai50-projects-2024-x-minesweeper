import itertools
import random

class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()
        self.board = [[False for _ in range(width)] for _ in range(height)]  # Create a board for mines

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                print("| X" if self.board[i][j] else "|  ", end="")
            print("|")
        print("--" * self.width + "-")

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """
        count = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1
        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines == self.mines_found


class Sentence:
    """
    Logical statement about a Minesweeper game
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
        if len(self.cells) == self.count:
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells that are known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        return set()

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
        Called when the AI is told that a given safe cell has a certain number of
        neighboring mines. This function should:
        1) Mark the cell as a move made.
        2) Mark the cell as safe.
        3) Add a new sentence to the AI's knowledge base based on the value of `cell` and `count`.
        4) Mark any additional cells as safe or as mines if it can be concluded.
        5) Add any new inferences to the AI's knowledge base.
        """
        # Mark the cell as a move made
        self.moves_made.add(cell)

        # Mark the cell as safe
        self.mark_safe(cell)

        # Determine the neighboring cells
        neighbors = self.get_neighbors(cell)

        # Remove known safes and mines from the neighboring cells
        unknown_neighbors = neighbors - self.safes - self.mines

        # Add the new sentence to the knowledge base if there are unknown neighbors
        if unknown_neighbors:
            new_sentence = Sentence(unknown_neighbors, count)
            self.knowledge.append(new_sentence)

        # Infer new knowledge from the current knowledge base
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
        Repeatedly checks the knowledge base to mark any cells as safe or as mines
        based on the known information. Also performs inference by checking for 
        subset relationships between sentences.
        """
        updated = True
        while updated:
            updated = False

            # First pass: mark known mines and safes
            for sentence in self.knowledge.copy():
                known_mines = sentence.known_mines()
                known_safes = sentence.known_safes()

                if known_mines:
                    for mine in known_mines:
                        if mine not in self.mines:
                            self.mark_mine(mine)
                            updated = True

                if known_safes:
                    for safe in known_safes:
                        if safe not in self.safes:
                            self.mark_safe(safe)
                            updated = True

            # Second pass: check for subsets and create new sentences
            for sentence1 in self.knowledge.copy():
                for sentence2 in self.knowledge.copy():
                    if sentence1 != sentence2 and sentence1.cells.issubset(sentence2.cells):
                        new_count = sentence2.count - sentence1.count
                        new_cells = sentence2.cells - sentence1.cells
                        if new_cells and new_count >= 0:  # Ensure non-negative count
                            new_sentence = Sentence(new_cells, new_count)
                            if new_sentence not in self.knowledge:
                                self.knowledge.append(new_sentence)
                                updated = True

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
        The move must not be a move that is known to be a mine.
        If no such moves are possible, the function should return None.
        """
        all_possible_moves = {(i, j) for i in range(self.height) for j in range(self.width)}
        available_moves = all_possible_moves - self.moves_made - self.mines
        if available_moves:
            return random.choice(list(available_moves))
        return None
