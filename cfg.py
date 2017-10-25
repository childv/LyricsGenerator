import nltk, pickle, random
from nltk.parse.generate import generate 
def CreateTermDict():
    lyrics = open('lyrics.txt', 'r', encoding='UTF-8').readlines()
    terminals = {}
    for l in lyrics[1:500]:
        if l[:2] != 'NA':
            text = nltk.word_tokenize(l)
            tokenized = nltk.pos_tag(text)
            for token in tokenized:
                word, pos = token
                if pos not in terminals:
                    terminals[pos] = []
                terminals[pos].append(word)
                    
    pickle.dump(terminals, open('terminals_dict.p', 'wb'))             
      
CreateTermDict()    
terminals = pickle.load(open('terminals_dict.p', 'rb'))

grammar_string = """
  S -> NP VP | ADVP NP VP | VBG VP | NP ADVP VP | S '.' | S IN S
  NP -> PRP | Nominal | CD Nominal | DT Adjectival | DT Adjectival Nominal | DT Nominal | Adjectival | Adjectival Nominal | NP PP | NP S
  VP -> VBZ NP | Verbal NP | VBZ ADVP | Verbal RB Verbal NP | Verbal | Verbal TO Verbal VP | VP PP | MD Verbal | MD RB Verbal | VP VBG PP
  PP -> IN NP | IN | IN PP
  ADVP -> DT VBN | ADVP RB | RB
  
  Verbal -> VB | VBP | VBD | VBN | Verbal VBN | Verbal VBG
  Nominal -> NN | NNS
  Adjectival -> JJ | JJS
  
  TO -> 'to'
"""

for pos in ['VB','VBP','VBD','VBG','VBZ','VBN','IN','MD','RB','PRP','CD','DT','JJ','JJS','NN','NNS']:
    indices = [int(random.randint(0,len(terminals[pos]) - 1)) for i in range(5)]
    grammar_string += ("%s -> '%s' | '%s' | '%s' | '%s' | '%s'\n "% (pos, terminals[pos][indices[0]],terminals[pos][indices[1]],terminals[pos][indices[2]],terminals[pos][indices[3]],terminals[pos][indices[4]]))
#print(grammar_string)    
our_grammar = nltk.CFG.fromstring(grammar_string)
sentences = []
for sentence in generate(our_grammar, n=500000, depth=5):
    sentences.append(' '.join(x for x in sentence) )
indices = [int(random.randint(0,len(sentences) - 1)) for i in range(5)]
for i in indices:
    print(sentences[i])
