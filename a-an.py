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
# nltk.download('cmudict')

arpabet = nltk.corpus.cmudict.dict()
# for word in ('barbels', 'barbeque', 'barbequed', 'barbequeing', 'barbeques'):
#     print(arpabet[word])

# print(arpabet['universe'])

filename=sys.argv[1]
file=open(filename,"r")
sentence = file.read()
sentence=sentence.lower()
# print(sentence)
inpwords = word_tokenize(sentence)
l=['A','E','I','O','U']
pot=[]
for i in range(0,len(inpwords)):
	# print(i)
	# print(inpwords[i])
	if(i==len(inpwords)-1):
		continue
	if (inpwords[i]=='a') :
		# print(inpwords[i])
		w=arpabet[inpwords[i+1]]
		# print(w)
		# print(w[0][0][0])
		if(w[0][0][0]  in l):
			print("Suggestion: an "+inpwords[i+1])
	elif(inpwords[i]=='an'):
		w=arpabet[inpwords[i+1]]
		if(w[0][0][0] not in l):
			print("Suggestion: a "+inpwords[i+1])
		

	# 	pot.append(i[0:-1].lower())
	# 	print(pot)
	# 	print("hlj")
	# 	for j in pot:
	# 		if (j not in words) :
	# 			suggested_words=sorted(edit1(j),key=P,reverse=True)
	# 			print("misspelled word:",j)
	# 			if(len(suggested_words)<=5):
	# 				print("sugestions:",suggested_words)
	# 			else:
	# 				print("suggestions:",suggested_words[:5])

	# 			# print("suggestions:",sorted(edit1(j),key=P,reverse=True))
	# 	pot=[]
	# else:
	# 	print(i)
	# 	if(i.isalpha()):
	# 		pot.append(i.lower())


