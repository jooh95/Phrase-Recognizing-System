import nltk

sentence = """He is a machine dancing on the floor."""

tokens = nltk.word_tokenize(sentence)
print(tokens)

tagged = nltk.pos_tag(tokens)
print(tagged)

attri = []
nt = ['no', 'not', "n't", 'never', 'neither', 'seldom', 'hardly', 'scarcely', 'rarely', 'nor', 'little', 'few']
will = ['will', "'ll"]
if tagged[0][1] == 'VBP':
    attri.append('imperative')
for word in tagged:
    if word[1] == 'VBD':  # 과거 동사
        attri.append('past')
    elif word[1] == 'VBP' or word[1] == 'VBZ':  # 현재 동사
        attri.append('present')
    elif word[1] == 'VBZ':
        attri.append('third')
    elif word[0].lower() in will:
        attri.append('future')
    elif word[0].lower() in nt:  # 부정
        attri.append('negative')
print(attri)
