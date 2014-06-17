#def compute():


def loadData():
    dTrain = open("data training.csv", "rb")
    dTesting = open("data testing.csv", "rb")
    return dTrain,dTesting

def main():
    import dispy
    import csv
    from numpy import vstack,array
    from scipy.cluster.vq import kmeans,vq

    dTrain,dTesting = loadData()
    reader = csv.reader(dTrain);
    myarr = []
    for row in reader:
        nrow = []
        for col in row:
            nrow.append(float(col))
        myarr.append(nrow)

    data = vstack(myarr)
    centroids,_ = kmeans(data,23)
    #cluster = dispy.JobCluster(compute)

if __name__ == '__main__':
    main()
