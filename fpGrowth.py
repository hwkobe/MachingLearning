# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 10:20:55 2016

@author: yuehui
"""
import json
import time
class treeNode:
    def __init__(self,nameValue,numOccur,parentNode):
        self.name=nameValue
        self.count=numOccur
        self.nodeLink=None
        self.parent=parentNode
        self.children={}
    
    def inc(self,numOccur):
        self.count+=numOccur
        
    def disp(self,ind=1):
        print '  '*ind,self.name,'  ',self.count
        for child in self.children.values():
            child.disp(ind+1)
            
def createTree(dataSet,minSup=1):
    headerTable={}
    for trans in dataSet:
        for item in trans:
            headerTable[item]=headerTable.get(item,0)+dataSet[trans]
    for k in headerTable.keys():
        if headerTable[k]<minSup:
            del(headerTable[k])
    freqItemSet=set(headerTable.keys())
    if len(freqItemSet)==0:  return None,None
    for k in headerTable:
        headerTable[k]=[headerTable[k],None]
    retTree=treeNode('Null Set',1,None)
    for tranSet,count in dataSet.items():
        localD={}
        for item in tranSet:
            if item in freqItemSet:
                localD[item]=headerTable[item][0]
        if len(localD)>0:
            orderedItems=[v[0] for v in sorted(localD.items(),key=lambda p:p[1],reverse=True)]
            updateTree(orderedItems,retTree,headerTable,count)
    return retTree,headerTable
    
def updateTree(item,inTree,headerTable,count):
    if item[0] in inTree.children:
        inTree.children[item[0]].inc(count)
    else:
        inTree.children[item[0]]=treeNode(item[0],count,inTree)
        if headerTable[item[0]][1]==None:
            headerTable[item[0]][1]=inTree.children[item[0]]
        else:
            updateHeader(headerTable[item[0]][1],inTree.children[item[0]])
    if len(item)>1:
        updateTree(item[1::],inTree.children[item[0]],headerTable,count)
        
def updateHeader(nodeToTest,targetNode):
    while (nodeToTest.nodeLink !=None):
        nodeToTest=nodeToTest.nodeLink
    nodeToTest.nodeLink=targetNode
    
def loadsimdata():
    simDat=[['r','z','h','j','p'],['z','y','x','w','v','u','t','s'],['z'],['r','x','n','o','s'],
            ['y','r','x','z','q','t','p'],['y','z','x','e','q','s','t','m']]
    return simDat
    
def createData(dictory,minsup=0):
    dataset=[]
    for key1 in dictory:
        lt=[]
        for key2 in dictory[key1]:
            if dictory[key1][key2]>minsup:
                lt.append(key2)
        dataset.append(lt)
    return dataset
                
def createInitSet(dataSet):
    retDict={}
    for trans in dataSet:
        #retDict[frozenset(trans)]=1
        retDict[frozenset(trans)]=retDict.get(frozenset(trans),0)+1
    return retDict
    
def ascendTree(leafNode,prefixPath):
    if leafNode.parent!=None:
       prefixPath.append(leafNode.name)
       ascendTree(leafNode.parent,prefixPath)
        
def findPrefixPathway(basePat,headtab):
    condPats={}
    copynode=headtab[basePat][1]
    while headtab[basePat][1]!=None:
        prefixPath=[]
        ascendTree(headtab[basePat][1],prefixPath)
        if len(prefixPath)>1:
            condPats[frozenset(prefixPath[1:])]=headtab[basePat][1].count
        #print condPats
        headtab[basePat][1]=headtab[basePat][1].nodeLink
    headtab[basePat][1]=copynode
    return condPats

def findPrefixPath(basePat,treeNode):
    condPats={}
    while treeNode!=None:
        prefixPath=[]
        ascendTree(treeNode,prefixPath)
        if len(prefixPath)>1:
            condPats[frozenset(prefixPath[1:])]=treeNode.count
        #print condPats
        treeNode=treeNode.nodeLink
    return condPats
    
def mineTree(inTree,headerTable,minSup,preFix,freqItemList):
    if bool(headerTable)==bool(None):
        return 'There is no item meet your requirement'
    bigL=[v[0] for v in sorted(headerTable.items(),key=lambda p: p[1])]
    #print bigL
    for basePat in bigL:
        #print basePat
        newFreqSet=preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(list(newFreqSet))
        condPattBases=findPrefixPath(basePat,headerTable[basePat][1])
        myCondTree,myHead=createTree(condPattBases,minSup)
        #print myHead
        if myHead!=None:
            #print 'conditional tree for:',newFreqSet
            #myCondTree.disp(1)
            mineTree(myCondTree,myHead,minSup,newFreqSet,freqItemList)
    
def changeForm(freq):  #if freq=[[lys2,lys1,asp1],[lys2,asp1]]
    for i in freq:     #then after changeForm  freq=[[asp1,lys2]]
       i.sort()
    chfreq=[]
    for item in freq:
        dic={}
        for it in item:
            dic[it[:3]]=it[-1]
        item=[]
        for k in dic:
            item.append(k+dic[k])
        item.sort()
        if item not in chfreq:
            chfreq.append(item)
    chfreq.sort(key=len)
    return chfreq
    
def getFreq(atomnumdic,support=150):
    dataset=createData(atomnumdic)
    initset=createInitSet(dataset)
    myfptree,myhead=createTree(initset,support)
    freq=[]
    #time1=time.time()
    mineTree(myfptree,myhead,support,set([]),freq)
    freq=changeForm(freq)
    freq.sort(key=len)
    return freq

def getFreqaa(freq,n):
    aalt,Ind=[],[]
    for item in freq:
        a=0
        for it in item:
            a+=int(it[-1])
        if a==n:
            Ind.append(freq.index(item))
    for index in Ind:
        for aa in freq[index]:
            if aa[:-1] not in aalt:
                aalt.append(aa[:-1])
    return aalt
    
def getaanum(freq):
    Ind=[]
    for item in freq:
        a=0
        for it in item:
            a+=int(it[-1])
        Ind.append(a)
    num=max(Ind)
    return num
if __name__=='__main__':
#   simdata=loadsimdata()
#   initset=createInitSet(simdata)
#   fptree,headtab=createTree(initset,3)
#   cod=findPrefixPathway('x',headtab)
#   print cod
#   con=findPrefixPath('x',headtab['x'][1])
#   print con
#   freq=[]
#   mineTree(fptree,headtab,3,set([]),freq)
   f=open('/home/yuehui/Working/DATASETS/aanumdicRBScoreD381.txt')
   atomdic=json.loads(f.readline())
   f.close()
   support=190
   dataset=createData(atomdic)
   initset=createInitSet(dataset)
   myfptree,myhead=createTree(initset,support)
   freq=[]
   #time1=time.time()
   mineTree(myfptree,myhead,support,set([]),freq)
   freq=changeForm(freq)
   print len(freq)
   #print freq
   #time2=time.time()
   #print time2-time1
   num=getaanum(freq)
   aalt=getFreqaa(freq,3)
   print num
   print aalt