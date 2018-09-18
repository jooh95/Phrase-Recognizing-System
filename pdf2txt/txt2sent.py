import re
import nltk

parts = ['abstract', 'content']


def extract_sents(text):
    # Reference 제거
    ref_start = max(text.rfind('Reference'),
                    text.rfind('REFERENCE'),
                    text.rfind('Bibliograph'),
                    text.rfind('BIBLIOGRAPH'))
    text = text[:ref_start]

    # spliting abstract and contents
    txt = {part: '' for part in parts}
    Abstract_start = text.find('Abstract')
    ABSTRACT_start = text.find('ABSTRACT')
    if Abstract_start == -1 and ABSTRACT_start == -1:  # 'Abstract', 'ABSTRACT'를 못 찾은 경우
        txt['abstract'] = ''
        txt['content'] = text
    else:
        if Abstract_start == -1:  # 'ABSTRACT'를 찾은 경우
            abstract_start = ABSTRACT_start + 'ABSTRACT'.__len__() + 1
        elif ABSTRACT_start == -1:  # 'Abstract'를 찾은 경우
            abstract_start = Abstract_start + 'Abstract'.__len__() + 1
        else:
            abstract_start = min(Abstract_start, ABSTRACT_start) + 'Abstract'.__len__() + 1

        text = text[abstract_start:].strip()
        pattern = re.compile('\n\s*\n+')
        m = pattern.search(text)
        if m is None:
            txt['abstract'] = ''
            txt['content'] = text
        else:
            txt['abstract'] = text[:m.end()].strip()
            txt['content'] = text[m.end():].strip()

    keys = txt.keys()

    for key in keys:
        sents = nltk.sent_tokenize(txt[key])
        new_text = ''
        for sent in sents:
            tokens = nltk.word_tokenize(sent)
            for word in tokens:
                new_text += word + ' '
            new_text += '\n'

        txt[key] = new_text
        '''
        # deleting more than two spaces
        txt[key] = re.sub(r'\n\n+', '.', txt[key])

        # deleting other characters than ascii
        # deleting (), [], {}
        txt[key] = re.sub(r'\(.*?\)', '', txt[key], flags=re.DOTALL)
        txt[key] = re.sub(r'\[.*?\]', '', txt[key], flags=re.DOTALL)
        txt[key] = re.sub(r'\{.*?\}', '', txt[key], flags=re.DOTALL)
        txt[key] = re.sub(r'"(.*?)"', '', txt[key], flags=re.DOTALL)
        txt[key] = re.sub(r'“(.*?)”', '', txt[key], flags=re.DOTALL)
        txt[key] = re.sub(r"'(.*?)'", '', txt[key], flags=re.DOTALL)

        # spliting string
        delimiters = ".", "?", "!", ";", ":"
        regexPattern = '|'.join(map(re.escape, delimiters))
        sentences = re.split(regexPattern, txt[key])

        # output text file
        sentsFile = 'sentences/' + obj.key.split('/')[-1].replace('.pdf', key + '.txt')
        ofp = open(sentsFile, 'w')
        for sentence in sentences:
            sentence = re.sub(r'-\s+', '', sentence).replace('\n', ' ').strip()
            if sentence.__len__() > 20:  # length of sentence 20 above
                ofp.write(sentence + '\n')
        ofp.close()
        '''

    return txt
