f = open("lnfa.in")
n = int(f.readline())
Q = [int(i) for i in range(n)]
m = int(f.readline())
E = [x for x in f.readline().split()]
E.append('$')
d = {}
for q in range(len(E)):
    d[E[q]] = q
#print (d)

q0 = int(f.readline())
k = int(f.readline())
F = [int (x) for x in f.readline().split()]
l = int(f.readline())

delta = [ {x: [-1] for x in E} for i in range(n)]
#print (delta)

for x in range(l):
    linie = f.readline()
    p = (int(linie.split()[0]), linie.split()[1], int(linie.split()[2]))
    if delta[p[0]][p[1]] == [-1]:
        delta[p[0]][p[1]] = [p[2]]
    else:
        delta[p[0]][p[1]].append(p[2])

#print(delta)]
def evaluate(cuvant, stare):
    global delta, n, m, rez

    if len(cuvant) != 0 :
        #print("starea: " + str(stare) + " cuvant: " + str(cuvant))
        if delta[stare]['$'] != [-1]:
            for st in delta[stare]['$']:
                evaluate(cuvant, st)

        if delta[stare][cuvant[0]] == [-1]:
            rez.append(False)
        else:
            stare = delta[stare][cuvant[0]]
            for st in stare:
                evaluate(cuvant[1:], st)
    else:
        if stare in F:
            rez.append(True)
        else:
            rez.append(False)


x = int(f.readline())
for cuvant in f:
    rez = []
    stare = q0
    evaluate(cuvant.strip(), stare)
    if True in rez:
        print("acceptat")
    else:
        print("respins")