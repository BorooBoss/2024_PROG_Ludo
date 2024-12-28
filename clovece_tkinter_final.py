import tkinter as tk
from random import randint
import time
n = 9
k = 3

""" 
    Ak nahodou toto cita nejaky clovek - vitaj v mojom zdrojaku.
    V prvom rocniku na FEIke som dostal zadanie spravit hru clovece, podla manualu, ktory je prilozeny na githube...
    S hrou mi pomahal kamarat, skoncili sme pri verzii pre 1 hraca, cely kod bol chaoticky naprogramovany, z neznameho dovodu som
    vo funkcii pohyb pristupoval k polu v opacnej logike, tieto problemy sa mi velmi nechcelo riesit... riesil som len to, co som musel.
    Hlavnym cielom, ktory som si dal rok po odovzdani tohto neprehladneho kodu - upravit kod aby bol funkcny pre 1-4 hracov vyuzitim objektov
    a cele tomu dat nejake graficke prostredie pomocou kniznice TKINTER. Vysledok nie je perfektny, kod by sa dal zredukovat a hlavne 
    napisat rozumnejsie, no nakolko to mala byt len vypln vianocnych prazdnin, tak som sa s istymi detailami nezaoberal. 
    Logika hry aj cele vykreslovanie by malo byt perfektne osetrene a to bolo pre mna hlavnou ulohou.
"""
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

def gensachovnicu(n): #Vygenerovanie pola 
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
                lines[i].append([f" {i} "])  # Pre menšie čísla ako 9 ulož celé číslo
            if i > 9:
                lines[i].append([f" {str(i)[-1]} "])  # Pre väčšie čísla poslednú cifru
            for j in range(n):
                if i == 0 or i == n-1:  # Pre prvý a posledný riadok
                    if j == mid or j == mid-1 or j == mid+1:
                        lines[i].append(["*"])
                    else:
                        lines[i].append([space])
                elif i == mid:  # Stred
                    if j == 0 or j == n-1:
                        lines[i].append(["*"])
                    elif j == mid:
                        lines[i].append(["X"])
                    else:
                        lines[i].append(["H"])
                elif i == mid-1 or i == mid+1:  # Pre stĺpce vedľa domčeka 
                    if j == mid:
                        lines[i].append(["H"])
                    else:
                        lines[i].append(["*"])
                else:
                    if j == mid:
                        lines[i].append(["H"])
                    elif j == mid-1 or j == mid+1:
                        lines[i].append(["*"])
                    else:
                        lines[i].append([space])
        lines.insert(0,first) #spojenie dvoch matic do jednej 
        return lines

def draw_board(pole, n, dice_value, canvas):  #TKINTER vykreslenie boardu
    canvas.delete("all")  # Vymaže starý obsah
    for i, row in enumerate(pole):
        for j, cell in enumerate(row):
            x1, y1 = j * 40 + 10, i * 40 + 10
            x2, y2 = x1 + 40, y1 + 40
            
            # Extrahujeme obsah bunky
            square = cell[0].strip() if cell else ""
            
            # Vykresli štvorce podľa obsahu
            if square == "A":
                canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="black")
                canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text="A", font=("Arial", 25))
            elif square == "B":
                canvas.create_rectangle(x1, y1, x2, y2, fill="RoyalBlue2", outline="black")
                canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text="B", font=("Arial", 25))
            elif square == "C":
                canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="black")
                canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text="C", font=("Arial", 25))
            elif square == "D":
                canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="black")
                canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text="D", font=("Arial", 25))
            elif square == "H":
                canvas.create_rectangle(x1, y1, x2, y2, fill="orange", outline="black")
                canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text="H", font=("Arial", 16))
            elif square == "*":
                canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="black")
                canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text="*", font=("Arial", 16))
            elif square == "X":
                canvas.create_rectangle(x1, y1, x2, y2, fill="goldenrod3", outline="black")
                canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text="X", font=("Arial", 16))
            elif square == "a":
                canvas.create_rectangle(x1, y1, x2, y2, fill="goldenrod1", outline="black")
                canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text="a", font=("Arial", 16))
            elif square == "b":
                canvas.create_rectangle(x1, y1, x2, y2, fill="goldenrod1", outline="black")
                canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text="b", font=("Arial", 16))
            elif square == "c":
                canvas.create_rectangle(x1, y1, x2, y2, fill="goldenrod1", outline="black")
                canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text="c", font=("Arial", 16))
            elif square == "d":
                canvas.create_rectangle(x1, y1, x2, y2, fill="goldenrod1", outline="black")
                canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text="d", font=("Arial", 16))
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                if square:  # Ak nie je prázdne, vykresli text
                    canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text=square, font=("Arial", 16))

    dice_size = 60
    dice_x = 65 * n - 60
    dice_y = 65 * n - 60
    canvas.create_rectangle(dice_x, dice_y, dice_x + dice_size, dice_y + dice_size, fill="lightgray", outline="black")
    canvas.create_text(dice_x + dice_size // 2, dice_y + dice_size // 2, text=str(dice_value), font=("Arial", 20, "bold"))

def kocka(player): 
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
         
        

    
#INIT hracov
players = []
remaining_pawns = k * (int(n/2) - 1)
names = [" A "," B "," C "," D "]
start_x = 1
start_y = 1
game = 0
counterA = ((n-2)*4)+3 #pocet policok od zaciatku presne pred domcek postavicky - "hracie pole"
pole = gensachovnicu(n)
for i in range(k):
    start_x, start_y = START_POSITIONS[i] 
    players.append(Player(names[i], start_x, start_y))
    pole[start_x][start_y][0] = players[i].name
    players[i].index = i

#TKINTER main loop
def game_loop(player_index=0):
    global game, pole, players

    if game == (k - 1):
        print("Hra skončila!")
        return

    current_player = players[player_index]

    if current_player.win:
        next_index = (player_index + 1) % k
        root.after(500, game_loop, next_index)
        return

    
    kocka(current_player)
    dice_value = current_player.throw
    #current_player.throw = int(input("hod "))
    print(f"Hráč {current_player.name} hodil {current_player.throw}")

    if current_player.ready == 0 and current_player.throw != 6:
        print(f"Hráč {current_player.name} potreboval 6 na začatie.")
    elif current_player.ready == 0 and current_player.throw == 6:
        print(f"Hráč {current_player.name} sa dostal na hracie pole.")
        current_player.x, current_player.y = START_POSITIONS[current_player.index]
        if pole[current_player.x][current_player.y][0] != " * ":
            kick(current_player, players)
        pole[current_player.x][current_player.y][0] = current_player.name
        current_player.ready = 1
    else:
        current_player.till_end -= current_player.throw
        if current_player.till_end < 0:
            current_player.id = -1
            game = pohyb(n, pole, current_player, players, game)
            current_player.id = 1
            current_player.till_end = ((n - 2) * 4) + 3
        else:
            pohyb(n, pole, current_player, players, game)

    draw_board(pole, n, dice_value, canvas)  
    next_index = (player_index + 1) % k
    root.after(1000, game_loop, next_index)

def start_game():
    global root, canvas
    root = tk.Tk()
    root.title("Človeče")
    canvas = tk.Canvas(root, width=65 * n + 20, height=65 * n + 20, bg="white")
    canvas.pack()
    draw_board(pole, n, 0, canvas)  


    root.after(100, game_loop) 
    root.mainloop()

start_game()

