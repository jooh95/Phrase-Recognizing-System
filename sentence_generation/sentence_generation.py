import nltk

# 'sentences.txt'에서 데이터 불러오기
f = open("sentences.txt", "r", encoding='UTF-8')
raw_data = f.read()
f.close()

# 한 줄 단위로 자르기
lines = [line.strip() for line in raw_data.splitlines()]
# print(lines)

# ':'로 끝나는 문장은 dictionary의 key로 분류
sentence_groups = {}
key = ''
for i in range(len(lines)):
    if (i == 0 and lines[i][-1] == ':') or (i > 0 and lines[i-1] == '' and lines[i][-1] == ':'):
        # 여기서부터 밑에까지 dictionary에 value로 넣는다.
        key = lines[i][:-1]
        sentence_groups[key] = []
    elif not lines[i] == '':
        sentence_groups[key].append(nltk.word_tokenize(lines[i]))

print(sentence_groups)

# 키보드 입력 값 받기
input_string = input()
input_tokens = nltk.word_tokenize(input_string)
input_pos = nltk.pos_tag(input_tokens)
# print(input_pos)

# 무시할 태그
pos_ignore = ['DT', ',']

for key in sentence_groups:
    for sentence in sentence_groups[key]:
        match = True
        compare_index = 0

        for input_token in input_pos:
            if input_token[1] in pos_ignore:
                continue

            for sentence_token in nltk.pos_tag(sentence)[compare_index:]:
                compare_index += 1

                if sentence_token[1] in pos_ignore:
                    continue

                if sentence_token[0] == 'X' and (input_token[1] == 'NN' or input_token[1] == 'NNP'):
                    compare_index -= 1
                    break

                if sentence_token[0] == 'Xs' and (input_token[1] == 'NNS' or input_token[1] == 'NNPS'):
                    compare_index -= 1
                    break

                if sentence_token[0].lower().find(input_token[0].lower()) != -1:
                    break

            if compare_index >= len(sentence):
                match = False
                break

        if match:
            print(sentence)
            print('Recommendations are below.')
            print(sentence_groups[key])

'''
# result 생성하기
result = origin

# 결과 출력하기
print(result)
'''
