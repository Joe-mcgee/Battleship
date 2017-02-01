import string
#constants
ship = '|'
BOARD_SIZE = 10
EMPTY = 'O'
HORIZONTAL_SHIP = '-'
VERTICAL_SHIP = '|'
MISS = '.'
HIT = '*'
SUNK = '#'
HEALTH = "1"
NO_HEALTH = "0"
alpha2num = dict(enumerate(string.ascii_uppercase, 0))
victory = False


SHIP_INFO = [
    ("Aircraft Carrier", 5),
    ("Battleship", 4),
    ("Submarine", 3),
    ("Cruiser", 3),
    ("Patrol Boat", 2)
]

# player, board and ship classes
class Board(object):
    # square list of lists, all elements empty, dimension of BOARD_SIZE
    def __init__(self):
        self.board = [[EMPTY] * BOARD_SIZE for location in range(BOARD_SIZE)]
 
        
class Ship(object):
    # square list of lists, all elements ints, dimenions of BOARD_SIZE
    def __init__(self):
        self.health = [[0] * BOARD_SIZE for location in range(BOARD_SIZE)] 
     
              
class Player:
    # name, 2 boards, and 5 ships 
    def __init__(self, name):
        self.name = name
        self.board = Board().board
        self.battle_space = Board().board
        self.aircraft_carrier = Ship().health
        self.battleship = Ship().health
        self.submarine = Ship().health
        self.cruiser = Ship().health
        self.patrol_boat = Ship().health
    
           
# prints board with axis'   
def board_print(board):
    print_board_heading()
    count = 0
    
    for row in board:
        row.insert(0, count)
        print(row)
        count += 1
        if count > 9:
            count = 0
# removes axis from board after print to avoid duplicate y axis       
    for row in board:
        row.pop(0)
    return board
                
def print_board_heading():
    print("     " + "    ".join([chr(c) for c in range(ord('A'), ord('A') + BOARD_SIZE)]))
        
def clear_screen():
    print("\033c", end="")
    
# handles ship placement
def ship_placer(Player):  
    for ship in SHIP_INFO:
        # to handle errors
        while True:
            try:
                count = 0
                print('where would you like to place your {}?'.format(ship))
            
                coords = input('please input coordinate in format (B4):')
                coords = coords.upper()
                orientation = input('would you like your {} in (H)orizontal or (V)ertical?'.format(ship))
                orientation = orientation.upper()
                # for orientation errors
                if orientation != 'H':
                    if orientation == 'V':
                        pass
                    else:
                        raise ValueError    
                x_letter, y = coords
                y = int(y)
                # convert letter to a number coordinate
                x = list(alpha2num.keys())[list(alpha2num.values()).index(x_letter)]
                
                # handles ship placement
                if orientation == "H":
                    validator = 0
                    # draws ship on board
                    while count < ship[1]:
                        # prevents overlapping ships
                        while validator < ship[1]:
                            if Player.board[y][x + validator] != EMPTY:
                                raise ValueError
                            validator += 1
                        if Player.board[y][x + count] == VERTICAL_SHIP:
                            raise TypeError
                        if Player.board[y][x + count] == EMPTY:  
                            Player.board[y][x + count] = HORIZONTAL_SHIP
                        count += 1
                    # creates ships with health and coordinates     
                    if count > 4:
                        count = 0
                        while count < ship[1]:
                            Player.aircraft_carrier[y][x + count] = 1
                            count += 1   
                    if count == 4:
                        count = 0
                        while count < ship[1]:
                            Player.battleship[y][x + count] = 1
                            count += 1  
                    if count == 3:
                        count = 0
                        while count < ship[1]:
                            if ship[0] == "Submarine":
                                Player.submarine[y][x + count] = 1
                                count += 1
                            if ship[0] == "Cruiser":
                                Player.cruiser[y][x + count] = 1
                                count += 1     
                    if count == 2:
                        count = 0
                        while count < ship[1]:
                            Player.patrol_boat[y][x + count] = 1
                            count += 1      
                    count = 0
                    
                elif orientation == "V":
                    validator = 0
                    while count < ship[1]:
                        while validator < ship[1]:
                            if Player.board[y + validator][x] != EMPTY:
                                raise ValueError
                            validator += 1
                        if Player.board[y + count][x] == HORIZONTAL_SHIP:
                            raise TypeError
                        if Player.board[y + count][x] == EMPTY: 
                            Player.board[y + count][x] = VERTICAL_SHIP
                        count += 1   
                    if count > 4:
                        count = 0
                        while count < ship[1]:
                            Player.aircraft_carrier[y + count][x] = 1
                            count += 1   
                    if count == 4:
                        count = 0
                        while count < ship[1]:
                            Player.battleship[y + count][x] = 1
                            count += 1  
                    if count == 3:
                        count = 0
                        while count < ship[1]:
                            if ship[0] == "Submarine":
                                Player.submarine[y + count][x] = 1
                                count += 1
                            if ship[0] == "Cruiser":
                                Player.cruiser[y + count][x] = 1
                                count += 1       
                    if count == 2:
                        count = 0
                        while count < ship[1]:
                            Player.patrol_boat[y + count][x] = 1
                            count += 1
                    count = 0    
                board_print(Player.board)
            # catches the various input errors   
            except (UnboundLocalError, ValueError, IndexError, TypeError) as err:
                print('please select a valid coordinate')
            else:
                break

# handles turn changes               
def end_turn(Player):
    input("Press a key to end your turn {}".format(Player.name))
    clear_screen()
    
    
def begin_turn(Player):
        ready = input("The turn has changed. are you ready to begin your turn, {}? (Y)".format(Player.name))
        if ready == "Y":
            board_print(Player.battle_space)
            board_print(Player.board)
        
        else:
            begin_turn(Player)
            
# game core       
def turn(Player):
    while True:
        try:
            coords = input("Where would you like to attack (B4) {}? ".format(Player.name))
            coords = coords.upper()
            x_letter, y = coords     
            y = int(y)
            x = list(alpha2num.keys())[list(alpha2num.values()).index(x_letter)]
            
            # handles updating boards and ship healths
            if Player == player1:
                # handles repeated strikes
                if player2.board[y][x] == HIT:
                    raise ValueError
                if player2.board[y][x] == MISS:
                    raise ValueError
                if player2.board[y][x] == EMPTY:
                    print('You failed to hit a target {}'.format(Player.name))
                    Player.battle_space[y][x] = MISS
                    player2.board[y][x] = MISS    
                else:
                    print('Its a hit {}! '.format(Player.name))
                    Player.battle_space[y][x] = HIT
                    player2.board[y][x] = HIT    
                if player2.aircraft_carrier[y][x] == 1:
                    player2.aircraft_carrier[y][x] = 0
                if player2.battleship[y][x] == 1:
                    player2.battleship[y][x] = 0
                if player2.cruiser[y][x] == 1:
                    player2.cruiser[y][x] = 0   
                if player2.submarine[y][x] == 1:
                    player2.submarine[y][x] = 0   
                if player2.patrol_boat[y][x] == 1:
                    player2.patrol_boat[y][x] = 0
                       
            if Player == player2:
                if player1.board[y][x] == HIT:
                    raise ValueError
                if player1.board[y][x] == MISS:
                    raise ValueError
                if player1.board[y][x] == EMPTY:
                    print('You failed to hit a target {}'.format(Player.name))
                    Player.battle_space[y][x] = MISS
                    player1.board[y][x] = MISS    
                else:
                    print('Its a hit {}! '.format(Player.name))
                    Player.battle_space[y][x] = HIT
                    player1.board[y][x] = HIT
                if player1.aircraft_carrier[y][x] == 1:
                    player1.aircraft_carrier[y][x] = 0
                if player1.battleship[y][x] == 1:
                    player1.battleship[y][x] = 0
                if player1.cruiser[y][x] == 1:
                    player1.cruiser[y][x] = 0  
                if player1.submarine[y][x] == 1:
                    player1.submarine[y][x] = 0   
                if player1.patrol_boat[y][x] == 1:
                    player1.patrol_boat[y][x] = 0
            board_print(Player.battle_space)
            board_print(Player.board)
            
        except (UnboundLocalError, ValueError, IndexError):
            print('please select a valid coordinate')
            
        else:
            break
        
# handles confirmation of sunken ships and victory condition
def kill_confirmer(Player):
    if Player == player1:
        if sum(sum(Player.aircraft_carrier, [])) == 0:
            print("you have sunk {}'s Aircraft Carrier!".format(player2.name))
        if sum(sum(Player.battleship, [])) == 0:
            print("you have sunk {}'s Battleship!".format(player2.name))
        if sum(sum(Player.submarine, [])) == 0:
            print("you have sunk {}'s Submarine!".format(player2.name))
        if sum(sum(Player.cruiser, [])) == 0:
            print("you have sunk {}'s Crusier!".format(player2.name))
        if sum(sum(Player.patrol_boat, [])) == 0:
            print("you have sunk {}'s Patrol Boat!".format(player2.name))
        # victory condition    
        if sum(sum(Player.aircraft_carrier, [])) == 0 and sum(sum(Player.battleship, [])) == 0 and sum(sum(Player.submarine, [])) == 0 and sum(sum(Player.cruiser, [])) == 0 and sum(sum(Player.patrol_boat, [])) == 0:
            print("you have dystroyed {}'s fleet! Congratulations!".format(player1.name))
            return True    
    
    if Player == player2:
        if sum(sum(Player.aircraft_carrier, [])) == 0:
            print("you have sunk {}'s Aircraft Carrier!".format(player1.name))
        if sum(sum(Player.battleship, [])) == 0:
            print("you have sunk {}'s Battleship!".format(player1.name))
        if sum(sum(Player.submarine, [])) == 0:
            print("you have sunk {}'s Submarine!".format(player1.name))
        if sum(sum(Player.cruiser, [])) == 0:
            print("you have sunk {}'s Crusier!".format(player1.name))
        if sum(sum(Player.patrol_boat, [])) == 0:
            print("you have sunk {}'s Patrol Boat!".format(player1.name))
    
        if sum(sum(Player.aircraft_carrier, [])) == 0 and sum(sum(Player.battleship, [])) == 0 and sum(sum(Player.submarine, [])) == 0 and sum(sum(Player.cruiser, [])) == 0 and sum(sum(Player.patrol_boat, [])) == 0:
            print("you have dystroyed {}'s fleet!, congratulations!".format(player2.name))
            return True
# control flow for game    
def game(player1, player2):
        victory = False
        while victory == False:
            begin_turn(player1)
            turn(player1)
            if kill_confirmer(player2) == True:
                victory = True
                break
            else:
                end_turn(player1)
                
                begin_turn(player2)
                turn(player2)
                if kill_confirmer(player1) == True:
                    victory = True
                    break
                else:
                    end_turn(player2)
# init for app
if __name__ == '__main__':
    print('Welcome to Battleship')
    # create player classes
    player1_name = input('What is your name player1?: ')
    player1 = Player(player1_name)
    player2_name = input('What is your name player2?: ')
    player2 = Player(player2_name)
    players = [player1, player2]
    clear_screen()
    # ship placement phase
    print('Time to place your ships {},'.format(player1.name))
    board_print(player1.board)
    ship_placer(player1)
    board_print(player1.board)
    clear_screen()
    print('Time to place your ships {}'.format(player2.name))
    board_print(player2.board)
    ship_placer(player2)
    clear_screen()
    # game phase 
    game(player1, player2)
    
    
    

    
     
    
    
    
    
    
    
    
   
    
    
    
    
    

