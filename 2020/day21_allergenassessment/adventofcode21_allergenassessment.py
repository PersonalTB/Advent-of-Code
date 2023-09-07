"""
*** *** ADVENT OF CODE - DAY 21 - Allergen Assessment *** ***

Src: https://adventofcode.com/2020/day/21
Setting: we're at a (foreign) restaurant, and we don't understand the language, but the allergens ARE listed in english, though incomplete
Challenge: find out which ingredients are associated with which allergens

Input: input.txt, a .txt file containing a list of foods, one per line, with its ingredients separated by spaces followed by some or all allergens 
format: ingredient0 ... ingredientn (contains allergen0 ... allergenn)

e.g.

mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)

Each allergen is found in exactly one ingredient. 
Each ingredient contains zero or one allergen. 
Allergens aren't always marked 
When they're listed, the ingredient that contains the listed allergen will be somewhere in the corresponding ingredients list
However, even if an allergen isn't listed, the ingredient that contains that allergen could still be present: maybe they forgot to label it

In the above example: none of the ingredients kfcds, nhms, sbzzf, or trh can contain an allergen. 
Counting the number of times any of these ingredients appear in any ingredients list produces 5 (sbzzf occurs twice)

Now, you can derive the dangerous ingredients. In the above example:

mxmxvkd contains dairy.
sqjhc contains fish.
fvjkl contains soy.

Arrange the ingredients alphabetically by their allergen and separate them by commas to produce your canonical dangerous ingredient list.
For the above example this is: mxmxvkd,sqjhc,fvjkl.

The challenge consists of two parts:
Part 1: Find which ingredients do NOT contain any of the allergens in your list. How many times do any of those ingredients appear?
Part 2: Having derived which ingredients contain which allergens, what is your canonical dangerous ingredient list?

"""

from collections import defaultdict
import networkx as nx
from matplotlib import pyplot as plt
import re 

data_file = open('input.txt','r')
#data_file = open('test_input.txt','r')
data = data_file.read().strip()

dishes = [(f.strip().split(' '), a.strip().split(', ')) for f,a in re.findall('([a-zA-Z ]+)\(contains ([a-zA-Z, ]+)\)', data)]
all_ingredients = set([item for f,a in dishes for item in f])
all_allergens = set([item for f,a in dishes for item in a])

# *** PART 1: Find which ingredients do NOT contain any of the allergens in your list. How many times do any of those ingredients appear? ***

print("Part 1: Find which ingredients do NOT contain any of the allergens in your list. How many times do any of those ingredients appear?")

# for each food, store its ingredients as being **potential** allergens, for all its associated allergens 
allergen_dict = defaultdict(list) 
for ingredients, allergens in dishes:
	for allergen in allergens:
		allergen_dict[allergen].append(set(ingredients))

# now, in order to find the potential allergenic ingredients per allergen, we can find the INTERSECTION over the lists per allergen
# i.e. the ingredients that are COMMON between the dishes, which might contain the associated allergen
# https://en.wikipedia.org/wiki/Intersection_(set_theory)
all_potential_allergens = []
for allergen in allergen_dict:
  potential_ingredients_for_allergen = set.intersection(*allergen_dict[allergen]) # find common ingredients between the dishes
  all_potential_allergens.append(potential_ingredients_for_allergen)
  allergen_dict[allergen] = list(potential_ingredients_for_allergen) # update the potential allergen list for this allergen

# all potential allergens are those ingredients which occur in any list of potential ingredients over all allergens
# i.e. the UNION between the sets of all potential allergens of all allergens
# https://en.wikipedia.org/wiki/Union_(set_theory)
all_potential_allergens = set.union(*all_potential_allergens)

# non-allergens are those foods which do not occur in the potential allergen set 
# i.e. the DIFFERENCE between the set of all foods, and those foods which we think are potential allergens
# https://en.wikipedia.org/wiki/Complement_(set_theory)
non_allergens = set.difference(all_ingredients, all_potential_allergens)

# for every menu-item, check which ingredients are in the non-allergen set
non_allergens_on_the_menu = [ingredient for ingredients,allergens in dishes for ingredient in ingredients if ingredient in non_allergens]

print(len(non_allergens_on_the_menu))

# solution for test_input.txt: 5
# solution for input.txt: 2786

# *** Part 2: Having derived which ingredients contain which allergens, what is your canonical dangerous ingredient list? ***

print("Part 2: Having derived which ingredients contain which allergens, what is your canonical dangerous ingredient list?")

"""
Matching two distinct sets with each other based on their connections is a bipartite graph matching problem.
Considering each allergen can be connected with only one ingredient, and we have removed all non-allergenic ingredients from the set,
we need to connect the nodes on the 'top' side (i.e. the ingredients), 1:1 with the nodes on the 'bottom' side
This is called a maximum matching problem, and can be solved with the Hopcroft-Karp matching algorithm.
see also: https://en.wikipedia.org/wiki/Matching_(graph_theory)#Maximal_matchings
see also: https://en.wikipedia.org/wiki/Hopcroft%E2%80%93Karp_algorithm
see also: https://towardsdatascience.com/matching-of-bipartite-graphs-using-networkx-6d355b164567 (note: open in private mode!)
"""

g = nx.Graph()
top = all_potential_allergens # top side = what we are going to match from, i.e. the foods
bottom = all_allergens # bottom side = what we need to match to, which are the allergens

g.add_nodes_from(top, bipartite=0) # make the graph bipartite, i.e. vertices on each 'side' can only be connected to those on the 'other side'
g.add_nodes_from(bottom, bipartite=1)

for allergen, ingredients in allergen_dict.items():
	for ingredient in ingredients:
		g.add_edge(ingredient,allergen)

#nx.draw(g); plt.show()

match = nx.bipartite.matching.hopcroft_karp_matching(g, top) 
#print(match)

# to get the canonical allergen ingredients list: 
# sort the allergens alphabetically, then join their ingredients with comma's in matching order
sorted_allergens = sorted(list(all_allergens))
associated_ingredients = [match[allergen] for allergen in sorted_allergens if allergen in match]
canonical_allergen_ingredient_list = ','.join(ingredient for ingredient in associated_ingredients)

print(canonical_allergen_ingredient_list) 

# solution for test_input.txt: mxmxvkd,sqjhc,fvjkl.
# solution for input.txt: prxmdlz,ncjv,knprxg,lxjtns,vzzz,clg,cxfz,qdfpq

"""

Reflection:

- Took me a while to "get" part 1, as I had already started working on the allergen-matching piece in part 2
- I recognized that it was a bipartite graph maximum matching problem as in day16
- It didn't seem to work then because I hadn't filtered out/eliminated the non-allergenic ingredients yet.
- After I learnt we can filter out the non-allergenic ingredients through set operations it became easier.
- At that point, I only had to figure out which operations I had to apply to filter them.
- Lessons learnt: be mindful and think in terms of sets and set operations!
- Take-away: don't start working on the more difficult problems (matching problem) when you can still simplify it (eliminate the non-allergenics)

"""
