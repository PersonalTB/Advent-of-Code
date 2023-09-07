"""
*** *** ADVENT OF CODE - DAY 2 - PASSWORD PHILOSOPHY *** ***

Src: https://adventofcode.com/2020/day/2
Setting: The password policy has changed for our company.
Challenge: We need to find out which passwords in our database (the input) are valid

Input: input.txt, a .txt file with entries from our password database in which each line has the policy and the password.
These are given as a "{policy}: {password}" tuple, with the policy having a format of "n0-n1 character"

E.g.:
6-7 z: dqzzzjbzz
13-16 j: jjjvjmjjkjjjjjjj
5-6 m: mmbmmlvmbmmgmmf
(etc.)

The challenge consists of 2 parts: 
Part 1 has the password policy mean that the character in the policy can only occur n times, where n must be BETWEEN n0 and n1, 
Part 2 has its password policy mean that the character in the policy MUST occur EITHER at position n0, OR position n1.

"""

# import regex
import re

# read data into list
# data format: each line of the data contains a "{policy}: {password}" tuple
# so we split by newline so each new policy: password tuple becomes its own element
inp_file = open('input.txt', 'r')
data = inp_file.read()
data = data.split('\n')

# *** PART 1 - How many passwords are valid according to their policies? - policy: password has to have a symbol min-to-max amount of times ***

# policy is of the format: n0-n1 s
# where s is the letter that has to appear in the password
# where n0-n1 indicates the least/most amount of times that letter may appear
# e.g. 1-3 a: aablkdsjowieur the password  is valid (a appears between 1 and 3 times)
# e.g. 1-3 a: weioroiuweoriuwoi is invalid (too few a)
# e.g. 1-3 a: aaaaaaaa is invalid (too many a)

print("PART 1: How many passwords are valid according to their policies? - policy: password has to have a symbol min-to-max amount of times")

valids = [] 

# iterate policy-password-tuples
for pw_set in data:

	# create regex to catch the policy and password elements
	# regex is of the form: n0-n1 s: pw
	# n0 - group 1: the index of the first possible occurrence of the policy-mandated symbol, is an integer with 1 or more digits, so: ([0-9]+)
	# n1 - group 2: the index of the second possible occurrence of the policy-mandated symbol, is an integer with 1 or more digits, so: ([0-9]+)
	# s - group 3: the string that we are looking for as per the policy, is one single lowercase letter, so: ([a-z])
	# pw - group 4: the password, can consist of one or more lowercase letters, so: ([a-z]+)
	pw_set_re = re.compile(r'([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)')

	if match := pw_set_re.match(pw_set):

		policy_low = match.group(1)
		policy_high = match.group(2)
		policy_s = match.group(3)
		pw = match.group(4)

		# count all occurrences of our policy string in the password
		cnt = len(re.findall(policy_s, pw))

		# is the password according to policy?
		valid = cnt >= int(policy_low) and cnt <= int(policy_high)

		#print('pw: {0} - policy_s: {1} - policy_low: {2} - policy_high: {3} - count: {4} - valid: {5}'.format(pw, policy_s, policy_low, policy_high, cnt, valid))

		# if valid, add to valids list
		if valid:
			valids.append(pw)


# how many pw are valid?
print(len(valids))

# solution: 542


# *** PART 2 - How many passwords are valid according to their new policy? - policy: password has to have a symbol in two specific locations ***

# policy is of the format: n0-n1 s
# where s is the letter that has to appear in the password
# where n0-n1 indicates the first OR second location that a letter must be, at one-index (so: 1 indicates the first position in the str, or index 0)
# e.g. for 1-3 a the password aablkdsjowieur is valid (a appears at the 1st element)
# e.g. for 1-3 a the password naablkdsjowieur is valid (a appears at the 3rd element)
# e.g. for 1-3 a the password nanblkdsjowieur is NOT valid (a appears at NEITHER position)
# e.g. for 1-3 a the password aaablkdsjowieur is NOT valid (a appears at BOTH positions, must be XOR)

print("\nPART 2: How many passwords are valid according to their policies? - policy: password has to have a symbol in two specific locations")

valids = [] 

# iterate policy-password-tuples
for pw_set in data:

	# create regex to catch the policy and password elements
	# regex is of the form: n0-n1 s: pw
	# n0 - group 1: the index of the first possible occurrence of the policy-mandated symbol, is an integer with 1 or more digits, so: ([0-9]+)
	# n1 - group 2: the index of the second possible occurrence of the policy-mandated symbol, is an integer with 1 or more digits, so: ([0-9]+)
	# s - group 3: the string that we are looking for as per the policy, is one single lowercase letter, so: ([a-z])
	# pw - group 4: the password, can consist of one or more lowercase letters, so: ([a-z]+)
	pw_set_re = re.compile(r'([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)')

	if match := pw_set_re.match(pw_set):

		policy_first = int(match.group(1))-1
		policy_second = int(match.group(2))-1
		policy_s = match.group(3)
		pw = match.group(4)

		# the policy-mandated symbol must be EITHER in location 1 OR location 2, NOT BOTH, NOR IN NEITHER
		valid_1 = policy_first >= 0 and policy_first < len(pw) and pw[policy_first] == policy_s 
		valid_2 = policy_second >= 0 and policy_second < len(pw) and pw[policy_second] == policy_s
		valid = valid_1 ^ valid_2 # ^ is xor

		#print('pw: {0} - policy_s: {1} - policy_first: {2} - policy_second: {3} - valid: {4}'.format(pw, policy_s, policy_first, policy_second, valid))

		# if valid, add to valids list
		if valid:
			valids.append(pw)


# how many pw are valid?
print(len(valids))

# solution: 360

"""

Reflection:

- this one was pretty nice
- discovered what the xor operator is in python
- discovered the walrus operator := 

"""
