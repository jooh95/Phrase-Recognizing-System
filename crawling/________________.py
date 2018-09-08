import os
import glob
import re
import copy


def check_string(s):
    after_s = re.findall('[^A-Za-z0-9]', s)
    if len(after_s) == 0:
        return True, s
    if "-" in after_s and len(after_s) == 1 and len(s) > 1:
        return True, s
    elif "," in after_s and len(after_s) == 1 and len(s) > 1:
        re_string = re.sub('[,]', '', s)
        print(s+" : "+re_string)
        return True, re_string
    return False, ""

def main():
    os.chdir("/Users/wonjun/PycharmProjects/EngDict/data/sentences/content")
    for file in glob.glob("*.txt"):
        print(file)
        data = ""
        data = open(file, encoding='utf-8').read().lower()
        linesList = data.split("\n")
        f = open("./next_data/next_"+file, "w", encoding="utf-8")
        for line in linesList:
            words = line.split(" ")
            ch_data_line = list()
            cnt = 0
            for word in words:
                boo, result = check_string(word)
                if len(word) == 1 or len(word) == 0:
                    continue
                if (boo == True):
                    if(result != ',' and result != '--'):
                        f.write(result + " ")
                        cnt += 1
                elif (word[0] == "\'") or (word[len(word) - 1] == "\'") or (word[0] == "\"") or (word[len(word) - 1] == "\"") or (word[0] == "(") or (word[len(word) - 1] == ")") or (word[len(word) - 2] == "\'"):
                    f.write(word + " ")
                    cnt += 1


            if cnt != 0:
                f.write("\n")
        f.close()


if __name__ == '__main__':
    main()