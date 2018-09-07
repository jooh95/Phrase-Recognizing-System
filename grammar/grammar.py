import nltk
from pattern3.en import conjugate

# sent에서 position 위치에 있는 단어를 result로 대체해라.
sent = "He throws balls."
position = 1
result = "pitch"

tokens = nltk.word_tokenize(sent)
# print(tokens)
tagged = nltk.pos_tag(tokens)
# print(tagged)

tag = tagged[position][1]
# print(tag)

verb_set = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}
dic = {}
dic['VB'] = ['infinitive', None, None, None, None]
dic['VBD'] = ['past', None, None, None, None]
dic['VBG'] = ['present', None, None, 'indicative', 'progressive']
dic['VBN'] = ['past', None, None, 'indicative', 'progressive']
dic['VBP'] = ['present', 1, 'singular', 'indicative', 'imperfective']
dic['VBZ'] = ['present', 3, 'singular', 'indicative', 'imperfective']

if tag in verb_set:
    result = conjugate(result,
                       tense=dic[tag][0],
                       person=dic[tag][1],
                       number=dic[tag][2],
                       mood=dic[tag][3],
                       aspect=dic[tag][4],
                       negated=False)
print(result)
