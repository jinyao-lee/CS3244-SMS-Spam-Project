import pandas as pd
import csv
import os

####
# Open the .csv file and load into list
####
data_dir = "C:\\Users\\jylee\\Documents\\[LOCAL]NUS Work Data\\CS3244\\SMS Spam Project\\data\\spam.csv"
df = pd.read_csv(data_dir, encoding="latin-1")

trainingSet = []
validationSet = []

with open(data_dir, encoding="latin-1") as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        trainingSet.append((row[0:3]))


####
# Shuffle data, then 20% of data to be validation set (at the very end of data)
####
import random
# random.shuffle(trainingSet)
for i in range(len(trainingSet)-1, int(0.8*len(trainingSet)), -1):
    validationSet.append(trainingSet[i])
    trainingSet.pop

print("Size of training set = " + str(len(trainingSet)))
print("Size of validation set = " + str(len(validationSet)))



####
# Following functions required to train and validate using KNN
####
def getSimilarity(record1, record2):
    len1 = len(record1[1].split())
    len2 = len(record2[1].split())
    num_common = 0
    d = dict()
    for word in record1[1].split():
        if word not in d:
            d[word] = 1
    for word in record2[1].split():
        if word in d:
            num_common += 1
    similarity = num_common / (len1 * len2) ** 0.5
    return similarity

def findKNN(train_data, record, k):
    # get the distance between every train_data and the record
    for i in range(0,len(train_data)):
        sim = getSimilarity(train_data[i], record)
        train_data[i][2] = sim
    # sort the train_data by similarity
    # from operator import itemgetter
    # train_data.sort(key = itemgetter(-1))
    # return the k nearest neighbor
    res = []
    for i in range(k):
        max_sim = 0
        max_sim_index = 0
        for i in range(0, len(train_data)):
            if train_data[i][2] > max_sim:
                max_sim = train_data[i][2]
                max_sim_index = i
        train_data[max_sim_index][2] = 0    # to ensure that no same nrighbour gets 'elected' again
        res.append(train_data[max_sim_index])
    return res

def judge(knn):
    num_ham = 0
    num_spam = 0
    for r in knn:
        if r[0] == 'ham':
            num_ham += 1
        else:
            num_spam += 1
    # print(num_ham)
    # print(num_spam)
    return "ham" if num_ham > num_spam else "spam"


####
# Print out accuracy of the KNN algorithm
####

correct = 0
wrong = 0    
k = 131

# for tracking
currIndex = 0
import copy
for d in validationSet:
    if (currIndex % 100 == 0):
        print("==== Currently processing " + str(currIndex) + " of " + str(len(validationSet)) + " validation sets ====")
    currIndex += 1

    knn = findKNN(trainingSet, d, k)   
    if judge(knn) == d[0]:
        correct += 1
    else:
        wrong += 1
        print(judge(knn))
        print(d[1])
    # print("\n")

accuracy = correct / (correct + wrong)

print("\ncorrect",correct)
print("\nwrong",wrong)
print("\naccuracy",accuracy)



####
# Try your own zaphalang messages
####

def tryYourOwnMessage(message):
    d = ['', message, '']
    knn = findKNN(trainingSet, d, k)
    print("RESULT OF: " + message + '\n' + judge(knn))

tryYourOwnMessage("<Rewards> StarHub: Starting from 100 points, you can indulge in these irresistible 1-for-1 deals with Dunkin Donuts, Ellenborough market cafe, Chicken Up& more. Grab them now at www.starhub.com/redeem . T&Cs apply. To UNSUB, reply UNSUB")
tryYourOwnMessage("INSTANT BET, INSTANT CASH FOR ONLINE SPORTSBOOK ONLINE LIVE CASINO/SLOTS HORSE RACING CLICK LINK TO APPLY http:api.whatsapp.com/send?phone=6582818137")
tryYourOwnMessage("Hi bro, just now u said that u need a soccer betting account, u prefer m8 or cmd? By the way, I hv horse racing, live casino and slot games too. U keen? Max")