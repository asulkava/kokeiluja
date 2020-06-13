def loop(deck, dealer_sum, player_sum, x, n):
    deck2 = deck.copy()
    deck2.remove(x)
    side_sum=0
    len_y = len(deck2)
    for y in deck2:
        new_sum=dealer_sum+x+y
        if new_sum<=21 and new_sum>player_sum:
            side_sum+=1
        elif new_sum<21 and n>0:
            side_sum+=loop(deck2, dealer_sum+x, player_sum, y, n-1)
    return side_sum/len_y

def bust_chances(player, dealer):
    deck = []
    for i in range(1,14):
        for j in range(0,4):
            deck.append(i)
    for x in player:
        deck.remove(x)
    for x in dealer:
        deck.remove(x)
    
    player_bust = 0
    dealer_bust = 0
    dealer_wins = 0
    player_sum = sum(player)
    dealer_sum = sum(dealer)
    for x in deck:
        if player_sum+x>21:
            player_bust+=1
        if dealer_sum+x>21:
            dealer_bust+=1

        if player_sum>21:
            dealer_wins+=1
        elif dealer_sum> player_sum:
            dealer_wins+=1
        elif dealer_sum+x <= 21 and dealer_sum+x > player_sum:
            dealer_wins+=1
        elif dealer_sum+x <= 21:
            dealer_wins+=loop(deck, dealer_sum, player_sum, x, 2)

    r1 = 100*player_bust/len(deck)
    r2 = 100*dealer_bust/len(deck)
    r3 = 100*(dealer_wins)/len(deck)
    return [round(r1, 2), round(r2, 2), round(r3, 2)]