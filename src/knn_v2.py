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
random.shuffle(trainingSet)
for i in range(len(trainingSet)-1, int(0.8*len(trainingSet)), -1):
    validationSet.append(trainingSet.pop())

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
k = 13


for k in range(71, 80, 2):

    # for tracking
    currIndex = 0
    import copy
    for d in validationSet:
        if (currIndex % 100 == 0):
            print("==== Currently processing " + str(currIndex) + " of " + str(len(validationSet)) + " validation sets ====")
        currIndex += 1

        knn = findKNN(trainingSet, d, k)   
        if judge(knn) == d[0]:  # If the predicted output is the same as the one in training data
            correct += 1
        else:
            wrong += 1
            # print(judge(knn))
            # print(d[1])
        # print("\n")

    accuracy = correct / (correct + wrong)

    print("\nk-value: ", k)
    print("correct: ",correct)
    print("wrong: ",wrong)
    print("training data accuracy: ",accuracy)
    
    with open(r"C:\Users\jylee\Documents\[LOCAL]NUS Work Data\CS3244\SMS Spam Project\data\kValidationError_v2.csv", 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow([k, 1-accuracy])
        csvFile.close()



####
# Try your own zaphalang messages
####
# numHamTotal = int(0)
# numSpamTotal = int(0)
# def tryYourOwnMessage(message):
#     global numHamTotal, numSpamTotal
#     d = ['', message, '']
#     knn = findKNN(trainingSet, d, k)
#     print("RESULT OF: -\n" + message + '\n=== ' + judge(knn) + ' ===\n')
#     if judge(knn) == 'ham':
#         numHamTotal += 1
#     else:
#         numSpamTotal += 1

# #HAMS
# tryYourOwnMessage("<Rewards> StarHub: Starting from 100 points, you can indulge in these irresistible 1-for-1 deals with Dunkin Donuts, Ellenborough market cafe, Chicken Up& more. Grab them now at www.starhub.com/redeem . T&Cs apply. To UNSUB, reply UNSUB")
# tryYourOwnMessage("<Rewards> StarHub: Get your hands on our 1-for-1 lunch buffet, Korean chicken wings, Bingsoo dessert to keep cool in this hot weather & more! Check it out at www.starhub.com/redeem now. T&Cs apply. To UNSUB, reply UNSUB")

# #SPAMS
# tryYourOwnMessage("INSTANT BET, INSTANT CASH FOR ONLINE SPORTSBOOK ONLINE LIVE CASINO/SLOTS HORSE RACING CLICK LINK TO APPLY http:api.whatsapp.com/send?phone=6582818137")
# tryYourOwnMessage("Hi bro, just now u said that u need a soccer betting account, u prefer m8 or cmd? By the way, I hv horse racing, live casino and slot games too. U keen? Max")
# tryYourOwnMessage("🔥We say YES when the bank say No🔥 💲Let us support your loan 🏧Flash approval + Instant Cash 🏦Offering Monthly Loan Up To 20 Months Repayment Term         💰💰💰💰💰💰💰💰 $5000 x 20Mnths =$320,    $8000 x 20Mnths =$480, $10,000 x 20Mnths = $600 Consolidate Loan    ☎Enquiries Call  +65 8627-342 Whatsapp        +65 8279-4186")
# tryYourOwnMessage("💲💲💲Ucash Credit💲💲💲 www.ucash77.com 🔥Personal Loan Flexible repayment singapore 🔥Foreigner Loan Fast processing & approval (Malaysian & Filipino) ⚠Strictly  Kept Confidential⚠ Contact & inquiries 📞📞📞 📞. Whatsapp +65 82676817 📞. Whatsapp +65 86489767  📞. Wechat (微信）- 6582676817")
# tryYourOwnMessage(" 💁🏻💁🏻‍♂🔈🔉🔊💰💰💰		🎖🎖🎖		ASIA ONLINE SPORTBOOKS 📲🖥		ONLINE SPORTSBET      ⚽⚾🏀🏈🏉🎾🎱🎳⛳🏌⛹🏐🏑🏒🏓		^Cash/Credit📲💻	LIVE CASINO AND JACKPOT GAMES	🎲⚀⚁⚂⚃⚄⚅🎲	🃏🃏🃏🎰🎰🎰	^Cash/Credit📲💻	HORSE RACING ACCOUNT	🥇🥈🐎🏇🐎🏇🐎	^Cash only📲💻		CASH^ 💰💰💰💰💰- Only Cash top up & Withdrawal accepted (Daily)	*Cash 💰💰💰     🏧Top Up - 24hrs		*Withdrawal 💰💰💰      🏧1300hrs - 1900hrs	CREDIT^^ (negotiable)		*Weekly Settlement    (Win/Loss)	*Credits given depending on income proof		ALL INTERESTED 🚻🆗🙋‍♂🙋‍♂🙋🙋🙋🙋‍♂🙋‍♂🙋‍♂	TO CHECK OUT LATEST PROMOTION WITH OUR FRIENDLY STAFFS @	📳 whatsapp 👍👍👍 (MARK)	65 84201070		 📞 65 84215787		Working hours 24hrs		THIS IS AN AUTO GENERATED NUMBER ONLY REPLY TO 84215787")
# tryYourOwnMessage("NEWLY COMPANY OPEN AREA ON SERANGOON 10K x36 MONTHS=330 20K x 36 MONTHS =660 50K x36 MONTHS=1600 100K x 36 MONTHS =3350 whatsapp me on 87321404 Bosco")
# tryYourOwnMessage("We provide online Sports Bet/Horse Racing/Live Casino Games with Daily Withdrawal.50% Welcome Bonus. Please WHATSAPP Winston For More Details at 83179087.")
# tryYourOwnMessage("NEWLY OFFER ! 10K x36 MONTHS=330 20K x 36 MONTHS =660 50K x 60 MONTHS=970 100K x 60 MONTHS =1940 whatsapp me on 87321404 Aaron")
# tryYourOwnMessage("360GLOBAL >Guaranteed Payout >Credit/Cash >High BONUS >SportBook >LiveCasino/Slot >Horse&Hound Racing CLICK LINK")
# tryYourOwnMessage("ABK Credit. We provide Business and Personal Loans. Monthly Installment Packages. 👉🏻 S$10000= 900 x 12 Months 👉🏻 S$20000= 1800 x 12 Months 👉🏻 S$30000= 2750 x 12 Months Up to 100k Do visit our website for more information, www.abkcredit.com Whatsapp : Kelvin Lim Click on the Below Link to message me without saving my number. https://wa.me/6584141640 This is an System Generated Message. For Enquiry , Please Click on Not Now👇🏻 at Bottom and Contact with us Directly.")

# print()
# print("Total number of HAM = " + str(numHamTotal))
# print("Total number of SPAM = " + str(numSpamTotal))