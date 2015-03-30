import sys
import os
import re
import random
import pickle
import codecs
import perceplearn

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
  
def defaultFormatTrainingFile(trainingFile):
  infile=open(trainingFile,'r',errors='ignore')
  lines = infile.readlines()
  trainingFileList=list()
  for line in lines:
    line='BEG/BEG '+line+' TER/TER'
    #print(line)
    trainingFileWordList=line.split()
    #print(trainingFileWordList)
    for i in range(1,len(trainingFileWordList)-1):
      printLine=''
      prevWord=trainingFileWordList[i-1]
      curWord=trainingFileWordList[i]
      nextWord=trainingFileWordList[i+1]
      #print('prevWord:'+prevWord+' '+'curWord:'+curWord+' '+'nextWord:'+nextWord)
      #prevWordList=prevWord.split('/')
      #curWordList=curWord.split('/')
      #nextWordList=nextWord.split('/')
      printLine=getTAG(curWord)+' '+'prevWord:'+getWORD(prevWord)+' '+'curWord:'+getWORD(curWord)+' '+'nextWord:'+getWORD(nextWord)
      printLine+=' '+getSuffixString(getWORD(curWord))
      trainingFileList.append(printLine)
  return trainingFileList

def getFormatStringList(formatString):
  formatList=list()
  if formatString=='its':
    formatList.append('its')
    formatList.append("it's")
    formatList.append('Its')
    formatList.append("It's")
  elif formatString=='your':
    formatList.append('your')
    formatList.append("you're")
    formatList.append('Your')
    formatList.append("You're")
  elif formatString=='their':
    formatList.append('their')
    formatList.append("they're")
    formatList.append('Their')
    formatList.append("They're")
  elif formatString=='lose':
    formatList.append('lose')
    formatList.append('loose')
    formatList.append('Lose')
    formatList.append('Loose')
  elif formatString=='too':
    formatList.append('too')
    formatList.append('to')
    formatList.append('Too')
    formatList.append('To')
  return formatList 

def customFormatTrainingFile(trainingFile,formatString):
  formatStringList=getFormatStringList(formatString)
  infile=open(trainingFile,'r',errors='ignore')
  lines = infile.readlines()
  trainingFileList=list()
  for line in lines:
    line='BEG/BEG '+line+' TER/TER'
    line=line.lower()
    #print(line)
    trainingFileWordList=line.split()
    #print(trainingFileWordList)
    for i in range(1,len(trainingFileWordList)-1):
      if getWORD(trainingFileWordList[i]) in formatStringList:
        printLine=''
        prevWord=trainingFileWordList[i-1]
        curWord=trainingFileWordList[i]
        nextWord=trainingFileWordList[i+1]
        #print('prevWord:'+prevWord+' '+'curWord:'+curWord+' '+'nextWord:'+nextWord)
        #prevWordList=prevWord.split('/')
        #curWordList=curWord.split('/')
        #nextWordList=nextWord.split('/')
        printLine=getWORD(curWord)+' '+'prevWord:'+getWORD(prevWord)+' '+'nextWord:'+getWORD(nextWord)+' '
        printLine+='prevTag:'+getTAG(prevWord)+' '+'nextTag:'+getTAG(nextWord)
        #printLine+=' '+getSuffixString(getWORD(curWord))
        #printLine+=' '+getTAG(curWord)
        trainingFileList.append(printLine)
  return trainingFileList


         
def main():
  if len(sys.argv) != 2:
    print ('usage: python3 postrain.py trainingFile')
    sys.exit(1)
  trainingFile = sys.argv[1]
  defaultTrainingFileList=defaultFormatTrainingFile(trainingFile)
  print('default...')
  #print(defaultTrainingFileList)
  perceplearn.initializeClassWeights(defaultTrainingFileList)
  perceplearn.adjustClassWeights(defaultTrainingFileList,'defaultModelFile.txt')
  perceplearn.flushDictionary()
  customTrainingFileList=customFormatTrainingFile(trainingFile,'its')
  print('its...')
  #print(customTrainingFileList)  
  perceplearn.initializeClassWeights(customTrainingFileList)
  perceplearn.adjustClassWeights(customTrainingFileList,'custom_its_ModelFile.txt')
  perceplearn.flushDictionary()
  customTrainingFileList=customFormatTrainingFile(trainingFile,'your')
  print('your...')
  #print(customTrainingFileList)  
  perceplearn.initializeClassWeights(customTrainingFileList)
  perceplearn.adjustClassWeights(customTrainingFileList,'custom_your_ModelFile.txt')
  perceplearn.flushDictionary()
  customTrainingFileList=customFormatTrainingFile(trainingFile,'their')
  print('their...')
  #print(customTrainingFileList)  
  perceplearn.initializeClassWeights(customTrainingFileList)
  perceplearn.adjustClassWeights(customTrainingFileList,'custom_their_ModelFile.txt')
  perceplearn.flushDictionary()
  customTrainingFileList=customFormatTrainingFile(trainingFile,'lose')
  print('lose...')
  #print(customTrainingFileList)  
  perceplearn.initializeClassWeights(customTrainingFileList)
  perceplearn.adjustClassWeights(customTrainingFileList,'custom_lose_ModelFile.txt')
  perceplearn.flushDictionary()
  customTrainingFileList=customFormatTrainingFile(trainingFile,'too')
  print('too...')
  #print(customTrainingFileList)  
  perceplearn.initializeClassWeights(customTrainingFileList)
  perceplearn.adjustClassWeights(customTrainingFileList,'custom_too_ModelFile.txt')
  

if __name__ == '__main__':
  main()
