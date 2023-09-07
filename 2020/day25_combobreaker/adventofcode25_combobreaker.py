"""
*** *** ADVENT OF CODE - DAY 25 - COMBO BREAKER *** ***

Src: https://adventofcode.com/2020/day/25
Setting: The RFID chip of your door doesn't work. Unfortunately for our door, we know a bit or two about crypto.
Challenge: We'll need to reverse-engineer the cryptographic handshake and inject our own code to open the door.

Input: input.txt, a .txt file containing the public keys of our door and RFID card.

e.g.

The handshake used by the card and the door involves an operation that transforms a subject number. 
To transform a subject number, start with the value 1. Then, a number of times called the loop size, perform the following steps:

Set the value to itself multiplied by the subject number.
Set the value to the remainder after dividing the value by 20201227.

The card always uses a specific, secret loop size when it transforms a subject number. 
The door always uses a different, secret loop size.

The cryptographic handshake works like this:

The card transforms the subject number of 7 according to the card's secret loop size. The result is called the card's public key.
The door transforms the subject number of 7 according to the door's secret loop size. The result is called the door's public key.
The card and door use the wireless RFID signal to transmit the two public keys (your puzzle input) to the other device. 
Now, the card has the door's public key, and the door has the card's public key. 
Because you can eavesdrop on the signal, you have both public keys, but neither device's loop size.
The card transforms the subject number of the door's public key according to the card's loop size. The result is the encryption key.
The door transforms the subject number of the card's public key according to the door's loop size. The result is this same encryption key.

If you can use the two public keys to determine each device's loop size, 
you will have enough information to calculate the secret encryption key that the card and door use to communicate; 
this would let you send the unlock command directly to the door!

For example, suppose you know that the card's public key is 5764801. 
With a little trial and error, you can work out that the card's loop size must be 8, 
because transforming the initial subject number of 7 with a loop size of 8 produces 5764801.

Then, suppose you know that the door's public key is 17807724. 
By the same process, you can determine that the door's loop size is 11, 
because transforming the initial subject number of 7 with a loop size of 11 produces 17807724.

At this point, you can use either device's loop size with the other device's public key to calculate the encryption key. 
Transforming the subject number of 17807724 (the door's public key) 
with a loop size of 8 (the card's loop size) 
produces the encryption key, 14897079. 

Transforming the subject number of 5764801 (the card's public key) 
with a loop size of 11 (the door's loop size) 
produces the same encryption key: 14897079.

The challenge consists of two parts:
Part 1: Find out what encryption key the handshake is trying to establish?
Part 2: 🌟🌟🌟 FREE BONUS STAR 🌟🌟🌟

"""

def read_data():
	data_file = open('input.txt','r')
	#data_file = open('test_input.txt','r')
	data = data_file.read().strip().split('\n')
	return data

# *** PART 1: Find out what encryption key the handshake is trying to establish?***

def transform(loop_size, subject_number = 7, mod = 20201227):
	value = 1
	for i in range(loop_size): 
		value = (value * subject_number) % mod
	return value

def handshake(public_key_door, public_key_card, loop_size_door, loop_size_card):
	encryption_key_door = transform(subject_number = public_key_card, loop_size = loop_size_door)
	encryption_key_card = transform(subject_number = public_key_door, loop_size = loop_size_card)
	return encryption_key_door == encryption_key_card, encryption_key_door, encryption_key_card

def inv_transform(public_key, subject_number = 7, mod = 20201227, max_loop_size = 1000):
	correct_loop_size = -1
	value = 1
	for correct_loop_size in range(1,max_loop_size): 
		value = (value * subject_number) % mod
		if value == public_key:
			break
	return correct_loop_size

def part1(data):

	print("Part 1: Find out what encryption key the handshake is trying to establish?")

	public_key_door = int(data[0])
	public_key_card = int(data[1])

	loop_size_door = inv_transform(public_key_door, max_loop_size = 100000000000)
	loop_size_card = inv_transform(public_key_card, max_loop_size = 100000000000)

	handshake_correct, encryption_key_door, encryption_key_card = handshake(public_key_door, public_key_card, loop_size_door, loop_size_card)

	print(f'public key door: {public_key_door}, public key card: {public_key_card}, loop size door: {loop_size_door}, loop_size_card: {loop_size_card}, handshake {handshake_correct}, encryption_key_card: {encryption_key_card}, encryption_key_door: {encryption_key_door}')

	if handshake_correct:
		print(f'handshake correct with encryption key: { encryption_key_door }')
	else:
		print('handshake failed')

	# solution for test_input.txt: 14897079
	# solution for input.txt: 12227206

# *** PART 2: 🌟🌟🌟 FREE BONUS STAR 🌟🌟🌟 ***

def part2(data):

	print("Part 2: 🌟🌟🌟 FREE BONUS STAR 🌟🌟🌟")

def main():
	data = read_data()
	part1(data)
	part2(data)

if __name__ == '__main__':
	main()

"""

Reflection:

- A little bit of public-private key encryption to finish off the year, nice!
- The free bonus star was thoughtful, not having me spend any more time on Christmas day ;)

"""
