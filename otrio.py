import numpy as np

class Player():


    def __init__(self, mark, id):

        self.mark = mark
        self.id = id

        self.pieces = {}
        self.pieces[0] = [mark+'1',mark+'1',mark+'1']
        self.pieces[1] = [mark+'2',mark+'2',mark+'2']
        self.pieces[2] = [mark+'3',mark+'3',mark+'3']

class Game():

    def __init__(self, players):

        print("Initializing board...")
        self.board = np.empty((3,3,3)).astype(int)
        self.game_over = False
        self._state = ""
        self.draw_board()
        print("Set empty scores")
        self.scores = {n:0 for n in range(players)}

        print("Setting up players")
        if players >= 2:
            self.players = {0: Player("A", 0), 1: Player("B", 1)}
        if players >= 3:
            self.players[3] = Player("C", 2)
        if players == 4:
            self.players[3] = Player("D", 3)
        if players <2 or players >4:
            print("Invalid player number selection. Must enter players from 2-4")

        self.player_count = players

        print("Setting up win conditions")
        self.win_conditions = {

            "Level 1 top_row":[[0,0,0], [0,0,1], [0,0,2]],
            "Level 1 mid_row":[[0,1,0], [0,1,1], [0,1,2]],
            "Level 1 bot_row":[[0,2,0], [0,2,1], [0,2,2]],
            "Level 1 left_col":[[0,0,0],[0,1,0], [0,2,0]],
            "Level 1 mid_col":[[0,0,1], [0,1,1], [0,1,2]],
            "Level 1 right_col":[[0,0,2], [0,1,2], [0,2,2]],
            "Level 1 left_diag":[[0,0,0], [0,1,1], [0,2,2]],
            "Level 1 right_diag":[[0,0,2], [0,1,1], [0,2,0]],

            "Level 2 top_row":[[1,0,0], [1,0,1], [1,0,2]],
            "Level 2 mid_row":[[1,1,0], [1,1,1], [1,1,2]],
            "Level 2 bot_row":[[1,2,0], [1,2,1], [1,2,2]],
            "Level 2 left_col":[[1,0,0], [1,1,0], [1,2,0]],
            "Level 2 mid_col":[[1,0,1], [1,1,1], [1,2,1]],
            "Level 2 right_col":[[1,0,2], [1,1,2], [1,2,2]],
            "Level 2 left_diag":[[1,0,0], [1,1,1], [1,2,2]],
            "Level 2 right_diag":[[1,0,2], [1,1,1], [1,2,0]],
            
            "Level 3 top_row":[[2,0,0], [2,0,1], [2,0,2]],
            "Level 3 mid_row":[[2,1,0], [2,1,1], [2,1,2]],
            "Level 3 bot_row":[[2,2,0], [2,2,1], [2,2,2]],
            "Level 3 left_col":[[2,0,0], [2,1,0], [2,2,0]],
            "Level 3 mid_col":[[2,0,1], [2,1,1], [2,2,1]],
            "Level 3 right_col":[[2,0,2], [2,1,2], [2,2,2]],
            "Level 3 left_diag":[[2,0,0], [2,1,1], [2,2,2]],
            "Level 3 right_diag":[[2,0,2], [2,1,1], [2,2,0]],

            "Single Column 0,0":[[0,0,0], [1,0,0], [2,0,0]],
            "Single Column 0,1":[[0,0,1], [1,0,1], [2,0,1]],
            "Single Column 0,2":[[0,0,2], [1,0,2], [2,0,2]],
            "Single Column 1,0":[[0,1,0], [1,1,0], [2,1,0]],
            "Single Column 1,1":[[0,1,1], [1,1,1], [2,1,1]],
            "Single Column 1,2":[[0,1,2], [1,1,2], [2,1,2]],
            "Single Column 2,0":[[0,2,0], [1,2,0], [2,2,0]],
            "Single Column 2,1":[[0,2,1], [1,2,1], [2,2,1]],
            "Single Column 2,2":[[0,2,2], [1,2,2], [2,2,2]],

            "Diag top_row asc":[[0,0,0], [1,0,1], [2,0,2]],
            "Diag top_row desc":[[2,0,0], [1,0,1], [0,0,2]],
            "Diag mid_row asc":[[0,1,0], [1,1,1], [2,1,2]],
            "Diag mid_row desc":[[2,1,0], [1,1,1], [0,0,2]],
            "Diag bot_row asc":[[0,2,0], [1,2,1], [2,2,2]],
            "Diag bot_row desc":[[2,2,0], [1,2,1], [0,2,2]],
            "Diag left_col asc":[[0,0,0], [1,1,0], [2,2,0]],
            "Diag left_col desc":[[0,2,0], [1,1,0], [2,0,0]],
            "Diag mid_col asc":[[0,0,1], [1,1,1], [2,2,1]],
            "Diag mid_col desc":[[0,2,1], [1,1,1], [2,0,1]],
            "Diag right_col asc":[[0,0,2], [1,1,2], [2,2,2]],
            "Diag right_col desc":[[2,2,2], [1,1,2], [0,0,2]],
            "Diag left_diag asc":[[0,0,0], [1,1,1], [2,2,2]],
            "Diag right_diag asc":[[2,0,0], [1,1,1], [0,2,2]],
            "Diag left_diag desc":[[0,2,0], [1,1,1], [2,0,2]],
            "Diag right_diag desc":[[2,2,0], [1,1,1], [0,0,2]],

                }

        print("Starting board state:")
        print(self._state)

    def draw_board(self):

        self._state = f"""
        Level 1\t\tLevel 2\t\tLevel 3\n
        {self.board[0,0,0]}|{self.board[0,0,1]}|{self.board[0,0,2]}\t\t{self.board[1,0,0]}|{self.board[1,0,1]}|{self.board[1,0,2]}\t\t{self.board[2,0,0]}|{self.board[2,0,1]}|{self.board[2,0,2]}       
        _____\t\t_____\t\t_____\t\t
        {self.board[0,1,0]}|{self.board[0,1,1]}|{self.board[0,1,2]}\t\t{self.board[1,1,0]}|{self.board[1,1,1]}|{self.board[1,1,2]}\t\t{self.board[2,1,0]}|{self.board[2,1,1]}|{self.board[2,1,2]}
        _____\t\t_____\t\t_____\t\t
        {self.board[0,2,0]}|{self.board[0,2,1]}|{self.board[0,2,2]}\t\t{self.board[1,2,0]}|{self.board[1,2,1]}|{self.board[1,2,2]}\t\t{self.board[2,2,0]}|{self.board[2,2,1]}|{self.board[2,2,2]}
        """

    def make_move(self, action, current_player_num):


        position = tuple(action)
        player_mark = self.players[current_player_num].pieces[action[0]].pop()

        self.board[position] = player_mark
        self.draw_board()
        self.current_player_num = (
            self.current_player_num + 1) % self.player_count


    def get_legal_actions(self):

        current_player = self.current_player_num

        valid_player_levels = [k for k,v in self.players[current_player].pieces.items() if len(v)>0]

        player_legal_board = self.board[valid_player_levels]

        legal_actions = list(np.argwhere(player_legal_board == 0))

        return [legal_actions, self.current_player_num]        

    
    def update_game(self, action, player):
        self.make_move(action, player)

    
    def is_game_over(self):

        avail_actions = self.get_legal_actions()[0]

        for win_condition in self.win_conditions.values():

            condition_state = [self.positions[num] for num in win_condition]           
            #empty = len([i for i in condition_state if i ==' '])
            #for player in self.players:
                #print(len([i for i in condition_state if i==self.players[player].mark])==2)

            #print("Win condition being checked: "+str(win_condition))
            #print("Win condition current state: "+str(condition_state))
            #print("Win condition slots like first slot: "+str(condition_state.count(condition_state[0])))
            #print("Win condition slots like second slot: "+str(condition_state.count(condition_state[1])))
            #print("Win condition slots like second slot: "+str(condition_state.count(condition_state[2])))
            #print("Win condition slot[0]: "+str(condition_state[0]))
            #print("Win condition slot[1]: "+str(condition_state[1]))
            #print("Win condition slot[2]: "+str(condition_state[2]))
            #print("Slots that are empty: "+str(empty))
            #print('\n')

            # this counts if all of the slots are the same as the first slot of the condition state, and that the slot is not empty
            if condition_state.count(condition_state[0]) == len(condition_state) and condition_state[0] != " ":
                open_positions = sum(x == ' ' for x in self.positions)
                if self.players[0].mark == condition_state[0]:
                    self.scores[0] = 10   
                    self.scores[1] = -10# - 10*open_positions
                elif self.players[1].mark == condition_state[0]:
                    self.scores[1] = 10
                    self.scores[0] = -10# - 10*open_positions
                #return True
        
        #if len(avail_actions) == 0:

            #return True
        #else:
            #return False

    def game_result(self):

        return self.scores

    def play_game(self):

        while not self.is_game_over():

            pos = int(input("Select a move.  "))
            self.make_move(pos, self.current_player_num)
            #print(self._state)

        for player_num in self.scores.keys():
            print(
                f"{self.players[player_num].mark}:  {self.scores[player_num]}")

        return self.scores
    

game = Game(4)
game.play_game()
