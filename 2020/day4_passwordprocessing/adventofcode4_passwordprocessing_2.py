import re, pandas

pp_data = open('input.txt', 'r').read() # read the input data from the text file
pp_df = pandas.DataFrame([dict(re.findall('([\w]+):([#\w]+)[ \n]?', pp_str)) for pp_str in pp_data.split("\n\n")]) # split into a list of individual passports, use regex to find their key-value pairs, make these into a dict, and load these into a pandas dataframe (where 1 row = 1 passport)
pp_df[['byr','iyr','eyr']] = pp_df[['byr','iyr','eyr']].apply(pandas.to_numeric, errors='coerce') # cast year-fields to number format
pp_df = pp_df.drop(columns = ['cid']) # drop the optional column, we're not using it in either part of the puzzle

print('Solution to part 1:', sum(pp_df.notnull().values.all(axis=1))) # find ROWS where all its values are NOT NULL, count these 

pp_df_valid = pandas.DataFrame() # to keep track of the validity of passport fields as specified in their ruleset
pp_df_valid['byr'] = pp_df['byr'].between(1920, 2002, inclusive = True) # are the year fields between their min/max values
pp_df_valid['iyr'] = pp_df['iyr'].between(2010, 2020, inclusive = True) # are the year fields between their min/max values
pp_df_valid['eyr'] = pp_df['eyr'].between(2020, 2030, inclusive = True) # are the year fields between their min/max values
pp_df_valid['hgt'] = pp_df['hgt'].notnull() & pp_df.loc[pp_df['hgt'].notnull(),'hgt'].apply(lambda x: 59 <= int(re.search('([0-9]+)(?=in)',x).group(1) if 'in' in x else -99) <= 76 or 150 <= int(re.search('([0-9]+)(?=cm)',x).group(1) if 'cm' in x else -99) <= 193 ) # if it is either a "cm" or "in" value, and the value is in between their respective min/max values
pp_df_valid['hcl'] = pp_df['hcl'].notnull() & pp_df.loc[pp_df['hcl'].notnull(),'hcl'].apply(lambda x: re.search('^#(?:[0-9a-fA-F]{1,2}){3}$', x) is not None ) # if the regex finds a match to a hexadecimal color pattern
pp_df_valid['ecl'] = pp_df['ecl'].notnull() & pp_df['ecl'].apply(lambda x: x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']) # if the value is in a given set of valid values
pp_df_valid['pid'] = pp_df['pid'].notnull() & pp_df['pid'].apply(lambda x: len(str(x)) == 9 and x.isnumeric()) # if the value is a numeric string of length 9

print('Solution to part 2:', sum(pp_df_valid.values.all(axis=1))) # find ROWS where ALL its validity checks evaluated to TRUE, count these