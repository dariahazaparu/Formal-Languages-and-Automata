f = open("dfa.in")
n = int(f.readline())
Q = [int(i) for i in range(n)]
m = int(f.readline())
E = [x for x in f.readline().split()]
d = {}
for q in range(len(E)):
    d[E[q]] = q
#print (d)

q0 = int(f.readline())
k = int(f.readline())
F = [int (x) for x in f.readline().split()]
l = int(f.readline())

delta = [[-1] * m for i in range(m)]

for x in range(l):
    linie = f.readline()
    p = (int(linie.split()[0]), linie.split()[1], int(linie.split()[2]))
    delta[p[0]][d[p[1]]] = p[2]
#print(delta)

def evaluate(cuvant):
    global delta, n, m
    stare = 0
    while len(cuvant) != 1:
        if delta[stare][d[cuvant[0]]] != -1:
            stare = delta[stare][d[cuvant[0]]]
            cuvant = cuvant[1:]
        else:
            return False

    if stare in F:
        return True
    else:
        return False

x = int(f.readline())
for cuvant in f:
   if evaluate(cuvant) == True:
       print ( "acceptat")
   else:
       print ( "respins")
