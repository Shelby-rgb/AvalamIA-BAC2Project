import copy
from copy import deepcopy
import time
import random
import json

from easyAI import Negamax, TwoPlayersGame, TT
from X_Player_class import AI_Player, Human_Player, Random_Player

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

"""
Comment jouer? 
    Pour initialiser Avalam, utiliser les paramètres suivants:
        - players : liste de 2 joueurs, en utilisant les classes X_Player. Exemple: [AI_Player(ai_algo, color=0), Human_Player(color=1)]
                    !!! le premier de la liste doit avoir color=0 et le second color=1
        - state : l'état du plateau, state['game'] par défaut
        - first_color : couleur du joueur qui commence, 0 ou 1
        - nmove : nombre de coups qui ont déja été joués, 0 par défault

    Pour initialiser les classes X_Player, utiliser les paramètres suivants:
        Uniquement pour AI_Player!
        - ai_algo : algorithme utilisé pour chercher le meilleur coup
        Pour les 3 X_Player:
        - name: optionnel, nom du joueur
        - color: couleur du joueur, 0 ou 1
    
    Pour initialiser ai_algo, créer les variables suivantes:
        - table = TT()
        - Negamax(depth, table) avec depth == nombre de coups que l'ia doit prévoir à l'avance
    
    Pour obtenir de l'ia un seul coup sans jouer toute la partie:
        - Utiliser la fonction AI_runner(state), state étant le body reçu par le serveur


    Exemple de commande pour jouer AI_Player vs Human_Player:

        board = state['game']
        table = TT()
        ai_algo = Negamax(16, tt=table)
        ia = AI_Player(ai_algo, color=0)
        human = Human_Player(color=1)
        players = [ia, human]
        game = Avalam(players, board, first_color=1)
        game.play()

    'Player 1' a les pions '0' et 'Player 2' a les pions '1'    
    Les tours sont représentées par un tuple de forme (pion dominant la tour, nbr de pions dans la tour)
    Quand c'est au tour de Human_Player de jouer, le joueur peut rentrer dans la ligne de commande:
        - le mouvement à jouer, sous forme de 4 numéros 'ab cd' avec a=ligne 'from', b=colonne 'from', c=ligne 'to', d=colonne 'to'
        - 'show moves' pour montrer tous les coups possibles
        - 'move #nbr' pour jouer le coups numéro 'nbr' proposés par 'show moves'
        - 'quit' pour interrompre le jeu
"""

"""
La classe Avalam permet essentiellement:
    - De lister tous les coups authorisés en fonction du plateau de jeu (possible_moves())
    - De modifier le plateau en fonction du mouvement demandé (make_move())
    - D'évaluer quel joueur à l'avantage (scoring())
    - De vérifier si le jeu est terminé (is_over())
    Les autres fonctions ne sont pas essentielles à un fonctionnement correct de Negamax
"""
class Avalam(TwoPlayersGame):

    def __init__(self, players, state=state['game'], first_color=0, nmove=0):
        self.nmove = nmove
        self.state = state
        self.players = players
        self.color = first_color
        if self.color == 1:
            self.nplayer = 2
        else:
            self.nplayer = 1
        self.step = time.time()
        self.max_time = 0

    #return liste de tous les mouvements possibles
    def possible_moves(self):
        state = self.state
        #_badmove return True si move est authorisé, False si non
        def _badmove(move, state):
            a = move[0]  
            b = move[1]  
            _from = self.state[a[0]][a[1]]
            _to = self.state[b[0]][b[1]]
            if a != b:
                if len(_from)+len(_to) <= 5:                                                                               
                    if len(_from)>0 and len(_to)>0:                                                                        
                        if a[0]==b[0]-1 or a[0]==b[0] or a[0]==b[0]+1:                                                     
                            if a[1]==b[1]-1 or a[1]==b[1] or a[1]==b[1]+1:                                                         
                                return True 
            return False
        #return une liste des cases ou se trouve une tour
        def _listing(state):
            board = state
            position_list = []
            for line in board:
                for tower in line:
                    if len(tower) > 0:
                        a = board.index(line)
                        b = line.index(tower)
                        pos = [a, b]
                        position_list.append(pos)
            return position_list
        position_list = _listing(state)
        possible_moves = []
        for elem in position_list:             
            u = elem[0]
            v = elem[1]
            if u != 0 and v != 0:
                if _badmove([elem, [u-1, v-1]], state) == True:
                    possible_moves.append([elem, [u-1, v-1]])
            if u != 0:
                if _badmove([elem, [u-1, v]], state) == True:
                    possible_moves.append([elem, [u-1, v]])
            if u != 0 and v != 8:
                if _badmove([elem, [u-1, v+1]], state) == True:
                    possible_moves.append([elem, [u-1, v+1]])

            if v != 0:
                if _badmove([elem, [u, v-1]], state) == True:
                    possible_moves.append([elem, [u, v-1]])
            if v != 8:
                if _badmove([elem, [u, v+1]], state) == True:
                    possible_moves.append([elem, [u, v+1]])

            if u != 8 and v != 0:
                if _badmove([elem, [u+1, v-1]], state) == True:
                    possible_moves.append([elem, [u+1, v-1]])
            if u != 8:
                if _badmove([elem, [u+1, v]], state) == True:
                    possible_moves.append([elem, [u+1, v]])
            if u != 8 and v != 8:
                if _badmove([elem, [u+1, v+1]], state) == True:
                    possible_moves.append([elem, [u+1, v+1]])
        return possible_moves

    #déplace une tour sur le plateau
    def make_move(self, move):
        state = self.state
        a = move[0]
        b = move[1]
        _from = state[a[0]][a[1]]
        _to = state[b[0]][b[1]]
        while len(_from) > 0:
            _to.append(_from[0])
            del(_from[0])
        return state

    #return le score en faveur du joueur en cour (nplayer)
    def scoring(self):
        state = self.state
        current_player = self.nplayer-1
        player_score = 0
        opponent_score = 0
        for line in state:
            for row in line:
                if len(row)>0:
                    if row[-1] == current_player:
                        player_score += 1
                    else:
                        opponent_score += 1

        def is_fridged(current_player, state):
            player_fridge = 0
            opponent_fridge = 0
            line = 0
            row = 0
            while line<9:
                while row<9:
                    fridge = 0
                    if len(state[line][row]) != 0:

                        if line != 0 and row != 0:
                            if len(state[line][row])+len(state[line-1][row-1]) >=5:
                                fridge += 1
                            
                        if line != 0:
                            if len(state[line][row])+len(state[line-1][row]) >=5:
                                fridge += 1
                        
                        if line != 0 and row != 8:
                            if len(state[line][row])+len(state[line-1][row+1]) >=5:
                                fridge += 1
                            
                        if row != 0:
                            if len(state[line][row])+len(state[line][row-1]) >=5:
                                fridge += 1
                        
                        if row != 8:
                            if len(state[line][row])+len(state[line][row+1]) >=5:
                                fridge += 1
                        
                        if line != 8 and row != 0:
                            if len(state[line][row])+len(state[line+1][row-1]) >=5:
                                fridge += 1
                            
                        if line != 8:
                            if len(state[line][row])+len(state[line+1][row]) >=5:
                                fridge += 1
                            
                        if line != 8 and row != 8:
                            if len(state[line][row])+len(state[line+1][row+1]) >=5:
                                fridge += 1
                    
                    if fridge == 8:
                        if state[line][row][-1] == current_player:
                            player_fridge += 0.42
                        else:
                            opponent_fridge += 0.42
                   
                    row+=1
                line+=1
            return player_fridge, opponent_fridge

        fridged = is_fridged(current_player, state)
        player_score += fridged[0]
        opponent_score += fridged[1]

        score = player_score - opponent_score
        return score

    #return True si le jeu est terminé
    def is_over(self):
        if len(self.possible_moves()) == 0:
            print(self.scoring())
            return True
        else:
            return False 
    
    #return True si le joueur en cour (nplayer) a perdu
    def lose(self):
        if self.scoring() > 0:
            return False
        else:
            return True
    
    #print le plateau sur terminal, les tours sont représentées par un tuple de forme (pion dominant la tour, nbr de pions dans la tour)
    def show(self):
        arena = self.state
        print('\n')
        print('      ', 0, '      ', 1, '      ', 2, '      ', 3, '      ', 4, '      ', 5, '      ', 6, '      ', 7, '      ', 8, '      ') 
        print('__ |________|_______ |________|________|________|________|________|________|________|')
        y = 0
        for line in arena:
            if len(line[0]) > 0:
                a = line[0][-1], len(line[0])
            else:
                a = '      '
            if len(line[1]) > 0:
                b = line[1][-1], len(line[1])
            else:
                b = '      '
            if len(line[2]) > 0:
                c = line[2][-1], len(line[2])
            else:
                c = '      '
            if len(line[3]) > 0:
                d = line[3][-1], len(line[3])
            else:
                d = '      '
            if len(line[4]) > 0:
                e = line[4][-1], len(line[4])
            else:
                e = '      '
            if len(line[5]) > 0:
                f = line[5][-1], len(line[5])
            else:
                f = '      '
            if len(line[6]) > 0:
                g = line[6][-1], len(line[6])
            else:
                g = '      '
            if len(line[7]) > 0:
                h = line[7][-1], len(line[7])
            else:
                h = '      '
            if len(line[8]) > 0:
                i = line[8][-1], len(line[8])
            else:
                i = '      '
            print(y, ' |', a, '|', b, '|', c, '|', d, '|', e, '|', f, '|', g, '|', h, '|', i, '|')
            if line == arena[8]: #state['game'][8]:
                print('__  ________________________________________________________________________________')
            else:
                print('   +-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --')
            y += 1
        self.check_time()

    #regarde le temps entre chaque coups
    def check_time(self):
        t = time.time()
        duration = t-self.step
        if duration > self.max_time:
            self.max_time = duration
        print(f'Joueur {self.nplayer-1} a répondu en {duration} secondes')
        self.step = t
    
    def make_random_choice(self):
        pm = self.possible_moves()
        rand_move = random.choice(pm)
        return rand_move

    #permet d'utiliser les tables de transposition, accélère l'ia
    def ttentry(self):
        return str(self.state)

#joue toute une partie random vs ia, plateau dans le terminal
def random_vs_ai(depth=2, random_color=1):
    board = state['game']
    table = TT()
    ai_algo = Negamax(depth, tt=table)
    if random_color == 1:
        players = [AI_Player(ai_algo, color=0), Random_Player(color=1)]
    else:
        players = [Random_Player(color=0), AI_Player(ai_algo, color=1)]
    game = Avalam(players, board, first_color=0)
    game.play()
    print(f'Temps max entre 2 coups: {game.max_time} secondes')

#permet de jouer soi même contre l'ia dans le terminal
def human_vs_ai(depth=2, human_color=1):
    board = state['game']
    table = TT()
    ai_algo = Negamax(depth, tt=table)
    if human_color == 1:
        players = [AI_Player(ai_algo, color=0), Human_Player(color=1)]
    else:
        players = [Human_Player(color=0), AI_Player(ai_algo, color=1)]
    game = Avalam(players, board, first_color=0)
    game.play()

#Renvoie le meilleur coup d'après Negamax, au format json
def AI_runner(state=state, depth=2):
    board = state['game']
    nmove = len(state['moves'])

    #l'ia est plus lente entre les coups 12 et 25
    if 12<nmove<25:
        depth = 1
    if 33<nmove:
        depth = 3

    #si des coups ont déjà été joués, on devrait avoir enregistré les tables au tour précédent
    if nmove != 0 and nmove != 1:
        with open('saved_TT.txt') as f:
            tab = f.read()
            tt = json.loads(tab)
        table = TT(own_dict=tt) 
    #si c'est une nouvelle partie on crée une nouvelle table
    else:
        table = TT()

    ai_algo = Negamax(depth, tt=table)

    if state['you'] == state['players'][0]:
        your_color = 0
        opponent_color = 1
        players = [AI_Player(ai_algo, color=your_color), Human_Player(color=opponent_color)]
    else:
        your_color = 1
        opponent_color = 0
        players = [Human_Player(color=opponent_color), AI_Player(ai_algo, color=your_color)]

    game = Avalam(players, board, first_color=your_color, nmove=nmove)
    move = game.get_move()

    dic_move_form = {
        "move": {
            "from": move[0],
            "to": move[1]
        },
        "message": "La Vulcania est toujours la"
    }
    #enregistre la TT, sera utilisée uniquement pour la partie en cours
    with open('saved_TT.txt', 'w') as f:
        json.dump(table.d, f)

    dic_move_form = json.dumps(dic_move_form)
    return dic_move_form


if __name__ == '__main__':  
    t = time.time()
    #print(AI_runner())
    random_vs_ai(depth= 2, random_color=0)
    print(f'La partie a duré {time.time()-t} secondes')
    

    


#C'est la vie de chateau?
