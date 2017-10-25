'''
lyricsGenerator.py
10/24/17


Driver program for our lyrics generator.

'''

import re


class UserInput:
	'''
	Outputs user input in a dictionary format of part in speech:list of words format
	'''
	def __init__(self):
		self.input = {}
		self.invalid_chars = re.compile("[^a-zA-Z-]")

	# Ensures input has no numbers or grammars
	def isValidInput(self, ls_str):
		for s in ls_str:
			if self.invalid_chars.match(s):
				return False
		return True

	# Initiates user input
	def getInput(self):
		print('''
	Welcome to the NLP Lyrics Generator!
	Generating the next greatest hit since 2017.

	Please enter input according to the following prompts.
	** NOTE: If you do not enter input as exactly specified, you might get some...odd songs! **
			''')

		ls_input_verbs = []
		ls_input_nouns = []

		userInputsVerbs = userInputsNouns = True


		# Main loop to get input
		while True:
			# Get verbs
			while userInputsVerbs:
				input_verbs = input("Enter up to three verbs separated by spaces, or 0 to exit: ")
				input_verbs.strip()
				if input_verbs == '0':
					break
				ls_input_verbs = input_verbs.split(" ")
				
				# More than 3 verbs
				if len(ls_input_verbs) > 3:
					print("Error! More than 3 verbs were entered")
				# No verbs
				elif len(ls_input_verbs) == 0:
					print("No verbs were entered.")
				else:
					if not self.isValidInput(ls_input_verbs):
						print("Invalid character detected in input. Please try again.")
					else:
						userInputsVerbs = False

			# Get nouns
			while userInputsNouns:
				input_nouns = input("Enter up to three nouns separated by spaces, or 0 to exit: ")
				ls_input_nouns = input_nouns.split(" ")
				
				# More than 3 verbs
				if len(ls_input_nouns) > 3:
					print("Error! More than 3 nouns were entered")
				# No verbs
				elif len(ls_input_nouns) == 0:
					print("No verbs were entered.")
				else:
					if not self.isValidInput(ls_input_nouns):
						print("Invalid character detected in input. Please try again.")
					else:
						userInputsNouns = False
			break







def main():
	user_input = UserInput()
	user_input.getInput()

if __name__ == '__main__':
	main()