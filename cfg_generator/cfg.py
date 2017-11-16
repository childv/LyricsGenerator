import nltk, pickle, random
from operator import itemgetter
from nltk.parse.generate import generate 

lyrics = open('ready.txt', 'r', encoding='UTF-8').readlines()
random.shuffle(lyrics)
split_i = int(9*len(lyrics)/10)
train_data = lyrics[:split_i]
test_data = lyrics[split_i:]

def CreateTermDict(test_data):
    terminals = {}
    for l in test_data:
        if l[:2] != 'NA':
            text = nltk.word_tokenize(l)
            tokenized = nltk.pos_tag(text)
            for token in tokenized:
                word, pos = token
                if pos not in terminals:
                    terminals[pos] = []
               	terminals[pos].append(word)
                    
    pickle.dump(terminals, open('terminals.p', 'wb'))             
      
CreateTermDict(test_data)       
        
def data_preprocessing(sent_list):

    #word_tokenize_list = nltk.word_tokenize(sent_list) #list of words
    #sent_tokenize_list = nltk.sent_tokenize(sent_list) #list of sentences

    ngrams = []
    for sent in sent_list:
        sn = nltk.word_tokenize(sent)
        #sn2 = ['<s>'] + sn + ['<\s>']
        ngrams.append(sn)

    return(ngrams)


def find_ngrams(input_list, n): #find all the ngrams in a sentence
  return list(zip(*[input_list[i:] for i in range(n)]))


def ngram_model(train, test, n=4):
    #P of each ngram = c(ngram)/c(history)
    all_ngrams = []
    #all_hist = []
    #make a list of all ngrams, associate probability with each
    for sent in train:
        words = find_ngrams(sent, n)
        for x in words:
            all_ngrams.append(x)

    count_ngrams = {} #all ngrams in train data + w3
    #count occurrences of each word
    for each in all_ngrams:
        if each not in count_ngrams.keys():
            count_ngrams[each] = 1
        else: 
            count_ngrams[each]+=1
            
    out_domain_ngrams = open('w4_.txt','r',encoding='UTF-8',errors='ignore').readlines()
    for line in out_domain_ngrams:
        split = line.split()
        ngram = tuple(split[1:])
        if ngram not in count_ngrams:
            count_ngrams[ngram] = int(split[0])
        else:    
            count_ngrams[ngram] += int(split[0])
                
    #each ngram has a probability, which is the count of that ngram/its history
    #print(count_ngrams)
    
    test_ngram_counts = {} #list of probs of all ngrams in the test set

      
    for sent in test:
        sent_prob = 1
        test_ngrams = find_ngrams(sent, n)
        for every in test_ngrams:
            if every in count_ngrams.keys():
                sent_prob = sent_prob*count_ngrams[every]
                #test_ngram_pairs[every]= count_ngrams[every]
            else: 
                sent_prob = sent_prob*1
            test_ngram_counts[' '.join(sent)] = sent_prob

    pairs = sorted(test_ngram_counts.items(), key=itemgetter(1), reverse=True)
    return pairs #ngrams + history with counts (training set)
    

terminals = pickle.load(open('terminals_dict.p', 'rb'))
print('Loaded pickle dict')
grammar_string = """
  S -> NP VP | RB NP VP | VBG VP | NP RB VP | S '.'
  NP -> PRP | Nominal | CD Nominal | DT Adjectival | DT Adjectival Nominal | DT Nominal | Adjectival | Adjectival Nominal | NP PP | NP S
  VP -> VBZ NP | Verbal NP | Verbal RB Verbal NP | Verbal | Verbal TO Verbal VP | VP PP | MD Verbal | MD RB Verbal | VP VBG PP
  PP -> IN NP | IN
  
  Verbal -> VB | VBP | VBD | VBN | Verbal VBN | Verbal VBG
  Nominal -> NN | NNS
  Adjectival -> JJ | JJS
  
  TO -> 'to'
"""

for pos in ['VB','VBP','VBD','VBG','VBZ','VBN','IN','MD','RB','PRP','CD','DT','JJ','JJS','NN','NNS']:
    indices = [int(random.randint(0,len(terminals[pos]) - 1)) for i in range(10)]
    grammar_string += ("%s -> '%s' | '%s' | '%s' | '%s' | '%s' | '%s' | '%s' | '%s' | '%s' | '%s'\n "% (pos, terminals[pos][indices[0]],terminals[pos][indices[1]],terminals[pos][indices[2]],terminals[pos][indices[3]],terminals[pos][indices[4]],terminals[pos][indices[5]],terminals[pos][indices[6]],terminals[pos][indices[7]],terminals[pos][indices[8]],terminals[pos][indices[9]]))
#print(grammar_string)    
our_grammar = nltk.CFG.fromstring(grammar_string)
sentences = []
for sentence in generate(our_grammar, n=500000, depth=7):
    sentences.append(' '.join(x for x in sentence) )

print('Generated sentences')    
    
preprocessed_test = data_preprocessing(sentences)  
preprocessed_train = data_preprocessing(train_data)

print('Preprocessed data')
probs = ngram_model(preprocessed_train, preprocessed_test)
print('Assigned probabilities to sentences...Wait for it!\n')
somewhat_grammatical = []
final = []

for x in range(1000):
    somewhat_grammatical.append(probs[x][0])
indices = [int(random.randint(0,len(somewhat_grammatical) - 1)) for i in range(8)]

for i in indices: #some rudimentary agreement
	if somewhat_grammatical[i].split()[0] in ["me", "i", "you", "they", "we"]:
		if somewhat_grammatical[i].split()[1][-1] == "s":
			somewhat_grammatical[i].split()[1] = somewhat_grammatical[i].split()[:1]
	if somewhat_grammatical[i].split()[0] == "me": 
		somewhat_grammatical[i] = "i "+ " ".join(x for x in somewhat_grammatical[i].split()[:-1])
	if somewhat_grammatical[i].split()[-1] == "they":
		somewhat_grammatical[i] = " ".join(x for x in somewhat_grammatical[i].split()[:-1]) + " them"
	elif somewhat_grammatical[i].split()[-1] == "she":
		somewhat_grammatical[i] = " ".join(x for x in somewhat_grammatical[i].split()[:-1]) + " her"
	elif somewhat_grammatical[i].split()[-1] == "he":
		somewhat_grammatical[i] = " ".join(x for x in somewhat_grammatical[i].split()[:-1]) + " him"
	final.append(somewhat_grammatical[i])


for each in final:
	print(each)


    
    