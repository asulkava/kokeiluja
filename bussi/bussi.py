import random

def one_round():
    array = []
    for i in range(0, 4):
        for j in range(1, 14):
            array.append(j)


    def take_random_cards(array, n):
        results = []
        for i in range(0, n):
            valinta = random.choice(array)
            results.append(valinta)
            try:
                array.remove(valinta)
            except OSError:
                print("Literally what.")
        return [results, array]

    [r1, array] = take_random_cards(array, 1)
    [r2, array] = take_random_cards(array, 2)
    [r3, array] = take_random_cards(array, 3)
    [r4, array] = take_random_cards(array, 4)

    board = [r1, r2, r3, r4]
    lost = False
    for i in range(0, 4):
        playercard = random.choice(board[i])
        [housechoice, array] = take_random_cards(array, 1)
        house = housechoice[0]
        playerchoice = False
        if playercard < 6:
            playerchoice = True
        if (playercard != house) and playerchoice and house > playercard:
            lost = True
            break
        elif (playercard != house) and (not playerchoice) and house < playercard:
            lost = True
            break

    if not lost:
        return 1
    else:
        return 0

n = 10000
voitot = 0
for i in range(0,n):
    voitot+=one_round()
print("Chance to win round: %.3f" %(100*voitot/n))
