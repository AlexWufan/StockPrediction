import sqlite3
import numpy as np
import math
import fetchdata2
import csv
import itertools

alpha = 0.005
beta = 11.1
M = 5
N = 10

def bayes_predict(name='YHOO'):
    # #read data from db
    global Y
    Y = fetchdata2.get_data(name)
    Y = Y[-10:]
    # print 'The trend is :'
    predicted_price = getm(N+1)[0][0]
    # print predicted_price
    price=[predicted_price]
    Y = Y.reshape(1,10).tolist()
    w=[]
    w=Y[0]
    w.append(price[0])
    # print w
    a = [round(i, 3) for i in w]
    return a

# Y = fetchdata.get_data('YHOO')

# #loadCsv
# def loadCsv(filename):
#     lines = csv.reader(open(filename, "rb"))
#     dataset = list(lines)
#     for i in range(len(dataset)):
#         dataset[i] = [float(x) for x in dataset[i]]
#     return dataset


# #load data from csv file
# filename = 'aapl1.csv'
# dataset = loadCsv(filename)
# print ('load data file {0} with {1} rows').format(filename, len(dataset))
# dataset.reverse()
# dataset = list(itertools.chain(*dataset))
# actual_price = dataset[10:11]
# print 'The actual price is ' + str(actual_price[0])
# dataset = dataset[0:10]

# load data from test csv file
# filename = 'data5.csv'
# dataset = loadCsv(filename)
# print ('load data file {0} with {1} rows').format(filename,len(dataset))
# dataset = list(itertools.chain(*dataset))





# try to output image, not implemented yet #######
# np.random.normal(Y.mean(), Y.std())
#
# mu, sigma = 0, 0.1 # mean and standard deviation
# s = np.random.normal(mu, sigma, 1000)
# #print s
#
# count, bins, ignored = plt.hist(s, 30, normed=True)
# plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
#                np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
#          linewidth=2, color='r')
# plt.show()

# get phi x
def getfy(x):
    fy = []
    for i in range(M + 1):
        fy.append(math.pow(x, i))
    fy = np.array(fy)
    fy = fy.reshape(fy.size, 1)
    return fy


# print getfy(11)
# print getfy(M).shape

# get inverseS
def getInverseS():
    I = np.eye((M + 1))
    temp = np.zeros([M + 1, 1])
    fy2 = getfy(N + 1)
    for i in range(1, N + 1):
        fy = getfy(i)

        # temp = temp + fy
        temp = temp + fy.dot(fy2.T)
    # inverseS = alpha*I + beta*(temp).dot(fy2.T)
    #same result!!!!!!!!!!!!!
    inverseS = alpha * I + beta * (temp)
    # print inverseS
    return inverseS


# get S^2, cunrrently useless
# def getInverseS2(x):
#     fy = getfy(x)
#     inverseS = getInverseS()
#     inverseS2 = beta**-1 + fy.T.dot(inverseS).T.dot(fy).dot(Y)
#     return inverseS2

# get m(x)
def getm(x):
    temp = np.zeros([M + 1, 1])
    for i in range(1, N + 1):
        fy = getfy(i)
        # print fy
        # print Y[i-1]
        temp += fy * Y[i - 1]
        # print temp
    fy2 = getfy(x)
    # print temp
    # print fy2
    S = np.linalg.inv(getInverseS())
    # print S
    m = beta * fy2.T.dot(S).dot(temp)
    return m




if __name__=='__main__':
    print bayes_predict('TWTR')

# price = bayes_predict('AAPL')
# print 'the predicted price is %f' % price

# print 'the absolute mean error is %f' % abs(predicted_price - actual_price[0])
# print 'the relative error is %f' % (abs(predicted_price - actual_price[0]) / float(actual_price[0]))
