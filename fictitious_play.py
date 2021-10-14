from math import *
from random import randint
import time
import operator as op
from functools import reduce

start_time = time.time()

# INPUTS

# NB For now, I am assuming that there are 2 players and uniform values

# Specify the number of possible valuations and bids

x = 101

# Specify the auction structure (first price vs all-pay)

first_price = 0

# Specify the number of players

n = 3

# Specify the number of time periods (slow if t >> 10,000)

t = 1000

print(f'There are {n} players and {t} time periods.')

if first_price == 1:
    print("This is a first-price auction.")
else:
    print("This is an all-pay auction")

# DEFINING THE BEST RESPONSE FUNCTION

# Let's define the set of possible bids

bid_space = list(range(0, x))

# As a preliminary, this function returns n choose r

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom  # or / in Python 2

# This function returns your chance of winning given your bid and the observed history of opponent bids

def p_win(bid, previous_bids):
    lower_bids = [element for element in previous_bids if element < bid]
    p_lower = len(lower_bids)/len(previous_bids)
    tied_bids = [element for element in previous_bids if element == bid]
    p_tied = len(tied_bids) / len(previous_bids)
    return sum([ncr(n-1, j)*p_lower**(n-1-j) * p_tied**j *(1/(j+1)) for j in range(0, n)])

# This function returns your expected payoff given your valuation, bid and the previous bids you observed

if first_price == 1:
    def payoff(valuation, bid, previous_bids):
        return (valuation - bid)*p_win(bid, previous_bids)
else:
    def payoff(valuation, bid, previous_bids):
        return valuation*p_win(bid, previous_bids) - bid

# This function returns your optimal bid given your valuation and the previous bids you observed

def best_response(valuation, previous_bids):
    possible_payoffs = [payoff(valuation, bid, previous_bids) for bid in bid_space]
    if max(possible_payoffs) <= 0:
        if first_price == 1:
            return floor(((n-1)*valuation)/n)
        else:
            return floor(((n-1)/n) * (valuation**n)/(x**(n-1)))
    else:
        return possible_payoffs.index(max(possible_payoffs))

# Finally, we define an 'evolution' function which returns a new round of bids given the values just drawn and the bid history

def evolution(historic_bids, values):
    optimal_bids = []
    for player in range(0, n):
        v = values[player]
        history = [element[:player] + element[player + 1:] for element in historic_bids]
        unpacked_history = [item for sublist in history for item in sublist]
        optimal_bid = best_response(v, unpacked_history)
        optimal_bids.append(optimal_bid)
    return optimal_bids

# CALCULATING BEST RESPONSES ITERATIVELY

# Let's define some important objects

value_history = []
bid_history = []

# Let's draw values (and specify bids) for the first round

values = [randint(0, x-1) for player in range(0, n)]
if first_price == 1:
    bids = [floor(((n-1)/n)*value) for value in values]
else:
    bids = [floor(((n - 1) / n) * ((value**n)/(x**(n-1)))) for value in values]

value_history.append(values)
bid_history.append(bids)

# Now we start the loop

tracker = 0
while tracker <= t:
    values = [randint(0, x-1) for player in range(0, n)]
    value_history.append(values)
    bid_history.append(evolution(bid_history, values))
    tracker += 1

all_bids = [item for sublist in bid_history for item in sublist]

bid_distribution = []

for bid in bid_space:
    matching_bids = [element for element in all_bids if element == bid]
    bid_distribution.append(len(matching_bids)/len(all_bids))

print("Value history")
print(value_history)

print("Bid history")
print(bid_history)

print("Bid distribution")
for element in bid_distribution:
    print(element)

print(f'Run time: {round((time.time() - start_time), 1)} seconds.')
