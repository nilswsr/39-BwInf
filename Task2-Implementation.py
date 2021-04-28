path = "spiesse10.txt"
file = open(path)

anzahl_obstsorten = int(file.readline().replace("\n", ""))
wunschsorten = [x for x in file.readline().replace("\n", "").split(" ") if x != ""]
anzahl_beobachtungen = int(file.readline().replace("\n", ""))

print("Donalds Wunschsorten: " + str(wunschsorten))
print(10*"=")
# M -> Beobachtungen, T -> alle Obstsorten, B -> eine Beobachtung
M = set()
T = set(wunschsorten)
for i in range(anzahl_beobachtungen):
    schuessel_nummern = [x for x in file.readline().replace("\n", "").split(" ") if x != ""]
    obstsorten = [x for x in file.readline().replace("\n", "").split(" ") if x != ""]
    # frozenset aus Schuesselnummern und Obstsorten erstellen und dem set M hinzufuegen
    B = frozenset(schuessel_nummern + obstsorten)
    M.add(B)
    # weitere Obstsorten dem set T hinzufuegen
    T = T.union(obstsorten)

# Funktion, um die Vereinigung von Sets in einem Set zu bestimmen
def union_of_sets(set_of_sets):
    return set().union(*set_of_sets)

# Funktion, um den Schnitt von Sets in einem Set zu bestimmen
def intersection_of_sets(set_of_sets):
    if set_of_sets != set():
        return frozenset.intersection(*set_of_sets)
    else:
        return frozenset()

obstmengen = {}

# Menge U -> alle Sorten, die sich Donald wünscht, aber in keiner der Beobachtungen vorkommen
U = T - union_of_sets(M)

# ob eindeutig bestimmt ist, aus welchen Schuesseln sich Donald bedienen muss
eindeutig = True
bedienen = set()
# ueber jede Schuesselnummer iterieren
for j in range(1, anzahl_obstsorten+1):
    if not str(j) in obstmengen:
        # fuer jede Schuessel, Menge A und N bestimmen
        A = set()
        N = set()
        for x in M:
            if str(j) in x:
                A.add(x)
            else:
                N.add(x)
        # K bestimmen
        K = union_of_sets(A) - union_of_sets(N)
        # Schnittmenge S nur mit Werten aus K
        S = intersection_of_sets(A).intersection(K)
        # Menge der Obstsorten O fuer Schuessel j bestimmen
        O = set([x for x in S if not x.isnumeric()])
        # O mit uebrige neu definieren, wenn leere Menge
        if not len(O):
            O = U.copy()

        # Menge der weiteren Schluesselnummer bestimmen, die die gleiche Obstsortenmenge haben
        W = set([x for x in S if x.isnumeric()])

        # Mengen in dictionary speichern
        for schuesselnummer in W:
            obstmengen[str(schuesselnummer)] = O.copy()
    else:
        O = obstmengen[str(j)]

    # ueber alle wuensche iterieren, und schauen wie viele donald davon moechte
    # wenn die erfuellten wuensche gleich der laenge von O entsprechen, nimmt er aus der schuessel
    # wenn sie 0 entsprechen, dann nicht
    # alles andere -> nicht mehr eindeutig
    wuensche_erfuellt = 0
    for obstsorte in O:
        if obstsorte in wunschsorten:
            wuensche_erfuellt += 1

    # Bestimmung, ob Donald aus Schuessel nimmt oder nicht & Programm-Ausgabe
    print("Schuessel:", j)
    if len(O):
        print("Inhalt: " + str(O))
    else:
        print("Inhalt: unbekannt")
    if not wuensche_erfuellt:
        print("Bedienen: Nein")
    elif wuensche_erfuellt == len(O):
        bedienen.add(j)
        print("Bedienen: Ja")
    else:
        eindeutig = False
        wahrscheinlichkeit = wuensche_erfuellt/len(O) * 100
        print("Bedienen: Zu "+str(wahrscheinlichkeit)+"% wahrscheinlich, dass eine richtige Obstsorte genommen wird")
    print("=" * 10)

if eindeutig:
    print("Es konnte eindeutig bestimmt werden, aus welchen Schuesseln sich Donald bedienen muss.")
    print("Er muss sich aus den Schuesseln:", bedienen, "bedienen.")
else:
    print("Es konnte nicht eindeutig bestimmt werden, aus welchen Schuesseln sich Donald bedienen muss.")
