import csv
from pathlib import Path

with open('try.csv', 'r', encoding="utf8") as file:
    reader = csv.reader(file)
    pos = 160
    neg = 160
    for row in reader:
        if row[1] == "1":
            with open("pos_train/"+ "relevant" + str(pos) + '.txt', 'a', encoding="utf8") as fil:
                fil.write(row[0])
                pos += 1
                print(pos,neg)
        else:
            with open("neg_train/"+ "irrelevant" + str(neg) + '.txt', 'a', encoding="utf8") as fil:
                fil.write(row[0])
                neg += 1
                print(pos,neg)


print("\n \n pos,neg finally",pos,neg)