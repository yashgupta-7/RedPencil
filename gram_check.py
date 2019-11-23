from nltk.tokenize import word_tokenize,sent_tokenize
from pattern.en import sentiment
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
import json
import urllib.request as urllib2
import requests
from pattern.en import *
import string
from nltk.corpus import words
words_dic=[i.lower() for i in words.words()]
punct = string.punctuation
actFreq = 0
def is_verb(word):
	for tmp in wn.synsets(w):
		if(tmp.name().split('.')[0] == w and tmp.pos()=='v'):
			return True
	return False
def getSynonyms(wordBefore, word, wordAfter,t):
	word=word.lower()
	s="%20".join([wordBefore, word, wordAfter])
	# print(s)
	actFreq = phraseFreqFinder("%20".join([wordBefore, word, wordAfter]))
	# print(word,)
	# print(actFreq)
	if(actFreq>30000):
		return []
	data=[]
	d2=['a','an','the']
	detpron=["that","those","this","these"]
	# print(t)
	# print(word)
	if("VB"  in t or "NN" in t):
		data=data+lexeme(word)
	if(is_verb(word)):
		data=data+lexeme(word)
		
	# print(lexeme(word))
	res=[]
	if(word in d2):
		data=d2
	if(word in detpron):
		data=detpron
	for wd in data:
		# print(wd)
		if(wd.lower() not in words_dic):
			# print(words)
			# print(wd.lower()+" not present")
			continue
		if(" not" in wd or "\'t" in wd):
			continue
		if (True):
			trigram = []
			if (wordBefore!="" and (wordBefore not in punct)):
				trigram.append(wordBefore)# trigram = [trigram wordBefore]
			trigram.append(wd)# trigram = [trigram wd]
			if (wordAfter!="" and (wordAfter not in punct)):
				trigram.append(wordAfter)# trigram = [trigram wordAfter]
			# print(trigram)
			if(wd is 'a' or wd is 'an'):
				if (wordAfter!="" and (wordAfter not in punct)):
					if(referenced(wordAfter).split()[0] != wd):
						continue
				else:
					continue
				# trigram.append(wordAfter)# trigram = [trigram wordAfter]
			
			# if()
			f = phraseFreqFinder("%20".join(trigram))
			# print(f)
			if (f>500 and f>actFreq):
				res.append((f,wd))
	return res

def getSynonymsFirstWord(word, wordAfter, wordAfterAfter,t):
	word=word.lower()
	actFreq = phraseFreqFinder("%20".join([word, wordAfter, wordAfterAfter]))
	s="%20".join([word, wordAfter, wordAfterAfter])
	# print(s)
	# print(word,)
	# print(actFreq)
	if(actFreq>30000):
		return []
	data=[]
	d2=['a','an','the']
	detpron=["that","those","this","these"]
	# print(t)
	# print(word)
	if("VB"  in t or "NN" in t):
		data=data+lexeme(word)
	if(is_verb(word)):
		data=data+lexeme(word)
		
	# print(lexeme(word))
	res=[]
	if(word in d2):
		data=d2
	if(word in detpron):
		data=detpron
	for wd in data:
		# print(wd)
		if(wd.lower() not in words_dic):
			# print(words)
			# print(wd.lower()+" not present")
			continue
		if(" not" in wd or "\'t" in wd):
			continue
		if (True):
			trigram = []
			trigram.append(wd)
			if (wordAfter!="" and (wordAfter not in punct)):
				trigram.append(wordAfter)# trigram = [trigram wordBefore]
			if (wordAfterAfter!="" and (wordAfterAfter not in punct)):
				trigram.append(wordAfterAfter)# trigram = [trigram wordAfter]
			if(wd is 'a' or wd is 'an'):
				if (wordAfter!="" and (wordAfter not in punct)):
					if(referenced(wordAfter).split()[0] != wd):
						continue
				else:
					continue
			# print(trigram)
			f = phraseFreqFinder("%20".join(trigram))
			# print(f)
			if (f>500 and f>actFreq):
				res.append((f,wd))
	return res


def getSynonymsEndWord(wordBeforeBefore, wordBefore, word,t):
	word=word.lower()
	if(word is 'a' or word is 'an'):
		return []
	actFreq = phraseFreqFinder("%20".join([ wordBeforeBefore, wordBefore, word]))
	# print(word)
	# print(actFreq)
	if(actFreq>30000):
		return []
	data=[]
	d2=['a','an','the']
	detpron=["that","those","this","these"]
	# print(t)
	# print(word)
	if("VB"  in t or "NN" in t):
		data=data+lexeme(word)
	if(is_verb(word)):
		data=data+lexeme(word)
		
	# print(lexeme(word))
	res=[]
	if(word in d2):
		data=d2
	if(word in detpron):
		data=detpron
	res = []
	for wd in data:
		if(wd.lower() not in words_dic):
			# print(words)
			# print(wd.lower()+" not present")
			continue
		if(" not" in wd or "\'t" in wd):
			continue
		
		if (True):
			trigram = []
			if (wordBeforeBefore!="" and (wordBeforeBefore not in punct)):
				trigram.append(wordBeforeBefore)# trigram = [trigram wordAfter]
			if (wordBefore!="" and (wordBefore not in punct)):
				trigram.append(wordBefore)# trigram = [trigram wordBefore]
			trigram.append(wd)
			f = phraseFreqFinder("%20".join(trigram))
			if (f>500 and f>actFreq):
				res.append((f,wd))
	return res

def tag(sentence):
	words = word_tokenize(sentence)
	words = pos_tag(words)
	return words

def paraphraseable(tag):
	l = ['JJ','NN','NNS','NNPS','RB','VB','VBD','VBG','VBN','VBP','VBZ','DT','IN']
	if tag in l:
		return True
	else:
		return False

def phraseFreqFinder(phrase):
	#phrase = "%20".join([wordBefore,word,wordAfter]).lower()
	# print(phrase)
	api_url = 'https://api.phrasefinder.io/search?corpus=eng-us&topk=1&format=tsv&query=' + phrase
	response = requests.get(api_url)
	# data = response.json()
	# data_format = json.dumps(data, indent=4, sort_keys=True)
	data = response.text
	#print(data.split('\t'))
	try:
		x = data.split('\t')[1]
	# lines = data.split("\n")
	# for l in lines:
	# 	print(l.split('\t')[1])
	# 	x = l.split('\t')[1]
		# print(x)
		return int(x)
	except:
		return 0


sentences = sent_tokenize(input())
# print(sentences)

for sent in sentences:
	sent  = sent.translate(str.maketrans('', '', string.punctuation))
	# sent = sent.replace(",","")
	words = tag(sent)
	lS = len(words)
	# print(words)
	for i in range(lS):

		(w,t) = words[i]

		if (i==0):
			if (lS>=3):
				wa = words[i+1][0]
				waa = words[i+2][0]
			elif (lS==2):
				wa = words[i+1][0]
				waa = ""
			else:
				wa = ""
				waa = ""
			if (paraphraseable(t)):
				syns = getSynonymsFirstWord(w,wa,waa,t)
				syns.sort(reverse=True)
				# print(syns)
				if (len(syns)!=0):
					print(w,[ x[1] for x in syns ])
			continue

		elif (i==len(words)-1):
			if (lS>=3):
				wb = words[i-1][0]
				wbb = words[i-2][0]
			elif (lS==2):
				wb = words[i-1][0]
				wbb = ""
			else:
				wb = ""
				wbb = ""
			if (paraphraseable(t)):
				syns = getSynonymsEndWord(wbb,wb,w,t)
				syns.sort(reverse=True)
				# print(syns)
				if (len(syns)!=0):
					print(w,[ x[1] for x in syns ])
			continue

		(wb,tb) = words[i-1]
		(wa,ta) = words[i+1]
		if (paraphraseable(t)):
			syns = getSynonyms(wb,w,wa,t)
			syns.sort(reverse=True)
			# print(syns)
			if (len(syns)!=0):
				print(w,[ x[1] for x in syns])	
