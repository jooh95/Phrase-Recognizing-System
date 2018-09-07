import nltk
from nltk.tag import pos_tag, map_tag
from pattern3.en import conjugate


dic = {}
dic['VBG'] = ['present', None, None, 'indicative', 'pregressive']



sent = "Moon is throwing a ball."
position = 2

text = nltk.word_tokenize(sent)
posTagged = pos_tag(text)
simplifiedTags = [(word, map_tag('en-ptb', 'universal', tag)) for word, tag in posTagged]
print(simplifiedTags)

result = 'pitch'

if simplifiedTags[position][1] == 'VERB':
    result = conjugate(result,
                       tense="present",
                       person=3,
                       number="singular",
                       mood="indicative",
                       aspect="progressive",
                       negated=False)