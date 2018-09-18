import nltk

sentence: str = 'The main purpose of this research is to provide information concerning the nearest ATM, Minimarket and Restaurant position by providing a computerized, properly managed and complete system.'

tokens = nltk.word_tokenize(sentence)
tags = nltk.pos_tag(tokens)

print(tags)
