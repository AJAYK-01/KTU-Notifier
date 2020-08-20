import csv
from pathlib import Path

with open('dataset.csv', 'r', encoding="utf8") as file:
    reader = csv.reader(file)
    pos = 0
    neg = 0
    for row in reader:
        if row[1] == "1":
            with open("pos/"+ "relevant" + str(pos) + '.txt', 'a', encoding="utf8") as fil:
                fil.write(row[0])
                pos += 1
                print(pos,neg)
        else:
            with open("neg/"+ "irrelevant" + str(neg) + '.txt', 'a', encoding="utf8") as fil:
                fil.write(row[0])
                neg += 1
                print(pos,neg)


print("\n \n pos,neg finally",pos,neg)