import nltk
original_grammar = nltk.data.load('grammars/large_grammars/atis.cfg')
original_parser = nltk.ChartParser(original_grammar)
s='i am  looking  for flights  ?'
# sent = ['show', 'me', 'northwest', 'flights', 'to', 'detroit', '.']
sent=s.split()
for i in original_parser.parse(sent):
	print(i[:-1])
	break