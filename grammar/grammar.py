import nltk
from pattern3.en import conjugate
from pattern3.en import pluralize, singularize, lemma
from pattern3.en import suggest


# sent에서 position 위치에 있는 단어를 result로 대체해라.
sent = "He had given up the game."
position = 2
result = "send"

tokens = nltk.word_tokenize(sent)
# print(tokens)
tagged = nltk.pos_tag(tokens)
print(tagged)

tag = tagged[position][1]
print('POS tag : ' + tag)


print(suggest(tokens[position]))
print('Lemma : ' + lemma(tokens[position]))

# 동사
verb_set = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}
dic = dict()
dic['VB'] = ['infinitive', None, None, None, None]
dic['VBD'] = ['past', None, None, 'indicative', None]
dic['VBG'] = ['present', None, None, 'indicative', 'progressive']
dic['VBN'] = ['past', None, None, 'indicative', 'progressive']
dic['VBP'] = ['present', 1, 'singular', 'indicative', 'imperfective']
dic['VBZ'] = ['present', 3, 'singular', 'indicative', 'imperfective']

if tag in verb_set:
    conjugated = conjugate(result,
                           tense=dic[tag][0],
                           person=dic[tag][1],
                           number=dic[tag][2],
                           mood=dic[tag][3],
                           aspect=dic[tag][4],
                           negated=False)
    result = conjugated if conjugated is not None else result

# 명사
noun_set = {'NN', 'NNS', 'NNP', 'NNPS'}

if tag in noun_set:
    if tag == 'NNS' or tag == 'NNPS':
        result = pluralize(result)
    else:
        result = singularize(result)

print('Result : ' + result)
