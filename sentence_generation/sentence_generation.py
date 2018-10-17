import nltk

# 상수
skip_word_len = 2  # X, Xs가 포함할 길이
word_gap = 1  # matching 시 단어 사이의 얼마나 많은 gap을 허용할 것인지.

# 'sentences.txt'에서 데이터 불러오기
f = open("sentences.txt", "r", encoding='UTF-8')
raw_data = f.read()
f.close()

# 한 줄 단위로 자르기
lines = [line.strip() for line in raw_data.splitlines()]
# print(lines)

# ':'로 끝나는 문장은 dictionary의 key로 분류
ref_groups = {}
key = ''
for i in range(len(lines)):
    if (i == 0 and lines[i][-1] == ':') or (i > 0 and lines[i-1] == '' and lines[i][-1] == ':'):
        # 여기서부터 밑에까지 dictionary에 value로 넣는다.
        key = lines[i][:-1]
        ref_groups[key] = []
    elif not lines[i] == '':
        ref_groups[key].append(nltk.word_tokenize(lines[i]))

print(ref_groups)

# 키보드 입력 값 받기
input_string = input()
input_tokens = nltk.word_tokenize(input_string)
input_pos = nltk.pos_tag(input_tokens)
print('input : ' + str(input_pos) + '\n')

print('matches :')

# 무시할 태그
pos_ignore = ['DT', ',']
skip = ['X', 'Xs', 'Y', 'Ys', 'Z', 'Zs', 'XYZ']
skip_pos = ['DT', 'PRP', 'PRP$', 'JJ', 'NN', 'NNS', 'NNP', 'NNPS']

for key in ref_groups:
    for ref_sentence in ref_groups[key]:
        ref_pos = nltk.pos_tag(ref_sentence)

        ref_index = 0
        input_index = 0

        gap_cnt = 0

        skip_word_save = {}
        save_on = False
        save_key = ''
        save_word_cnt = 0

        while ref_index < len(ref_pos) and input_index < len(input_pos):
            # 단어끼리 매칭이 되는 경우
            if ref_pos[ref_index][1] == input_pos[input_index][1] and \
                    ref_pos[ref_index][0].lower().find(input_pos[input_index][0].lower()) != -1:
                ref_index += 1
                input_index += 1
                save_on = False
                continue

            # X에 누적
            if save_on:
                if save_word_cnt < skip_word_len and input_pos[input_index][1] in skip_pos:
                    skip_word_save[save_key] += ' ' + input_pos[input_index][0]
                    input_index += 1
                    save_word_cnt += 1
                else:
                    save_on = False
                continue

            # X나 Y가 나타날 경우
            if ref_pos[ref_index][0] in skip and input_pos[input_index][1] in skip_pos:
                save_on = True
                save_key = ref_pos[ref_index][0]

                skip_word_save[save_key] = input_pos[input_index][0]
                save_word_cnt = 1

                ref_index += 1
                input_index += 1
                continue

            if ref_pos[ref_index][1] in pos_ignore:
                ref_index += 1
                continue
            if input_pos[input_index][1] in pos_ignore:
                input_index += 1
                continue

            ref_index += 1

            gap_cnt += 1
            if gap_cnt > word_gap:
                break

        if input_index >= len(input_pos):  # match
            print(ref_sentence)
            # print(skip_word_save)
            print(ref_groups)
            print()
'''
# result 생성하기
result = origin

# 결과 출력하기
print(result)
'''
