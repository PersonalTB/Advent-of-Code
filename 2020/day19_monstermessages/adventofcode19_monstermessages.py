"""
*** *** ADVENT OF CODE - DAY 19 - MONSTER MESSAGES *** ***

Src: https://adventofcode.com/2020/day/19
Setting: the elves' intelligence agency captured data of a sea monster, but the data is corrupted
Challenge: find the uncorrupted data

Input: input.txt, a .txt file containing the valid rules of your data, and the data of the sea monster

e.g.

0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb

In the above example, ababbb and abbbab match rule 0 (so the amount of valid messages according to rule 0 is 2)

The challenge consists of two parts:
Part 1: How many messages completely match rule 0?
Part 2: How many messages completely match rule 0 with recursive rules?

"""

import re
import regex

data_file = open('input.txt','r')
#data_file = open('test_input.txt','r') # for testing part 1 (answer: 2)
#data_file = open('test_input2.txt','r') # for testing part 2 (answer: 12)
data = data_file.read().strip()

rules, data = data.split('\n\n') # the rules and the data are separated in the input by 1 blank line (i.e. 2 newlines right after each other)
rules = dict([(idx, [subrule.split(' ') for subrule in rule.split(' | ')]) for idx, rule in re.findall('([0-9]+): ([0-9ab"| ]+)', rules)])
data = data.split('\n') 

# *** PART 1: How many messages completely match rule 0? ***

print("Part 1: How many messages completely match rule 0? ")

def get_regex_for_rule(rule_to_check, rules):

    if '"' in rule_to_check: # if we're at the leaf of the parsing tree and we find a value, just return the leaf-value
        return rule_to_check.replace('"','')
    else: # else, iterate over the subnodes
        return '(' + '|'.join([''.join(get_regex_for_rule(el,rules) for el in subrule) for subrule in rules[rule_to_check]]) + ')'

rule = regex.compile(get_regex_for_rule('0',rules))
print([regex.fullmatch(rule, d) is not None for d in data].count(True)) # only count those lines of data which fully match the rule

# solution for test_input.txt: 2
# solution for input.txt: 205

# *** PART 2: How many messages completely match rule 0 with recursive rules? ***

"""
Part 2 becomes easier when you see that: 
- only two rules need to be changed, as per the hint that you shouldn't make it too difficult (i.e. don't create your own formal language parser)
- and that only **CERTAIN LOOPS** are created

The rules that change are the following

8: 42 | 42 8
11: 42 31 | 42 11 31

In terms of regex: 

8 becomes 42+ (i.e. a series of 1 or more times the number 42)
11 becomes: 42 11? 31 (i.e. a 42, then **possibly** the same rule itself again, then 31)

The recursion in the first case can be done easily by the standard + token in regular regexes,
The second case can be done by using the 3rd party "regex" library (NOT the standard re library) specifying a recursion pattern in the regex
"""

print("Part 2: How many messages completely match rule 0 with recursive rules? ")

def get_recursing_regex_for_rule(rule_to_check, rules):

    if '"' in rule_to_check: # if we're at the leaf of the parsing tree and we find a value, just return this value
        return rule_to_check.replace('"','')
    
    else: # else, iterate over the subnodes

        if rule_to_check == '8': # only change the subrules that need changing to recurse, i.e. change 8 to 42+
            return get_recursing_regex_for_rule("42", rules) + '+'
        elif rule_to_check == '11': # only change the subrules that need changing to recurse, i.e. change 11 to 42 11? 31
            rule42 = get_recursing_regex_for_rule("42", rules)
            rule31 = get_recursing_regex_for_rule("31", rules)
            return f'(?P<recursion>{rule42}(?&recursion)?{rule31})'

        else: # else, iterate over the subnodes as normal
            return '(' + '|'.join([''.join([get_recursing_regex_for_rule(el, rules) for el in subrule]) for subrule in rules[rule_to_check]]) + ')'

rule = regex.compile(get_recursing_regex_for_rule('0',rules))
print([regex.fullmatch(rule, d) is not None for d in data].count(True)) # only count those lines of data which fully match the rule 0

# solution for test_input2.txt: 12
# solution for input.txt: 329

"""

Reflection:

- figured at the start I could make a regex from the rules as it looked like formal grammar, but wasn't quite sure how
- I then started checking the rules recursively "manually" 
- after that, it frustrated me I was just applying the regex checks manually, and tried to find out how I could represent it in regexes anyway
- wasn't that hard in the end, though the regexes can obviously become unwieldily large if the ruleset becomes huge/recursive
- in part 2, for this reason, I switched to the regex module, which supports recursive regexes
- it took a bit of puzzling how to implement loops, until I realized the hints in the challenge 
- i.e. DONT try to recreate full grammar parsing, ONLY change the rules which need to be changed; and carefully look at the specific loops created
- today I also learnt the count function for lists
- I also learnt you can cast function results to bool: if it returns an object, bool = true, else if it is None, bool = false

"""
