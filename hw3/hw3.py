import sys
import pandas as pd
import numpy as np
import csv
import io
import re
import string



def preprocess():
    f = open("trainingSet.txt", "r")
    train = f.readlines()
    train_data = []
    train_labels = []
    wordbag = []
    for line in train:
        a = line.split('\t')
        s = a[0].translate(None, string.punctuation)
        s = s.strip().lower()
        train_data.append(s)
        train_labels.append(int(a[1].strip('\r\n')))
        wordbag.extend(s.split())
    
    f = open("testSet.txt","r")
    test = f.readlines()
    test_data = []
    test_labels = []
    for line in test:
        a = line.split('\t')
        s = a[0].translate(None, string.punctuation)
        s = s.strip().lower()
        test_data.append(s)
        test_labels.append(int(a[1].strip('\r\n')))

    
    wordbag = list(set(wordbag)) 
    wordbag.sort()
    
    f1 = open("preprocessed_train.txt", "w")
    wordbag.append("classlabel")
    
    features = str(wordbag)[1:-1]
    f1.write(features)
    f1.write("\n")
    


    train_vectors = np.zeros(shape=(len(train_data), len(wordbag)))
    for i in range(len(train_data)):
        vector = []
        for j in range(len(wordbag)-1):
            if wordbag[j] in train_data[i]:
                vector.append(1)
            else:
                vector.append(0)
        vector.append(train_labels[i])
        train_vectors[i] = vector
        f1.write(str(vector)[1:-1])
        f1.write("\n")

    f1.close()


    f1 = open("preprocessed_test.txt", "w")
    f1.write(features)
    f1.write("\n")


    test_vectors = np.zeros(shape=(len(test_data), len(wordbag)))
    for i in range(len(test_data)):
        vector = []
        for j in range(len(wordbag)-1):
            if wordbag[j] in test_data[i]:
                vector.append(1)
            else:
                vector.append(0)
        vector.append(test_labels[i])
        test_vectors[i] = vector
        f1.write(str(vector)[1:-1])
        f1.write("\n")

    f1.close()

    return train_vectors, test_vectors


def classification():
    train_vectors, test_vectors = preprocess()

    train_labels_pos = train_vectors[:,1359:]
    train_vectors = train_vectors[:,:1359]


    test_labels = test_vectors[:,1359:]
    test_vectors = test_vectors[:,:1359]

    num_pos = np.sum(train_labels_pos)
    num_neg = len(train_labels_pos) - num_pos

    p_pos = num_pos/len(train_labels_pos)
    p_neg = num_neg/len(train_labels_pos)
  
   


    # get #of positive review and neg review the i-th word appeared
    train_labels_pos = np.transpose(train_labels_pos)
    pos_word_v = np.dot(train_labels_pos, train_vectors)
    
    train_labels_neg = 1 - train_labels_pos
    neg_word_v = np.dot(train_labels_neg, train_vectors)



    pos_word_v = pos_word_v + 1
    neg_word_v = neg_word_v + 1
    num_pos = num_pos + 2
    num_neg = num_neg + 2

    p_x_y_pos = np.divide(pos_word_v, num_pos)
    p_x_y_neg = np.divide(neg_word_v, num_neg)
   

    
    a_p_x_y_pos = 1-p_x_y_pos
    a_p_x_y_neg = 1-p_x_y_neg
    a_p_x_y_pos = a_p_x_y_pos.transpose()
    a_p_x_y_neg = a_p_x_y_neg.transpose()
    a_p_x_y_pos = np.log(a_p_x_y_pos)
    a_p_x_y_neg = np.log(a_p_x_y_neg)
    



    p_x_y_pos = p_x_y_pos.transpose()
    p_x_y_pos = np.log(p_x_y_pos)

    
    pos_result_v = np.dot(train_vectors, p_x_y_pos) + np.dot(1-train_vectors, a_p_x_y_pos)
    pos_result_v = pos_result_v + np.log(p_pos)


 




    p_x_y_neg = p_x_y_neg.transpose()
    
    p_x_y_neg = np.log(p_x_y_neg)

    
    neg_result_v = np.dot(train_vectors, p_x_y_neg) + np.dot(1-train_vectors, a_p_x_y_neg)
    neg_result_v = neg_result_v + np.log(p_neg)
    

   
    
    accuracy = 0.0
    for i in range(499):
        if pos_result_v[i][0] > neg_result_v[i][0]:
            if train_labels_pos[0][i] == 1:
                accuracy += 1
                
        elif neg_result_v[i][0] > pos_result_v[i][0]:
            if train_labels_pos[0][i] == 0:
                accuracy += 1
                

    
    accuracy = (accuracy/499.0)*100.0

    print("the percentage of the train accuracy is {}%".format(accuracy))
    f1 = open("results.txt", "w")
    f1.write("===Used trainingSet.txt for both training and testing===\n")
    f1.write("the percentage of the train set accuracy is {}%".format(accuracy))
    f1.write("\n")
    f1.write("\n")
    f1.write("\n")

    
    
    
    pos_final_v = np.dot(test_vectors, p_x_y_pos) + np.dot(1-test_vectors, a_p_x_y_pos)
    pos_final_v = pos_final_v + np.log(p_pos)
 

    neg_final_v = np.dot(test_vectors, p_x_y_neg) + np.dot(1-test_vectors, a_p_x_y_neg)
    neg_final_v = neg_final_v + np.log(p_neg)


    
    accuracy = 0.0
    for i in range(len(test_labels)):
        if pos_final_v[i][0] > neg_final_v[i][0]:
            if test_labels[i][0] == 1:
                accuracy += 1
            
        elif neg_final_v[i][0] > pos_final_v[i][0]:
            if test_labels[i][0] == 0:
                accuracy += 1
                

  
    accuracy = (accuracy/497)*100.0
    
    print("the percentage of the test accuracy is {}%".format(accuracy))
    f1.write("===Used trainingSet.txt for training and used testSet.txt for testing===\n")
    f1.write("the percentage of the test set accuracy is {}%".format(accuracy))
    f1.write("\n")
    f1.close()

    
    

def main():
    classification()
    



if __name__ == "__main__":
    main()