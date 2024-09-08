import itertools
import random

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
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
        return self.mines_found == self.mines


class Sentence():
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        if len(self.cells) == self.count:
            return set(self.cells)
        return set()

    def known_safes(self):
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
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
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
    # Mark the cell as a move made
        self.moves_made.add(cell)

    # Mark the cell as safe
        self.mark_safe(cell)

    # Add a new sentence to the knowledge base based on the cell and count
        neighbors = self.get_neighbors(cell)
        new_sentence = Sentence(neighbors, count)
    
    # Remove known mines and safes from the new sentence
        for mine in self.mines.copy():
            new_sentence.mark_mine(mine)
            for safe in self.safes.copy():
                new_sentence.mark_safe(safe)
    
        if new_sentence.cells:
            self.knowledge.append(new_sentence)
    
    # Keep updating knowledge base by combining sentences
        updated = True
        while updated:
            updated = False
            safes_to_mark = set()
            mines_to_mark = set()
            for sentence in self.knowledge:
                safes_to_mark |= sentence.known_safes()
                mines_to_mark |= sentence.known_mines()
        
            for safe in safes_to_mark:
                if self.mark_safe(safe):
                    updated = True
                    for mine in mines_to_mark:
                        if self.mark_mine(mine):
                            updated = True
        
        # Iterate over pairs of sentences to infer new information
            for s1 in self.knowledge.copy():
                if s1.cells == set():
                    continue
                for s2 in self.knowledge.copy():
                    if s1 == s2 or s2.cells == set():
                        continue
                    if s1.cells.issubset(s2.cells):
                        new_cells = s2.cells - s1.cells
                        new_count = s2.count - s1.count
                        new_sentence = Sentence(new_cells, new_count)
                        if new_sentence not in self.knowledge:
                            self.knowledge.append(new_sentence)
                            updated = True

    # Remove empty sentences
        self.knowledge = [s for s in self.knowledge if s.cells]

    def get_neighbors(self, cell):
        neighbors = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) != (0, 0):
                    ni, nj = cell[0] + i, cell[1] + j
                    if 0 <= ni < self.height and 0 <= nj < self.width:
                        neighbors.add((ni, nj))
        return neighbors

    def infer_new_knowledge(self):
        new_knowledge_found = True

        while new_knowledge_found:
            new_knowledge_found = False

            for sentence in self.knowledge[:]:
                safes = sentence.known_safes()
                mines = sentence.known_mines()

                if safes:
                    new_knowledge_found = True
                    for safe in safes:
                        self.mark_safe(safe)

                if mines:
                    new_knowledge_found = True
                    for mine in mines:
                        self.mark_mine(mine)

                if len(sentence.cells) == 0:
                    self.knowledge.remove(sentence)

            # Infer new sentences from subsets
            for sentence1 in self.knowledge[:]:
                for sentence2 in self.knowledge[:]:
                    if sentence1 == sentence2:
                        continue

                    if sentence1.cells.issubset(sentence2.cells):
                        new_cells = sentence2.cells - sentence1.cells
                        new_count = sentence2.count - sentence1.count
                        inferred_sentence = Sentence(new_cells, new_count)

                        if inferred_sentence not in self.knowledge and len(new_cells) > 0:
                            self.knowledge.append(inferred_sentence)
                            new_knowledge_found = True

    def make_safe_move(self):
        for move in self.safes:
            if move not in self.moves_made:
                return move
        return None

    def make_random_move(self):
        choices = [(i, j) for i in range(self.height)
                   for j in range(self.width)
                   if (i, j) not in self.moves_made and (i, j) not in self.mines]
        if choices:
            return random.choice(choices)
        return None
