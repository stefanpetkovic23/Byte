import copy
import turtle
import heapq
from collections import deque
import random
from config import heuristic_weights, dubina
from byteHeuristics import count_tokens_on_board, count_tokens_on_top_of_stacks, evaluate_central_control, evaluate_diagonal_neighbors, evaluate_full_stack_control

scr = turtle.Screen()
ttl = turtle.Turtle()
ttlDots = turtle.Turtle()

# Globalne promenljive za praćenje stekova
brojStekovaBelih = 0
brojStekovaCrnih = 0
brojFigura, brojStekova = 0, 0

m: int
n: int
covek: bool


def draw():
    for i in range(4):
        ttl.forward(45)
        ttl.left(90)
    ttl.forward(45)


def unesiDim():
    while True:
        s = input("Unesite dimenzije table (format: x,y): ")
        dimensions = s.split(",")

        if len(dimensions) != 2:
            print("Pogresan unos. Unesite ponovo.")
            continue

        try:
            global m, n
            m = int(dimensions[0])
            n = int(dimensions[1])

            if (m == n) and (m == 8) or (8 <= m <= 16 and 8 <= n <= 16 and m % 2 == 0 and n % 2 == 0):
                return m, n
            else:
                print("Pogresne dimenzije. Unesite ponovo.")
        except ValueError:
            print("Pogresan unos. Unesite ponovo.")


def koIgraIgru():
    p = input("Da li igru igrate protiv računara(C) ili čoveka(H): ")
    if (p == 'C' or p == 'c'):
        return "racunar"
    elif (p == 'H' or p == 'h'):
        return "covek"
    else:
        print("Pogresan unos")
        return koIgraIgru()


def koIgraPrvi():
    p = input("Odaberite ko igra prvi potez računar(C) ili čovek(H): ")
    if (p == 'C' or p == 'c'):
        return "racunar"
    elif (p == 'H' or p == 'h'):
        return "covek"
    else:
        print("Pogresan unos")
        return koIgraPrvi()


def izborPrvogIgraca():
    p = input("Izaberite ko će igrati prvi (X ili O): ").upper()
    if p == 'X':
        return True
    elif p == 'O':
        return False
    else:
        print("Pogrešan unos. Pokušajte ponovo.")
        return izborPrvogIgraca()


def unosParametaraIgre():
    dimenzije = unesiDim()
    koIgra = koIgraIgru()
    if (koIgra == "racunar"):
        ko_igra_prvi = koIgraPrvi()
    else:
        ko_igra_prvi = None
    prvi_igrac = izborPrvogIgraca()
    return dimenzije[0], dimenzije[1], koIgra, ko_igra_prvi, prvi_igrac


def inicijalnaTabla(size: int, tabla):
    scr.setup(size * 75 + 20, size * 75 + 20)

    ttl.speed(90)

    ttl.hideturtle()
    for i in range(size):
        ttl.penup()
        ttl.goto(-size * 45 / 2 - 20, -size * 45 / 2 + i * 45 + 10)
        ttl.write(str(i + 1), align="center", font=("Arial", 12, "normal"))

    row_labels = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")[:size]
    for i, label in enumerate(row_labels):
        ttl.penup()
        ttl.goto(-size * 45 / 2 + i * 45 + 25, size * 45 / 2 + 30)
        ttl.write(label, align="center", font=("Arial", 12, "normal"))

    for j in range(size):
        ttl.up()
        ttl.setpos(-size * 45 / 2, -size * 45 / 2 + j * 45)
        ttl.down()

        for k in range(size):
            if (j + k) % 2 == 0:
                clr = 'white'
            else:
                clr = 'brown'

            ttl.fillcolor(clr)
            ttl.begin_fill()
            draw()
            ttl.end_fill()

    prikazTabla(tabla, size)


def crtajPolje(polje: dict, row, col, size, delete):
    for ind, dot in enumerate(polje):
        coefK = 0
        coefY = 0
        if (len(polje) == 1):
            coefK = 0.5
            coefY = 0.5
        else:
            if (ind == 0 or ind == 3 or ind == 6):
                coefK = 0.1
            elif (ind == 1 or ind == 4 or ind == 7):
                coefK = 0.5
            else:
                coefK = 0.9

            if (0 <= ind <= 2):
                coefY = 0.1
            elif (3 <= ind <= 5):
                coefY = 0.5
            else:
                coefY = 0.9

        x = -size * 45 / 2 + (col + coefK) * 45
        y = -size * 45 / 2 + (row + coefY) * 45
        if (delete == True):
            ttlDots.penup()
            ttlDots.goto(x, y)
            ttlDots.pendown()
            ttlDots.dot(5, 'brown')
        else:
            if dot == 'O':
                ttlDots.penup()
                ttlDots.goto(x, y)
                ttlDots.pendown()
                ttlDots.dot(5, 'orange')
            elif dot == 'X':
                ttlDots.penup()
                ttlDots.goto(x, y)
                ttlDots.pendown()
                ttlDots.dot(5, 'black')
            else:
                continue


def prikazTabla(tabla, size):
    ttlDots.clear()
    ttlDots.hideturtle()

    for row in range(0, size):
        for col in range(0, size):
            crtajPolje(tabla[row][col]['stek'], row, col, size, False)
            if (len(tabla[row][col]['stek']) == 8):
                crtajPolje(tabla[row][col]['stek'], row, col, size, True)


def praznaTabla(dim1, dim2):
    val = [[{'vlasnik': '', 'stek': []}
            for _ in range(dim2)] for _ in range(dim1)]

    global brojStekova, brojFigura
    for row in range(1, dim1 - 1):
        for col in range(dim2):
            if (row % 2 != 0 and col % 2 == 0) or (row % 2 == 0 and col % 2 != 0):
                if row % 2 != 0 and col % 2 == 0:
                    val[row][col]['stek'].append('O')
                    val[row][col]['vlasnik'] = 'O'
                    brojFigura += 1
                elif row % 2 == 0 and col % 2 != 0:
                    val[row][col]['stek'].append('X')
                    val[row][col]['vlasnik'] = 'X'
                    brojFigura += 1

    brojStekova = brojFigura // 8
    return val


def find_paths_bfs(table, row, col, path=None, visited=None, is_start=True):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    if not (0 <= row < 8 and 0 <= col < 8) or (row, col) in visited:
        return []

    path.append((row, col))
    visited.add((row, col))

    if not is_start and ('O' in table[row][col]['stek'] or 'X' in table[row][col]['stek']):
        return [path]

    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    paths = []

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        paths.extend(find_paths_bfs(table, new_row, new_col,
                                    path.copy(), visited.copy(), is_start=False))

    return paths


def filter_shortest_paths(paths):
    if not paths:
        return []

    shortest_length = min(len(path) for path in paths)

    shortest_paths = [path for path in paths if len(path) == shortest_length]

    adjusted_second_elements = set(
        (path[1][0], path[1][1]) for path in shortest_paths if len(path) > 1)

    return list(adjusted_second_elements)


def odigraj_potez(tabla, start_row, start_col, target_row, target_col, mesto_na_steku):
    if (start_row % 2 != 0 and start_col % 2 == 0) or (start_row % 2 == 0 and start_col % 2 != 0):
        if (target_row % 2 != 0 and target_col % 2 == 0) or (target_row % 2 == 0 and target_col % 2 != 0):
            if abs(start_row - target_row) == 1 and abs(start_col - target_col) == 1:
                if tabla[start_row][start_col]['stek']:
                    if ((mesto_na_steku == 0 and len(tabla[target_row][target_col]['stek']) == 0) or (
                            mesto_na_steku < len(tabla[target_row][target_col]['stek']))):
                        if len(tabla[start_row][start_col]['stek'])-mesto_na_steku + len(tabla[target_row][target_col]['stek']) <= 8:
                            figura = tabla[start_row][start_col]['stek'].pop(
                                mesto_na_steku)

                            elementi_iznad = tabla[start_row][start_col]['stek'][mesto_na_steku:]
                            tabla[start_row][start_col]['stek'] = tabla[start_row][start_col]['stek'][:mesto_na_steku]

                            tabla[target_row][target_col]['stek'].append(
                                figura)
                            tabla[target_row][target_col]['stek'].extend(
                                elementi_iznad)

                            prikazTabla(tabla, n)

                            return True
                        else:
                            print(
                                "Zbir elemenata na startnoj i ciljnoj poziciji prelazi dozvoljeni broj.")
                    else:
                        print(
                            "Visina na koju želite da pomerite figuricu nije dozvoljena")
                else:
                    print("Na startnoj poziciji nema figure koju želimo pomeriti.")
            else:
                print("Pomeranje se vrši isključivo dijagonalno za jedno polje.")
        else:
            print("Ciljno polje nije tamno.")
    else:
        print("Startno polje nije tamno.")


def validnoPolje(row, col):
    return 0 <= row < n and 0 <= col < n


def unos_poteza(tabla, koPrvi):
    while True:

        try:
            while True:
                try:
                    start_row = int(
                        input("Unesite red startne pozicije (1-8): "))
                    if 1 <= start_row <= 8:
                        start_row -= 1
                        break
                    else:
                        print("Nevažeći unos za red. Pokušajte ponovo.")
                except ValueError:
                    print("Nevažeći unos za red. Pokušajte ponovo.")

            while True:
                try:
                    start_col = input("Unesite kolonu (A-H): ").upper()
                    if len(start_col) == 1 and 'A' <= start_col <= 'H' and start_col.isalpha():
                        start_col = ord(start_col) - ord('A')
                        break
                    else:
                        print("Nevažeći unos za startnu kolonu. Pokušajte ponovo.")
                except ValueError:
                    print("Nevažeći unos za startnu kolonu. Pokušajte ponovo.")

            sviPutevi = find_paths_bfs(tabla, start_row, start_col)
            samoNajkrajci = filter_shortest_paths(sviPutevi)
            najboljiPotezi = samoNajkrajci

            while True:
                try:
                    smer = input(
                        "Unesite smer pomeranja (GL, GD, DL, DD): ").upper()
                    if smer in ['GL', 'GD', 'DL', 'DD']:
                        new_row, new_col = start_row, start_col

                        if smer == 'GL':
                            new_row += 1
                            new_col -= 1
                        elif smer == 'GD':
                            new_row += 1
                            new_col += 1
                        elif smer == 'DL':
                            new_row -= 1
                            new_col -= 1
                        elif smer == 'DD':
                            new_row -= 1
                            new_col += 1

                        if validnoPolje(new_row, new_col):
                            target_row, target_col = new_row, new_col
                            break
                        else:
                            print(
                                "Nevažeći unos za smer pomeranja. Pokušajte ponovo.")
                    else:
                        print("Nevažeći unos za smer pomeranja. Pokušajte ponovo.")
                except ValueError:
                    print("Nevažeći unos za smer pomeranja. Pokušajte ponovo.")

            potez = (target_row, target_col)
            print(f"potez: {potez}")
            print(f"najboljiPotezi: {najboljiPotezi}")

            if potez not in najboljiPotezi:
                print("Možete odigrati bolji potez od ovoga. Probajte ponovo")
                continue
            else:
                print("Valid move")

            stek_na_poziciji = tabla[start_row][start_col]['stek']
            if not stek_na_poziciji:
                print("Na startnoj poziciji nema elemenata na steku. Pokušajte ponovo.")
                continue  # Vraćanje korisnika na početak petlje

            while True:
                try:
                    mesto_na_steku = int(
                        input(f"Unesite mesto na steku (0-{len(stek_na_poziciji) - 1}): "))
                    if 0 <= mesto_na_steku < len(stek_na_poziciji):
                        break
                    else:
                        print(
                            "Na startnoj poziciji steka ne postoji element. Pokušajte ponovo.")
                except ValueError:
                    print("Nevažeći unos za mesto na steku. Pokušajte ponovo.")

            if ((koPrvi == True and tabla[start_row][start_col]['stek'][mesto_na_steku] == 'O') or (
                    koPrvi == False and tabla[start_row][start_col]['stek'][mesto_na_steku] == 'X')):
                print("Ne možete igrati tuđom figuricom")
                continue

            dobarPotez = odigraj_potez(tabla, start_row, start_col,
                                       target_row, target_col, mesto_na_steku)

            if (dobarPotez):
                return not koPrvi
            else:
                continue

        except ValueError:
            print("Nevažeći unos. Pokušajte ponovo.")


def heuristika_za_potez(board, player):
    score = (heuristic_weights['diagonal_neighbors'] * evaluate_diagonal_neighbors(board, player) +
             heuristic_weights['central_control'] * evaluate_central_control(board, player) +
             heuristic_weights['tokens_on_board'] * count_tokens_on_board(board, player) +
             heuristic_weights['tokens_on_top_of_stacks'] * count_tokens_on_top_of_stacks(board, player) +
             heuristic_weights['full_stack_control'] * evaluate_full_stack_control(board, player, brojStekova, brojStekovaBelih, brojStekovaCrnih))
    return score


def min_max(tabla, dubina, alfa, beta, maksimizacija, igrac, odigraniPotezi):
    if dubina == 0 or KrajIgre(tabla, m, n):
        return None, heuristika_za_potez(tabla, igrac)

    validni_potezi = generisi_validne_poteze(tabla, igrac)

    for odigranPotez in odigraniPotezi:
        if (odigranPotez in validni_potezi):
            validni_potezi.remove(odigranPotez)

    if maksimizacija:
        najbolji_potez = None
        vrednost_najboljeg_poteza = float('-inf')

        vrednost_heuristike = heuristika_za_potez(tabla, igrac)

        validni_potezi = sorted(
            validni_potezi, key=lambda potez: heuristika_za_potez(tabla, igrac))
        for potez in validni_potezi:

            _, vrednost_poteza = min_max(
                tabla, dubina - 1, alfa, beta, False, 1-igrac, odigraniPotezi)

            if vrednost_poteza > vrednost_najboljeg_poteza:
                vrednost_najboljeg_poteza = vrednost_poteza
                najbolji_potez = potez

            alfa = max(alfa, vrednost_najboljeg_poteza)
            if alfa >= beta:
                break

        return najbolji_potez, vrednost_najboljeg_poteza
    else:
        najbolji_potez = None
        vrednost_najboljeg_poteza = float('inf')

        vrednost_heuristike = heuristika_za_potez(tabla, igrac)
        validni_potezi = sorted(
            validni_potezi, key=lambda potez: heuristika_za_potez(tabla, igrac))
        for potez in validni_potezi:
            # nova_tabla = kopiraj_tablu(tabla)

            _, vrednost_poteza = min_max(
                tabla, dubina - 1, alfa, beta, True, 1-igrac, odigraniPotezi)

            if vrednost_poteza < vrednost_najboljeg_poteza:
                vrednost_najboljeg_poteza = vrednost_poteza
                najbolji_potez = potez

            beta = min(beta, vrednost_najboljeg_poteza)
            if alfa >= beta:
                break

        return najbolji_potez, vrednost_najboljeg_poteza


def proveri_potez(tabla, start_row, start_col, target_row, target_col, mesto_na_steku):
    if (start_row % 2 != 0 and start_col % 2 == 0) or (start_row % 2 == 0 and start_col % 2 != 0):
        if (target_row % 2 != 0 and target_col % 2 == 0) or (target_row % 2 == 0 and target_col % 2 != 0):
            if abs(start_row - target_row) == 1 and abs(start_col - target_col) == 1:
                if tabla[start_row][start_col]['stek']:
                    if ((mesto_na_steku == 0 and len(tabla[target_row][target_col]['stek']) == 0) or (
                            mesto_na_steku < len(tabla[target_row][target_col]['stek']))):
                        if len(tabla[start_row][start_col]['stek'])-mesto_na_steku + len(tabla[target_row][target_col]['stek']) <= 8:
                            return True
    return False


def generisi_validne_poteze(tabla, igrac):
    validni = []

    for i in range(len(tabla)):
        for j in range(len(tabla[i])):

            stek_na_poziciji = tabla[i][j]['stek']
            if stek_na_poziciji and not igrac:
                if ('O' in stek_na_poziciji):
                    svi_putevi = find_paths_bfs(tabla, i, j)
                    samo_najkrajci = filter_shortest_paths(svi_putevi)
                    najbolji_potezi = samo_najkrajci

                    for potez in najbolji_potezi:
                        validni.append((i, j, potez[0], potez[1]))

            if stek_na_poziciji and igrac:
                if ('X' in stek_na_poziciji):
                    svi_putevi = find_paths_bfs(tabla, i, j)
                    samo_najkrajci = filter_shortest_paths(svi_putevi)
                    najbolji_potezi = samo_najkrajci

                    for potez in najbolji_potezi:
                        validni.append((i, j, potez[0], potez[1]))
    return validni


def kopiraj_tablu(tabla):
    return copy.deepcopy(tabla)


def odigraj_potez_racunar(tabla, igrac, odigraniPotezi):
    najbolji_potez, _ = min_max(
        tabla, dubina, 10, 10, True, igrac, odigraniPotezi)

    if najbolji_potez is not None:
        start_row, start_col, end_row, end_col = najbolji_potez
        stek_sa_pozicije = tabla[start_row][start_col]['stek']

        for index, figurica in enumerate(stek_sa_pozicije):
            if (igrac and figurica == 'X') or (igrac == False and figurica == 'O'):
                dobarPotez = odigraj_potez(tabla, start_row, start_col,
                                           end_row, end_col, index)
                if (dobarPotez):
                    print(f"Računar je odigrao potez: {najbolji_potez}")
                    return

        odigraniPotezi.append(najbolji_potez)
        odigraj_potez_racunar(tabla, igrac, odigraniPotezi)


def simulirajPotez(tabla, igrac, odigraniPotezi):
    najbolji_potez, _ = min_max(
        tabla, dubina, 10, 10, True, igrac, odigraniPotezi)

    if najbolji_potez is None:
        return False

    start_row, start_col, end_row, end_col = najbolji_potez
    stek_sa_pozicije = tabla[start_row][start_col]['stek']

    for index, figurica in enumerate(stek_sa_pozicije):
        if (igrac and figurica == 'X') or (igrac == False and figurica == 'O'):
            dobarPotez = proveri_potez(
                tabla, start_row, start_col, end_row, end_col, index)
            if dobarPotez:
                return True

    odigraniPotezi.append(najbolji_potez)
    return simulirajPotez(tabla, igrac, odigraniPotezi)


def proveri_kraj_igre(tabla, dim1, dim2):
    global brojStekova, brojStekovaBelih, brojStekovaCrnih

    for row in range(dim1):
        for col in range(dim2):
            if (row % 2 != 0 and col % 2 == 0) or (row % 2 == 0 and col % 2 != 0):
                if tabla[row][col]['stek'] and len(tabla[row][col]['stek']) == 8:
                    vlasnik = tabla[row][col]['stek'][-1]
                    if vlasnik == 'O':
                        brojStekovaBelih += 1
                    elif vlasnik == 'X':
                        brojStekovaCrnih += 1
                    tabla[row][col]['stek'] = []
                    break

    if brojStekovaBelih > brojStekova / 2:
        return 'O'
    elif brojStekovaCrnih > brojStekova / 2:
        return 'X'
    else:
        return None


def KrajIgre(tabla, dim1, dim2):
    rezultat = proveri_kraj_igre(tabla, dim1, dim2)
    global brojStekovaBelih, brojStekovaCrnih
    if (rezultat == "O" or rezultat == "X"):
        print(f"Igra je gotova. Pobednik je igrač {rezultat}.")
        exit()
    else:
        print(f"Crni igrač ima {brojStekovaCrnih} stekova, a beli {
              brojStekovaBelih} ")
        return False


m, n, koIgra, covekRacunar, koPrvi = unosParametaraIgre()
tabla = praznaTabla(m, n)
inicijalnaTabla(m, tabla)


if (koIgra == "covek"):
    while (not KrajIgre(tabla, m, n)):
        koPrvi = unos_poteza(tabla, koPrvi)

else:
    print(
        f"Stanje pre petlje - covekRacunar: {covekRacunar}, koPrvi: {koPrvi}")
    while not KrajIgre(tabla, m, n):
        if covekRacunar == "racunar":
            odigraniPotezi = []
            odigraj_potez_racunar(tabla, koPrvi, odigraniPotezi)
            koPrvi = not koPrvi
            covekRacunar = "covek"
        else:
            odigraniPotezi = []
            simuliraj = simulirajPotez(tabla, koPrvi, odigraniPotezi)
            if (simuliraj):
                koPrvi = unos_poteza(tabla, koPrvi)
            else:
                print("Pošto ne možete odigrati ni jedan potez, potez se prepušta")
                koPrvi = not koPrvi
            covekRacunar = "racunar"
