import nltk
import sys
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
import json
import urllib.request as urllib2
import requests
import string
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
from nltk.corpus import wordnet as wn
import json
import urllib.request as urllib2
import requests
import string
import re
from collections import Counter
from nltk.corpus import words
import string

punct = string.punctuation
# nltk.download('words')
# filename=sys.argv[1]
def conv(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(conv(open('big.txt').read()))
file=open("google-10000-english.txt","r")
words=file.read().split()
# uniq_words = set(open('dictionary.txt').read().split())
# words=[i.lower() for i in words.words()]
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
# inpwords = pos_tag(word_tokenize(sentence))
# print(inpwords)

# for i in range(len(inpwords)):

# 	if (i==0):
# 		wb = ""
# 	else:
# 		(wb,tb) = inpwords[i-1] 

# 	(w,t) = inpwords[i]
# 	print(w,t)
def getSynonyms(wordBefore, data, wordAfter):
	res=[]
	for i in data:
		wd = i
		if (True):
			trigram = []
			if (wordBefore!="" and (wordBefore not in punct)):
				trigram.append(wordBefore)# trigram = [trigram wordBefore]
			trigram.append(wd)# trigram = [trigram wd]
			if (wordAfter!="" and (wordAfter not in punct)):
				trigram.append(wordAfter)# trigram = [trigram wordAfter]
			f = phraseFreqFinder("%20".join(trigram))
			# print(f)
			if (f>200):
				res.append((f,wd))
	return res

def getSynonymsFirstWord(data, wordAfter, wordAfterAfter):
	res = []
	for i in data:
		wd = i
		if (True):
			trigram = []
			trigram.append(wd)
			if (wordAfter!="" and (wordAfter not in punct)):
				trigram.append(wordAfter)# trigram = [trigram wordBefore]
			if (wordAfterAfter!="" and (wordAfterAfter not in punct)):
				trigram.append(wordAfterAfter)# trigram = [trigram wordAfter]
			f = phraseFreqFinder("%20".join(trigram))
			if (f>200):
				res.append((f,wd))
	return res


def getSynonymsEndWord(wordBeforeBefore, wordBefore, data):
	res = []
	for i in data:
		wd = i['word']
		if (True):
			trigram = []
			if (wordBeforeBefore!="" and (wordBeforeBefore not in punct)):
				trigram.append(wordBeforeBefore)# trigram = [trigram wordAfter]
			if (wordBefore!="" and (wordBefore not in punct)):
				trigram.append(wordBefore)# trigram = [trigram wordBefore]
			trigram.append(wd)
			f = phraseFreqFinder("%20".join(trigram))
			if (f>200):
				res.append((f,wd))
	return res

def phraseFreqFinder(phrase):
	api_url = 'https://api.phrasefinder.io/search?corpus=eng-us&topk=1&format=tsv&query=' + phrase
	response = requests.get(api_url)
	data = response.text
	try:
		x = data.split('\t')[1]
		return int(x)
	except:
		return 0

pot=[]
# file=open(filename,"r")
# sentence = file.read()
inpwords = pos_tag(word_tokenize(input()))
ln=len(inpwords)
for i in range(ln):
	# print(i)
	(w,t)=inpwords[i]
	j=w
	if (w.isalpha() and w not in words) :
		suggested_words=sorted(edit1(j),key=P,reverse=True)
		# print(suggested_words)
		print("misspelled word:",j)
		if(len(suggested_words)<=5):
			print("sugestions:",suggested_words)
		else:
			suggested_words=suggested_words[:5]
		if (i==0):
			if (ln>=3):
				wa = inpwords[i+1][0]
				waa = inpwords[i+2][0]
			elif (ln==2):
				wa = inpwords[i+1][0]
				waa = ""
			else:
				wa = ""
				waa = ""
			if (True):
				syns = getSynonymsFirstWord(suggested_words,wa,waa)
				syns.sort(reverse=True)
				# print(syns)
				if (len(syns)!=0):
					print(w,[ x[1] for x in syns ])
			continue

		elif (i==len(inpwords)-1):
			if (ln>=3):
				wb = inpwords[i-1][0]
				wbb = inpwords[i-2][0]
			elif (ln==2):
				wb = inpwords[i-1][0]
				wbb = ""
			else:
				wb = ""
				wbb = ""
			if (True):
				syns = getSynonymsEndWord(wbb,wb,suggested_words)
				syns.sort(reverse=True)
				# print(syns)
				if (len(syns)!=0):
					print(w,[ x[1] for x in syns ])
			continue

		(wb,tb) = inpwords[i-1]
		(wa,ta) = inpwords[i+1]
		if (True):
			syns = getSynonyms(wb,suggested_words,wa)
			syns.sort(reverse=True)
			# print(syns)
			if (len(syns)!=0):
				print(w,[ x[1] for x in syns ])	

		# print("suggestions:",suggested_words)

				# print("suggestions:",sorted(edit1(j),key=P,reverse=True))
		# pot=[]



