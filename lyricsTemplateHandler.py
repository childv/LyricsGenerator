'''
lyricsTemplateReader.py
10/25/17
Veronica Child

Takes in user input and outputs lyrics by selecting a random template and inserting direct user input and
random lyrics.

** Must be run in Python 3

'''

import lyricsGenerator
import json
import random
import sys
# NLTK apparently does not support verb conjugations, instead consider the following:
# https://stackoverflow.com/questions/18942096/how-to-conjugate-a-verb-in-nltk-given-pos-tag
# Library for verb conjugation: https://www.clips.uantwerpen.be/pattern
from nltk.corpus import wordnet as wn
from pattern.en import conjugate
from nltk import word_tokenize, pos_tag

class TemplateHandler:
	def __init__(self):
		self.d_templates = None
		self.readTemplates() # sets templates
		
		self.mapping_word_types = {
		'nouns':'N',
		'verbs': 'V',
		'adjectives': 'A',
		'adverbs': 'R'}

		# Initialize synset of template types
		self.happy_synset = wn.synsets('happy', 'a')[0]
		self.sad_synset = wn.synsets('sad', 'a')[0]


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
				# Gets available user input
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

						# Converts user input to present tense if verb
						if key == 'V':
							mapping[key] = self.conjugateVerb(mapping[key], 'inf')

					# If no more user input words available, add a randomly generated word based on prior inputted words
					else:
						# Attempts to generate a random word
						foundRandom = False
						for i in range(len(given)):
							rand_word = self.getRandomWord(given[random.randint(0, len(given)-1)], word_type_symbol.lower())
							if rand_word is not None:
								mapping[key] = rand_word
								found_random = True
								break
						# No random word available, reassign a word from given
						if found_random is False:
							mapping[key] = given[random.randint(0, len(given)-1)]

		return mapping


	# Conjugates variable given a tense. Tenses can be inf, 1 - 3sg, pl, and part.
	# Replace 'p' with 'inf' or add a 'p' to any other tense to get the past tense
	# @param verb 	string verb
	# @param tense 	string indicating tense
	# @return 		string conjugated verb
	def conjugateVerb(self, verb, tense):
		conjugated = conjugate(verb, tense)
		return conjugated


	# Returns a synset restricted by POS for a given word if available, else same word
	# @param word 	string word
	# @param pos	string pos ('v', 'n', 'a', 'r')
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
		while char != '>' and (char != ':') and (i < len(token)):
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

					# Conjugate verb if needed
					if (key_type[0] == 'V') and (':' in token):
						tense = token[token.index(':')+1: -1] # get tense
						word_type = self.conjugateVerb(word_type, tense)
					
					part_lyrics.append(word_type)

				# Else predefined lyrical line, add to lyrics
				else:
					part_lyrics.append(token)

			# Include none check for join?

			complete_part = ''.join(part_lyrics)
			lyrics.append(complete_part)

		complete_lyrics = '\n \n'.join(lyrics) # separate parts by new line
		return complete_lyrics


	# Returns most similar template genre based on user input and similarity score
	# @param d_user_input	dictionary containing user input of different POS
	# @return 				string name of template form to use
	def getMostSimilarTemplate(self, d_user_input):
		# Collect list of user input
		synset_list = []
		for key in d_user_input:
			# Get part of speech tag for word net
			pos = self.getWordTypeSymbol(key).lower()
			for word in d_user_input[key]:
				# Get synset of tagged words if possible
				try:
					synset = wn.synsets(word, pos)[0]
					# Filter out Nones
					synset_list.append(synset)
				except:
					pass

		# For each word of the user input
		# HAPPY
		happy_score = 0.0
		count = 0
		for synset in synset_list:
			s = synset.path_similarity(self.happy_synset)
			if s is not None:
				happy_score += s
				count += 1
		happy_score = happy_score / count
		
		# SAD
		sad_score = 0.0
		count = 0
		for synset in synset_list:
			s = synset.path_similarity(self.sad_synset)
			if s is not None:
				sad_score += s
				count += 1
		sad_score = sad_score / count

		# Return template type based on score similarity
		if sad_score < happy_score:
			template_type = 'happy'
		elif sad_score > happy_score:
			template_type = 'sad'
		else:
			template_type = random.choice(['happy', 'sad'])
		return template_type


	# Generate template-based lyrics
	# @param d_user_input 	dictionary containing user input of different POS
	# @return 				string lyrics
	def generateLyrics(self, d_user_input):
		template_type = self.getMostSimilarTemplate(d_user_input)
		# Read templates if not initiated
		if self.d_templates is None:
			self.readTemplates()

		# Pick a template based on sentiment of user input
		d_template = self.d_templates[template_type][random.randint(0, len(self.d_templates)-1)]
		# ** COMMENT OUT ABOVE AND UNCOMMENT BELOW TO SELECT A SPECIFIC TEMPLATE specify type and index**
		#d_template = self.d_templates[template_type][-1]

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

