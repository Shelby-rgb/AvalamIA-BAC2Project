import re
import random

state = {
	"game": [
		[ [],  [],  [], [0], [1],  [],  [],  [],  []],
		[ [],  [],  [], [1], [0], [1], [0], [1],  []],
		[ [],  [], [1], [0], [1], [0], [1], [0], [1]],
		[ [],  [], [0], [1], [0], [1], [0], [1], [0]],
		[ [], [0], [1], [0],  [], [0], [1], [0],  []],
		[[0], [1], [0], [1], [0], [1], [0],  [],  []],
		[[1], [0], [1], [0], [1], [0], [1],  [],  []],
		[ [], [1], [0], [1], [0], [1],  [],  [],  []],
		[ [],  [],  [],  [], [1], [0],  [],  [],  []]
	],
	"moves": [],
	"players": ["LUR", "LRG"],
	"you": "LUR"
}

class AI_Player:       
    def __init__(self, AI_algo, name = 'AI', color=0):
        self.AI_algo = AI_algo
        self.name = name
        self.move = {}
        self.color = color

    def ask_move(self, game):
        return self.AI_algo(game)

class Human_Player:
    def __init__(self, name = 'Human', color=0):
        self.name = name
        self.color = color

    def regex_move(self, move):
        str_list = list(move)
        int_list = []
        for number in str_list:
            if number != ' ':
                int_list.append(int(number))
        return [[int_list[0], int_list[1]], [int_list[2], int_list[3]]]

    def ask_move(self, game):
        possible_moves = game.possible_moves()
        # The str version of every move for comparison with the user input:
        possible_moves_str = list(map(str, game.possible_moves()))
        move = "NO_MOVE_DECIDED_YET"
        while True:
            move = input("\nPlayer %s what do you play ? "%(game.nplayer))
            if move == 'show moves':
                print ("Possible moves:\n"+ "\n".join(
                       ["#%d: %s"%(i+1,m) for i,m in enumerate(possible_moves)])
                       +"\nType a move or type 'move #move_number' to play.")

            elif move == 'quit':
                raise KeyboardInterrupt

            elif move.startswith("move #"):
                # Fetch the corresponding move and return.
                move = possible_moves[int(move[6:])-1]
                return move

            elif str(move) in possible_moves_str:
                # Transform the move into its real type (integer, etc. and return).
                move = possible_moves[possible_moves_str.index(str(move))]
                return move

            else:
                pattern = r" *[0-9] *[0-9] *[0-9] *[0-9] *"

                mvt = re.compile(pattern)
                if mvt.match(move) is not None:
                    return self.regex_move(move)

class Random_Player:
    def __init__(self, name='Random', color=0):
        self.name = name
        self.state = state
        self.color = color

    def ask_move(self, game):
        pm = game.possible_moves()
        return random.choice(pm)


