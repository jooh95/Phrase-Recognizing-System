import nltk
from pattern3.en import conjugate, singularize

verb_set = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}
noun_set = {'NN', 'NNS', 'NNP', 'NNPS'}


def lemmatize(text):
    sentences = [nltk.pos_tag(nltk.word_tokenize(sentence)) for sentence in nltk.sent_tokenize(text)]
    print(sentences)

    result = []

    for sentence in sentences:
        tmp = []
        for tup in sentence:
            word = tup[0]
            tag = tup[1]

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

            tmp.append(word)

        result.append(tmp)

    return result


text = '''Now a days , artificial intelligence have terribly very important role in day to day life . 
whether it 's Finger print recognition or Face detection , artificial intelligence found its usability . '''
print(lemmatize(text))