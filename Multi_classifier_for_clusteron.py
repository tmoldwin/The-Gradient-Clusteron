'''
multiclassifier for clusteron
'''
from clusteron import Clusteron
import numpy as np
import DataOrganizer as do
import scipy.special as sp

class MultiClassifier():

    def __init__(self, num_of_classes = 10):
        self.algorithm = 'multi_clusteron'
        _,_,self.x_test,self.y_test,_,_ = do.get_data(self.algorithm)
        self.num_of_classes = num_of_classes
        self.clusteron_vec = [None]*self.num_of_classes
        self.accuracy_vec = []#for the multiclassifier
        
    def train(self,num_of_epochs):
        for i in range(self.num_of_classes):
            print('clusteron ',i)
            algorithm = 'clusteron'
            x_train, y_train, x_test, y_test, x_train_balanced, y_train_balanced = do.get_data(algorithm, i)

            pos_data,neg_data,pos_train_Y,neg_train_Y = do.split_data_by_posVal(x_train_balanced,y_train_balanced,i)
            
            test_pos,test_neg,_,_ = do.split_data_by_posVal(x_test,y_test,i)
            clusteron = Clusteron(x_train,neg_data,x_train_balanced,y_train_balanced,
                                  test_pos,test_neg,
                                  x_test,
                                  y_test,i,
                                  syn_at_halfVal=10)
            clusteron.learning_algo(num_of_epochs)
            self.clusteron_vec[i] = clusteron
        self.test(self.x_test,self.y_test)
        return
    
    def test(self,dataset,Y):
        P = len(Y)
        vec = [None]*np.size(Y)*self.num_of_classes
        prediction_matrix = np.matrix(np.reshape(vec,(P,self.num_of_classes)))
        for i in range(self.num_of_classes):
            _,example_outputs = self.clusteron_vec[i].calculate_activation_by_dataset_new(dataset,Y)
            example_outputs = example_outputs - self.clusteron_vec[i].prediction_threshold
            example_outputs_normlized = (example_outputs - np.min(example_outputs))/(np.max(example_outputs)-np.min(example_outputs))
            prediction_vec = sp.expit(example_outputs_normlized)
            prediction_matrix[:,i] = np.reshape(prediction_vec,(P,1))
        predictions = np.argmax(prediction_matrix,1)
        accuracy = sum(np.where(np.squeeze(np.array(predictions)) == np.squeeze(Y),1,0))/P
        print('full test accuracy = ',accuracy)
        self.accuracy_vec.append(accuracy)
        return 
