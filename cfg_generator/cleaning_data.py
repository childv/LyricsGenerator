#splits words that are stuck together by looking them up in a dictionary
import enchant
d = enchant.Dict("en_US")

lyrics = open('split.txt', 'r', encoding='UTF-8').readlines()
ready = open('ready.txt', 'w', encoding='UTF-8')

for line in lyrics:
	new_line = []
	line = line.split()
	for i in range(len(line)):
		if d.check(line[i]) == False and len(line[i])>2 and line[i][-2:]!="in":
			w1 = line[i][0]
			w2 = line[i][1:]
			both_word = d.check(w1) == True and d.check(w2) == True and (len(w1)>1 or w1=="a" or w1=="i") and (len(w2)>1 or w2=="a" or w2=="i")
			while not both_word and w2!="":
				w1 = w1 + w2[0]
				w2 = w2[1:]
				both_word = d.check(w1) == True and d.check(w2) == True and (len(w1)>1 or w1=="a" or w1=="i") and (len(w2)>1 or w2=="a" or w2=="i")

			if both_word:
				new_line.append(w1)
				new_line.append(w2)
				print(w1)
				print(w2+'\n')
			else:
				new_line.append(line[i])
		else:
			new_line.append(line[i])
	x = " ".join(y for y in new_line)
	ready.write(x+'\n')



