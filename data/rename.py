import os

list1 = os.listdir("pos_test/")
list2 = os.listdir("neg_test/")

num=250

for i in list1:
    os.rename("pos_test/"+i,"pos_test/relevant"+str(num)+".txt")
    print("relevant"+str(num)+".txt")
    num=num+1