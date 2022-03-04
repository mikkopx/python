def menu():
    print("OSTOSLISTA 1.0")
    print("1. Lisää tuote")
    print("2. Tarkista ostoslista")
    print("3. Lopeta\n")

def check():
    print("OSTOSLISTA:")
    for x, y in ostot.items():
        print(x, y, "€")

ostot = {}
menu()
valinta = 0

while valinta != 3:
    valinta = int(input("Anna valinta: "))
    if valinta == 1:
        tuote = input("Tuote: ")
        tuote = tuote.upper()
        hinta = input("Hinta: ")
        ostot[tuote] = float(hinta)
    elif valinta == 2:
        check()

max_h= max(ostot.values())
max_t = max(ostot, key=ostot.get)
min_h = min(ostot.values())
min_t = min(ostot, key=ostot.get)

print("")
print(f"Kallein tuote: {max_t} {max_h} €")
print(f"Edullisin tuote: {min_t} {min_h} €\n")
check()