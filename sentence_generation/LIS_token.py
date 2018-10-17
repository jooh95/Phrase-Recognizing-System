from conjugation import lemmatize

# 'sentences.txt'에서 데이터 불러오기
f = open("sentences.txt", "r", encoding='UTF-8')
raw_data = f.read()
f.close()
# 한 줄 단위로 자르기
lines = [line.strip() for line in raw_data.splitlines()]

# 사용자 입력 문장 불러오기
in_sent = input()
# tokenizing and lemmatizing input sentence
in_sent = lemmatize(in_sent)
print(in_sent)

match_len = 0
match_sent = ''

for line in lines:
    comp_sent = lemmatize(line)
    print(comp_sent)

    # 최장 증가 수열
    d = [[0] * (len(comp_sent) + 1) for i in range(2)]
    for i in range(1, len(in_sent)+1):
        for j in range(1, len(comp_sent)+1):
            this_row = i % 2
            former_row = 1 - this_row
            d[this_row][j] = max(d[former_row][j],
                                 d[this_row][j-1],
                                 d[former_row][j-1]+1
                                 if in_sent[i-1].lower() == comp_sent[j-1].lower() else d[former_row][j-1])

    match_point = d[len(in_sent) % 2][len(comp_sent)]
    if match_point > match_len:
        match_len = match_point
        match_sent = line

print(match_sent)
