import nltk
import sys
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
from nltk.corpus import wordnet as wn
import json
import urllib.request as urllib2
# import requests
import string
import re
from collections import Counter
from nltk.corpus import words
# nltk.download('words')
filename=sys.argv[1]
def conv(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(conv(open('big.txt').read()))

uniq_words = set(open('dictionary.txt').read().split())
words=[i.lower() for i in words.words()]
# words=[i.lower() for i in uniq_words]
# print(words)
def P(word, N=sum(WORDS.values())): 
    # "Probability of `word`."
    return WORDS[word] / N

def edit1(word):
	word=word.lower()
	# word will be lower case
	n=len(word)
	letters="abcdefghijklmnopqrstuvwxyz"
	# edit
	edit=[word[:i]+j+word[i+1:] for i in range(0,n) for j in letters]
	# print(len(edit))
	# delete
	delete=[word[:i]+word[i+1:] for i in range(0,n) ]
	
	# insert
	insert=[word[:i]+j+word[i:] for i in range(0,n) for j in letters]
	
	# transpose
	trans=[word[:i]+word[i+1]+word[i]+word[i+2:] for i in range(0,n-1) ]
	# print(trans)
	cand=set(edit+delete+insert+trans)
	return set([i for i in cand if i in words])
	# combine all and return
	# return [i for i in edit+delete+insert+trans ]
def edit2(word):
	return set([j for i in edit1(word) for j in edit1(i) ])

# print(filename)
file=open(filename,"r")
sentence = file.read()
inpwords = pos_tag(word_tokenize(sentence))
# print(inpwords)

# for i in range(len(inpwords)):

# 	if (i==0):
# 		wb = ""
# 	else:
# 		(wb,tb) = inpwords[i-1] 

# 	(w,t) = inpwords[i]
# 	print(w,t)

pot=[]
for i,j in inpwords:
	# print(i)
	if (i=='.' or i=='?' or i == '!') :
		# pot.append(i[0:-1].lower())
		# print(pot)
		for j in pot:
			if (j not in words) :
				print("misspelled word:",j)
				print("suggestions:",sorted(edit1(j),key=P,reverse=True))
		pot=[]
	else:
		if(i.isalpha()):
			pot.append(i.lower())


