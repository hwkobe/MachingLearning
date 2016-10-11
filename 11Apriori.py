# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 09:33:59 2016

@author: yuehui
"""
import sys
sys.path.append('/home/yuehui/Working/python/PDB/PDB try/UsedCode/')
#import Atom_types
import json

####################normal pattern recognize##################################
def Patternfind(dic,pattern,m,minsupport,minoccur):
    ylt=dic.keys()
    #xlt=dic[ylt[0]].keys()
    lt,N=[],len(ylt)
    for i in range(len(pattern)):
        for j in range(i+1,len(pattern)):
            P1=list(pattern[i])[:m];P2=list(pattern[j])[:m]
            P1.sort();P2.sort()
            if P1==P2:
                lt.append(list(set(pattern[i]+pattern[j])))
    pattern=[];supportData={}
    for p in lt:
        n=0
        for j in ylt:
            for i in p:        
                if dic[j][i]<=minoccur:
                    nod=0
                    break
                else:
                    nod=1
            if nod:
               n+=1
        support=n*1.0/N
        if support>=minsupport:
            #print p,n*1.0/N
            pattern.append(p)
            supportData[str(p)]=support
    return pattern,supportData

def creatP1(dic,minsupport,minoccur):
    ylt=dic.keys()
    xlt=dic[ylt[0]].keys()
    N,pattern=len(ylt),[]
    supportData={}
    for i in xlt:
        n=0
        for j in ylt:
            if dic[j][i]>minoccur:# the num of i >n, we define it happens
                n+=1
        support=n*1.0/N
        if support>=minsupport:
            pattern.append([i])
            supportData[str([i])]=support
    return pattern,supportData        

def PatternRe(dic,minsupport,minoccur=20):
    pattern,supp=creatP1(dic,minsupport,minoccur)
    supportData=supp
    pattern=[pattern]
    m=0
    while len(pattern[m])>0:
        print m
        patternchild,supp=Patternfind(dic,pattern[m],m,minsupport,minoccur)
        pattern.append(patternchild)
        supportData.update(supp)
        m+=1
    return pattern,supportData

if __name__=='__main__':
    minsupport=0.734
    f=open('/home/yuehui/Working/DATASETS/atomdicRBScoreD381.txt')
    atomdic=json.loads(f.readline())
    f.close()        
#    p=PatternRe(atomdic)
#    dic={'a':{1:1,2:0,3:1,4:1,5:0},'b':{2:1,3:1,5:1,1:0,4:0},'c':{1:1,2:1,3:1,5:1,4:0},'d':{2:1,5:1,1:0,3:0,4:0}}
    p1,di=PatternRe(atomdic,minsupport)
#    f=open('/home/yuehui/Working/python/PDB/PDB try/DataStore/apriori-pattern.txt','w')
#    f.write(json.dumps(p1))
#    f.close()
#    f=open('/home/yuehui/Working/python/PDB/PDB try/DataStore/apriori-supportdic.txt','w')
#    f.write(json.dumps(di))
#    f.close()
    print p1
    print di
##############################################################################
def loadDataset():
    return [[1,2,3,4],[2,4,5],[1,2,3],[2,5]]

def creatC1(dataSet):
    C1=[]
    for trans in dataSet:
        for item in trans:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset,C1)
    
def scanD(D,Ck,minsupport):
    ssCnt={}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not ssCnt.has_key(can): ssCnt[can]=1
                else: ssCnt[can]+=1
    numItems=float(len(D))
    retList=[]
    supportData={}
    for key in ssCnt:
        support=ssCnt[key]/numItems
        if support>=minsupport:
            retList.insert(0,key)
        supportData[key]=support
    return retList,supportData
    
def aprioriGen(Lk,k):
    retList=[]
    lenLk=len(Lk)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            L1=list(Lk[i])[:k-2];L2=list(Lk[j])[:k-2]
            L1.sort();L2.sort()
            if L1==L2:
                retList.append(Lk[i] | Lk[j])
    return retList
    
def apriori(dataSet,minsupport=0.5):
    C1=creatC1(dataSet)
    D=map(set,dataSet)
    L1,supportData=scanD(D,C1,minsupport)
    L=[L1]
    k=2
    while len(L[k-2])>0:
        Ck=aprioriGen(L[k-2],k)
        Lk,supK=scanD(D,Ck,minsupport)
        supportData.update(supK)
        L.append(Lk)
        k+=1
    return L,supportData
        
