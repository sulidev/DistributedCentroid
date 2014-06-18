import csv
import pickle
from numpy import vstack,array
from scipy.cluster.vq import kmeans,vq
import os

def computeDistance(dTestRow,dCentroid):
    from scipy.spatial.distance import euclidean
    jarak = []
    for row in dCentroid:
        jarak.append(euclidean(dTestRow,row))

    jos = 999999999999
    c = 0
    idx = 9999
    for s in jarak:
        if(s < jos):
            jos = s
            idx = c
        c = c + 1
    return jos,idx

def cekFile():
    if(os.path.exists('centroids.txt')):
        return True
    else:
        return False

def loadData():
    dTrain = []
    dloaded = []
    if(cekFile()!=True):
        dTrain = open('data training.csv', 'rb')
    else:
        dCentroid = open('centroids.txt', 'rb')
        dloaded = pickle.load(dCentroid)

    dTesting = open('data testing.csv', 'rb')
    reader = csv.reader(dTesting)
    myarr = []
    for row in reader:
        nrow = []
        for col in row:
            nrow.append(float(col))
        myarr.append(nrow)

    return dTrain,myarr,dloaded

def computeCentroid(dTrain):
    reader = csv.reader(dTrain)
    myarr = []
    for row in reader:
        nrow = []
        for col in row:
            nrow.append(float(col))
        myarr.append(nrow)

    data = vstack(myarr)
    centroids,_ = kmeans(data,23)
    pickle.dump(centroids,open('centroids.txt','wb'))
    return centroids

def main():
    import dispy

    dTrain,dTesting,dCentroid = loadData()
    if(cekFile()!=True):
        dCentroid = computeCentroid(dTrain)

    cluster = dispy.JobCluster(computeDistance, nodes=['10.151.62.21','10.151.38.67'])
    jobs = []
    for x in range(1000):
        job = cluster.submit(dTesting[x],dCentroid)
        jobs.append(job)

    for job in jobs:
        jos,idx = job()
        print 'Distance %d in class %d' % (jos,idx)

if __name__ == '__main__':
    main()
