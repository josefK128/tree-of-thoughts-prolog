# two-player coroutine board game

import asyncio

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'

    def print_board(self):
        for i in range(0, 9, 3):
            print(' | '.join(self.board[i:i+3]))
            if i < 6:
                print('-' * 9)

    async def get_move(self):
        while True:
            try:
                move = int(input(f"Player {self.current_player}, enter your move (0-8): "))
                if 0 <= move <= 8 and self.board[move] == ' ':
                    return move
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Enter a number between 0 and 8.")

    async def play_game(self):
        while True:
            self.print_board()
            move = await self.get_move()
            self.board[move] = self.current_player

            if self.check_winner():
                self.print_board()
                print(f"Player {self.current_player} wins!")
                break
            elif ' ' not in self.board:
                self.print_board()
                print("It's a tie!")
                break

            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]

        for a, b, c in winning_combinations:
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                return True
        return False

async def main():
    game = TicTacToe()
    await game.play_game()

if __name__ == "__main__":
    asyncio.run(main())
