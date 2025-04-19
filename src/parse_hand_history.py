import pandas as pd
from hand_evaluator import def_flush, def_pair

def parse_hand_history(file_path):
    hands = []
    current_hand = None  # Start with None to ensure proper initialization
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # Check for the start of a new hand with a broader pattern
            if 'PokerStars' in line and ('Hand' in line or 'Game' in line):
                if current_hand is not None:  # Only append if current_hand exists
                    # Ensure all required keys are present before appending
                    if 'bets' not in current_hand:
                        current_hand['bets'] = 0
                    if 'winnings' not in current_hand:
                        current_hand['winnings'] = 0
                    if 'position' not in current_hand:
                        current_hand['position'] = ''
                    if 'hole_cards' not in current_hand:
                        current_hand['hole_cards'] = ''
                    hands.append(current_hand)
                # Initialize new hand
                hand_id = line.split('#')[1].split(':')[0] if '#' in line else line.split()[-1]
                current_hand = {
                    'hand_id': hand_id,
                    'bets': 0,
                    'winnings': 0,
                    'position': '',
                    'hole_cards': ''
                }
            if not current_hand:  # Skip if current_hand hasn't been initialized
                continue
            if 'Seat' in line and 'nickyb123' in line:
                if 'button' in line:
                    current_hand['position'] = 'Button'
                elif 'small blind' in line:
                    current_hand['position'] = 'Small Blind'
                elif 'big blind' in line:
                    current_hand['position'] = 'Big Blind'
                else:
                    current_hand['position'] = 'Other'
            if 'Dealt to nickyb123' in line:
                current_hand['hole_cards'] = line.split('[')[1].split(']')[0]
            if 'nickyb123:' in line and ('calls' in line or 'raises' in line or 'bets' in line):
                words = line.split()
                try:
                    if words[-1] == 'all-in' and words[-3] == 'and':  # Handle "bets 895 and is all-in"
                        amount = float(words[-4])
                        if 'bets' not in current_hand:  # Extra safeguard
                            current_hand['bets'] = 0
                        current_hand['bets'] += amount
                    else:  # Handle regular bets like "calls 20"
                        amount = float(words[-1])
                        if 'bets' not in current_hand:  # Extra safeguard
                            current_hand['bets'] = 0
                        current_hand['bets'] += amount
                except (ValueError, IndexError) as e:
                    print(f"Error parsing bet in line: '{line}' - {e}")
                    continue
            if 'nickyb123 collected' in line:
                winnings_str = line.split('collected')[1].split('from')[0].strip()
                winnings = float(winnings_str.strip('()'))
                current_hand['winnings'] = winnings
        if current_hand is not None:  # Handle the last hand
            if 'bets' not in current_hand:
                current_hand['bets'] = 0
            if 'winnings' not in current_hand:
                current_hand['winnings'] = 0
            if 'position' not in current_hand:
                current_hand['position'] = ''
            if 'hole_cards' not in current_hand:
                current_hand['hole_cards'] = ''
            hands.append(current_hand)
    return hands

# Parse the hand history file
hands_data = parse_hand_history('hand_history2.txt')
df = pd.DataFrame(hands_data)

# Convert hole cards to a list format for evaluation
df['hole_cards_list'] = df['hole_cards'].apply(lambda x: x.split() if x else [])
df['is_pair'] = df['hole_cards_list'].apply(lambda cards: def_pair(cards) if len(cards) >= 2 else False)
df['is_suited'] = df['hole_cards_list'].apply(lambda cards: def_flush(cards) if len(cards) >= 2 else False)

# Analysis
print("Hand History with Hand Strength:")
print(df[['hand_id', 'hole_cards', 'position', 'is_pair', 'is_suited', 'bets', 'winnings']].head(10))

print("\nOverall Stats:")
print(f"Total Hands Played: {len(df)}")
print(f"Average Bet per Hand: ${df['bets'].mean():.2f}")
print(f"Average Winnings per Hand: ${df['winnings'].mean():.2f}")
print(f"Win Rate: {(df['winnings'] > 0).mean():.2%}")

print("\nWin Rate by Position:")
print(df.groupby('position')['winnings'].apply(lambda x: (x > 0).mean()).map('{:.2%}'.format))

print("\nWin Rate for Pairs:")
pair_win_rate = df[df['is_pair']]['winnings'].apply(lambda x: x > 0).mean()
print(f"{pair_win_rate:.2%}")

print("\nWin Rate for Suited Cards:")
suited_win_rate = df[df['is_suited']]['winnings'].apply(lambda x: x > 0).mean()
print(f"{suited_win_rate:.2%}")