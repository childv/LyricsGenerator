'''
lyricsGenerator.py
10/24/17


Driver program for our lyrics generator.

'''

import re
import sys
import lyricsTemplateHandler as lth


class UserInputHandler:
	'''
	Outputs user input in a dictionary format of part in speech:list of words format
	'''
	def __init__(self):
		self.d_input = None
		self.invalid_chars = re.compile("[^a-zA-Z]")

	# Ensures input has no numbers or grammars
	def isValidInput(self, ls_str):
		for s in ls_str:
			if self.invalid_chars.match(s):
				return False
		return True


	# Initiates user input
	def askForUserInput(self):
		# reset user input
		ls_input_verbs = []
		ls_input_nouns = []
		ls_input_adjectives = []

		userInputsVerbs = userInputsNouns = userInputsAdjectives = True
		self.d_input = {'verbs':[], 'nouns':[], 'adjectives': []} # reset user input


		# Main loop to get input
		while True:
			# Get verbs
			while userInputsVerbs:
				input_verbs = raw_input("Enter up to three verbs separated by spaces, or 0 to exit: ")
				input_verbs.strip()
				# Check if exit
				if input_verbs.strip() == '0':
					sys.exit()
				ls_input_verbs = input_verbs.strip().split(" ")
				
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
						# Add verbs to input dictionary
						self.d_input['verbs'] = ls_input_verbs
						userInputsVerbs = False

			# Get nouns
			while userInputsNouns:
				input_nouns = raw_input("Enter up to three nouns separated by spaces, or 0 to exit: ")
				
				# Check if exit
				if input_nouns.strip() == '0':
					sys.exit()
				ls_input_nouns = input_nouns.strip().split(" ")
				
				# More than 3 verbs
				if len(ls_input_nouns) > 3:
					print("Error! More than 3 nouns were entered")
				# No verbs
				elif len(ls_input_nouns) == 0:
					print("No nouns were entered.")
				else:
					if not self.isValidInput(ls_input_nouns):
						print("Invalid character detected in input. Please try again.")
					else:
						# Add nouns to input dictionary
						self.d_input['nouns'] = ls_input_nouns
						userInputsNouns = False
			
			# Get adjectives
			while userInputsAdjectives:
				input_adjectives = raw_input("Enter up to three adjectives separated by spaces, or 0 to exit: ")
				
				# Check if exit
				if input_adjectives.strip() == '0':
					sys.exit()
				ls_input_adjectives = input_adjectives.strip().split(" ")
				
				# More than 3 verbs
				if len(ls_input_adjectives) > 3:
					print("Error! More than 3 adjectives were entered")
				# No verbs
				elif len(ls_input_adjectives) == 0:
					print("No adjectives were entered.")
				else:
					if not self.isValidInput(ls_input_adjectives):
						print("Invalid character detected in input. Please try again.")
					else:
						# Add adjectives to input dictionary
						self.d_input['adjectives'] = ls_input_adjectives
						userInputsAdjectives = False

			print('\n')
			break;
			

	# Returns dictionary containing user input
	def getUserInput(self):
		if self.d_input is not None:
			return self.d_input

		# Request user input if none
		else:
			self.askForUserInput()
			return self.d_input



# Driver of lyrics generator
def main():
	# Initialize handlers

	input_handler = UserInputHandler()
	template_handler = lth.TemplateHandler()
	
	# Print welcome message
	print('''
Welcome to the NLP Lyrics Generator!
Generating the next greatest hit since 2017.

Please enter input according to the following prompts.
** NOTE: If you do not enter input as exactly specified, you might get some...odd songs! **
	''')

	while True:
		input_handler.askForUserInput()
		user_input = input_handler.getUserInput()
		# Do some awesome thing with the user input
		lyrics = template_handler.generateLyrics(user_input)
		print(lyrics)
		print('\n')


if __name__ == '__main__':
	main()