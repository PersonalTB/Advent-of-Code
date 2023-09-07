"""
*** *** ADVENT OF CODE - DAY 22 - CRAB COMBAT *** ***

Src: https://adventofcode.com/2020/day/22
Setting: bored from sailing, we want to play a game of Combat with our Space Cards, and there's even an opponent: a small crab that climbed aboard.
Challenge: Fortunately, it doesn't take long to teach the crab the rules. Play the game. 

Input: input.txt, a .txt file containing the decks of both players

e.g.

Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10

The rules of the game of Combat:
The game consists of a series of rounds. 
Both players draw their top card, and the player with the higher-valued card wins the round. 
The winner keeps both cards, placing them on the bottom of their own deck so that the winner's card is above the other card. 
If this causes a player to have all of the cards, they win, and the game ends.
Once the game ends, you can calculate the winning player's score. 
The bottom card in their deck is worth the value of the card multiplied by 1, 
the second-from-the-bottom card is worth the value of the card multiplied by 2, and so on. 
With 10 cards, the top card is worth the value on the card multiplied by 10.
The sum of these is the winning players' score.

At the end of the game in the above example, player 2 is the winner with deck: 3, 2, 10, 6, 8, 5, 9, 4, 7, 1; this makes his score: 306

The rules of the game of Recursive Combat:
The game consists of a series of rounds with a few changes:
Before playing cards, if there was a previous round that had exactly the same decks in **this** game, player 1 wins by default. 
Otherwise, the players begin the round by each drawing the top card of their deck as normal.
If both players have as many cards remaining in their deck >= the value of the card they drew, a **new** game of Recursive Combat is played.
Otherwise, at least one player does not have enough cards left to recurse; the winner of the round is the player with the higher-value card.
The winner of the round takes the two cards dealt at the beginning of the round and places them on the bottom of their own deck 
Note that the winner's card this time might be the lower-valued of the cards if they won the round due to winning a sub-game. 
If collecting cards by winning the round causes a player to have all of the cards, they win, and the game ends.

At the end of the game in the above example, player 2 is the winner with deck: 7, 5, 6, 2, 4, 1, 10, 8, 9, 3; this makes his score: 291

The challenge consists of two parts:
Part 1: Play the small crab in a game of Combat using the two decks you just dealt. What is the winning player's score?
Part 2: Play the small crab in a game of Recursive Combat using the two decks you just dealt. What is the winning player's score?

"""

from copy import deepcopy
import re
import time

def read_data():
	data_file = open('input.txt','r')
	#data_file = open('test_input.txt','r')
	#data_file = open('test_input2.txt','r') # for testing part 2's infinite recursion rule
	players = [[int(card) for card in deck.split('\n') if card != ''] for deck in re.findall('Player [0-9]+:\n([0-9\n]+)', data_file.read().strip())]
	return players

# *** PART 1: Play the small crab in a game of Combat using the two decks you just dealt. What is the winning player's score? ***

# rules:
# for each round,
# have both players throw their top card,
# the player who threw the highest valued card wins
# the winner of the round gets both cards and adds them highest value card on top to the bottom of their deck
# this continues while any player still has cards
# at the end of the game, the score is counted as the sum of the reversed index of the card in the deck multiplied by their value

def Combat(player_deck):

	players = deepcopy(player_deck)

	winner = -1
	while sum([len(deck) != 0 for deck in players]) > 1: # while there are still at least two players playing:
		cards_thrown = [deck.pop(0) for deck in players if len(deck) > 0]
		max_value = max(cards_thrown)
		winner = cards_thrown.index(max_value)
		cards_thrown = [cards_thrown.pop(winner)] + cards_thrown # take out the winning card and place it on top
		players[winner] += cards_thrown

	score = sum([(len(players[winner])-ind) * val for ind, val in enumerate(players[winner])])
	return winner, score

def part1(players):
	print("Part 1: Play the small crab in a game of Combat using the two decks you just dealt. What is the winning player's score? ")
	winner, score = Combat(players)
	print(f'Player {winner} wins with score {score}')

# solution for test_input.txt: 306
# solution for input.txt: 32448

# *** PART 2: Play the small crab in a game of Recursive Combat using the two decks you just dealt. What is the winning player's score? ***

# rules:
# for each round,
# if the current deck configuration has already happened before, player1 wins by default
# else, have both players throw their top card,
# if both players have n cards left >= the value they threw, recurse, and start a new game with their remaining deck
# if this sub-game returns as a win for a player, 
# else, the player who threw the highest valued card wins the round
# the winner of the round gets both cards and adds them highest value card on top to the bottom of their deck
# this continues while any player still has cards
# at the end of the game, the score is counted as the sum of the reversed index of the card in the deck multiplied by their value

def RecursiveCombat(player_deck, depth = -1):

	depth += 1
	players = deepcopy(player_deck)
	configs = []

	winner = -1
	while sum([len(deck) != 0 for deck in players]) > 1: # while there are still at least two players playing:

		if str(players) in configs: # if our current deck configuration already happened before, player 0 wins
			winner = 0
			break

		configs.append(str(players)) 

		cards_thrown = [deck.pop(0) for deck in players if len(deck) > 0]

		if all([len(players[player]) >= card for player,card in enumerate(cards_thrown)]):
			winner, _, depth = RecursiveCombat([deck[:cards_thrown[player]] for player,deck in enumerate(players)], depth)
		else:
			max_value = max(cards_thrown)
			winner = cards_thrown.index(max_value)

		cards_thrown = [cards_thrown.pop(winner)] + cards_thrown # take out the winning card and place it on top
		players[winner] += cards_thrown

	score = sum([(len(players[winner])-ind) * val for ind, val in enumerate(players[winner])])
	return winner, score, depth

def part2(players):
	print("Part 2: Play the small crab in a game of Recursive Combat using the two decks you just dealt. What is the winning player's score?")
	tic = time.perf_counter()
	winner, score, depth = RecursiveCombat(players)
	toc = time.perf_counter()
	print(f'Player {winner} won with score {score} having played recursive combat to a depth of {depth} which took {toc - tic}s')

# solution for test_input.txt: 291
# solution for input.txt: 32949

def main():
	players = read_data()
	part1(players)
	part2(players)

if __name__ == '__main__':
	main()

"""

Reflection:

- Fun! 
- Used the f-string and enumerate this time. Useful!
- Only mistake: when recursing, I forgot to cut down the players' decks to the amount of cards shown on their previously thrown card
- This caused a (seemingly) infinite loop

"""
