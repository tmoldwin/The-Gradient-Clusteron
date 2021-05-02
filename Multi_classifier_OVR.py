'''
OVR multiclassifier without SM
'''
import numpy as np
import sklearn.metrics as skmat
from G_Clusteron_OVR import G_Clusteron_OVR
    
class MultiClassifier():

    def __init__(self,train_set,train_Y,test_set,test_Y,classes,radius,bias_synapse = False,
                 bias_synapse_weight = 10):
        self.train_set = train_set
        self.train_Y = train_Y
        self.test_set = test_set
        self.test_Y = test_Y
        self.num_of_classes = len(classes)
        self.clusteron_vec = [None]*self.num_of_classes
        self.accuracy_vec = []
        self.bs = bias_synapse
        self.bsw = bias_synapse_weight
        for i in range(self.num_of_classes):
            posVal = classes[i]
            print('clusteron ',posVal)
            clusteron = G_Clusteron_OVR(self.train_set,self.train_Y,
                                        self.test_set,self.test_Y,
                                        posVal,radius,bias_synapse=self.bs,
                                        bias_synapse_weight=self.bsw)
            self.clusteron_vec[i] = clusteron
        if bias_synapse:
            r,c = np.shape(self.train_set)
            self.train_set = np.hstack((np.ones((r,1)),self.train_set))
            self.test_set = np.hstack((np.ones((len(self.test_set),1)),self.test_set))
        
    def train(self,num_of_epochs,batch_size,location_lr,weight_lr, bias_lr,
              learning_protocol,W_momentum, B_momentum, L_momentum,plot_accuracy):#deleted: w_momentum=False,b_m=true,l_m=true
        for i in range(self.num_of_classes):
            print('clusteron ',i)
            self.clusteron_vec[i].train(num_of_epochs,learning_protocol,batch_size,location_lr,
                                        weight_lr,bias_lr,W_momentum,B_momentum,
                                        L_momentum,plot_accuracy=plot_accuracy,test=True)    
        self.test(self.test_set,self.test_Y)
        return    
    
    def test(self,dataset,Y):
        P = len(Y)
        vec = [None]*np.size(Y)*self.num_of_classes
        prediction_matrix = np.matrix(np.reshape(vec,(P,self.num_of_classes)))
        for i in range(self.num_of_classes):
            activations_mat = self.clusteron_vec[i].calculate_activations_by_dataset(dataset)
            outputs = self.clusteron_vec[i].calculate_outputs_from_activations(activations_mat)
            probability_predictions = self.clusteron_vec[i].calculate_predictions_from_outputs(outputs,function='logistic',predictions='probability')
            prediction_matrix[:,i] = np.reshape(probability_predictions,(P,1))
        predictions = np.argmax(prediction_matrix,1)
        accuracy = sum(np.where(np.squeeze(np.array(predictions)) == np.squeeze(Y),1,0))/P
        print('Multiclassifier accuracy = ',accuracy)
        self.accuracy_vec.append(accuracy)
        confusionMat = skmat.confusion_matrix(Y, predictions)
        return 
