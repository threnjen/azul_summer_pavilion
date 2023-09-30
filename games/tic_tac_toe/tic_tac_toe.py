from typing import Any

from games.game_components.base_game_object import GameEnvironment
from .player import TicTacToePlayer
from typing import ClassVar
from .action import TicTacToeAction
import numpy as np


class TicTacToe(GameEnvironment):
    """Tic tac toe game"""

    positions: list[str] = [" "] * TicTacToeAction.ACTION_SPACE_SIZE
    game_over: bool = False
    current_player_num: int = 0
    win_conditions: ClassVar[dict[str, list[int]]] = {
        "top_row": [0, 1, 2],
        "left_diag": [0, 4, 8],
        "mid_row": [3, 4, 5],
        "bot_row": [6, 7, 8],
        "right_diag": [6, 4, 2],
        "left_col": [0, 3, 6],
        "mid_col": [1, 4, 7],
        "right_col": [2, 5, 8],
    }
    player_marks: ClassVar[dict[int, str]] = {0: "X", 1: "O"}

    @property
    def current_player(self) -> TicTacToePlayer:
        return self.players[self.current_player_num]

    def model_post_init(self, __context: Any) -> None:
        if self.players is None:
            self.players = {
                player_num: TicTacToePlayer(
                    player_number=player_num, mark=self.player_marks[player_num]
                )
                for player_num in range(self.player_count)
            }

    # not clear if this is needed since we can call game.model_dump()
    def get_game_state(self) -> tuple:
        return (
            tuple(self.positions),
            tuple(self.scores.values()),
            (self.game_over),
            (self.current_player_num),
        )

    # same as above, likely unnecessary
    def update_game_state(self, game_state: tuple):
        (
            self.positions,
            temp_scores,
            self.game_over,
            self.current_player_num,
        ) = game_state
        self.positions = list(self.positions)
        self.scores.update(zip(self.scores.keys(), temp_scores))

    @property
    def board(self):
        """Just draw an ASCII board."""
        board = f"""\n
        {self.positions[0]}|{self.positions[1]}|{self.positions[2]}       
        _____
        {self.positions[3]}|{self.positions[4]}|{self.positions[5]}
        _____
        {self.positions[6]}|{self.positions[7]}|{self.positions[8]}"""

        return board

    def get_current_player(self) -> int:
        return self.current_player_num

    def get_available_actions(self, special_policy: bool = False) -> list:
        """Gets available moves in a dictionary.
        The bot will only ever need the keys; values should be unknown
        """
        legal_actions = [
            self.generate_action_from_position(i)
            for i in range(TicTacToeAction.ACTION_SPACE_SIZE)
            if self.positions[i] == " "
        ]

        # print(f"Original legal actions: {legal_actions}")

        if special_policy:
            special_policy_actions = []
            for win_condition in self.win_conditions.values():
                condition_state = self.get_condition_state(win_condition)

                if (
                    " " in condition_state
                    and condition_state.count(self.current_player.mark) == 2
                ):
                    special_policy_actions += [
                        TicTacToeAction(
                            np.eye(TicTacToeAction.ACTION_SPACE_SIZE, dtype=int)[
                                position
                            ]
                        )
                        for position in win_condition
                        if self.positions[position] == " "
                    ]

            special_policy_actions = list(set(special_policy_actions))
            if len(special_policy_actions) > 0:

                # print(
                #    f"Available win positions for {self.player_marks[current_player]}, Special policy legal actions: {special_policy_actions}"
                # )
                return special_policy_actions

        return legal_actions

    def update_game_with_action(
        self, action: TicTacToeAction, player: TicTacToePlayer = None
    ):
        """Makes a move on the board and draws it"""

        self.positions[action.position] = self.current_player.mark
        self.game_over = self.check_game_over()

        self.current_player_num = (self.current_player_num + 1) % self.player_count

    def get_condition_state(self, win_condition: list[int]):
        return [self.positions[num] for num in win_condition]

    def is_game_over(self):
        return self.game_over

    def check_game_over(self):
        """Checks for the eight win conditions, and whether there are moves left.

        Returns:
            bool: Over or not
        """

        for win_condition in self.win_conditions.values():
            condition_state = self.get_condition_state(win_condition)
            if (
                condition_state.count(condition_state[0]) == len(condition_state)
                and condition_state[0] == self.current_player.mark
            ):
                self.current_player.player_score = 1
                self.players[(self.current_player_num + 1) % self.player_count].player_score = -1
                return True

        if len(self.get_available_actions()) == 0:
            self.players[0].player_score = 0
            self.players[1].player_score = 0
            return True
        else:
            return False

    @property
    def scores(self):
        return {
            player_num: player.player_score
            for player_num, player in self.players.items()
        }

    def get_game_scores(self):
        return self.scores

    def play_game(self):
        while not self.is_game_over():
            pos = int(input("Select a move.  "))
            action = self.generate_action_from_position(pos)
            self.update_game_with_action(action, self.current_player_num)
            print(self.board)
        for player_num, player in self.players.items():
            print(f"{player_num}:  {player.player_score}")

        return self.scores

    def generate_action_from_position(self, position: int):
        return np.array(
            [
                1 if i == position else 0
                for i in range(TicTacToeAction.ACTION_SPACE_SIZE)
            ]
        ).view(TicTacToeAction)


if __name__ == "__main__":
    game = TicTacToe(player_count=2)
    game.play_game()
