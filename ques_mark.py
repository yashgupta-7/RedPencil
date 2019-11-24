import nltk
from nltk.tokenize import word_tokenize,sent_tokenize
from pattern.en import sentiment
from nltk.tag import pos_tag
# nltk.download('nps_chat')
posts = nltk.corpus.nps_chat.xml_posts()[:10000]


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
print(nltk.classify.accuracy(classifier, test_set))
# line=input()
# print(line)
# print(classifier.classify(dialogue_act_features(line)))
sentences = sent_tokenize(input())
for sent in sentences:
	print(sent)	
	print(classifier.classify(dialogue_act_features(sent)))
