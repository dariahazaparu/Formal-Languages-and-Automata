# In fisier sunt 4 exemple de automate: 
#   1) lnfa;
#   2) nfa;
#   3) dfa;
#   4) pentru a testa daca s-au eliminat corect starile in dfa_to_dfa_min.
# Codul citeste doar un singur automat, deci trebuie modificat fisierul pentru a le testa pe celelalte.
# Afisarea se face pe ecran.

import queue


def citire_lnfa():
    global n, Q, m, E, d, q0, k, F, l, delta
    f = open("lambda_nfa_to_dfa_min.in")
    n = int(f.readline())
    Q = [int(i) for i in range(n)]
    m = int(f.readline())
    E = [x for x in f.readline().split()]
    E.append('$')
    d = {}
    for q in range(len(E)):
        d[E[q]] = q
    # print (d)

    q0 = int(f.readline())
    k = int(f.readline())
    F = [int(x) for x in f.readline().split()]
    l = int(f.readline())
    delta = {i: {x: [] for x in E} for i in range(n)}
    # print(delta)

    for x in range(l):
        linie = f.readline()
        p = (int(linie.split()[0]), linie.split()[1], int(linie.split()[2]))
        if not delta[p[0]][p[1]]:
            delta[p[0]][p[1]] = [p[2]]
        else:
            delta[p[0]][p[1]].append(p[2])
    # print (delta)


def lnfa_to_nfa():
    global n, Q, m, E, d, q0, k, F, l, delta

    # pasul 1 - calculare lambda inchidere
    lambda_inchidere = [[i] for i in Q]

    gasit = 0
    for stare in Q:
        if delta[stare]['$'] != []:
            gasit = 1

    if gasit == 1:
        for i in Q:

            if delta[i]['$']:
                lambda_inchidere[i].extend(delta[i]['$'])

            for k in range(l):
                for j in Q:
                    if j in lambda_inchidere[i]:
                        lambda_inchidere[i].extend(delta[j]['$'])

        for i in range(len(lambda_inchidere)):
            lambda_inchidere[i] = list(set(lambda_inchidere[i]))
            # eliminare duplicate
        # print(lambda_inchidere)

        # Pasul 2
        # Calculare a doua coloana tabel
        tranzitie = []
        for litera in E:
            if litera != '$':

                litera_n = [[] for i in Q]
                for i in range(len(Q)):
                    for stare in lambda_inchidere[i]:
                        if delta[stare][litera]:
                            litera_n[i].extend(delta[stare][litera])

                for i in range(len(litera_n)):
                    litera_n[i] = list(set(litera_n[i]))

                tranzitie.append(litera_n)

        # calculare a 3a coloana pt fiecare litera
        E.remove('$')
        d_n = {str(i): tranzitie[d[i]] for i in E}
        delta_n = [{x: [] for x in E} for i in range(n)]

        for litera in E:

            L_mai_mare = []
            for stare_ext in d_n[litera]:
                L = []
                if stare_ext:
                    for st in stare_ext:
                        L.extend(lambda_inchidere[st])
                L_mai_mare.append(list(set(L)))

            for i in range(len(L_mai_mare)):
                delta_n[i][litera] = L_mai_mare[i]

        # Pasul 3 - actualizare stari finale
        F_n = []
        for stare in Q:
            if lambda_inchidere[stare]:
                for sf in F:
                    if sf in lambda_inchidere[stare]:
                        F_n.append(stare)
        F_n = list(set(F_n))

        # Pasul 4 - eliminarea starilor redundante
        # dictionar de dictionare pentru delta, in loc de lista de dictionare, ca sa pot elimina stari
        delta_N = {i: delta_n[i] for i in Q}
        stari_inlocuite = {}

        for stare1 in Q:
            for stare2 in Q:
                if stare1 < stare2 and stare1 in delta_N.keys() and stare2 in delta_N.keys():
                    if (stare1 in F_n and stare2 in F_n) or (stare1 not in F_n and stare2 not in F_n):
                        if delta_N[stare1] == delta_N[stare2]:
                            stari_inlocuite[stare2] = stare1
                            del delta_N[stare2]

        # actualizare stari existente
        for stare in Q:
            if stare not in delta_N.keys():
                Q.remove(stare)

        # stergerea starilor inexistente si inlocuirea lor
        for stare in Q:
            for litera in E:
                for st in delta_N[stare][litera]:
                    if st in stari_inlocuite.keys():
                        delta_N[stare][litera].remove(st)
                        delta_N[stare][litera].append(stari_inlocuite[st])
                delta_N[stare][litera] = list(set(delta_N[stare][litera]))

        # actualizare variabile pentru afisare corecta
        delta = delta_N
        F = F_n
        # print (delta)
    else:
        E.remove('$')
        for stare in Q:
            if delta[stare]['$'] == []:
                del delta[stare]['$']
        # print (delta)


def nfa_to_dfa():
    global n, Q, m, E, d, q0, k, F, l, delta

    # Pasul 1 - eliminarea nedeterminismului
    q = queue.Queue()
    q.put(str(q0))
    # Pornim cu o coada in care adaugam doar starea initiala q0.

    delta_n = {}
    stari_genenerate = []
    # o dublura a cozii pentru a putea verifica daca x se afla in coada

    delta = {str(i): delta[i] for i in Q}
    while not q.empty():
        st = q.get()
        delta_n[st] = {}
        for litera in E:

            # Apoi pentru fiecare stare din coada q si fiecare caracter din alfabet:
            # calculam delta[stare][caracter] = [qx0, qx1, ..., qxk], k >= 0
            temp = []
            for stare in str(st):
                temp.extend(delta[stare][litera])
                temp = list(set(temp))
                # Tranzitia acestei stari cu un caracter va fi reuniunea starilor accesibile cu caracterul din toate starile componente.

            if len(temp) == 0:
                delta_n[st][litera] = []
            else:
                if temp not in stari_genenerate:
                    # Daca noua stare fromata qx0...xk nu a mai fost vizitata, atunci o adaugam in coada.
                    stari_genenerate.append(temp)
                    k = ''
                    # cream starea qx0...xk
                    for stp in temp:
                        k += str(stp)
                    q.put(k)
                delta_n[st][litera] = temp

    # unesc starile in care ajunge un caracter pentru a crea o singura stare
    for stare in delta_n.keys():
        for litera in E:
            k = ''
            for st in delta_n[stare][litera]:
                k += str(st)
            delta_n[stare][litera] = k

    # Pasul 2
    # starile finale
    F_n = []
    for stare in delta_n.keys():
        for litera in stare:
            if int(litera) in F:
                F_n.append(stare)

    # Pasul 3 - redenumirea
    nr = len(delta_n.keys())
    Q_n = [str(i) for i in range(nr)]
    Q_n2 = [str(i) for i in range(nr)]

    stari_inlocuite = {}
    # dictionar pentru a inlocui starile
    for cheie in delta_n.keys():
        if cheie in Q_n:
            stari_inlocuite[cheie] = int(cheie)
            Q_n.remove(cheie)
    # Q_n are doar starile care nu mai exista din automatul initial

    for cheie in delta_n.keys():
        if cheie not in Q_n2:
            stari_inlocuite[cheie] = int(Q_n[0])
            Q_n.pop(0)
    # starile compuse se transforma si preiau un element din Q_n, starile ramase

    delta = {int(stari_inlocuite[i]): delta_n[i] for i in stari_inlocuite.keys()}
    Q = [i for i in range(nr)]
    for stare in Q:
        for litera in E:
            if delta[stare][litera] in stari_inlocuite.keys():
                delta[stare][litera] = stari_inlocuite[delta[stare][litera]]
    # delta = matricea finala de dfa in care se redenumesc starile compuse in
    # echivalentele lor din stari_inlocuite

    # redenunmirea starilor finale
    F = []
    for stare_f in F_n:
        if stare_f in stari_inlocuite.keys():
            F.append(stari_inlocuite[stare_f])
        else:
            F.append(stare_f)
    F = list(set(F))
    # print (delta)


def dfa_to_dfa_min():
    global n, Q, m, E, d, q0, k, F, l, delta, stari_posibile

    # Pasul 1
    n = len(Q)
    # Construim matricea de echivalenta si o marcam pe toata cu TRUE.
    # Marcam doar partea stanga jos, matricea ind simetrica.
    matrice = [[True] * i for i in range(n)]
    # Marcam cu FALSE toate perechile (q, r), unde q stare finala si r stare nefinala.
    for stare_f in Q:
        for stare_nef in Q:
            if stare_f in F and stare_nef not in F and stare_f != stare_nef:

                if stare_f > stare_nef:
                    matrice[stare_f][stare_nef] = False
                else:
                    matrice[stare_nef][stare_f] = False

    for stare in delta.keys():
        for litera in E:
            if delta[stare][litera] == '':
                delta[stare][litera] = -1
    # Marcam cu FALSE toate perechile (q, r) pentru care (delta(q, a), delta(r, a)) sunt marcate cu
    # FALSE, oricare ar fi a un caracter din alfabet.
    # Repetam pana nu mai apar modicari.
    schimbare = 0
    while schimbare == 0:
        for litera in E:
            schimbare = 1
            for sf in Q:
                for sn in Q:
                    if delta[sf][litera] > delta[sn][litera]:
                        if matrice[delta[sf][litera]][delta[sn][litera]] == False:
                            if sf > sn:
                                if matrice[sf][sn] == True:
                                    schimbare = 0
                                matrice[sf][sn] = False
                            else:
                                if matrice[sn][sf] == True:
                                    schimbare = 0
                                matrice[sn][sf] = False
    # se formeaza grupurie de echivalenta
    groups = [{i} for i in range(n)]
    for sf in Q:
        for sn in Q:
            if sf > sn :
                if matrice[sf][sn] == True:
                    groups[sf] = groups[sf].union(groups[sn])
                    groups[sn] = set()
    groups_n = []
    for st in groups:
        if st :
            groups_n.append(st)

    # Pasul 2
    # creez starile noi generate pe baza grupurilor de echivalenta
    stari_generate = []
    for gr in groups_n:
        k = ''
        for f in gr:
            k += str(f)
        stari_generate.append(k)
    stari_generate_2 = {i: [stare for stare in stari_generate if str(i) in stare] for i in Q}

    # tabelul de la pasul 2
    delta_n = {stare: {litera: [] for litera in E} for stare in stari_generate}
    for stare in delta_n.keys():
        for litera in E:
            for st in stare:
                x = delta[int(st)][litera]
                if x in stari_generate_2.keys():
                    delta_n[stare][litera].extend(stari_generate_2[x])
                    delta_n[stare][litera] = list(set(delta_n[stare][litera]))

    # matricea e completata doar de un singur caracter
    for stare in delta_n.keys():
        for litera in E:
            if delta_n[stare][litera] != []:
                delta_n[stare][litera] = delta_n[stare][litera][0]

    # Pasul 3 - calcularea starilor initiale si finale
    q0 = stari_generate_2[q0][0]
    F_n = []
    for stare_f in F:
        F_n.extend(stari_generate_2[stare_f])
    F = list(set(F_n))


    # Pasul 4 - starile dead-end
    # valori are starile care pot duce in stari finale
    # in valori nu se afla si starile finale
    valori = []
    for stare in delta_n.keys():
        q = queue.Queue()
        q.put(stare)
        vizite = []
        if stare == q0:
            # pentru pasul 5, am nevoie de toate starile din care pot ajunge din q0
            stari_posibile = [q0]
        while not q.empty():
            st = q.get()
            for litera in E:
                if delta_n[st][litera] != []:
                    stari_posibile.append(delta_n[st][litera])
                    if delta_n[st][litera] not in vizite:
                        q.put(delta_n[st][litera])
                        vizite.append(delta_n[st][litera])
                        if delta_n[st][litera] in F_n:
                            # a ajuns in stare finala
                            valori.append(stare)
    stari_posibile = set(stari_posibile)

    # eliminarea starilor dead end din liniile matricei
    delta_N = delta_n.copy()
    for stare in delta_n.keys():
        if stare not in valori:
            if stare not in F:
                del delta_N[stare]
    # inlocuirea componentelor matricei cu lista vida in cazul in care duceau intr o
    # stare dead end
    for stare in delta_N.keys():
        for litera in E:
            if delta_N[stare][litera] not in valori:
                if delta_N[stare][litera] not in F:
                    delta_N[stare][litera] = []

    # Pasul 5
    # eliminarea starilor neaccesibile din liniile matricei
    delta_NN = delta_N.copy()
    for stare in delta_N.keys():
        if stare not in stari_posibile:
            del delta_NN[stare]

    # redenumirea starilor ramase
    stari_inlocuite = {}
    x = 0
    for stare in delta_NN.keys():
        stari_inlocuite[stare] = x
        x += 1

    delta = {stari_inlocuite[i]: delta_NN[i] for i in delta_NN.keys()}
    for stare in delta.keys():
        for litera in E:
            if delta[stare][litera] != []:
                delta[stare][litera] = stari_inlocuite[delta[stare][litera]]

    # actualizarea multimii de stari finale
    F_n = []
    for stare in F:
        F_n.append(stari_inlocuite[stare])
    F = F_n

    # actualizarea multimii de stari si a starii initiale
    Q = []
    for stare in delta.keys():
        Q.append(stare)
    q0 = stari_inlocuite[q0]
    # print(delta)


def afisare():
    global n, Q, m, E, d, q0, k, F, l, delta
    print("DATELE PENTRU AUTOMATUL REZULTAT")
    n = len(Q)
    print("Numarul de stari: {}.".format(n))
    print("Starile sunt: {}.".format(Q))
    print("Alfabetul are {} litere.".format(m))
    print("Literele sunt: {}.".format(E))
    print("Starea initiala este: {}.".format(q0))
    k = len(F)
    print("Numar de stari finale: {}.".format(k))
    print("Acestea sunt: {}.".format(F))
    l = 0
    for stare in delta.keys():
        for litera in E:
            if delta[stare][litera] != []:
                l += 1
    print("Automatul are {} tranzitii.".format(l))
    print("Tranzitiile sunt:")
    for stare in delta.keys():
        for litera in E:
            if delta[stare][litera] == '':
                delta[stare][litera] = []
    for stare in delta.keys():
        for litera in E:
            if delta[stare][litera] != []:
                # print ("\tDin starea {} spre starea {} cu litera {}.".format(stare, delta[stare][litera], litera))
                print("\t{} ---> {} ---> {}".format(stare, litera, delta[stare][litera]))


citire_lnfa()
lnfa_to_nfa()
nfa_to_dfa()
dfa_to_dfa_min()
afisare()
