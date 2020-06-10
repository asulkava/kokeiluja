import random

def one_game():
    array = []
    for i in range(0, 4):
        for j in range(1, 14):
            array.append(j)


    def take_random_cards(array, n):
        results = []
        end = False
        if len(array)<n:
            end = True
        else:
            for i in range(0, n):
                valinta = random.choice(array)
                results.append(valinta)
                array.remove(valinta)
        return [results, array, end]

    [r1, array, l] = take_random_cards(array, 1)
    [r2, array, l] = take_random_cards(array, 2)
    [r3, array, l] = take_random_cards(array, 3)
    [r4, array, l] = take_random_cards(array, 4)

    board = [r1, r2, r3, r4]

    round = 0
    won_index = 0
    while won_index < 4:
        round +=1
        won_index = 0
        for i in range(0,4):
            #playercard = random.choice(board[i])
            playercard = board[i][0]
            [housechoice, array, l] = take_random_cards(array, 1)
            if l:
                return 999
            house = housechoice[0]
            playerchoice = False
            if playercard < 6:
                playerchoice = True
            if playerchoice and house < playercard:
                won_index+=1
            elif (not playerchoice) and house > playercard:
                won_index+=1
            elif playercard == house:
                won_index+=1
            else:
                # lost so replace board
                [replace, array, l] = take_random_cards(array, i)
                if l:
                    return 999
                for x in replace:
                    board[i][0] = x
            i+=1
        
        
    return round

n = 10000
wins = 0
for i in range(0,n):
    if not one_game()==999:
        wins+=1
print("Chance to ever win: %.3f" % (100*wins/n))
