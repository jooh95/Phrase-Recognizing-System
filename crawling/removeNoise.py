import os
import glob

os.chdir('./sentences')
data = ""
for file in glob.glob("*.txt"):
    print(file)
    data += open(file).read().lower()
f = open("../midData.txt", "w");
f.write(data)
f.close()
print("close file")

path = 'midData.txt'
text = open(path).read().lower()
data = text
linesList = data.split("\n")
ch_data = list()

f = open("./ch_data3.txt", "w")

for line in linesList:
    words = line.split(" ")
    ch_data_line = list()
    for word in words:
        if(len(word) >= 3):
            if(word.isalpha()):
                f.write(word + " ")
    f.write("\n")
f.close()
