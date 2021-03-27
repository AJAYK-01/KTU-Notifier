import csv
count=-1
content_less=0
with open('newdatatemp.csv', 'r') as file:
    reader = csv.reader(file)
    newreader=[]
    for row in reader:
        count=count+1
        if(count==0):
            continue
        try:
            if(str(row[1])==""):
                row[1]=row[0]
                row[1].replace('"','')
            newreader.append(row[1:])
        except:
            print("error",count)

    file = open('try.csv', 'w+', newline ='')
    with file:
        write = csv.writer(file)
        write.writerows(newreader)



        
