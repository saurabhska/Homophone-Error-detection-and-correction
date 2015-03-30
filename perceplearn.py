import sys
import os
import re
import random
import codecs
import pickle

avgWeights=dict()
globalVocabulary=dict()
classWeights = dict()
backupWeights=dict()

def flushDictionary():
  global avgWeights
  global globalVocabulary
  global classWeights
  global backupWeights
  backupWeights.clear()
  classWeights.clear()
  globalVocabulary.clear()
  avgWeights.clear()

def backupWeightDictionary(curWrongClassifiedCount):
  global backupWeights
  global avgWeights
  backupWeights[curWrongClassifiedCount]=avgWeights.copy()

def writeModelFile(modelFile,minWrongClassifiedCount):
  global backupWeights
  outfile=open(modelFile,'wb')
  dumpDict=backupWeights[minWrongClassifiedCount]
  pickle.dump(dumpDict, outfile)
  outfile.close()
  #print('writing to model file...')
  #print(dumpDict)


def printClassWeights():
  global classWeights
  global avgWeights
  global backupWeights
  print('classWeights')
  for key,value in classWeights.items():
    print("printing for key :"+key)
    print(value)
  print('avgWeights')
  for key,value in avgWeights.items():
    print("printing for key :"+key)
    print(value)
  print('backupWeights')
  for key,value in backupWeights.items():
    print("printing for key :"+key)
    print(value)

def addClassName(name):
  global classWeights
  global avgWeights
  tempDict=dict()
  avgTempDict=dict()
  if name not in classWeights:
    classWeights[name]=tempDict
    avgWeights[name]=avgTempDict

def updateGlobalVocabulary(documentWordList):
  global globalVocabulary
  global classWeights
  global avgWeights
  for word in documentWordList:
    if word not in globalVocabulary:
      globalVocabulary[word]=0
      
def updateClassWeights():
  global classWeights
  global globalVocabulary
  global avgWeights
  for className,value in classWeights.items():
    for word in globalVocabulary:
      value[word]=0
    classWeights[className]=value
  for className,value in avgWeights.items():
    for word in globalVocabulary:
      value[word]=0
    avgWeights[className]=value
        
def initializeClassWeights(trainingFileList):
  global globalVocabulary
  for line in trainingFileList:
    nameOfClass=line.partition(' ')[0]
    addClassName(nameOfClass)
    #line=line.lower()
    #line=re.sub('[^A-Za-z0-9 \n]+', '', line)
    documentWordList=line.split()
    #print('documentWordList')
    #print(documentWordList)    
    del documentWordList[0]
    updateGlobalVocabulary(documentWordList)
  updateClassWeights()
  #print('globalVocabulary')
  #print(globalVocabulary)
  
def addWeights(dictA,featureList):
  for word in featureList:
    if word in dictA.keys():
      dictA[word]+=1
  return dictA
  
def substractWeights(dictA,featureList):
  for word in featureList:
    if word in dictA.keys():
      dictA[word]-=1
  return dictA  
  
def getFeatureVector(line):
  #line=line.lower()
  #line=re.sub('[^A-Za-z0-9 \n]+', '', line)
  documentWordList=line.split()
  del documentWordList[0]
  return documentWordList
  
def findMax(computedValues):
  flag=0
  for key,value in computedValues.items():
    if flag==0:
      max_value=value
      returnLabel=key
      flag=1
    else:
      if value > max_value:
        max_value=value
        returnLabel=key
  return returnLabel
      
def computeDotProduct(weightVector,featureList):
  returnValue=0
  for word in featureList:
    if word in weightVector.keys():
      returnValue+=weightVector[word]
  return returnValue
  
def computeClassLabel(featureList):
  global classWeights
  weight=dict()
  computedValues=dict()
  for label, weightVector in classWeights.items():
    value=computeDotProduct(weightVector,featureList)
    computedValues[label]=value
  #print('computedValues')
  #print(computedValues)
  return findMax(computedValues)
  
def updateAvgWeights():
  global classWeights
  global avgWeights
  #print('classWeights')
  #print(classWeights)
  #print('avgWeights')
  #print(avgWeights)  
  for avgKey,avgValue in avgWeights.items():
    #print('avgKey')
    #print(avgKey)
    #print('avgValue')
    #print(avgValue)
    tempClassWeights=classWeights[avgKey]
    #print('tempClassWeights')
    #print(tempClassWeights)
    for key,value in avgValue.items():
      #print('key :'+key)
      #print('value')
      #print(value)
      avgValue[key]+=tempClassWeights[key]
    avgWeights[avgKey]=avgValue
    
def adjustClassWeights(lines,modelFile):
  global avgWeights
  global globalVocabulary
  global classWeights 
  global backupWeights
  #infile=open(trainingFile,'r',errors='ignore')
  #lines = infile.readlines()
  minWrongClassifiedCount=len(lines)+1
  #print('Initially minWrongClassifiedCount= '+str(minWrongClassifiedCount))
  weight=dict()
  loopCounter=0
  while loopCounter < 30:
    #print('loop number '+str(loopCounter))
    random.shuffle(lines)
    curWrongClassifiedCount=0
    for line in lines:
      #print('line is: '+line)
      originalLabel=line.partition(' ')[0]
      featureList=getFeatureVector(line)
      #print('featureList')
      #print(featureList)
      predictedLabel=computeClassLabel(featureList)
      #print('originalLabel: '+originalLabel+ ' predictedLabel:'+predictedLabel)
      if originalLabel != predictedLabel:
        curWrongClassifiedCount+=1
        weight=addWeights(classWeights[originalLabel],featureList)
        classWeights[originalLabel]=weight
        weight=substractWeights(classWeights[predictedLabel],featureList)
        classWeights[predictedLabel]=weight  
      #print('classWeights')
      #print(classWeights)      
    #print('Wrongly classified in loop number '+str(loopCounter)+' is '+str(curWrongClassifiedCount))
    if minWrongClassifiedCount > curWrongClassifiedCount:
      minWrongClassifiedCount=curWrongClassifiedCount
    if loopCounter!=0:
      updateAvgWeights()
    loopCounter+=1
    #print('avgWeights')
    #print(avgWeights)    
    backupWeightDictionary(curWrongClassifiedCount)
  #print('Minimum wrong classified count is '+str(minWrongClassifiedCount))
  #print('backupWeightDictionary')
  #print(backupWeights)
  writeModelFile(modelFile,minWrongClassifiedCount)
  
def getTrainingFileList(trainingFile):
  infile=open(trainingFile,'r',errors='ignore')
  lines = infile.readlines()
  trainingFileList=list()
  for line in lines:
    trainingFileList.append(line)
  infile.close()
  return trainingFileList
  
  
def main():
  if len(sys.argv) != 3:
    print ('usage: python3 perceplearn.py trainingFile modelFile')
    sys.exit(1)
  trainingFile = sys.argv[1]
  modelFile = sys.argv[2]
  #initializeClassWeights(trainingFile)
  #printClassWeights()
  #adjustClassWeights(trainingFile,modelFile)
  trainingFileList=getTrainingFileList(trainingFile)
  initializeClassWeights(trainingFileList)
  adjustClassWeights(trainingFileList,modelFile)
  
if __name__ == '__main__':
  main()
