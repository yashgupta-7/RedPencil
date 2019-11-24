import nltk
from nltk.tokenize import word_tokenize,sent_tokenize
from pattern.en import sentiment
from nltk.tag import pos_tag
import string
from pattern.en import sentiment
from nltk.tag import pos_tag
from nltk.corpus import words
import re
# nltk.download('nps_chat')
posts = nltk.corpus.nps_chat.xml_posts()[:100000]
words_dic=words.words()
punct = string.punctuation
start_words=["who","why","can","is","was","were","do","are","whom","whose"]
def tag(sentence):
	words = word_tokenize(sentence)
	words = pos_tag(words)
	return words
# var=0
def capitalise(sent):
	# sent  = sent.translate(str.maketrans('', '', string.punctuation))
	# sent = sent.replace(",","")
	words = tag(sent)
	lS = len(words)
	ans=[]
	fl=0
	# for 
	for i in range(lS):
		(w,t)=words[i]
		if(t=='UH'):
			fl=1
			# print("excl")
		if(i==0):
			w=w.lower()
			w=w[0].upper()+w[1:]
			ans.append(w)
			continue
		if(w==","):
			ans.append(w)
			continue

		w=w.lower()
		if(w=='a'):
			ans.append(w)
			continue
		if(w=='i'):
			ans.append('I')
			continue
		if(t=='NNP' or t=='NNPS'):
			w=w[0].upper()+w[1:]
			ans.append(w)
			continue
		# w=w[0].upper()+w[1:]
		# if(w in words_dic):
		# 	ans.append(w)
		# 	continue
		if(w.lower() in words_dic):
			ans.append(w.lower())
			# words[i][0]=w.lower()
			continue
		w=w[0].upper()+w[1:]
		# words[i][0]=w
		ans.append(w)


	# print(words)
	# print(ans)
	l=len(ans)
	s=""
	for i in range(l):
		if(i==l-1 or ans[i+1]==','):
			s+=ans[i]
		else:
			s+=ans[i]
			s+=" "
	# print(s)
	return (s,fl,words[0][0])



def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
    return features
# print(posts)
featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]
size = int(len(featuresets) * 0.1)
train_set, test_set = featuresets[size:], featuresets[:size]
classifier = nltk.NaiveBayesClassifier.train(train_set)
# print(nltk.classify.accuracy(classifier, test_set))
# line=input()
# print(line)
# print(classifier.classify(dialogue_act_features(line)))
l=[]
# sentences =re.split('(?<=[.!?]) *',input())
sentences =re.split(' *[.!?]+ *',input())

print(sentences)
for sent in sentences:
	if(sent==""):
		continue
	# print(x)
	# var=0
	x="Question"
	l.append(x)
	if(sent[-1]=='.' or sent[-1]=='?' or sent[-1]=='!'):
		sent=sent[:-1]
	# sent=sent[0].upper()+sent[1:]
	# print(sent[0])
	(s,fl,fw)=capitalise(sent)
	print(s,end="")	
	x=classifier.classify(dialogue_act_features(s))
	# print(sent[0].lower())
	if(fl==1):
		print("!",end=" ")
	elif("Question" in x or fw.lower() in start_words):
		print("?",end=" ")
	else:
		print(".",end=" ")
# print(l)
print()
# print("favour" in words_dic)
# print("A" in words_dic)
# caps=[]
# for w in words_dic:
# 	if(w[0].isupper()):
# 		caps.append(w)

# print(caps)
