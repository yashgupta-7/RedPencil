from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
import json
import urllib.request as urllib2
import requests
import string

punct = string.punctuation
iitbLingo = ['arbit','bandi','chamka','craxxxx','dac','dadda','ditch','dosa','enthu','farra','freshie','god','infi','insti','junta','liby','macha','matka','mug','paf']
LingoMeans = ['arbitrary','girl','understand','achievement','Disciplinary Action Committee','Dual Degree Student','drop','Dean of Student Affairs','enthusiasm','FR','First Year Student','awesome','infinite','institute','people','library','rock','MTech Student','study','Performing Arts Festival']
actFreq = 0

def getSynonyms(wordBefore, word, wordAfter):
	actFreq = phraseFreqFinder("%20".join([wordBefore, word, wordAfter]))
	api_url = 'https://api.datamuse.com/words?ml='
	api_url = api_url + word
	if (wordBefore!="" and (wordBefore not in punct)):
		api_url = api_url + '&lc=' + wordBefore
	if (wordAfter!="" and (wordAfter not in punct)):
		api_url = api_url + '&rc=' + wordAfter
	api_url = api_url + '&max=5'
	# print(api_url)
	data = json.load(urllib2.urlopen(api_url))
	data_format = json.dumps(data, indent=4, sort_keys=True)
	res = []
	for i in data:
		wd = i['word']
		if (pos_tag([wd])[0][1]==pos_tag([word])[0][1]):
			trigram = []
			if (wordBefore!="" and (wordBefore not in punct)):
				trigram.append(wordBefore)# trigram = [trigram wordBefore]
			trigram.append(wd)# trigram = [trigram wd]
			if (wordAfter!="" and (wordAfter not in punct)):
				trigram.append(wordAfter)# trigram = [trigram wordAfter]
			f = phraseFreqFinder("%20".join(trigram))
			if (f>10000):
				res.append((f,wd))
	return res

def getSynonymsFirstWord(word, wordAfter, wordAfterAfter):
	actFreq = phraseFreqFinder("%20".join([word, wordAfter, wordAfterAfter]))
	api_url = 'https://api.datamuse.com/words?ml='
	api_url = api_url + word
	if (wordAfter!="" and (wordAfter not in punct)):
		api_url = api_url + '&rc=' + wordAfter
	api_url = api_url + '&max=5'
	# print(api_url)
	data = json.load(urllib2.urlopen(api_url))
	data_format = json.dumps(data, indent=4, sort_keys=True)
	res = []
	for i in data:
		wd = i['word']
		if (pos_tag([wd])[0][1]==pos_tag([word])[0][1]):
			trigram = []
			trigram.append(wd)
			if (wordAfter!="" and (wordAfter not in punct)):
				trigram.append(wordAfter)# trigram = [trigram wordBefore]
			if (wordAfterAfter!="" and (wordAfterAfter not in punct)):
				trigram.append(wordAfterAfter)# trigram = [trigram wordAfter]
			f = phraseFreqFinder("%20".join(trigram))
			if (f>10000):
				res.append((f,wd))
	return res


def getSynonymsEndWord(wordBeforeBefore, wordBefore, word):
	actFreq = phraseFreqFinder("%20".join([wordBeforeBefore, wordBefore, word]))
	api_url = 'https://api.datamuse.com/words?ml='
	api_url = api_url + word
	if (wordBefore!="" and (wordBefore not in punct)):
		api_url = api_url + '&lc=' + wordBefore
	api_url = api_url + '&max=5'
	# print(api_url)
	data = json.load(urllib2.urlopen(api_url))
	data_format = json.dumps(data, indent=4, sort_keys=True)
	res = []
	for i in data:
		wd = i['word']
		if (pos_tag([wd])[0][1]==pos_tag([word])[0][1]):
			trigram = []
			if (wordBeforeBefore!="" and (wordBeforeBefore not in punct)):
				trigram.append(wordBeforeBefore)# trigram = [trigram wordAfter]
			if (wordBefore!="" and (wordBefore not in punct)):
				trigram.append(wordBefore)# trigram = [trigram wordBefore]
			trigram.append(wd)
			f = phraseFreqFinder("%20".join(trigram))
			if (f>10000):
				res.append((f,wd))
	return res

def tag(sentence):
	words = word_tokenize(sentence)
	words = pos_tag(words)
	return words

def paraphraseable(tag):
	l = ['JJ','NN','NNS','NNPS','RB','VB','VBD','VBG','VBN','VBP','VBZ']
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

		if w in iitbLingo:
			print(w,[LingoMeans[iitbLingo.index(w)]])
			continue

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
				syns = getSynonymsFirstWord(w,wa,waa)
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
				syns = getSynonymsEndWord(wbb,wb,w)
				syns.sort(reverse=True)
				# print(syns)
				if (len(syns)!=0):
					print(w,[ x[1] for x in syns ])
			continue

		(wb,tb) = words[i-1]
		(wa,ta) = words[i+1]
		if (paraphraseable(t)):
			syns = getSynonyms(wb,w,wa)
			syns.sort(reverse=True)
			# print(syns)
			if (len(syns)!=0):
				print(w,[ x[1] for x in syns ])	
