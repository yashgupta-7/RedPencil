from nltk.tokenize import word_tokenize,sent_tokenize
from pattern.en import sentiment
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
import json
import urllib.request as urllib2
import requests
from pattern.en import *
import string
# from nltk.corpus import words
adj_dic={}
file=open("quan.txt","r")
adj_dic["quan"]=file.read().split()

file=open("middle.txt","r")
adj_dic["middle"]=file.read().split()

file=open("obs.txt","r")
adj_dic["obs"]=file.read().split()

file=open("size.txt","r")
adj_dic["size"]=file.read().split()

file=open("shape.txt","r")
adj_dic["shape"]=file.read().split()

file=open("age.txt","r")
adj_dic["age"]=file.read().split()

file=open("color.txt","r")
adj_dic["color"]=file.read().split()

file=open("origin.txt","r")
adj_dic["origin"]=file.read().split()

file=open("mat.txt","r")
adj_dic["mat"]=file.read().split()

val={}
val["quan"]=0
val["middle"]=0.5
val["obs"]=1
val["size"]=2
val["age"]=3
val["shape"]=4
val["color"]=5
val["origin"]=6
val["mat"]=7

des={}
des[0]="quan"
des[0.5]="middle"
des[1]="obs"
des[2]="size"
des[3]="age"
des[4]="shape"
des[5]="color"
des[6]="origin"
des[7]="mat"

adject=[]
dic={}
for i,j in adj_dic.items():
	adject=adject+[wb.lower() for wb in j]
	for word in j:
		dic[word.lower()]=val[i]
# print(adject)
# print(dic)


# print(dic["very"])
# words_dic=[i.lower() for i in words.words()]

sentences = sent_tokenize(input())
# print(sentences)

for sent in sentences:
	# sent  = sent.translate(str.maketrans('', '', string.punctuation))
	# sent = sent.replace(",","")
	words = tag(sent)
	lS = len(words)
	ans=[]
	# print(words)
	pr=[]
	for i in range(lS):
		(w,t)=words[i]
		wt=w
		w=w.lower()
		if(w in adject):
			
			pr.append((dic[w],wt))
		else:
			pr.sort()
			if(len(pr)!=0):
				for j in pr:
					ans.append(j[1])
				pr=[]
				# ans=ans+pr
			# else:
			ans.append(wt)
	pr.sort()
	if(len(pr)!=0):
		for j in pr:
			ans.append(j[1])
			pr=[]
			
	ln=len(ans)
	s=""
	for i in range(ln):
		if(i==ln-1 or ans[i+1]=="," or ans[i+1]=="." or ans[i+1]=="?" or ans[i+1]=="!"):
			s+=ans[i]
		else:
			s+=ans[i]
			s+=" "

	print(s,end=" ")
print()


