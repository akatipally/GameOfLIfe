import sys, pygame

from game import GameOfLife

from pygame import Rect, QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYDOWN, K_SPACE, K_t, K_p

class GameRendering:
    def __init__(self, board_size, cell_size, initial_state=[]):
        pygame.init()
        self.board_size = board_size
        self.cell_size = cell_size
        self.game = GameOfLife(self.board_size, self.cell_size, initial_state)

    def run(self):
        size = 1000, 1000
        black = 0, 0, 0
        white = 255, 255, 255

        font = pygame.font.Font(None, 64)
        playing_text = font.render('Playing..', True, black)
        not_playing_text = font.render('Paused..', True, black)

        screen = pygame.display.set_mode(size)

        playing = False
        toggle_fill_erase = True
        change_cells = False
        alpha = 0

        clock = pygame.time.Clock()

        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game.print_state()
                    sys.exit()

                elif event.type == MOUSEBUTTONDOWN: change_cells = True

                elif event.type == MOUSEBUTTONUP: change_cells = False

                elif event.type == KEYDOWN and event.key == K_t:
                    toggle_fill_erase = not toggle_fill_erase
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    playing = not playing
                    display_playing_text = playing
                    alpha = 250
                elif event.type == KEYDOWN and event.key == K_p:
                    self.game.print_state()


            screen.fill(white)

            if change_cells:
                coordinates = pygame.mouse.get_pos()
                self.set_cell(coordinates, toggle_fill_erase)

            # draw game
            for row in range(0, self.board_size, self.cell_size):
                pygame.draw.line(screen, black, (row, 0), (row, self.board_size))
            for col in range(0, self.board_size, self.cell_size):
                pygame.draw.line(screen, black, (0, col), (self.board_size, col))
            for cell in self.game.get_alive():
                left = cell[1]
                top = cell[0]
                pygame.draw.rect(screen, black, Rect(left, top, 10, 10))

            # draw text if needed
            if alpha > 0:
                alpha = max(0, alpha - 50)
                if display_playing_text:
                    txt = playing_text.copy()
                else:
                    txt = not_playing_text.copy()
                txt.fill((0, 0, 0, alpha), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(txt, (50, 50))

            if playing:
                self.game.advance_time()
            pygame.display.flip()
            clock.tick(60)

    def set_cell(self, coordinates, state):
        self.game.set_cell(coordinates[1], coordinates[0], state)

rendering = GameRendering(1000, 10)
rendering.run()



