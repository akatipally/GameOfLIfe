from collections import defaultdict

# 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# 2. Any live cell with two or three live neighbors lives on to the next generation.
# 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
# 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
class GameOfLife:
    def __init__(self, board_size, cell_size, initial_alive=[]):
        if initial_alive is None:
            initial_alive = []
        self.board_size = board_size
        self.cell_size = cell_size
        self.board = defaultdict(lambda: defaultdict(lambda: False))
        for entry in initial_alive:
            self.board[entry[0]][entry[1]] = True

    def get_alive(self):
        res = []
        for row, cols in self.board.items():
            for col in cols.keys():
                if self.board[row][col]:
                    res.append((row, col))
        return res

    def set_cell(self, row, col, state):
        row = row - (row % self.cell_size)
        col = col - (col % self.cell_size)
        self.board[row][col] = state

    def advance_time(self):
        new_board = defaultdict(lambda: defaultdict(lambda: False))
        for row, cols in list(self.board.items()):
            for col in list(cols.keys()):
                alive = self.board[row][col]
                if not alive:
                    continue
                neighbors = self.get_neighbors(row, col, self.cell_size, self.board_size)
                live_neighbor_count = 0
                for neighbor in neighbors:
                    neighbor_row, neighbor_col = neighbor[0], neighbor[1]
                    neighbor_alive = self.board[neighbor_row][neighbor_col]
                    if neighbor_alive:
                        live_neighbor_count += 1
                    # Rule 4
                    if not neighbor_alive and not new_board[neighbor_row][neighbor_col]:
                        dead_cell_neighbors = self.get_neighbors(neighbor_row, neighbor_col, self.cell_size, self.board_size)
                        dead_cell_neighbors_count = 0
                        for alt_neighbor in dead_cell_neighbors:
                            alt_neighbor_row, alt_neighbor_col = alt_neighbor[0], alt_neighbor[1]
                            alt_alive = self.board[alt_neighbor_row][alt_neighbor_col]
                            if alt_alive:
                                dead_cell_neighbors_count += 1
                        if dead_cell_neighbors_count == 3:
                            new_board[neighbor_row][neighbor_col] = True
                # Rule 1
                if live_neighbor_count < 2:
                    new_board[row][col] = False
                # Rule 2
                elif live_neighbor_count > 3:
                    new_board[row][col] = False
                # Rule 3
                else:
                    new_board[row][col] = True
        self.board = new_board

    @staticmethod
    def get_neighbors(current_row, current_col, cell_size, board_size):
        res = []
        possible_rows = [current_row]
        possible_cols = [current_col]
        if current_row > 0:
            possible_rows.append(current_row - cell_size)
        if current_row < board_size - cell_size:
            possible_rows.append(current_row + cell_size)
        if current_col > 0:
            possible_cols.append(current_col - cell_size)
        if current_col < board_size - cell_size:
            possible_cols.append(current_col + cell_size)

        for row in possible_rows:
            for col in possible_cols:
                if row == current_row and col == current_col:
                    continue
                res.append((row, col))
        return res

    def print_state(self):
        string = ''
        for entry in self.get_alive():
            string += '(' + str(entry[0]) + ',' + str(entry[1]) + '), '
        print(string)


inputs = [
    (500, 500),
    (500, 510),
    (500, 520),
    (510, 500),
    (520, 510)
]
game = GameOfLife(1000, 10, inputs)
game.advance_time()
game.print_state()
game.advance_time()
game.print_state()
game.advance_time()
game.print_state()
