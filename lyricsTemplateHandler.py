'''
lyricsTemplateReader.py
10/25/17
Veronica Child

Takes in user input and outputs lyrics by selecting a random template and inserting direct user input and
random lyrics

'''

import lyricsGenerator
import json
import random
import sys
# NLTK apparently does not support verb conjugations, instead consider the following:
# https://stackoverflow.com/questions/18942096/how-to-conjugate-a-verb-in-nltk-given-pos-tag
# Library for verb conjugation: https://www.clips.uantwerpen.be/pattern
from nltk.corpus import wordnet as wn

class TemplateHandler:
	def __init__(self):
		self.d_templates = None
		self.readTemplates() # sets templates
		
		self.mapping_word_types = {
		'nouns':'N',
		'verbs': 'V',
		'adjectives': 'A',
		'adverbs': 'R'}


	# Reads in lyrics_templates.json and converts it into
	# a python dictionary by setting global variable d_templates
	def readTemplates(self):
		# Read json 
		try:
			with open('lyrics_templates.json') as json_data:
				self.d_templates = json.load(json_data)
		# Error: Unable to parse json
		except Exception as e:
			print('Unable to read in JSON template file due to the following error:')
			print(e)
			sys.exit() #Maybe exit out of module instead of exiting whole program


	# Get symbol letter given word type
	# @param key 	word type
	# @return 		string word initial type
	def getWordTypeSymbol(self, word_type):
		return self.mapping_word_types[word_type]


	# Creates mapping of user input to a particular symbol
	# @param 	d_input 	dictionary of word type : user input
	# @param 	layout	 	JSON dictionary of template layout
	# @return 	dicitonary mapping user input to template layout
	def createInputMapping(self, d_input, layout):
		mapping = {}
		# Cross template specifications with user input
		for t in layout:
			if t != 'form':
				num_needed = layout[t] # get number of word types needed
				
				words = []
				# Needed word type not defined by user, generate own
				if t in d_input:
					# Copy user input
					given = d_input[t]
					# Copy user input as needed
					words = []
					for w in given:
						words.append(w)
					random.shuffle(words) # shuffle word order

				# Assign to mapping
				for i in range(0, num_needed):
					# create mapping key (ex. N1)
					word_type_symbol = self.getWordTypeSymbol(t) # get mapping key: N, V, A (adj), R (adverb)
					key = ''.join([word_type_symbol, str(i+1)]) # create key: A1, V2, etc.
					
					# Add set user input word to mapping
					if len(words) > 0:
						mapping[key] = words.pop()
					# If no more words available, add a randomly generated word based on inputted words
					else:
						rand_word = self.getRandomWord(given[random.randint(0, len(given)-1)], word_type_symbol.lower())
						mapping[key] = rand_word

		return mapping


	# Returns a synset restricted by POS for a given word if available, else same word
	# @param 	string word
	# @param 	string pos ('v', 'n', 'a', 'r')
	# @return 	string generated word
	def getRandomWord(self, word, pos):
		# Get synsets of all words
		synsets = wn.synsets(word, pos=pos.lower())
		
		# Similar words available
		if len(synsets) != 0: 
			random.shuffle(synsets) # randomize synsets

			# Try to get a random word from the synset
			for syn in synsets:
				similar_words = syn.lemma_names() # return lemmas of similar words

				# Available lemmas
				if len(similar_words) != 0:
					random.shuffle(similar_words) # randomize synset lemmas
					# Get a random word lemma
					rand_word = similar_words.pop()
					rand_word = rand_word.replace("_", " ") # clean up string
					
					# Continue to get another word if it's the same
					while (rand_word == word) and (len(similar_words) != 0):
						rand_word = similar_words.pop()
						rand_word = rand_word.strip()
						if rand_word != word:
							rand_word = rand_word.replace("_", " ") # clean up string
							return rand_word
					
					return rand_word
			
		# Similar words not available, return same word
		return word


	# Retrieves key symbol from token for mapping
	# @param token 	string token containg key symbol
	# @return 		string key for mapping
	def getKeyType(self, token):
		key_type = []
		i = 1 # Skip open "<"
		char = token[i]

		# Retrieve symbol
		while char != '>' and (i < len(token)):
			key_type.append(char)
			i += 1
			char = token[i]

		key = ''.join(key_type)
		return key


	# Fills in lyrics given user mappings
	# @param d_mapping 	 	dictionary of word phrase needed to word key,value pirs
	# @param d_templates	JSON dictionary of lyric template
	# @ return 				string lyrics
	def completeLyrics(self, d_mapping, d_template):
		lyrics = []
		parts = d_template['parts']

		# Process song parts
		for key_part in d_template['layout']['form']:
			try:
				part = parts[key_part]
			except Exception:
				print('ERROR: Unable to find specified song part: ' + key_part)
				break

			# Iterate through list of tokens of song part
			part_lyrics = []
			for token in part:
				# Get mapping symbol if encountered substitution string
				if token[0] == '<':
					key_type = self.getKeyType(token)
					word_type = d_mapping[key_type]
					# *** MODIFY WORD TO FIT CONTEXT OF SENTENCE ***
					# print('Word type: ')
					# print(word_type)
					
					part_lyrics.append(word_type)

				# Else predefined lyrical line, add to lyrics
				else:
					part_lyrics.append(token)

			complete_part = ''.join(part_lyrics)
			lyrics.append(complete_part)

		complete_lyrics = '\n \n'.join(lyrics) # separate parts by new line
		return complete_lyrics


	# Generate template-based lyrics
	# @param user_input 	dictionary containing user input of different POS
	# @return 				string lyrics
	def generateLyrics(self, d_user_input):
		# Read templates if not initiated
		if self.d_templates is None:
			self.readTemplates()

		# Pick a random template dictionary
		d_template = self.d_templates[random.randint(0, len(self.d_templates)-1)]
		# ** COMMENT OUT ABOVE AND UNCOMMENT BELOW TO SELECT A SPECIFIC TEMPLATE (index by position)**
		#d_template = self.d_templates[-1]

		# Create a dictionary mapping user input to a particular key in template
		d_input_mapping = self.createInputMapping(d_user_input, d_template['layout'])

		complete_lyrics = self.completeLyrics(d_input_mapping, d_template)


		return complete_lyrics.strip()


def main():
	gen = lyricsGenerator.UserInput()
	handler = TemplateHandler()
	lyrics = handler.generateLyrics(gen.getUserInput())
	print(lyrics)


if __name__ == '__main__':
	main()

