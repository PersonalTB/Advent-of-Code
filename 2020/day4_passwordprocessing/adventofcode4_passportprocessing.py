"""
*** *** ADVENT OF CODE - DAY 4 - PASSPORT PROCESSING *** ***

Src: https://adventofcode.com/2020/day/4
Setting: we need to scan passports for validity.
Challenge: from passport data (input), determine which are valid

Input: input.txt, a .txt file with passport information. 
Each passport is separated with 2 newlines
Each passport is represented with its data separated by space or a single newline 
Each passpot field is represented as a key:value pair

Example:

ecl:#eef340 eyr:2023 hcl:#c0946f pid:244684338 iyr:2020 cid:57 byr:1969 hgt:152cm

pid:303807545 cid:213 ecl:gry hcl:#fffffd
eyr:2038 byr:1951
hgt:171cm iyr:2011

(etc.)

The challenge is made up of 2 parts:
Part 1 - In your batch file, how many passports are valid? - determine if all fields are present on a passport
Part 2 - determine if all fields are present and valid as per a given ruleset

"""

# imports for: 
# regex (to match patterns), 
# and pandas (to create dataframes and evaluate the validity checks over columns)
import re
import pandas as pd

# load input data into dataframe

# read the input 
inp_file = open('input.txt', 'r')
inp_data = inp_file.read()

# split the passport data into separate lists so we can evaluate them separately (split on double newlines \n\n)
inp_data_split = inp_data.split("\n\n")

# read the passports into a dataframe
# 1. for each passport, split into a list of key-value tuples based on a regex of the form "{key}:{value}", with tuples separated by \n or whitespace
# 2. load this list of key-value tuples into a dictionary
# 3. make the list of dictionaries into one single dataframe
passports = [dict(re.findall('([\w]+):([#\w]+)[ \n]?', p)) for p in inp_data_split] 
pp_df = pd.DataFrame(passports)

# *** PART 1 - In your batch file, how many passports are valid? - check if all required fields are present ***

print("Part 1: In your batch file, how many passports are valid? - check if all required fields are present")

# specify which columns to check
optional_columns = ['cid']
check_columns = [el for el in pp_df.columns if el not in optional_columns] 

# calculate which passports are valid, 
# i.e. for each row, check whether ALL its columns are filled with some value (check across the row's columns, so axis = 1)
pp_df_valid = pp_df[check_columns].notnull().values.all(axis=1)

# show how many of them are true (since bool value True = 1, we can sum them to obtain the total number of Trues / valid passports in the set)
print(sum(pp_df_valid))

# solution: 206

# *** PART 2 - In your batch file, how many passports are valid? - check if fields are present and valid as per the requirements ***

"""
The given requirements / validity checks for the passport fields:

    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.

"""

print('\nPart 2: In your batch file, how many passports are valid? - check if fields are present and valid as per the requirements')

# cast years to numeric format to easily make them comparable with numbers, and coerce errors (so that NaNs stay NaNs)
pp_df['byr'] = pp_df['byr'].apply(pd.to_numeric, errors='coerce')
pp_df['iyr'] = pp_df['iyr'].apply(pd.to_numeric, errors='coerce')
pp_df['eyr'] = pp_df['eyr'].apply(pd.to_numeric, errors='coerce')

# create dataframe to keep track of the validity of our original data set
pp_df_valid = pd.DataFrame()

# now check each column of the data with its requirements:
# for all year fields: check if they are between the given min and max values; if they happen to be NaNs, the 'between'-function returns a False
# check if height is not null, and the height is between the given values based on whether they are in cm or in
# check if the hair color is not null, and if it is matches the format of #(followed by 6 numbers or a-f) using regex
# check if eye color is not null, and if it is in the list of acceptable values
# check if the passport id is not null, and if it is a numeric string that is 9 digits long
# check if the country id is not null (will be ignored later)

pp_df_valid['byr'] = pp_df['byr'].between(1920, 2002, inclusive = True)
pp_df_valid['iyr'] = pp_df['iyr'].between(2010, 2020, inclusive = True)
pp_df_valid['eyr'] = pp_df['eyr'].between(2020, 2030, inclusive = True)
pp_df_valid['hgt'] = pp_df['hgt'].notnull() & pp_df.loc[pp_df['hgt'].notnull(),'hgt'].apply(lambda x: True if ('cm' in x and 150 <= int(x.replace('cm','')) <= 193) or ('in' in x and 59 <= int(x.replace('in','')) <= 76) else False)
pp_df_valid['hcl'] = pp_df['hcl'].notnull() & pp_df.loc[pp_df['hcl'].notnull(),'hcl'].apply(lambda x: re.search('#[0-9a-f]{6}', x) is not None )
pp_df_valid['ecl'] = pp_df['ecl'].notnull() & pp_df['ecl'].apply(lambda x: True if x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'] else False)
pp_df_valid['pid'] = pp_df['pid'].notnull() & pp_df['pid'].apply(lambda x: True if len(str(x)) == 9 and x.isnumeric() else False)
pp_df_valid['cid'] = pp_df['cid'].notnull()

# specify which columns to check
optional_columns = ['cid']
check_columns = [el for el in pp_df_valid.columns if el not in optional_columns]

# calculate which passports are valid, 
# i.e. in the validity df, for each row, check whether all its values evaluated to true (across the row's columns, so axis = 1)
valids = pp_df_valid[check_columns].values.all(axis=1)

# show how many of them are true (since bool value True = 1, we can sum them to obtain the total number of Trues / valid passports in the set)
print(sum(valids))

# solution: 123

"""
Reflection:

- took a long time to wrangle the data into the dictionaries and the eventual dataframe
- took some time to discover the necessary pandas dataframe functions (between, to_numeric, notnull, isnull) and the indexing (loc)
- am content with the pythonic/idiomatic way I chose to program some checks and the final validity check, chaining functions and using lambda
- used to manually separate key-value pairs, construct a dictionary-format string from these, and use ast.literal_eval to make strings into dicts
- wasn't super content that I had to use ast.literal_eval instead of just making dictionaries directly, so I fixed this by using regexes
- made a smaller version, <20 lines, just to see how much I could push it; see adventofcode4_passwordprocessing_2.py

"""
