"""
*** *** ADVENT OF CODE - DAY 6 - CUSTOM CUSTOMS *** ***

Src: https://adventofcode.com/2020/day/6
Setting: we are at customs, and need to fill out forms. we have 26 'yes/no' questions labelled a-z. We need to answer it PER GROUP (e.g. per family)
Challenge: people misunderstand the form, and fill them out individually; you are asked to help compile the "per group" answers from the individual ones

Input: input.txt, a .txt file with a listing of the answers to the questions, 
Each 'yes' answer is encoded as the letter of said question. Each 'no' answer is NOT listed. e.g. "abf" means 'yes' to questions a, b, f, 'no' to the rest
Where each group is separated by one blank line (i.e. TWO newlines), and within groups, individual answers are encoded per line (separated by ONE newline)

e.g.

cady
ipldcyf
xybgcd
gcdy
dygbc

rwhvugmspoyzfbnlcxqtdj
avqdpntxrclufbjswgzh
qbvwgzpfsrjtdxnculh
jhrpclwdxgqibfsntzuv

(etc.)

The challenge consists of 2 parts.
Part 1 - For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?
Part 2 - For each group, count the number of questions to which everyone answered "yes". What is the sum of those counts?

"""

data_file = open('input.txt', 'r')
data = data_file.read()
data_per_group = data.split('\n\n') # separate each group into their own sublist

""" *** PART 1 - For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts? ***

Example:
abc
ab
bc

bc
bcd
e

d

3 groups; 
WITHIN the 1st group, there was overlap in the 'yes' answers, but in aggregate, only 3 unique 'yes' ansers, 
in 2nd group 4 uniques, 
in group 1, 1 unique
in total, across the groups: 3 + 4 + 1 = 8 'yes' answers
"""

print('PART 1: For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?')

n_per_group = [len(set(d.replace('\n',''))) for d in data_per_group] # how many unique answers are there per group?

print(sum(n_per_group)) # sum the trues (1s) to get the total count of positive answers across groups

# solution: 6291

""" *** PART 2 - For each group, count the number of questions to which everyone answered "yes". What is the sum of those counts? ***

Example:
abc
ab
bc

bc
bcd
e

d

3 groups; 
WITHIN the 1st group, there was overlap in the 'yes' answers, but in aggregate, only 1 'yes' anser every one had ('b'), 
in 2nd group 0, 
in group 1, 1 
in total, across the groups: 1 + 0 + 1 = 2 'yes' answers
"""

print('\nPART 2: For each group, count the number of questions to which everyone answered "yes". What is the sum of those counts?')

sum_n_per_group = 0

for group in data_per_group:

	group = group.strip() # strip all trialing newlines
	n_persons = group.count('\n') + 1 # each person is separated by a newline, so just count the newlines and add the first person
	set_of_answers = set(group.replace('\n','')) # find the complete set of all answers (without the newlines)
	counts = [group.count(answer) for answer in set_of_answers] # count how many times the unique answers in the set occurred in the group
	co_occurring_answers = [count == n_persons for count in counts] # list whether we find that the entire group answered a question positively
	n_co_occurring_answers = sum(co_occurring_answers) # since True == 1, we can sum how many times we found a co-occurring answer for the entire group
	
	sum_n_per_group += n_co_occurring_answers # add the count of co-occurring answers for this group to the grand total across group

	#print(group, n_persons, set_of_answers, counts, co_occurring_answers, n_co_occurring_answers, sum_n_per_group)

print(sum_n_per_group)

# solution: 3052

"""

Reflection:

- not super difficult this time
- just a lot of for-loops, so we can also do this in humongous list comprehensions... 
- so, adventofcode62.py is my two-line re-write of this script

"""
