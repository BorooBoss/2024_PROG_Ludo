
from random import randint
import time

#general
n = 7
k = 3
playerA = 1

START_POSITIONS = {
    0 : (1, int(n/2)+2),
    1 : (int(n/2)+2, n),
    2 : (n, int(n/2)),
    3 : (int(n/2), 1)
}

class Player:
    def __init__(player, name, start_x, start_y):
        player.name = name
        player.x = start_x
        player.y = start_y
        #player.old_x = start_x
        #player.old_y = start_y
        player.throw = 0
        player.till_end = ((n-2)*4)+3 #poocet policok do konca 
        player.id = 1
        player.pawns = int(n/2)-1 #pocet figurok
        player.home = 0
        player.index = 0
        player.ready = 1  
        player.win = False

def gensachovnicu(n): #podmienka rozemru sachovnice - nemoze byt parne cislo
    if n % 2 == 0:
        print("neplatny vstup ")
        return
    else:
        space = "   "
        mid = ((n-1)//2) #suradnica stredu  
        lines = [] #prazdna matica cislo 2

        first = [[space]] #prva matica 
        for i in range(n):
            first.append([f" {str(i)[-1]} "]) #vlozime do nej cisla od 0 po n-1, zapisujeme iba poslednu cifru cisla

        for i in range(n):
            lines.append([]) 
            if i <= 9:
                lines[i].append([f" {i} "]) #pre mensie cisla ako 9 uloz cele cislo
            if i > 9 :
                lines[i].append([f" {str(i)[1]} "]) #pre vacsie cisla uloz iba poslednu cifru 
            for j in range(n):
                if i == 0 or i == n-1: #pre prvy a posledny riadok
                    if j == mid or j == mid-1 or j == mid+1:
                        lines[i].append([" * "])
                    else:
                        lines[i].append([space])
                elif i == mid: #stred
                    if j == 0 or j == n-1:
                        lines[i].append([" * "])
                    elif j == mid:
                        lines[i].append([" X "])
                    else:
                        lines[i].append([" H "])
                elif i == mid-1 or i == mid+1: #pre stlpce vedla domceku 
                    if j == mid:
                        lines[i].append([" H "])
                    else:
                        lines[i].append([" * "])
                else:
                    if j == mid:
                        lines[i].append([" H "])
                    elif j == mid-1 or j == mid+1:
                        lines[i].append([" * "])
                    else:
                        lines[i].append([space])
    lines.insert(0,first) #spojenie dvoch matic do jednej 
    return lines

def kocka(player): #funkcia na vytvorenie hracej kocky
    throw = randint(1, 6)
    player.throw = throw

def tlacenka(pole):
    for i in pole: #prechadzam riadky 
        for j in i: #prechadzam stlpce
            for k in j: #prechadzam konkretne prvky, ktore boli v matici 
                print(k, end="")
        print()

def getpos(player, pole): #funkcia na ziskanie hraca 
    for y in range(len(pole)): 
        for x in range(len(pole)):
            if pole[y][x][0] == player.name: #ked sa na kombinacii suradnic nachadza "A" vrat mi suradnice
                player.x = x
                player.y = y
                
def kick(player, players):
        for other_player in players:
            #print(pole[player.x][player.y][0], other_player.name)
            if other_player.name == pole[player.x][player.y][0]:
                other_player.ready = 0
                other_player.till_end = ((n-2)*4)+3
                print(other_player.name, other_player.ready)
                #other_player.x, other_player.y = START_POSITIONS[other_player.index]
                #pole[other_player.x][other_player.y][0] = other_player.name
                print(f"{player.name} vyhodil {other_player.name}!")
                break

def kick2(player, players):
        for other_player in players:
            #print(pole[player.x][player.y][0], other_player.name)
            if other_player.name == pole[player.y][player.x][0]:
                other_player.ready = 0
                other_player.till_end = ((n-2)*4)+3
                print(other_player.name, other_player.ready)
                #other_player.x, other_player.y = START_POSITIONS[other_player.index]
                #pole[other_player.x][other_player.y][0] = other_player.name
                print(f"{player.name} vyhodil {other_player.name}!")
                break

def home(player,mid, game): #co ked uz nemam panaky? 3 a mid 4
    if player.pawns > 0:  # Presun do domčeka
        if player.index == 0:
             pole[1 + player.pawns][mid][0] = player.name.lower()
        elif player.index == 1:
             pole[mid][n - player.pawns][0] = player.name.lower()
        elif player.index == 2:
             pole[n - player.pawns][mid][0] = player.name.lower()
        elif player.index == 3:
             pole[mid][1 + player.pawns][0] = player.name.lower()
        pole[player.y][player.x][0] = " * "  # Pôvodnú pozíciu označ hviezdičkou
        player.pawns -= 1
        player.id = 1
        player.ready = 0
        if player.pawns == 0:
            game += 1
            player.win = True
        return game

def pohyb(n, pole, player, players, game):

    mid = int(n/2)+1 #stred sachovnice pre oba smery
    right_upper_start = [1,mid+1] #12 suradnic kazdeho rohu hry , v ktorom meni panacik smer
    right_upper_inner = [mid-1,mid+1]
    right_upper_end = [mid-1,n]
    right_lower_start = [mid+1,n]
    right_lower_inner = [mid+1,mid+1]
    right_lower_end = [n,mid+1]
    left_lower_start = [n,mid-1]
    left_lower_inner = [mid+1,mid-1]
    left_lower_end = [mid+1,1]
    left_upper_start = [mid-1,1]
    left_upper_inner = [mid-1,mid-1]
    left_upper_end = [1,mid-1] #koniec suradnic
    getpos(player, pole)
    pole[player.y][player.x][0] = " * "  # Označ starú pozíciu hviezdičkou
    while player.throw != 0 and player.id == 1: #kym hod nie je nula a zaroven hrac ma hodnotu 1 - pohni sa cez podmienky
        if player.x == right_upper_inner[1] and player.y < right_upper_inner[0]: #podmienka pre kazdy roh aby to davalo zmysel
            player.y+=1
        elif player.x < right_upper_end[1] and player.y == right_upper_end[0] and player.x > (mid-1): #nastal problem - trebalo pridal dalsiu podmienku aby to platilo len pre "prvy kvadrant" a nie pre druhy 
            player.x+=1
        elif player.x == right_lower_start[1] and player.y < right_lower_start[0]:
            player.y+=1
        elif player.x > right_lower_inner[1] and player.y == right_lower_inner[0]:
            player.x-=1
        elif player.x == right_lower_end[1] and player.y < right_lower_end[0]:
            player.y+=1
        elif player.x > left_lower_start[1] and player.y == left_lower_start[0]:
            player.x-=1
        elif player.x == left_lower_inner[1] and player.y > left_lower_inner[0]:
            player.y-=1
        elif player.x > left_lower_end[1] and player.y == left_lower_end[0]:
           player.x-=1
        elif player.x == left_upper_start[1] and player.y > left_upper_start[0]:
            player.y-=1
        elif player.x < left_upper_inner[1] and player.y == left_upper_inner[0]:
            player.x+=1
        elif player.x == left_upper_end[1] and player.y > left_upper_end[0]:
            player.y-=1
        elif player.x < right_upper_start[1] and player.y == right_upper_start[0]:
            player.x+=1
        else :
            print("nedobre daco")
        player.throw -=1 #odpocitaj od hodu -1
    if player.id == -1:
        game = home(player,mid, game)
        return game

    # Ak na novej pozícii stojí iný hráč
    if pole[player.y][player.x][0] != " * ":
        kick2(player, players)
    print(f"Hráč {player.name} sa presunul na {player.y}, {player.x}.")
    pole[player.y][player.x][0] = player.name  
        

##hod 6 a az tak zacni hrat - asi mam, korektne pozicie pri vyhodeni,domceky 
        

    
#MAIN
players = []
remaining_pawns = k * (int(n/2) - 1)
names = [" A "," B "," C "," D "]
start_x = 1
start_y = 1
counterA = ((n-2)*4)+3 #pocet policok od zaciatku presne pred domcek postavicky - "hracie pole"
help_k = names[k-1] #k ale "k"
pole = gensachovnicu(n)
for i in range(k):
    start_x, start_y = START_POSITIONS[i] 
    players.append(Player(names[i], start_x, start_y))
    pole[start_x][start_y][0] = players[i].name
    players[i].index = i
    if (i != (k-1)): #vsetkym nastav do predch. hodnotu k, poslednemu tam nechaj hodnotu "+"
        players[i].pred_znak = help_k


#pole = gensachovnicu(n)
#pole[1][int(n/2)+2][0] = " A " #pridaj na zaciatok hraca
game = 0
counterA = ((n-2)*4)+3 #pocet policok od zaciatku presne pred domcek postavicky - "hracie pole"
###while numPlayersA != 0:
while game != (k-1): #kym mame hracov
    for i in range(k):
        if players[i].win == True:
            continue
        #kocka(players[i])
        players[i].throw = int(input("hod "))

        if players[i].ready == 0 and players[i].throw != 6: #ak som mimo policka a nehodim 6 
            print(f"Hrac{players[i].name}hodil {players[i].throw} no potreboval 6")
            tlacenka(pole)
            continue
        elif players[i].ready == 0 and players[i].throw == 6:
            print("som v elife")
            players[i].x, players[i].y = START_POSITIONS[players[i].index]
            if pole[players[i].x][players[i].y][0] != " * ":
                print("aj tu som")
                kick(players[i], players)
            pole[players[i].x][players[i].y][0] = players[i].name
            players[i].ready = 1
            print(f"Hrac{players[i].name}hodil {players[i].throw}")
            tlacenka(pole)
            continue
        print(f"Hrac{players[i].name}hodil {players[i].throw}")
        players[i].till_end = players[i].till_end - players[i].throw #od poctu policok pola (pocet od zaciatku po policko pred domcekom)
        if players[i].till_end < 0: #ked je pocet policok mensi ako 0 - je v dome
            players[i].id = -1 #nastav mu hodnotu -1 aby ho nepriradilo do zlej podmienky 
            game = pohyb(n, pole, players[i], players, game) #zavolam znova pohyb 
            players[i].id = 1 #daj hracovi hodnotu 1 - aby sa vratil do povodneho while cyklu
            players[i].till_end = ((n-2)*4)+3 #counter nastav na povodne cislo - nech to cele moze fungovat pre dalsieho hraca
        else:
            pohyb(n, pole, players[i], players, game) #ked je counter vacsi ako 0 - zapni pohyb
        tlacenka(pole) #vytlac
        time.sleep(0.5) 
        
        if game == (k-1):
            break
        #print(f"debug till end = {players[i].till_end}")



