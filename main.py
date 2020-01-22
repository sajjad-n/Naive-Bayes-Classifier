import xlrd
import math
import random


def average(data_list):
    sum = 0
    for i in range(0, len(data_list)):
        sum = sum + data_list[i]
    return sum / len(data_list)


def standard_deviation(data_list):
    avg = average(data_list)
    std = 0
    for i in range(0, len(data_list)):
        std = std + math.pow((data_list[i] - avg), 2)
    var = std / len(data_list)
    return math.sqrt(var)


def possibility(x, avg, std):
    return (1 / (math.sqrt(2 * math.pi) * std)) * math.exp(-1 / 2 * math.pow((x - avg) / std, 2))


w1 = []  # pass - 1
w2 = []  # not pass - 0
avg1 = 0
std1 = 0
avg2 = 0
std2 = 0

# reading training set
sheet = xlrd.open_workbook("Training Set.xlsx")
trainingSet = sheet.sheet_by_index(0)

for i in range(0, trainingSet.nrows):
    iq = trainingSet.cell_value(i, 0)
    label = trainingSet.cell_value(i, 1)
    if label == 1:
        w1.append(iq)
    else:
        w2.append(iq)

print("\nw1: ", w1, "\nw2: ", w2, "\n")

# calculating c1 and c2
p_w1 = len(w1) / trainingSet.nrows
p_w2 = len(w2) / trainingSet.nrows

# calculating average and standard deviation
avg1 = average(w1)
std1 = standard_deviation(w1)
avg2 = average(w2)
std2 = standard_deviation(w2)
print("w1-> avg:", avg1, " std:", std1, " p(w1):", p_w1, "\nw2-> avg:", avg2, " std:", std2, " p(w2):", p_w2, "\n")

# reading test set
sheet = xlrd.open_workbook("Test Set.xlsx")
testSet = sheet.sheet_by_index(0)

# predict test data
noOfTruePredicts = 0
for i in range(0, testSet.nrows):
    testLabel = testSet.cell_value(i, 1)
    testIQ = testSet.cell_value(i, 0)
    p1 = possibility(testIQ, avg1, std1) * p_w1
    p2 = possibility(testIQ, avg2, std2) * p_w2

    if p1 > p2:
        print("IQ:", testIQ, " predict: 1", " label:", testLabel)
        if testLabel == 1:
            noOfTruePredicts = noOfTruePredicts + 1
    elif p1 < p2:
        print("IQ:", testIQ, " predict: 0", " label:", testLabel)
        if testLabel == 0:
            noOfTruePredicts = noOfTruePredicts + 1
    else:
        print("IQ:", testIQ, " predict:", random.randint(0, 1), "(randomly)", " label:", testLabel)

accuracy = (noOfTruePredicts / testSet.nrows) * 100
print("\nNumber of true predicts:", noOfTruePredicts, ' of', testSet.nrows)
print("Accuracy is:", round(accuracy), "%")
