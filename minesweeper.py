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

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
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

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self, ai):
        """ Returns the set of all cells in self.cells known to be mines. """
        return {cell for cell in self.cells if cell in ai.mines}

    def known_safes(self, ai):
        """ Returns the set of all cells in self.cells known to be safe. """
        return {cell for cell in self.cells if cell in ai.safes}

    def count_mines(self, ai):
        """ Returns a set of known mines in the sentence. """
        return self.cells.intersection(ai.mines)

    def count_safes(self, ai):
        """ Returns a set of known safe cells in the sentence. """
        return self.cells.intersection(ai.safes)

    def mark_mine(self, ai, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1  # Decrease count of mines by 1

    def mark_safe(self, ai, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        # No decrement on count as a safe does not affect mine count
        # No decrement on count as a safe does not affect mine count

class MinesweeperAI():
    """
    Minesweeper game player
    """

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
        """ Updates knowledge based on the cell clicked and the count of mines around it. """
        self.moves_made.add(cell)  # Mark the cell as moved
        self.mark_safe(cell)  # Mark the clicked cell as safe

        # Get neighboring cells
        neighbors = self.get_neighbors(cell)
        new_sentence_cells = neighbors - self.safes - self.mines  # Exclude known safes and mines

        # Create a new sentence representing the current cell's neighbors and count
        new_sentence = Sentence(new_sentence_cells, count)
        self.knowledge.append(new_sentence)  # Add it to knowledge

        # Check for new inferences
        self.infer_new_knowledge()

    def get_neighbors(self, cell):
        """ Returns the set of neighboring cells for the given cell. """
        neighbors = set()
        for i in range(-1, 2):  # -1, 0, 1
            for j in range(-1, 2):  # -1, 0, 1
                if (i, j) != (0, 0):  # Exclude the cell itself
                    ni, nj = cell[0] + i, cell[1] + j
                    if 0 <= ni < self.height and 0 <= nj < self.width:
                        neighbors.add((ni, nj))
        return neighbors

    def infer_new_knowledge(self):
        """ Check knowledge base for new safe cells or mines and add sentences. """
        while True:  # Keep looping until no new knowledge is found
            new_knowledge_found = False

        # Check each sentence for known safes and mines
        for sentence in self.knowledge:
            # Check if any known mines exist in the sentence
            mines = sentence.known_mines(self)
            if mines:
                for mine in mines:
                    self.mark_mine(mine)
                    new_knowledge_found = True

            # Check if any known safes exist in the sentence
            safes = sentence.known_safes(self)
            if safes:
                for safe in safes:
                    self.mark_safe(safe)
                    new_knowledge_found = True

        # Now we try to infer new sentences based on the ones we have
        new_sentences = []
        for i in range(len(self.knowledge)):
            for j in range(i + 1, len(self.knowledge)):
                sentence1 = self.knowledge[i]
                sentence2 = self.knowledge[j]

                # If sentence1 is a subset of sentence2
                if sentence1.cells.issubset(sentence2.cells):
                    new_cells = sentence2.cells - sentence1.cells
                    new_count = sentence2.count - sentence1.count
                    if new_cells and new_count >= 0:  # Ensure we have a valid new sentence
                        new_sentences.append(Sentence(new_cells, new_count))

        # Add newly inferred sentences to knowledge
            self.knowledge.extend(new_sentences)

        # If no new knowledge was gathered, break the loop
            if not new_knowledge_found:
                break


    def make_safe_move(self):
        """ Returns a safe cell to proceed in the Minesweeper board. """
        safe_moves = self.safes - self.moves_made
        if safe_moves:
            return safe_moves.pop()  # Return one safe move
        return None  # No safe moves available

    def make_random_move(self):
        """ Returns a random move that hasn't been made already and isn't a known mine. """
        all_possible_moves = set()
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell not in self.moves_made and cell not in self.mines:
                    all_possible_moves.add(cell)

        if all_possible_moves:
            return random.choice(list(all_possible_moves))  # Choose a random move
        return None  # No moves are possible