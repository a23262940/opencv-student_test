import numpy as np
import cv2
import csv

train_picture = []
labels = []

with open('train.csv') as file:
    rows = csv.DictReader(file)
    for i in rows:
       # print(i['ID'],i["Label"])
        image = cv2.imread("./train_images/"+str(i['ID']))
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        train_picture += [gray]
        labels += [int(i['Label'])]

x = np.array(train_picture)
train = x.reshape(-1,262144).astype(np.float32)
train_labels = np.repeat(labels,1)[:,np.newaxis]
knn = cv2.ml.KNearest_create()
knn.train(train,cv2.ml.ROW_SAMPLE,train_labels)

id = []
labels = []

with open('test.csv',newline='') as file1:
    rows = csv.DictReader(file1)
    for i in rows:
        image = cv2.imread('./test_images/'+str(i['ID']))
        id += [i['ID']]
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        y = np.array(gray)
        test = y.reshape(-1,262144).astype(np.float32)
        ret,result,negihbours,dist = knn.findNearest(test,k=1)
        labels += [result]

with open('test1.csv','w',newline='') as file2:
    filename = ['ID','Label']
    write = csv.DictWriter(file2,fieldnames=filename)
    write.writeheader()
    for i,j in enumerate(labels):
        write.writerow({"ID": id[i],'Label': j[0][0]})

cv2.waitKey(1)
cv2.destroyAllWindows()