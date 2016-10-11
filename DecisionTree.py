# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 16:28:28 2016
@author: hwkobe
"""
import operator
from math import log
import TreePlotter


def CalcShannonEnt(dataset):
    NumEntries = len(dataset)
    LabelCounts = {}
    for feature in dataset:
        CurrentLabel = feature[-1]
        if CurrentLabel not in LabelCounts.keys():
            LabelCounts[CurrentLabel] = 0
        LabelCounts[CurrentLabel] += 1
    ShannonEnt = 0.0
    for key in LabelCounts:
        prob = float(LabelCounts[key])/NumEntries
        ShannonEnt -= prob * log(prob,2)
    return ShannonEnt
    
def SplitDataSet(dataset, axis, value):
    RetDataSet = []
    for feature in dataset:
        if feature[axis] == value:
            reducedFeature = feature[:axis]
            reducedFeature.extend(feature[axis+1:])
            #print reducedFeature
            RetDataSet.append(reducedFeature)
    return RetDataSet
    
def ChooseBestFeature(dataset):
    NumFeatures = len(dataset[0]) - 1
    BaseEntropy = CalcShannonEnt(dataset)
    BestInfoGain = 0.0; BestFeature = -1
    for i in range(NumFeatures):
        FeatList = [example[i] for example in dataset]
        UniqueVals = set(FeatList)
        #print UniqueVals
        NewEntropy = 0.0
        for value in UniqueVals:
            SubDataSet = SplitDataSet(dataset,i,value)
            prob = len(SubDataSet)/float(len(dataset))
            NewEntropy += prob * CalcShannonEnt(SubDataSet)
        inforGain = BaseEntropy - NewEntropy
        #print BaseEntropy, inforGain
        if (inforGain >= BestInfoGain):
            BestInfoGain = inforGain
            BestFeature = i
    return BestFeature
    
def MajorityCnt(ClassList):
    ClassCount = {}
    for vote in ClassList:
        if vote not in ClassCount.keys(): ClassCount[vote] = 0
        ClassCount[vote] += 1
    sortedClassCount = sorted(ClassCount.iteritems(),key=operator.itemgetter(1),reverse = True)
    return sortedClassCount[0][0]
    
def CreatTree(dataset,labels):
    ClassList = [example[-1] for example in dataset]
    if ClassList.count(ClassList[0]) == len(ClassList):
        return ClassList[0]
    if len(dataset[0]) == 1:
        return MajorityCnt(ClassList)
    BestFeat = ChooseBestFeature(dataset)
    BestFeatLabel = labels[BestFeat]
    myTree = {BestFeatLabel:{}}
    del(labels[BestFeat])
    FeatValues = [example[BestFeat] for example in dataset]
    UniqueVals = set(FeatValues)
    for value in UniqueVals:
        SubLabels = labels[:]
        myTree[BestFeatLabel][value] = CreatTree(SplitDataSet(dataset,BestFeat,value),SubLabels)
    return myTree

def Classify(InputTree,FeatLabels,TestVec):
    ClassLabel = 'B'
    FirstStr = InputTree.keys()[0]
    SecondDict = InputTree[FirstStr]
    FeatIndex = FeatLabels.index(FirstStr)
    for key in SecondDict.keys():
        if TestVec[FeatIndex] == key:
            if type(SecondDict[key]).__name__=='dict':
                ClassLabel = Classify(SecondDict[key],FeatLabels,TestVec)
            else: ClassLabel = SecondDict[key]
    return ClassLabel

if __name__ == '__main__':
    dataset = [[u'T', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'D', u'P', u'B', 'no'], [u'D', u'P', u'B', 'no'], [u'D', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'D', u'P', 'no'], [u'T', u'P', u'D', 'no'], [u'D', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'D', 'no'], [u'T', u'P', u'B', 'no'], [u'D', u'P', u'D', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'D', 'no'], [u'T', u'P', u'B', 'no'], [u'D', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'D', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'D', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'D', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'D', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'D', 'no'], [u'T', u'N', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'D', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'P', u'P', 'no'], [u'T', u'P', u'B', 'no'], [u'T', u'D', u'P', 'yes'], [u'D', u'D', u'B', 'yes'], [u'D', u'N', u'B', 'yes'], [u'D', u'D', u'D', 'yes'], [u'D', u'D', u'D', 'yes'], [u'D', u'A', u'D', 'yes'], [u'T', u'D', u'P', 'yes'], [u'T', u'D', u'B', 'yes'], [u'D', u'D', u'D', 'yes'], [u'T', u'D', u'D', 'yes'], [u'T', u'N', u'B', 'yes'], [u'D', u'A', u'D', 'yes'], [u'T', u'D', u'D', 'yes'], [u'T', u'D', u'D', 'yes'], [u'D', u'D', u'D', 'yes'], [u'D', u'D', u'D', 'yes'], [u'T', u'D', u'D', 'yes'], [u'D', u'A', u'D', 'yes'], [u'D', u'D', u'D', 'yes'], [u'D', u'D', u'D', 'yes'], [u'D', u'A', u'D', 'yes'], [u'D', u'D', u'D', 'yes'], [u'D', u'D', u'D', 'yes'], [u'T', u'D', u'B', 'yes'], [u'T', u'D', u'P', 'yes'], [u'D', u'D', u'D', 'yes'], [u'D', u'D', u'D', 'yes'], [u'T', u'D', u'D', 'yes'], [u'T', u'D', u'D', 'yes'], [u'T', u'D', u'D', 'yes'], [u'D', u'D', u'D', 'yes'], [u'T', u'D', u'B', 'yes'], [u'T', u'P', u'B', 'yes'], [u'D', u'D', u'D', 'yes'], [u'D', u'A', u'P', 'yes'], [u'T', u'D', u'D', 'yes'], [u'D', u'D', u'P', 'yes'], [u'T', u'D', u'D', 'yes'], [u'T', u'D', u'D', 'yes'], [u'T', u'D', u'D', 'yes'], [u'T', u'D', u'D', 'yes'], [u'D', u'D', u'D', 'yes'], [u'T', u'N', u'B', 'yes'], [u'D', u'N', u'B', 'yes'], [u'T', u'D', u'D', 'yes'], [u'D', u'D', u'D', 'yes'], [u'D', u'D', u'D', 'yes'], [u'D', u'D', u'D', 'yes'], [u'D', u'A', u'D', 'yes'], [u'T', u'N', u'B', 'yes']]#[[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels = ['surfacing','flippers','ff']
    myTree = CreatTree(dataset,labels)
    print myTree
    TreePlotter.CreatPlot(myTree)    

       