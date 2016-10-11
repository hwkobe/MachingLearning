# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 08:59:02 2016

@author: yuehui
"""

from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt
import os

def createDataSet():
    group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A','A','B','B']
    return group,labels

def filematrix(filecontext):
    num=len(filecontext)
    datamat=zeros((num,3))
    labels=[]
    index=0
    s=''
    for line in filecontext:
        line=line.strip().split('\t')
        datamat[index,:]=line[:3]
        s+=line[-1]
        index+=1
    labelstring=['largeDoses','smallDoses','didntLike']
    for string in labelstring:
        s=s.replace(string,['3','2','1'][labelstring.index(string)])
    for i in s:
        labels.append(int(i))
    return datamat,labels
    
def filemat(filecontext):
    datamat=[]
    labels=[]
    s=''
    for line in filecontext:
        line=line.strip().split('\t')
        datamat.append(line[:3])
        s+=line[-1]
    datamat=array(datamat,dtype=float64)
    labelstring=['largeDoses','smallDoses','didntLike']
    for string in labelstring:
        s=s.replace(string,['3','2','1'][labelstring.index(string)])
    for i in s:
        labels.append(int(i))
    return datamat,labels
    
def autoNorm(dataset):
    minVals=dataset.min(0)
    maxVals=dataset.max(0)
    ranges=maxVals-minVals
    normDataset=zeros(shape(dataset))
    m=dataset.shape[0]
    normDataset=dataset-tile(minVals,(m,1))
    normDataset=normDataset/tile(ranges,(m,1))
    return normDataset,ranges,minVals

def classify(inX,dataset,labels,k):
    datasetsize=dataset.shape[0]
    diffmat=tile(inX,(datasetsize,1))-dataset
    sqdiffmat=diffmat**2
    sqdistances=sqdiffmat.sum(axis=1)
    distances=sqdistances**0.5
    sorteddistindicies=distances.argsort()
    classcount={}
    for i in range(k):
        voteilabel=labels[sorteddistindicies[i]]
        classcount[voteilabel]=classcount.get(voteilabel,0)+1
    sortedclasscount=sorted(classcount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedclasscount[0][0]
    
def dataSelfTest(normMat,labels,Ratio=0.10,k=3):
    m=normMat.shape[0]
    numTestVecs=int(Ratio*m)
    errorCount=0.0
    for i in range(numTestVecs):
        classifierResult=classify(normMat[i,:],normMat[numTestVecs:m,:,],labels[numTestVecs:m],k)
        print 'the classifier came back with: %d, the real answer is: %d' % (classifierResult,labels[i])
        if classifierResult!=labels[i]:
            errorCount+=1.0
    print 'the total error rate is: %f' % (errorCount/float(numTestVecs))

def testdataTest(traindata,trainlabel,testdata,testlabel,k=5):
    errorCount=0.0
    numtest=len(testdata)
    for i in range(numtest):
        classifierResult=classify(testdata[i],traindata,trainlabel,k)
        print 'the classifier came back with: %d, the real answer is: %d' % (int(classifierResult),int(testlabel[i]))
        if classifierResult!=testlabel[i]:
            errorCount+=1.0            
    print errorCount,'the total error rate is: %f' % (errorCount/float(numtest))
    
def classifyPerson(filecon):
    resultList=['not at all','in small does','in large does']
    ffMiles=float(raw_input('frequent flier miles earned per year?'))
    percentTats=float(raw_input('percentage of time spent playing video games?'))
    icecream=float(raw_input('liters of ice cream consumed per year?'))
    inArr=array([ffMiles,percentTats,icecream])
    data,label=filemat(filecon)
    normMat,ranges,minVals=autoNorm(data)
    classifierResult=classify((inArr-minVals)/ranges,normMat,label,3)
    print 'You will probably like this person:',resultList[classifierResult-1]       

def numrecog(path):
    pathdic=os.listdir(path)
    mat=zeros((len(pathdic),1024))
    labels,n=[],0
    for fname in pathdic:
        labels.append(fname[0])
        pathes=os.path.join(path,fname)
        f=open(pathes)
        filecontent=f.readlines()
        lines=''
        for line in filecontent:
            lines+=line.strip()
        mat[n,:]=list(lines)
        n+=1
    return mat,labels
    
if __name__ =='__main__':
##############the part of dating choosing##################################
#    f=open('/home/yuehui/Working/python/Coding/Machine-Learning/dataset/datingTestSet.txt')
#    filecon=f.readlines()
#    f.close()
#    data,label=filemat(filecon)
#    normMat,ranges,minVals=autoNorm(data)
#    dataSelfTest(normMat,label)
#    fig=plt.figure()
#    ax=fig.add_subplot(111)
#    ax.scatter(normMat[:,1],normMat[:,0],15.0*array(label),15.0*array(label))
#    plt.show()
#    classifyPerson(filecon)
############the part of number recognize####################################
    trainingpath='/home/yuehui/Working/python/Coding/Machine-Learning/dataset/digits/trainingDigits'
    trainMat,trainLabel=numrecog(trainingpath)
    testpath='/home/yuehui/Working/python/Coding/Machine-Learning/dataset/digits/testDigits/'
    #testpath='/home/yuehui/Working/python/Coding/Machine-Learning/New Folder/'
    testMat,testLabel=numrecog(testpath)
    testdataTest(trainMat,trainLabel,testMat,testLabel,3)


    
    