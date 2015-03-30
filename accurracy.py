import sys
import os
import re
import codecs
import pickle

itsVocabularyList=["its","Its","it's","It's"]
tooVocabularyList=["to","To","Too","too"]
yourVocabularyList=["your","Your","you're","You're"]
theirVocabularyList=["their","Their","they're","They're"]
loseVocabularyList=["lose","Lose","loose","Loose"]
vocabularyList=["its","Its","it's","It's","to","To","Too","too",
"your","Your","you're","You're","their","Their","they're","They're","lose","Lose","loose","Loose"]


def main():
  global vocabularyList
  if len(sys.argv) != 4:
    print ('usage: python3 accurracy.py error.txt answer.txt output.txt')
    sys.exit(1)
  errorFile = sys.argv[1]
  answerFile = sys.argv[2]
  outputFile = sys.argv[3]
  
  errorFileInfile=open(errorFile,'r',errors='ignore')
  errorlines = errorFileInfile.readlines()
  errorFileInfile.close()

  answerFileInfile=open(answerFile,'r',errors='ignore')
  answerlines = answerFileInfile.readlines()
  answerFileInfile.close()
  
  outputFileInfile=open(outputFile,'r',errors='ignore')
  outputlines = outputFileInfile.readlines()
  outputFileInfile.close()
  
  if (len(errorlines) != len(answerlines) or len(errorlines) != len(outputlines)):
    print("Line count mismatch...")
    print('errorFilelines: '+ str(len(errorlines)))
    print('answerFilelines: '+ str(len(answerlines)))
    print('outputFilelines: '+ str(len(outputlines)))
    sys.exit(1)

  numRightCorrections=0
  numWrongCorrections=0
  numActualCorrections=0
  #print('errorFilelines: '+ str(len(errorlines)))
  #print('answerFilelines: '+ str(len(answerlines)))
  #print('outputFilelines: '+ str(len(outputlines)))

  for i in range(0,len(errorlines)):
    errorline=errorlines[i]
    answerline=answerlines[i]
    outputline=outputlines[i]
    
    errorlineWords=errorline.split()
    answerlineWords=answerline.split()
    outputlineWords=outputline.split()
    #len(errorlineWords)
    for j in range(0,len(errorlineWords)):
      if errorlineWords[j] in vocabularyList:
        #print("errorlineWord :" +errorlineWords[j])
        #print("answerlineWord :" +answerlineWords[j])
        #print("outputlineWords :" +outputlineWords[j])
        if errorlineWords[j] != answerlineWords[j]:
          numActualCorrections+=1
          #print("answerlineWord :" +answerlineWords[j])
          #print("outputlineWordS :" +outputlineWords[j])
          if answerlineWords[j] == outputlineWords[j]:
            numRightCorrections+=1  
          else:
            numWrongCorrections+=1
        if (errorlineWords[j] == answerlineWords[j] and errorlineWords[j] != outputlineWords[j]):
          #print("errorlineWord :" +errorlineWords[j])
          #print("answerlineWord :" +answerlineWords[j])
          #print("outputlineWords :" +outputlineWords[j])
          numWrongCorrections+=1
  print('Number of actual corrections: '+str(numActualCorrections))
  print('Number of right corrections: '+str(numRightCorrections))            
  print('Number of wrong corrections: '+str(numWrongCorrections))            
  precision=numRightCorrections/(numWrongCorrections+numRightCorrections)
  recall=numRightCorrections/numActualCorrections
  fscore=(2*precision*recall)/(recall+precision)
  print('Precision: '+str(precision))
  print('Recall: '+str(recall))
  print('fscore: '+str(fscore))
  #print('Accuracy: '+str(numRightCorrections/))
  
  
  
      
    
if __name__ == '__main__':
  main()
