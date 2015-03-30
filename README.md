Error Detection and Correction: Dealing with Homophone Confusion
**************************************************************************************************************************************
In written language, errors involving the use of words that sound similar or the same are fairly common. For example, the word its is frequently used where it's should, and vice-versa. Other confusable pairs include: they're/their/there, you're/your and loose/lose.

This assignment involves developing an approach for detecting and correcting such errors. We ony correct these specific types of confusion (in either direction):

    it's vs its
    you're vs your
    they're vs their
    loose vs lose
    to vs too

Assignment URL: http://appliednlp.bitbucket.org/hw3/index.html
**************************************************************************************************************************************

Approach:

For correcting spellings, I have used the probabilistic approach with the context (previous
and next words) of the 5 pairs of words that we are targeting to correct. 

Below are the formulae used in calculating and selecting the best fit for the word at any given 
potential correction position.

Scoring Function:
S(Wi Wj Wk) = log(P(combine(Wi Wj Wk)|Wj)) + log(P(pre(Wi)|Wj)) + log(P(suc(Wk)|Wj)) + log(P(Wj))

where:
P(combine(Wi Wj Wk)|Wj) = #(Wi Wj Wk) / #(Wj)   //Event that Wi and Wk are preceding and succeding words respectively given that Wj occurs
P(pre(Wi)|Wj)           = #(Wi Wj) / #(Wj)      //Event that Wi is the preceding word given that Wj occurs
P(suc(Wk)|Wj)           = #(Wj Wk) / #(Wj)      //Event that Wk is the succeding word given that Wj occurs
P(Wj)                   = #Wj / #Total Words    //Event that Wj occurs

#(Wi Wj Wk) = Number of occurrences of sequence Wi Wj Wk
#(Wi Wj)    = Number of occurrences of sequence Wi Wj
#(Wj Wk)    = Number of occurrences of sequence Wj Wk
#(Wj)       = Number of occurrences of word Wj

Wi          = Previous word of the word that we are targeting to correct
Wj          = A word that we are targeting to correct
Wk          = Next word of the word that we are targeting to correct

Given a training file and test file, the code first uses the NLTK WordNetLemmatizer to find the number of unique words in training file.
It then scans the training file and counts the number of occurences of each word (in our targeted corrections) and of the sequences mentioned above to store in the model file. It then computes the prior probabilities for each word Wi in our target correction set.

The code then scans the test file and looks for corrections. If the currently scanned word is in the targeted set of corrections, it then computes and returns the word with argmax probability between the word and its corresponding switchable word. 

Below are the switchable sets of words-

    it's vs its
    you're vs your
    they're vs their
    loose vs lose
    to vs too

While computing the conditional probability, if the word-sequence does not appears in training set and hence in the model, I used the 
Add-One smoothing.

For training purpose I have used the data corpus from NLTK.
*****************************************************************************************************************************
Source Code and Files:

hw3.output.txt      : Output of the code with corrections on test dataset.

probabilityModel.py : Code that corrects spellings based on probabilistic approach.
                      Usage: python3 probabilityModel.py training-file test-file output-file

accurracy.py        : Code to compute the accurracy of the  spell correcter code.
                      Usage: python3 accurracy.py error.txt answer.txt output.txt
                      
*****************************************************************************************************************************
Performance Results on Development Set

Number of actual corrections: 7398
Number of right corrections: 7284
Number of wrong corrections: 375
Precision: 0.9510379945162554
Recall: 0.9845904298459043
fscore: 0.9675234110380555

where -

precision=numRightCorrections/(numWrongCorrections+numRightCorrections)
recall=numRightCorrections/numActualCorrections
fscore=(2*precision*recall)/(recall+precision)
*****************************************************************************************************************************
Third-Party Software

I have used the NLTK WordNetLemmatizer to find the number of unique words in training text.
*****************************************************************************************************************************
References:
The Switchabalizer, presentation by Oskar Singer
*****************************************************************************************************************************
Other Details:

Note: This is additional details of what I tried, but I am submitting the above probabilistic approach for my grading.

I have also tried using the POSTAG approach apart from my submission of the probabilistic approach. But the accuracy
I got with POSTAGGING approach was about 92% (with prevWord, prevTag, nextWord, nextTag as features) and then using
perceptron on it. So the probabilistic approach seems better.

Approach:
Apply perceplearn on the training file and learn six models. First the normal model as in assignment 2, and the other 5
binary models with 1 model each, for the 5 pairs of words we are targeting to correct. Then use these 6 models to predict
the right word.

Code for POSTAG approach:
train.py : Used for learning model from the training file.
correct.py : Used to predict right wrd for correction using the learnt model.
perceplearn.py : Implementation of average perceptron for learning the model.
*****************************************************************************************************************************
