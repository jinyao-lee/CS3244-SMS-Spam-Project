##################
# Difference between knn_v2 and knn_v3: -
#   knn_v2: Randomly shuffles and takes 20% of the training set as the validation set.
#   knn_v3: Randomly shuffles, then splits the data into 10 blocks. This implements 10-fold cross validation.
##################

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
# Cleans and rids message of any funny characters, leaving only alphanumeric characters,
#   and certain special characters.
####
def cleanMessage(message):
    message = message.lower()
    message = str(message)

    i = 0
    while i < len(message):
        if i >= len(message):
            print(i, " ", len(message))
        
        if ord(message[i]) < 32 or ord(message[i]) > 126:
            message = message[:i] + " " + message[i+1:]
        i += 1
    return message

# Clean the training set first
for i in range(len(trainingSet)):
    trainingSet[i][1] = cleanMessage(trainingSet[i][1])


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
    similarity = num_common / (len1 + len2) ** 0.5
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
# Shuffle data, then implement 10-fold validation
####
import random
random.shuffle(trainingSet)
chunkSize = int(0.1 * len(trainingSet))
dataChunk = []

for i in range(0, len(trainingSet), chunkSize):
    if len(trainingSet)-i < chunkSize:
        break
    dataChunk.append(trainingSet[i:i+chunkSize])



print("Size of entire set = " + str(len(trainingSet)))
print("Number of chunks = " + str(len(dataChunk)))


####
# Print out accuracy of the KNN algorithm
####

correct = 0
wrong = 0    
k = 7   # Optimal k-value is 7 for this application


for k in range(1, 31, 2):
    cumulativeAccuracy = 0.0
    for validationChunkNumber in range(len(dataChunk)):
        validationDataSet = dataChunk[validationChunkNumber]

        trainingDataSet = []
        for i in range(len(dataChunk)):
            if i == validationChunkNumber:
                continue
            trainingDataSet.extend(dataChunk[i])

        print("Size of trainingSet: ", len(trainingDataSet))
        print("Size of validationSet: ", len(validationDataSet))
        print("Currently processing batch ", validationChunkNumber, " of ", len(dataChunk)-1, " for K = ", k, "...")

        for d in validationDataSet:
            knn = findKNN(trainingDataSet, d, k)   
            if judge(knn) == d[0]:  # If the predicted output is the same as the one in training data
                correct += 1
            else:
                wrong += 1
        cumulativeAccuracy += correct / (correct + wrong)
        correct = wrong = 0

    cumulativeAccuracy = cumulativeAccuracy/len(dataChunk)
    print("\nAccuracy for K = ", k, ": ", cumulativeAccuracy, "\n\n")

    # Write to CSV file for purpose of analyzing
    with open(r"C:\Users\jylee\Documents\[LOCAL]NUS Work Data\CS3244\SMS Spam Project\data\kValidationError.csv", 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow([k, 1-cumulativeAccuracy])
        csvFile.close()



####
# Try your own zaphalang messages
####
numHamTotal = int(0)
numSpamTotal = int(0)
def tryYourOwnMessage(message):
    message = cleanMessage(message)

    global numHamTotal, numSpamTotal
    d = ['', message, '']
    knn = findKNN(trainingSet, d, k)
    print("RESULT OF: -\n" + message + '\n=== ' + judge(knn) + ' ===\n')
    if judge(knn) == 'ham':
        numHamTotal += 1
    else:
        numSpamTotal += 1


# tryYourOwnMessage("Type your message here.")
