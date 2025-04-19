def def_card_number(card):
    return card[:-1]  # Extracts rank (e.g., '8d' -> '8')

def def_suit(card):
    return card[-1]  # Extracts suit (e.g., '8d' -> 'd')

def def_flush(hand):
    first_suit = def_suit(hand[0])
    suits = [def_suit(card) for card in hand]
    return all(suit == first_suit for suit in suits)

def def_pair(hand):
    ranks = [def_card_number(card) for card in hand]
    return any(ranks.count(rank) >= 2 for rank in set(ranks))