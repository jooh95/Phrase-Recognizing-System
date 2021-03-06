import nltk
from pattern3.text import conjugate, singularize

verb_set = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}
noun_set = {'NN', 'NNS', 'NNP', 'NNPS'}


def lemmatize(sentence):
    pairs = nltk.pos_tag(nltk.word_tokenize(sentence))

    result = []

    for pair in pairs:
        word = pair[0]
        tag = pair[1]

        # 동사
        if tag in verb_set:
            conjugated = conjugate(word,
                                   tense='infinitive',
                                   person=None,
                                   number=None,
                                   mood=None,
                                   aspect=None,
                                   negated=False)
            word = conjugated if conjugated is not None else word

        # 명사
        elif tag in noun_set:
            word = singularize(word)

        result.append((word, tag))

    return result


sentence: str = 'The main purpose of this research is to provide information concerning the nearest ATM, Minimarket and Restaurant position by providing a computerized, properly managed and complete system.'

tokens = nltk.word_tokenize(sentence)
tags = nltk.pos_tag(tokens)
lemmatized = lemmatize(sentence)

for tag in tags:
    print(tag)

print('------------------------')

for pair in lemmatized:
    print(pair)
