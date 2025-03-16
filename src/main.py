# src/main.py

def count_cards(hand):
    """Count the total number of cards in the hand."""
    return len(hand)

def detect_pair(hand):
    """Detect if there’s a pair (two cards of the same rank) in the hand."""
    ranks = [card.split()[0] for card in hand]  # Extract ranks (e.g., "Ace", "King")
    for rank in set(ranks):  # Use set to avoid counting the same pair twice
        if ranks.count(rank) >= 2:
            return True, rank
    return False, None

def check_flush(hand):
    """Check if the hand is a flush (all cards of the same suit)."""
    suits = [card.split()[-1] for card in hand]  # Extract suits (e.g., "Spades", "Hearts")
    first_suit = suits[0] if suits else None
    return len(suits) >= 5 and all(suit == first_suit for suit in suits)

def evaluate_hand(hand):
    """Evaluate the hand and print results."""
    card_count = count_cards(hand)
    has_pair, pair_rank = detect_pair(hand)
    is_flush = check_flush(hand)

    print(f"Hand: {hand}")
    print(f"Number of cards: {card_count}")
    if has_pair:
        print(f"Pair detected with rank: {pair_rank}")
    else:
        print("No pair detected")
    if is_flush:
        print("Flush detected!")
    else:
        print("No flush detected")

# Test the bot with sample hands
if __name__ == "__main__":
    # Test hand 1: Pair of Aces
    hand1 = ["Ace of Spades", "Ace of Hearts", "King of Clubs", "Queen of Diamonds", "Jack of Spades"]
    evaluate_hand(hand1)

    # Test hand 2: Flush (all Spades)
    hand2 = ["Ace of Spades", "Two of Spades", "Three of Spades", "Four of Spades", "Five of Spades"]
    evaluate_hand(hand2)

    # Test hand 3: No pair or flush
    hand3 = ["Ace of Spades", "King of Hearts", "Queen of Clubs", "Jack of Diamonds", "Ten of Spades"]
    evaluate_hand(hand3)