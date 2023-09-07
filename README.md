# Advent-of-Code

My solutions to the Advent of Code puzzles.

## 2020

Src: https://adventofcode.com/2020

* **Day 1: Report Repair**: Find the 2- and 3-element combinations from the input that sum to 2020. Used itertools.combinations.
* **Day 2: Password Philosophy**: Find out which passwords in our database (the input) are valid according to a password policy. Used regex.
* **Day 3: Tobbogan Trajectory**: Skiing down a slope (mapped in the input), count how many trees we encounter.
* **Day 4: Passport Processing**: From passport data (input), determine which are valid according to rules. Used regex, and pandas dataframe operations.
* **Day 5: Binary Boarding**: Find the free seat based on which seats are taken (the input), where each seat is coded by binary space partitioning. Used binary string decoding.
* **Day 6: Custom Customs**: Compile a customs forms as per the given rules, based on grouped individual answers (the input). 
* **Day 7: Handy Haversacks**: From rules specifying which bags can hold which other bags, find out which bags can contain, and are contained within your bag: a shiny gold bag. Used a recursive counting function.
* **Day 8: Handheld Halting**: Find the infinite loop in the instructions of the boot code (input), and fix it. Used a simple backtracking search.
* **Day 9: Encoding Error**: Find the weakness in the "XMAS" cypher by finding which element in your encrypted text (input) is not a combination of a preamble section of the message, and finding the contiguous set that sum up to that element's value.
* **Day 10: Adapter Array**: Our charger doesn't work with an outlet. We do have a lot of adapters with various "joltage" transforming capacities (input). Find out how we can connect our laptop to the charging outlet. Used a low-to-high updating strategy, instead of trying to actually generate all possible paths to our goal state. 
* **Day 11: Seating Systems**: From a map of the layout of the ferry (input), apply the Conway's Game of Life-like seating rules people use to find the final, stable situation, both with a neighborhood function, and a line-of-sight-like method of counting. 
* **Day 12: Rain Risk**: With the given action-set our ferry takes (the input), determine our position relative to the starting position, both by using absolute and a relative waypoint-based navigation. 
* **Day 13: Shuttle Search**: We need to get the first bus that arrives according to its schedule (input). Find out how long we need to wait for the first bus arrives, and find out at which time the buses all arrive one minute apart from each other in their order of listing. I used and tried implementing my own Chinese Remainder Theorem solver to solve this. 
* **Day 14: Docking Data**: The port has docking software incompatible with the ferry's due to a bitmask system in its initialization. 
Challenge: emulate the bitmask system to correctly initialize the docking parameters in memory. Used recursion in assigning the "floating" memory addresses.
* **Day 15: Rambunctious Recitation**: We play a memory game, and try to figure out what the nth spoken number will be. Managed to create an efficient  "memorization system" to store only the necessary information. 
* **Day 16: Ticket Translation**: Our tickets are unreadable save for its value fields. From these values, those on surrounding tickets, and the 'rules' that the fields' values follow, derive which values are what fields. Used pandas dataframe methods and bipartite graph maximal matching.
* **Day 17: Conway Cubes**: Create a Conway's Game of Life simulation in 3+ dimensions. Used numpy and convolutions as a neighborhood counting method.
* **Day 18: Operation Order**: Help with maths homework, but evaluate the expressions based on alternative operator precedence order. Used python's Abstract Syntax Tree (ast) library with a very dirty, hacky method of swapping precedence order and operations.
* **Day 19: Monster Messages**: The elves' intelligence agency captured data of a sea monster, but the data is corrupted. Find the un-corrupted data. Dynamically constructed (recursive) regexes.
* **Day 20: Jurassic Jigsaw**: We received a tiled satellite image (input) in a random order and orientation. Re-assemble the image and find the seaslugs in the image. Implemented a depth-first search scramble puzzle solver, and used convolution on the final image to find the slugs.
* **Day 21: Allergen Assessment**: From a list of foreign ingredients and their allergens, derive which ingredients contain which allergens. Used set operations and bipartite graph maximal matching.
* **Day 22: Crab Combat**: From our dealt cards, play a game of "Combat" and "Recursive Combat" against a friendly crab companion, and find the final state and the winner's score. Used recursion.
* **Day 23: Crab Cups**: Play the game of cups with the crab with lots and lots of rounds and cups. Implemented the game state efficiently using a dict containing cups and their neighbours. The pickup/replace operation was done by just switching around neighbor references.
* **Day 24: Lobby Layout**: The lobby has its hexagonal tiles flipped between black and white, from day to day, according to specified rules and tile-finding instructions. Figure out how many tiles are flipped after n days. Used regex to parse the tile-finding instructions, and coded the initial state as a dict. For part 2, I implemented a GOL using convolution as a neighbour-counting method, with a hexagonal convolution kernel.
* **Day 25: Combo Breaker**: The RFID chip of your door doesn't work. Unfortunately for our door, we know a bit or two about crypto. We'll need to reverse-engineer the cryptographic handshake and inject our own code to open the door. 

## Requirements

The code is written in Python 3 and uses numpy, pandas, prettyprint, sympy, matplotlib, networkx, scipy, regex. To install, run: 

`pip install numpy pandas sympy matplotlib networkx scipy regex`

## How to run

To run the code, in terminal or cmd, cd to the folder in which the code is located and run via: 

`python3 [path_to_file]`
