import nltk
from pattern3.text import conjugate, singularize

verb_set = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}
noun_set = {'NN', 'NNS', 'NNP', 'NNPS'}
pos_ignore = ['DT', ',', '.', ':']


def lemmatize(sentence):
    result = []

    tagged_sent = nltk.pos_tag(nltk.word_tokenize(sentence))

    for pair in tagged_sent:
        word = pair[0]
        tag = pair[1]

        if tag in pos_ignore:
            continue

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

        result.append(word)

    return result
