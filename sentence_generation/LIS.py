import nltk
import math

# 상수
skip = 2  # 두 단어는 건너뛰어도 된다
match_percent = 0.66

in_sent = input().lower()

# 'sentences.txt'에서 데이터 불러오기
f = open("sentences.txt", "r", encoding='UTF-8')
raw_data = f.read()
f.close()
# 한 줄 단위로 자르기
lines = [line.strip() for line in raw_data.splitlines()]

# tokenizing
'''
in_sent = nltk.word_tokenize(in_sent.lower())
comp_sent = nltk.word_tokenize(comp_sent.lower())
'''

match_len = -99999

for line in lines:
    comp_sent = line.lower()
    # character 단위
    # 최장 증가 수열
    d = [[0] * (len(comp_sent) + 1) for i in range(2)]
    for i in range(1, len(in_sent)+1):
        for j in range(1, len(comp_sent)+1):
            this_row = i % 2
            former_row = 1 - this_row
            d[this_row][j] = max(d[former_row][j],
                                 d[this_row][j-1],
                                 d[former_row][j-1]+1 if in_sent[i-1] == comp_sent[j-1] else d[former_row][j-1])

    match_point = d[len(in_sent) % 2][len(comp_sent)]  # * (-0.1 * math.log(len(comp_sent)+1, 10))
    if match_point > match_len:
        match_len = match_point
        match_sent = comp_sent

print(match_sent)
