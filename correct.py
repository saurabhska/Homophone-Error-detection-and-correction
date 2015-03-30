import sys
import os
import re
import codecs
import pickle

classWeights = dict()
classITSWeights = dict()
classTOOWeights = dict()
classYOURWeights = dict()
classLOSEWeights = dict()
classTHEIRWeights = dict()
classWeights = dict()
taggedInputLinesList = list()
itsVocabularyList=["its","Its","it's","It's"]
tooVocabularyList=["to","To","Too","too"]
yourVocabularyList=["your","Your","you're","You're"]
theirVocabularyList=["their","Their","they're","They're"]
loseVocabularyList=["lose","Lose","loose","Loose"]
vocabularyList=["its","Its","it's","It's","to","To","Too","too",
"your","Your","you're","You're","their","Their","they're","They're","lose","Lose","loose","Loose"]

def getTAG(word):
  if '/' in word:
    wordList=word.split('/')
    return wordList[-1]
  return word
  
def getWORD(word):
  if '/' in word:
    wordList=word.split('/')
    lastWord=wordList[-1]
    pos=len(word)-len(lastWord)-1
    return word[:pos]
  return word

def getWordshape(word):
  #print(word)
  word=re.sub('[^A-Za-z0-9 ]+', '-', word)
  #print(word)
  word=re.sub('[a-z]+', 'a', word)
  word=re.sub('[A-Z]+', 'A', word)
  word=re.sub('[0-9]+', '9', word)
  #print(word)
  word=re.sub('[A]+', 'A', word)
  #print(word)
  word=re.sub('[a]+', 'a', word)
  #print(word)
  word=re.sub('[-]+', '-', word)  
  return word
  
def getSuffixString(word):
  suffix3=''
  suffix2=''
  wshape=''
  returnString=''
  wordLength=len(word)
  if wordLength < 3:
    suffix3=word
    suffix2=word
    wshape=getWordshape(word)
  else:
    suffix3=word[-3:]
    suffix2=word[-2:]
    wshape=getWordshape(word)
  returnString='suffix3:'+suffix3+' '+'suffix2:'+suffix2+' '+'wshape:'+wshape
  return returnString

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
  
def computeClassLabel(feature):
  #print(featureList)
  global classWeights
  computedValues=dict()
  curWord=''
  featureList=feature.split()
  for label, weightVector in classWeights.items():
    value=0
    for word in featureList:
      #print('word: '+word)
      wordList=list()
      if '::' in word:
        wordList.append(word.replace("::",""))
        wordList.append(":")
      else:
        #wordList=word.split(':')
        pos=word.find(':')
        wordList.append(word[:pos])
        pos+=1
        wordList.append(word[pos:])
      #print(wordList)
      if wordList[0]=='curWord':
        curWord=wordList[1]
      if word in weightVector:
        value+=weightVector[word]
    computedValues[label]=value
  #print('computedValues')
  #print(computedValues)
  curWord=curWord+'/'+findMax(computedValues)
  #print('computedValues')
  #print(curWord)
  return curWord
  
def computeCorrectWord(feature,classWeights):
  #print('inside computeCorrectWord...')
  #print('feature...')
  #print(feature)
  #print('classWeights...')
  #print(classWeights)  
  computedValues=dict()
  curWord=''
  featureList=feature.split()
  for label, weightVector in classWeights.items():
    value=0
    for word in featureList:
      if word in weightVector:
        value+=weightVector[word]
    computedValues[label]=value
  #print('computedValues')
  #print(computedValues)
  curWord=findMax(computedValues)
  #print('computedValues')
  #print('======================'+curWord)
  return curWord
  
    
  
def readWeights():
  global classITSWeights
  global classTOOWeights
  global classYOURWeights
  global classLOSEWeights
  global classTHEIRWeights
  global classWeights
  modelread=open('custom_its_ModelFile.txt','rb')
  classITSWeights=pickle.load(modelread)
  modelread.close()
  
  modelread=open('custom_too_ModelFile.txt','rb')
  classTOOWeights=pickle.load(modelread)
  modelread.close()
  
  modelread=open('custom_your_ModelFile.txt','rb')
  classYOURWeights=pickle.load(modelread)
  modelread.close()
  
  modelread=open('custom_lose_ModelFile.txt','rb')
  classLOSEWeights=pickle.load(modelread)
  modelread.close()
  
  modelread=open('custom_their_ModelFile.txt','rb')
  classTHEIRWeights=pickle.load(modelread)
  modelread.close()
  
  modelread=open('defaultModelFile.txt','rb')
  classWeights=pickle.load(modelread)
  modelread.close()          
  
def formatInputLine(line):
  #infile=open(testFile,'r',errors='ignore')
  #lines = infile.readlines()
  #infile.close()
  inputLineList=list()
  #for line in lines:
  line='BEG '+line+' TER'
  #print(line)
  inputLineWordList=line.split()
  #print(trainingFileWordList)
  for i in range(1,len(inputLineWordList)-1):
    printLine=''
    prevWord=inputLineWordList[i-1]
    curWord=inputLineWordList[i]
    nextWord=inputLineWordList[i+1]
    #print('prevWord:'+prevWord+' '+'curWord:'+curWord+' '+'nextWord:'+nextWord)
    printLine='prevWord:'+prevWord+' '+'curWord:'+curWord+' '+'nextWord:'+nextWord
    printLine+=' '+getSuffixString(curWord)
    inputLineList.append(printLine)
    #print(inputLineList)
  return inputLineList  
  
def spellCheck(printLine,curWord):
  #print("inside  spellCheck....")
  #print('printLine...'+printLine)
  #print('curWord...'+curWord)
  global classITSWeights
  global classTOOWeights
  global classYOURWeights
  global classLOSEWeights
  global classTHEIRWeights
  temp=dict()  
  if curWord in itsVocabularyList:
    temp=classITSWeights
  if curWord in tooVocabularyList:
    temp=classTOOWeights
  if curWord in yourVocabularyList:
    temp=classYOURWeights
  if curWord in theirVocabularyList:
    temp=classTHEIRWeights
  if curWord in loseVocabularyList:
    temp=classLOSEWeights
  #print('temp dictionary......')
  #print(temp)
  return computeCorrectWord(printLine,temp)

def correctCase(correctWord,orgWord):
  if orgWord.islower():
    return correctWord.lower()
  elif orgWord.isupper():
    return correctWord.upper()
  elif not orgWord.islower() and not orgWord.isupper():
    correctWord=correctWord[0].upper()+correctWord[1:]
    return correctWord
  return correctWord

      
def correctText(taggedInputLinesList):
  correctedTextList=list()
  for line in taggedInputLinesList:
    #print(line)
    outputLine=''
    line='BEG/BEG '+line+' TER/TER'
    inputLineWordList=line.split()
    for i in range(1,len(inputLineWordList)-1):
      printLine=''
      prevWord=inputLineWordList[i-1]
      curWord=inputLineWordList[i]
      nextWord=inputLineWordList[i+1]
      if getWORD(curWord).lower() not in vocabularyList:
        outputLine+=getWORD(curWord)+' '
      else:
        orgWord=getWORD(curWord)
      #print('prevWord:'+prevWord+' '+'curWord:'+curWord+' '+'nextWord:'+nextWord)
        printLine='prevWord:'+getWORD(prevWord).lower()+' '+'nextWord:'+getWORD(nextWord).lower()
        printLine+=' '+'prevTag:'+getTAG(prevWord).lower()+' '+'nextTag:'+getTAG(nextWord).lower()
        correctWord=spellCheck(printLine,getWORD(curWord).lower())
        caseCorrectedWord=correctCase(correctWord,orgWord)
        #print("***************************"+correctWord)
        outputLine+=caseCorrectedWord+' '
    correctedTextList.append(outputLine)
  return correctedTextList
  

def main():
  outputLine=''
  if len(sys.argv) != 2:
    print ('usage: python3 correct.py test.txt')
    sys.exit(1)
  #modelFile = sys.argv[1]
  testFile = sys.argv[1]
  readWeights() 
  
  infile=open(testFile,'r',errors='ignore')
  lines = infile.readlines()
  infile.close()
  
  #sys.stdin = codecs.getreader('utf8')(sys.stdin.detach(), errors='ignore')
  #lines = sys.stdin.readlines()
  
  for line in lines:
    outputLine=''
    featureList = formatInputLine(line)
    #featureList=inputData.split()
    #print(featureList)
    for feature in featureList:
      outputLine+=computeClassLabel(feature)+' '
    taggedInputLinesList.append(outputLine)
    #print(taggedInputLinesList)
  correctedTextDataList=correctText(taggedInputLinesList)
  
  for line in correctedTextDataList:
    print(line) 
    
    
if __name__ == '__main__':
  main()
