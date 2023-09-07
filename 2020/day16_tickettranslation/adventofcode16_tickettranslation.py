"""
*** *** ADVENT OF CODE - DAY 16 - TICKET TRANSLATION *** ***

Src: https://adventofcode.com/2020/day/16
Setting: we need to board a train, but we can't read what the fields on our tickets mean, but we CAN read the values
Challenge: from the values, those on surrounding tickets, and the 'rules' that the fields' values follow, derive which values are what fields

Input: input.txt, a .txt file containing the rules, the values on our ticket, and the values on surrounding tickets

e.g.

class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12

In this example, the values 4, 55, and 12 are are not valid for any field. 
Adding together all of the invalid values produces your ticket scanning error rate: 4 + 55 + 12 = 71.

The challenge consists of 2 parts:
Part 1: What is your ticket scanning error rate?
Part 2: Derive the fields from the valid tickets, then multiply the values on your ticket of the fields that start with "departure" 

"""

from functools import reduce
import matplotlib.pyplot as plt 
import networkx as nx
import operator 
import pandas as pd
import re # useful: https://regexr.com/

data_file = open('input.txt','r')
#data_file = open('test_input.txt','r') # for testing part 1
#data_file = open('test_input2.txt','r') # for testing part 2
data = data_file.read().strip()

rules = re.search('([\w:\- \n]+)your ticket:',data).group(1).strip().split('\n') # rules come before the 'your ticket' section
rule_names = [(re.search('([\w ]+):[ \w]+', d).group(1)) for d in rules] # separate the name and ranges based on the format "name: r0-r1 or r2-r3"
rule_ranges = [(re.findall('([0-9]+)-([0-9]+)', d)) for d in rules] # for each rule, create a list containing tuples of valid value ranges

your_ticket = [int(d) for d in re.search('your ticket:\n([0-9,]+)', data).group(1).strip().split(',')]
your_ticket_df = pd.DataFrame(your_ticket)

nearby_tickets = [[int(d) for d in r.strip().split(',')] for r in re.search('nearby tickets:\n([0-9,\n]+)',data).group(1).strip().split('\n')]
nearby_tickets_df = pd.DataFrame(nearby_tickets)

# *** PART 1: What is your ticket scanning error rate? ***

print('Part 1: What is your ticket scanning error rate?')

def is_valid_according_to_rule(x,r): return any([int(a) <= x <= int(b) for (a,b) in r]) # cell follows a rule if it is in any of its valid ranges
def is_valid(x): return any([is_valid_according_to_rule(x, rule_range) for rule_range in rule_ranges]) # cell is valid if any rule is followed

invalid_fields_df = ~nearby_tickets_df.applymap(lambda x: is_valid(x)) # find cells where not one rule applies, i.e the inverse of the valid cells

print(int(nearby_tickets_df.where(invalid_fields_df).sum().sum())) # print the sum of the values in these invalid cells

# solution for test_input.txt: 71
# solution for input.txt: 20060

# *** PART 2: Derive the fields from the valid tickets, then multiply the values on your ticket of the fields that start with "departure"***

print('Part 2: Derive the fields from the valid tickets, then multiply the values on your ticket of the fields that start with "departure"')

invalid_tickets = nearby_tickets_df.index[invalid_fields_df.any(axis=1)] # invalid tickets are all *rows* where any one field is invalid
nearby_tickets_df = nearby_tickets_df.drop(invalid_tickets, axis = 0) # only keep the valid tickets

# find out which fields are **potentially** valid fields for which columns (iterate over columns, check which columns satisfy which rulesets)

# this function is the same as is_valid_according_to_rule, but now it works over entire dataframe column series
# i.e. it checks if the column is between the values for each range in the ruleset
# after that, it takes the bitwise-or over the individual range-checks (i.e. checks if each rows evaluated to true for ANY ONE of the checks)
# after that, it checks if the entire column evaluated true
# if so, the entire column corresponds to a ruleset
def series_is_according_to_rule(x,r): return reduce(lambda x, y: x | y, [x.between(int(a),int(b)) for (a,b) in r]).all()

# for each column in the dataframe, check which of the rulesets it corresponds to
valid_df = nearby_tickets_df.apply(lambda x: [i for i in range(len(rules)) if series_is_according_to_rule(x, rule_ranges[i])])

# because some columns can be valid for several rulesets (1:N), we need to prune them down and find the 1:1 matches between columns and rulesets
# you can view this as a maximal matching problem over a graph,
# the columns are the nodes on the left side
# these are connected to the rulesets/field names on the right side
# i.e. for each 'potential match' between column and field/rule name, there is an edge in the graph
# now, find a situation where there can be only ONE match/edge between each pair of left/right nodes in the graph (i.e. maximal matching problem)
# to solve this, we will use the networkx python package, and the hopcroft_karp_matching algorithm for finding the maximal matching
# see also: https://en.wikipedia.org/wiki/Matching_(graph_theory)#Maximal_matchings
# see also: https://en.wikipedia.org/wiki/Hopcroft%E2%80%93Karp_algorithm
# see also: https://towardsdatascience.com/matching-of-bipartite-graphs-using-networkx-6d355b164567 (note: open in private mode!)

g = nx.Graph()
top = list(range(len(valid_df))) # top side = what we are going to match from, i.e. the column values
bottom = rule_names # bottom side = what we need to match to, which are the rule names

g.add_nodes_from(bottom, bipartite=0) # make the graph bipartite, i.e. vertices on each 'side' can only be connected to those on the 'other side'
g.add_nodes_from(top, bipartite=1)

for field, values in valid_df.iteritems(): # make an edge for each *potential match* we found by checking which rulesets are valid per column
	for name in values:
		g.add_edge(rule_names[name], field)

#nx.draw(g); plt.show()

match = nx.bipartite.matching.hopcroft_karp_matching(g, top) # find Maximal Matching (i.e. the graph where each node is connected by only 1 edge)

#nx.draw(match); plt.show() # show the graph object visually

#print(match) # check: for test_input2.txt, this must be: 0 = row, 1 = class, 3 = seat

departure_values = [your_ticket_df.iloc[match[m]][0] for m in match if type(m) is str and 'departure' in m] # find all values for departure fields
print(reduce(operator.mul, [1] + departure_values)) # apply multiplication to these, and start off with a 1 as a base multiplier

# solution for input.txt: 2843534243843

"""

Reflection:

- wrestled a lot with pandas this time, on checking the columns
- also wrestled with the bipartite maximal matching problem until I figured out the mathematical problem discription, 
- then, the tool networkx popped up and it was quite easy to solve 

"""
