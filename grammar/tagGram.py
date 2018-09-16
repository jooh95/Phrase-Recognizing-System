import nltk
import boto3
import re

s3 = boto3.resource('s3')
bucket = s3.Bucket('learningdatajchswm9')
pattern = re.compile('sentences/.+abstract[.]txt')

extag = [',', '(', ')', ':', "''", 'LS']


def tag_gram(ngrams, text, num_gram):
    sents = text.splitlines()

    tokens = []
    tagged = []
    tags = []
    for sent in sents:
        tokens.append(nltk.word_tokenize(sent))
        list_of_tags = nltk.pos_tag(tokens[-1])
        list_of_tags = [item for item in list_of_tags if item[1] not in extag]
        tagged.append(list_of_tags)
        tags.append([tup[1] for tup in tagged[-1]])
    # print(tags)

    # ngram 리스트 만들기
    list_ngrams = []
    for t in tags:
        list_ngrams = list_ngrams + [tuple(t[x:x + num_gram]) for x in range(0, len(t) - num_gram + 1)]

    # ngram 빈도 세기
    for ng in list_ngrams:
        if ng in ngrams:
            ngrams[ng] += 1
        else:
            ngrams[ng] = 1

    return ngrams


one_grams = {}  # {('NN',): 132, ...}

for obj in bucket.objects.all():
    try:
        m = pattern.match(obj.key)
        if m is not None:  # 우리가 원하는 pdf 파일이면
            bucket.download_file(obj.key, obj.key)  # sentences 폴더에 파일 다운로드 성공.
            print(obj.key)

            ifp = open(obj.key, 'r', encoding='UTF-8')
            orgTxt = ifp.read()
            ifp.close()

            one_grams = tag_gram(one_grams, orgTxt, 1)
            print(one_grams)

    except Exception as e:
        print(e)
