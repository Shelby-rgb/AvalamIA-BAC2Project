# AVALAM-PROJECT
Project Avalam
Règles du jeu:
http://www.oya.fr/?post/2014/12/09/73-avalam-est-a-oya

L'IA est basée sur le framework easyAI, voir:
https://github.com/Zulko/easyAI/blob/master/README.rst

L'IA utilise Negamax, une variante de Minimax avec élagage 'alpha/beta'.
https://en.wikipedia.org/wiki/Negamax

Pour évaluer l'état du jeu de sorte que Negamax sache quels sont les meilleurs coups, le code utilise une fonction scoring. Celle ci calcule dans un premier temps le nombre de tours que possède chaque équipe (le score direct). Ensuite, elle cherche si cette tour pourrait encore se déplacer ou être prise par l'adversaire. Si non, c'est qu'elle est 'figée'. Elle ne bougera plus de la partie et donc le point qu'elle rapporte peut être considéré comme acquis. Ces tours valorisent le score du joueur qui la possède.
Par exemple une tour de 5 pions ne bougeras plus tandis qu'un tour d'un seul pion peut encore se faire prendre par l'équipe adverse.

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
  
  UPDATE: utiliser la fonction human_vs_ai()

'Player 1' a les pions '0' et 'Player 2' a les pions '1'    
Les tours sont représentées par un tuple de forme (pion dominant la tour, nbr de pions dans la tour)
Quand c'est au tour de Human_Player de jouer, le joueur peut rentrer dans la ligne de commande:
    - le mouvement à jouer, sous forme de 4 numéros 'ab cd' avec a=ligne 'from', b=colonne 'from', c=ligne 'to', d=colonne 'to'
    - 'show moves' pour montrer tous les coups possibles
    - 'move #nbr' pour jouer le coups numéro 'nbr' proposés par 'show moves'
    - 'quit' pour interrompre le jeu
