import sys
import os
import re
import codecs
import pickle
import math
import nltk

def Lemmatizer(trainingFile):
  wnl = nltk.WordNetLemmatizer()
  LemmaList = []
  fopen = open(trainingFile, 'r',encoding='UTF-8')
  counter=0
  for line in fopen:
    counter+=1
    line = re.sub(r"[^A-Za-z ]+", '', line)
    LemmaList = LemmaList+[wnl.lemmatize(word) for word in line.split()]
    print(str(counter))
  return len(set(LemmaList))

vocabularyList=["its","it's","to","too","your","you're","their","they're","lose","loose"]
vocabularyOccurrenceDict=dict()
priorProbabilities=dict()
itsVocabularyList=["its","it's"]
tooVocabularyList=["to","too"]
yourVocabularyList=["your","you're"]
theirVocabularyList=["their","they're"]
loseVocabularyList=["lose","loose"]
numUniqueWords=0


def computePriorProbabilities(totalWordCount):
  global priorProbabilities
  global vocabularyList
  global vocabularyOccurrenceDict
  #vocabularyLength=len(vocabularyOccurrenceDict.keys())
  for word in vocabularyList:
    if word in vocabularyOccurrenceDict.keys():
      priorProbabilities[word]=math.log((vocabularyOccurrenceDict[word])/(totalWordCount))
    else:
      priorProbabilities[word]=math.log(1/(totalWordCount+1))
      
def computeConditionalProbabilities(compoundWord,baseWord):
  global priorProbabilities
  global vocabularyList
  global vocabularyOccurrenceDict
  global numUniqueWords
  #vocabularyLength=len(vocabularyOccurrenceDict.keys())
  vocabularyOccurrenceDictkeys=vocabularyOccurrenceDict.keys()
  if baseWord in vocabularyOccurrenceDictkeys:
    baseWordCount=vocabularyOccurrenceDict[baseWord]
  else:
    baseWordCount=1
  if compoundWord in vocabularyOccurrenceDictkeys:
    compoundWordCount=vocabularyOccurrenceDict[compoundWord]+1
  else:
    compoundWordCount=1
  return math.log(compoundWordCount/(baseWordCount+numUniqueWords))
  
def getString(prevWord,curWord,nextWord,strType):
  global vocabularyList
  global vocabularyOccurrenceDict
  if strType=='PRE':
    return 'prevWord:'+prevWord+'|'+'nextWord:'+curWord
  elif strType=='SUC':
    return 'prevWord:'+curWord+'|'+'nextWord:'+nextWord
  elif strType=='TRI':
    return 'prevWord:'+prevWord+'|'+'curWord:'+curWord+'|'+'nextWord:'+nextWord
    
def addWordToVocabulary(word):
  global vocabularyOccurrenceDict
  if word in vocabularyOccurrenceDict:
    vocabularyOccurrenceDict[word]+=1
  else:
    vocabularyOccurrenceDict[word]=1

def updateWordOccurrenceCount(prevWord,curWord,nextWord):
  global vocabularyList
  global vocabularyOccurrenceDict
  addWordToVocabulary(curWord)
  preString=getString(prevWord,curWord,nextWord,'PRE')
  addWordToVocabulary(preString)
  sucString=getString(prevWord,curWord,nextWord,'SUC')
  addWordToVocabulary(sucString)
  triString=getString(prevWord,curWord,nextWord,'TRI')
  addWordToVocabulary(triString)
  
def scanTrainingFile(trainingFile):
  global vocabularyList
  global vocabularyOccurrenceDict
  totalWordCount=0
  with open(trainingFile,'r') as infile:
    for line in infile:
      line='BEG '+line+' TER'
      line=line.lower()
      wordList=line.split()
      totalWordCount+=len(wordList)-2
      for i in range(1,len(wordList)-1):
        if wordList[i] in vocabularyList:
          updateWordOccurrenceCount(wordList[i-1],wordList[i],wordList[i+1])
  #vocabularyOccurrenceDict['totalWordCount']=totalWordCount
  return totalWordCount

def correctCase(correctWord,orgWord):
  #print('correctWord.........'+correctWord)
  #print('orgWord.............'+orgWord)
  if orgWord.islower():
    return correctWord.lower()
  elif orgWord.isupper():
    return correctWord.upper()
  elif not orgWord.islower() and not orgWord.isupper():
    correctWord=correctWord[0].upper()+correctWord[1:]
    return correctWord
  return correctWord

def computeCorrectWord(prevWord,curWord,nextWord,vocabularyList):
  global priorProbabilities
  value1=priorProbabilities[vocabularyList[0]]
  tempString=getString(prevWord,vocabularyList[0],nextWord,'PRE')
  value1+=computeConditionalProbabilities(tempString,vocabularyList[0])
  tempString=getString(prevWord,vocabularyList[0],nextWord,'TRI')
  value1+=computeConditionalProbabilities(tempString,vocabularyList[0])  
  tempString=getString(prevWord,vocabularyList[0],nextWord,'SUC')
  value1+=computeConditionalProbabilities(tempString,vocabularyList[0])
  value2=priorProbabilities[vocabularyList[1]]
  tempString=getString(prevWord,vocabularyList[1],nextWord,'PRE')
  value2+=computeConditionalProbabilities(tempString,vocabularyList[1])
  tempString=getString(prevWord,vocabularyList[1],nextWord,'SUC')
  value2+=computeConditionalProbabilities(tempString,vocabularyList[1])    
  tempString=getString(prevWord,vocabularyList[1],nextWord,'TRI')
  value2+=computeConditionalProbabilities(tempString,vocabularyList[1])    
  if value1 > value2:
    return vocabularyList[0]
  return vocabularyList[1]

def spellCheck(prevWord,curWord,nextWord):
  global itsVocabularyList
  global tooVocabularyList
  global yourVocabularyList
  global theirVocabularyList
  global loseVocabularyList
  if curWord in itsVocabularyList:
    return computeCorrectWord(prevWord,curWord,nextWord,itsVocabularyList)
  elif curWord in tooVocabularyList:
    return computeCorrectWord(prevWord,curWord,nextWord,tooVocabularyList)
  elif curWord in yourVocabularyList:
    return computeCorrectWord(prevWord,curWord,nextWord,yourVocabularyList)
  elif curWord in theirVocabularyList:
    return computeCorrectWord(prevWord,curWord,nextWord,theirVocabularyList)
  elif curWord in loseVocabularyList:
    return computeCorrectWord(prevWord,curWord,nextWord,loseVocabularyList)  
    
def correctText(lines):
  correctedTextList=list()
  for line in lines:
    #print(line)
    outputLine=''
    #line='BBEG/BBEG '+'BEG/BEG '+line+' TER/TER'+' TTER/TTER'
    line='BEG '+line+' TER'
    inputLineWordList=line.split()
    for i in range(1,len(inputLineWordList)-1):
      printLine=''
      #pprevWord=inputLineWordList[i-2]
      prevWord=inputLineWordList[i-1]
      curWord=inputLineWordList[i]
      nextWord=inputLineWordList[i+1]
      #nnextWord=inputLineWordList[i+2]
      if curWord.lower() not in vocabularyList:
        outputLine+=curWord+' '
      else:
        orgWord=curWord
        correctWord=spellCheck(prevWord.lower(),curWord.lower(),nextWord.lower())
        caseCorrectedWord=correctCase(correctWord,orgWord)
        #print("***************************"+correctWord)
        outputLine+=caseCorrectedWord+' '
    correctedTextList.append(outputLine)
  return correctedTextList

def scanTestFile(testFile,outputFile):
  infile=open(testFile,'r',errors='ignore')
  lines = infile.readlines()
  infile.close()
  correctedTextDataList=correctText(lines)  
  outfile=open(outputFile,'w')
  for line in correctedTextDataList:
    outfile.write(line)
    outfile.write("\n") 
  outfile.close()

def main():
  global numUniqueWords
  outputLine=''
  if len(sys.argv) != 4:
    print ('usage: python3 probabilityModel.py training-file test-file output-file')
    sys.exit(1)
  trainingFile = sys.argv[1]
  testFile = sys.argv[2]
  outputFile = sys.argv[3]
  numUniqueWords=Lemmatizer(trainingFile)
  #numUniqueWords=48853
  #numUniqueWords=89176
  print('numUniqueWords: '+str(numUniqueWords))
  totalWordCount=scanTrainingFile(trainingFile)
  computePriorProbabilities(totalWordCount)
  scanTestFile(testFile,outputFile)
     
if __name__ == '__main__':
  main()
