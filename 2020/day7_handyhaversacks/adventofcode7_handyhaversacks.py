"""
*** *** ADVENT OF CODE - DAY 7 - HANDY HAVERSACKS

Src: https://adventofcode.com/2020/day/7
Setting: there are issues in luggage processing! Regulations changed, specifying that bags must be color-coded and must contain specific other colored bags
Challenge: find out which bags are necessary for your bag: a shiny gold bag

Input: input.txt, a .txt file containing the ruleset for which bag can contain which other bag(s)
e.g.
mirrored silver bags contain 4 wavy gray bags.
clear tan bags contain 5 bright purple bags, 1 pale black bag, 5 muted lime bags.
dim crimson bags contain 5 vibrant salmon bags, 2 clear cyan bags, 2 striped lime bags, 5 vibrant violet bags.
mirrored beige bags contain 4 pale gold bags, 1 pale aqua bag.
pale maroon bags contain 2 dotted orange bags.
dim tan bags contain no other bags.
(etc.)

The challenge consists of two parts:
Part 1: Find out how many bag colors can eventually contain at least one shiny gold bag?
Part 2: Find out how many bags we'll have in total if we have one shiny gold bag

"""

import re, pprint

data_file = open('input.txt','r')
#data_file = open('test_input.txt','r')
#data_file = open('test_input2.txt','r')

bag_data = data_file.read().strip().split('\n')

# for ease of lookup: create a dict containing which bags are inside which, and a dict to keep track of the amount of those
bags_dict = dict()
amounts_dict = dict()

for bd in bag_data:
	bd = bd.replace(' no ', ' 0 ')
	first_str, rest_str = bd.split('contain')
	first = re.search('[, ]?([a-zA-Z ]+) bag[s]?[.]?', first_str.strip()).group(1)
	rest = re.findall('[, ]?([a-zA-Z ]+) bag[s]?[.]?', rest_str.strip())
	numbers = re.findall('([0-9]+)', bd.strip())
	bags_dict[first] = rest
	amounts_dict[first] = numbers

pp = pprint.PrettyPrinter()
pp.pprint(bags_dict)
pp.pprint(amounts_dict)

# *** PART 1 - How many bag colors can eventually contain at least one shiny gold bag?***

print("Part 1: How many bag colors can eventually contain at least one shiny gold bag?")

def check_bags(bag_type, bags_dict):

	bags_which_can_hold_type = []

	for key in bags_dict:
		if bag_type in bags_dict[key]:
			if key not in bags_which_can_hold_type: bags_which_can_hold_type.append(key)
			bags_which_can_hold_type.extend([el for el in check_bags(key, bags_dict) if el not in bags_which_can_hold_type])

	return bags_which_can_hold_type

bags_which_can_hold_gold = check_bags('shiny gold', bags_dict)

print(bags_which_can_hold_gold)

print(len(bags_which_can_hold_gold))

# solution for test_input.txt: 4
# solution: 259

# *** PART 2 - Find out how many bags we'll have in total if we have one shiny gold bag ***

print("\nPart 2: ")

def count_bags(bag_type, bags_dict, amounts_dict):

	n_bags = 0

	if bag_type in bags_dict and bag_type in amounts_dict:

		for bag_ind in range(len(bags_dict[bag_type])):

			next_bag = bags_dict[bag_type][bag_ind]

			n_bags += int(amounts_dict[bag_type][bag_ind]) # how many bags are in the bag we're considering now?
			n_bags += int(amounts_dict[bag_type][bag_ind]) * count_bags(next_bag, bags_dict, amounts_dict) # how many bags are inside ALL OF THOSE?

	return n_bags

print(count_bags('shiny gold', bags_dict, amounts_dict))

# solution for test_input2.txt: 126
# solution: 45018

"""

REFLECTION:

- There's probably a way better option of doing this, but it works
- got confused by the bag counting part: forgot to also count the bags we're currently considering

"""