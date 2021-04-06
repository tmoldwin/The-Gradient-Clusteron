#G-Clusteron

import random
import numpy as np
from matplotlib import pyplot as plt
import general_Gclusteron_functions as genFunc
    
class G_Clusteron_Parent():

    def __init__(self,train_set,train_Y,test_set,test_Y,posVal,radius, 
                 weights = False,init_distance_scale=None,bias_synapse = False,
                 bias_synapse_weight = 10):
        self.train_set = train_set
        self.train_Y = train_Y
        self.binary_train_Y = np.where(train_Y == posVal,1,0)
        self.test_set = test_set
        self.test_Y = test_Y
        self.binary_test_Y = np.where(test_Y == posVal,1,0)
        self.num_of_syn = np.shape(self.train_set)[1]
        self.radius = radius
        self.init_distance_scale = init_distance_scale
        self.locations = self.init_locations()
        self.bias = 0
        self.delta_bias = 0
        self.m_locations = 0
        self.v_locations = 0
        self.m_bias = 0
        self.v_bias = 0
        self.m_weights = 0
        self.v_weights = 0
        self.m_bias_w = 0#for weights, as oppsed to locations
        self.v_bias_w = 0
        self.weights = self.init_weights()
        if bias_synapse:
            self.train_set = genFunc.add_bias_synapse(self.train_set)
            self.test_set = genFunc.add_bias_synapse(self.test_set)
            self.weights = np.hstack((bias_synapse_weight,self.weights))
            self.num_of_syn = np.shape(self.train_set)[1]
            self.locations = self.init_locations()
            print("bias synapse on")
        self.delta_locations = np.zeros(self.num_of_syn)
        self.train_x_w = np.multiply((self.train_set),self.weights)
        self.num_of_examples = np.shape(self.train_set)[0]
        self.posVal = posVal
        self.training_examples_used = []#vector of the specific examples used during training with batch size of 1
        self.calculate_D_matrix()#distance,G,and delta locations matrices
        self.calculate_F_matrix()
    
    def init_locations(self):#location_params should be dict, scale should be 0.01
        return np.random.random(self.num_of_syn)*self.init_distance_scale
    
    def init_weights(self):
        return np.ones(self.num_of_syn)
    
    @classmethod
    def fromdict(cls, datadict):
        "Initialize MyData from a dict's items"
        return cls(datadict.items())
        
    def calculate_F_matrix(self):
        self.F_matrix = genFunc.calculate_F_matrix(self.distance_matrix, self.radius)

    def calculate_D_matrix(self):
        self.distance_matrix = genFunc.calculate_D_matrix(self.locations)

    def calculate_delta_locations_per_dataset(self,dataset,prediction_minus_y):
        return genFunc.calculate_delta_locations(self.F_matrix,self.distance_matrix,
                                                 dataset, self.weights, prediction_minus_y)

    def calculate_delta_weights(self,activations,prediction_minus_y):
        return genFunc.calculate_delta_weights(activations,self.weights,prediction_minus_y)

    def calculate_delta_bias(self,prediction_minus_y):
        return genFunc.calculate_delta_bias(prediction_minus_y)

    def update_locations(self,learning_rate, delta_locations, momentum = True):
        if momentum:
            delta_locations, self.m_locations, self.v_locations = genFunc.calculate_momentum_update(delta_locations,self.m_locations,self.v_locations)
        self.locations += learning_rate * delta_locations
        return

    def update_weights(self,learning_rate,delta_weights,momentum=True):#weight update for a batch, per epoch
        if momentum:
            delta_weights,self.m_weights,self.v_weights = genFunc.calculate_momentum_update(delta_weights,self.m_weights,self.v_weights)
        self.weights += learning_rate * delta_weights
        return
    
    def update_bias(self,learning_rate,delta_bias,momentum=True):#weight update for a batch, per epoch
        if momentum:
            delta_bias,self.m_bias,self.v_bias = genFunc.calculate_momentum_update(delta_bias,self.m_bias,self.v_bias)
        self.bias += learning_rate*delta_bias
        return

    def calculate_activations_by_dataset(self,dataset):
        return genFunc.calculate_activations(dataset, self.weights, self.F_matrix)
 
    def calculate_outputs_from_activations(self, activation_mat):
        return genFunc.calculate_outputs_from_activations(activation_mat, self.bias)

    def calculate_predictions_from_outputs(self,outputs,function,predictions='binary'):
        return genFunc.calculate_predictions_from_outputs(outputs)

    def calculate_error_term(self,prediction_vec,correct_y):
        return prediction_vec - correct_y

    def train_epoch(self, epoch_num,learning_protocol, batch_size, location_lr, weight_lr,
                    bias_lr,W_momentum, B_momentum, L_momentum,TOY_predict=0):
        self.calculate_D_matrix()#distance,G,and delta locations matrices
        self.calculate_F_matrix()
        ##Generate dataset for batch
        rand_vec = np.random.choice(range(self.num_of_examples),batch_size,replace=False)
        if batch_size == 1:
            self.training_examples_used.append(rand_vec[0])
        activations_matrix = self.calculate_activations_by_dataset(self.train_set[rand_vec])
        self.activations = activations_matrix#added this line so that I can pull the activations for the TOY model
        outputs_vec = self.calculate_outputs_from_activations(activations_matrix)
        prediction_vec = self.calculate_predictions_from_outputs(outputs_vec,self.bias)
        correct_y = self.binary_train_Y[rand_vec]#for OVR I added binary here, so if it breaks on SM, check this
        predict_minus_y_vec = self.calculate_error_term(prediction_vec,correct_y)
        if learning_protocol in ['B','L']:
            delta_locations = self.calculate_delta_locations_per_dataset(self.train_set[rand_vec],predict_minus_y_vec)
        if learning_protocol in ['B','W']:
            delta_weights = self.calculate_delta_weights(activations_matrix,predict_minus_y_vec)
        delta_bias = self.calculate_delta_bias(predict_minus_y_vec)
        
        if learning_protocol in ['B','L']:
            self.update_locations(location_lr, delta_locations, L_momentum)    
        if learning_protocol in ['B','W']:
            self.update_weights(weight_lr, delta_weights, W_momentum)  
        self.update_bias(bias_lr, delta_bias, B_momentum)    

    def train(self,epochs,learning_protocol, batch_size, location_lr, weight_lr,
              bias_lr,W_momentum, B_momentum, L_momentum,
              test=True,test_epoch=5,plot_accuracy = True):#deleted: w_momentum=true,b_m=true,l_m=true
        accuracy_vec = []
        for epoch in range(epochs):
            self.train_epoch(epoch,learning_protocol, batch_size, location_lr,
                        weight_lr, bias_lr,W_momentum, B_momentum,L_momentum)
            print('epoch = ',epoch)
            if test:
                if epoch%test_epoch==0:
                    accuracy = self.test(self.test_set,
                                         self.binary_test_Y)
                    accuracy_vec.append(accuracy)
            else:
                accuracy = self.test(self.test_set,self.binary_test_Y)
                accuracy_vec.append(accuracy)

        #when_finished()
        if plot_accuracy:
            plt.plot(np.arange(len(accuracy_vec)),accuracy_vec)
            plt.title('test set accuracy')
            plt.show()
        self.max_accuracy = np.max(accuracy_vec)
        print('max acc = ',self.max_accuracy)
        self.accuracy_vec = accuracy_vec
        return

    def test(self,test_set,binary_test_Y):
        return genFunc.test_accuracy(test_set,binary_test_Y,self.weights,self.F_matrix,
                                     self.bias)
