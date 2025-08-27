#General G-Clusteron
import random
import numpy as np
import matplotlib
from matplotlib.animation import FuncAnimation
from matplotlib import cm
from matplotlib import pyplot as plt
import pickle as pkl
import seaborn as sns
import cProfile
import pstats
from scipy import stats
import scipy.special as sp
import os
import sys
import shutil
from sklearn.metrics import roc_curve
import DataOrganizer as do
import codecs,json
import copy

class Clustering_algo():

    def __init__(self,train_set,train_Y,posVal,test_set=None,test_Y=None,
                radius = 0.4,bias = 1,XOR=False,init_weights = 'random',
                 init_locations = 'random', location_scale = 1, shuffle=True):
        self.train_set = train_set
        self.train_Y = train_Y
        self.binary_train_Y = np.where(train_Y == posVal,1,0)
        self.test_set = test_set
        self.test_Y = test_Y
        self.binary_test_Y = np.where(test_Y == posVal,1,0)
        ##self.pos_data,self.neg_data,pos_train_Y,neg_train_Y = do.split_data_by_posVal(train_set,train_Y,posVal)
        ##self.test_pos,self.test_neg,pos_test_Y,neg_test_Y = do.split_data_by_posVal(test_set,test_Y,posVal)
        self.num_of_syn = np.shape(self.train_set)[1]
        self.radius = radius
        self.test_accuracy_vec = np.array([])
        self.bias = bias
        k = -(self.radius**2)/np.log(0.5)
        if init_locations == 'random':
            self.initial_locations = np.random.uniform(-1,1,np.shape(train_set)[1])
        elif init_locations == 'linspace':
            initial_locations = abs(np.linspace(0,1,np.shape(train_set)[1]))
            if shuffle:
                np.random.shuffle(initial_locations)
            self.initial_locations = initial_locations
        elif init_locations == 'ones':
            self.initial_locations = np.ones(np.shape(train_set)[1])
        elif init_locations == 'normal_f':
            self.initial_locations = np.zeros(np.shape(train_set)[1])
            random_f = np.random.random(1)*location_scale
            self.initial_locations[1] = np.sqrt(-(k)*np.log(random_f))
        elif init_locations == 'normal_f_converge':#this was done to only get initialization that are expected to converge
            self.initial_locations = np.zeros(np.shape(train_set)[1])
            random_f = np.random.random(1)*location_scale
            self.initial_locations[1] = np.sqrt(-(k)*np.log(random_f))
            f_init_dist = np.exp(-((self.initial_locations[0]-self.initial_locations[1])**2)/k)
            while f_init_dist<=0.5:
                random_f = np.random.random(1)*location_scale
                self.initial_locations[1] = np.sqrt(-(k)*np.log(random_f))
                f_init_dist = np.exp(-((self.initial_locations[0]-self.initial_locations[1])**2)/k)
        self.locations = copy.deepcopy(self.initial_locations)
        if init_weights == 'random':
            self.initial_weights = np.random.uniform(-1,1,np.shape(train_set)[1])
        elif init_weights == 'ones':
            self.initial_weights = np.ones(np.shape(train_set)[1])
        elif init_weights == 'convergable':#this was done to only get initialization that are expected to converge
            self.initial_weights = np.random.uniform(-1,1,np.shape(train_set)[1])
            w_1,w_2 = self.initial_weights[0],self.initial_weights[1]
            while not ((np.sign(w_1)!=np.sign(w_2)) and (abs(w_1)<2*abs(w_2)) and (abs(w_2)<2*abs(w_1))):
                self.initial_weights = np.random.uniform(-1,1,np.shape(train_set)[1])
                w_1,w_2 = self.initial_weights[0],self.initial_weights[1]
        self.weights = copy.deepcopy(self.initial_weights)
        self.train_x_w = np.multiply((self.train_set),self.weights)
        self.num_of_examples = np.shape(self.train_set)[0]
        self.posVal = posVal
        self.XOR = XOR
        self.convergence = -1
        #print(self.weights)
        
    @classmethod
    def fromdict(cls, datadict):
        "Initialize MyData from a dict's items"
        return cls(datadict.items())
     
    def calculate_distance_matrix(self,initial=False):#use old file if loading old locations
        if initial:
            tile_mat = np.tile(self.initial_locations,(self.num_of_syn,1))
            self.distance_matrix = np.transpose(np.mat(self.initial_locations))-tile_mat
        else:
            tile_mat = np.tile(self.locations,(self.num_of_syn,1))    
            self.distance_matrix = np.transpose(np.mat(self.locations))-tile_mat
        return self.distance_matrix
        
    def calculate_G_matrix(self,distance_matrix):
        k = -(self.radius**2)/np.log(0.5)
        self.G_matrix = np.exp((-np.multiply(distance_matrix,distance_matrix))/k)#e^-(l(i)-l(j))^2
        return self.G_matrix

    def calculate_delta_location_matrix(self,G_matrix,distance_matrix):
        self.delta_location_matrix = np.multiply(G_matrix,distance_matrix)
        return self.delta_location_matrix

    def update_locations(self,example,distance_matrix,delta_location_matrix,
                         L_minus_Y,location_update_sign=-1,x_j_example=None,vector_field=False):
        XtX = np.transpose(np.matrix(example))*example
        delta_location_matrix_2 = np.multiply(delta_location_matrix,XtX)
        delta_locations = np.squeeze(np.array(np.sum(delta_location_matrix_2,0)))
        k = -(self.radius**2)/np.log(0.5)
        #print('L_Y in func = ',L_minus_Y)
        return delta_locations*L_minus_Y#-delta_locations for positive data

    def calculate_just_activations(self,dataset):
        x_w_example = np.multiply((dataset),self.weights)
        fi_mins_j_matrix = np.dot(x_w_example,self.G_matrix)
        activations_matrix = np.multiply(x_w_example,fi_mins_j_matrix)
        example_outputs = np.squeeze(np.asarray(np.sum(activations_matrix,1)))
        return example_outputs,activations_matrix

    def calculate_activation_by_dataset(self,dataset,Y,datatype = 'train',normalize_outputs = None,
                                        multiclass = False,num=None):#Y must be binary
        if np.shape(dataset)[0] == 1:
                dataset = np.array([dataset,])
                x_w_example = dataset
        else:
            x_w_example = np.multiply((dataset),self.weights)
        fi_mins_j_matrix = np.dot(x_w_example,self.G_matrix)
        self.fi_mins_j_matrix = fi_mins_j_matrix
        self.x_w_example = x_w_example
        activations_matrix = np.multiply(np.matrix(x_w_example),fi_mins_j_matrix)
        #print(np.shape(activations_matrix))
        self.synapse_average = sum(activations_matrix)/len(Y) #vector of synapse average activations
        example_outputs = np.squeeze(np.asarray(np.sum(activations_matrix,1)))
        #print(np.shape(example_outputs))
        #print('eo = ',example_outputs[:10])
        if normalize_outputs: example_outputs = 2*(example_outputs-min(example_outputs))/(max(example_outputs)-min(example_outputs))-1
        if len(Y) == 1:
            pass
        else:
            if datatype == 'train':
                    fpr = dict()
                    tpr = dict()
                    fpr,tpr,biases = roc_curve(Y,example_outputs)
                    #self.bias = biases[np.argmax((tpr-fpr+1)/2)] #comment in for MNIST
        logistic_function = sp.expit((example_outputs - self.bias))
        #print('lo = ',logistic_function)
        if multiclass:
            logistic_function = sp.expit((example_outputs - self.bias)/(np.std(example_outputs)))    
        predicts_binary = np.where(logistic_function>=0.5,1,0)
        #print('predict = ',predictions)
        pmy = predicts_binary - np.squeeze(Y)
        #print(' p - y = ',pmy)
        #print('Y = ',Y)
        #print('pmy = ',sum(pmy))
        if len(Y) == 1:                                          
            pass
        else:
            fps = sum(x == 1 for x in pmy)/sum(x == 0 for x in Y)
            fngs = sum(x == -1 for x in pmy)/sum(x == 1 for x in Y)
        accuracy = 1-((np.sum(abs(predicts_binary-np.squeeze(Y))))/len(dataset))
        #print(len(dataset))
        #print('accuracy = ',accuracy)
        #if not self.XOR:
        predictions = logistic_function
        return activations_matrix,example_outputs,predictions,accuracy,predicts_binary

    def learn(self,epochs,location_learning_rate = 0.0001,bias_learning_rate=500,batch_size = 10,
              num_of_arrows=5,vector_field = False,momentum_weights=False,momentum_locations=False,
              weight_learning_rate=0.1,location_update_sign=-1,plot=False,stop_early=False,
              break_if_accuracy_goes_under_1=False):
                
        #Good values for balanced data set
#         learning_rate = 0.0001
#         batch_size = 50 #size of batches for mini batch learning
#         bias_learning_rate =500 was good for MNIST
        location_mat = np.empty((epochs+1, self.num_of_syn))
        activations_mat = np.empty((epochs+1, self.num_of_syn))
        weights_mat = np.empty((epochs+1, self.num_of_syn))
        weights_mat[0] = self.weights
        if vector_field:
            vector_field_mat = np.empty((epochs+1, num_of_arrows))
            vector_field_x_j_example = self.train_x_w
        location_mat[0] = self.initial_locations
        m_bias = 0
        v_bias = 0
        m_locations = 0
        v_locations = 0
        m_weights = 0
        v_weights = 0
        beta1 = 0.9
        beta2 = 0.999
        eps = 1e-8
        train_accuracies = []
        #test_accuracies = []
        bias_vec = []
        SNR_vec = []
        self.distance_matrix = self.calculate_distance_matrix(initial=True)
        self.G_matrix = self.calculate_G_matrix(self.distance_matrix)
        self.delta_location_matrix = self.calculate_delta_location_matrix(self.G_matrix,self.distance_matrix)
        _,_,_,_,_ = self.calculate_activation_by_dataset(self.train_set,self.binary_train_Y)
        activations_mat[0] = self.synapse_average
        mat_of_hits = np.empty((self.num_of_examples,epochs))#matrix of values for correct predictions
        vec_of_exmpls_trained_on = []
        #mat_of_hits[:,:self.num_of_syn] = np.int0(self.train_set)
        #vector_field_mat[0] = self.update_locations(vector_field_example,self.distance_matrix,self.delta_location_matrix)
        for epoch in range(epochs):
            #print('epoch=',epoch)
            #print('weights = ',self.weights)
            #print('bias = ',self.bias)
            if vector_field:
                vector_field_mat[epoch] = self.create_vector_field(vector_field_x_j_example,num_of_arrows)
            delta_locations = np.zeros(np.shape(self.locations))
            self.distance_matrix = self.calculate_distance_matrix()
            self.G_matrix = self.calculate_G_matrix(self.distance_matrix)
            self.delta_location_matrix = self.calculate_delta_location_matrix(self.G_matrix,self.distance_matrix)
            delta_bias = 0
            delta_weights = np.zeros(np.shape(self.weights))
            if epoch == 0 and len(self.train_Y) != 1:
                if self.test_set:
                    _,example_outputs,_,_,_ = self.calculate_activation_by_dataset(self.test_set,self.binary_test_Y,datatype = 'test')
            activations_matrix,example_outputs,predictions,accuracy,predicts_binary = self.calculate_activation_by_dataset(self.train_set,self.binary_train_Y)
            mat_of_hits[:,epoch] = predictions
            #print('predictions = ',predictions)
            if self.num_of_examples == 1:
                L_minus_Y = predictions - self.binary_train_Y 
                delta_locations += self.update_locations(self.train_x_w,self.distance_matrix,
                                                         self.delta_location_matrix,L_minus_Y,
                                                         location_update_sign)
                delta_bias += L_minus_Y
                if vector_field:
                    vector_field_x_j_example = self.train_x_w#example to be used for w_i_x_i_w_j_x_j for vector field
            else:
                rand_vec = np.random.choice(range(self.num_of_examples),batch_size,replace=True)
                for num in rand_vec:
##                    print('example = ',self.train_set[num])
                    vec_of_exmpls_trained_on.append(self.train_set[num])
                    L_minus_Y = predictions[num] - self.binary_train_Y[num]
                    
                    act_divid_by_wts = np.array(activations_matrix[num])/self.weights
                    delta_weights -= np.random.randn(self.num_of_syn)*0.0 + np.squeeze(2*act_divid_by_wts*L_minus_Y) #lambd*self.weights
                    
                    delta_locations -= np.random.randn(self.num_of_syn)*0.0 + self.update_locations(self.train_x_w[num],
                                                             self.distance_matrix,
                                                             self.delta_location_matrix,
                                                             L_minus_Y)
                    #print(delta_locations)
                    current_dist = np.abs(self.locations[0]-self.locations[1])
                    final_dist = np.abs(self.locations[0]+delta_locations[0]-(self.locations[1]+delta_locations[1]))
##                    print('current dist = ',current_dist)
##                    print('final dist = ',final_dist)
##                    print('delta_locations = ',delta_locations)
##                    print('locations = ',self.locations)
##                    print('L_Y = ',L_minus_Y)
##                    print('Prediction = ',predictions[num])
##                    print('True Y = ',self.binary_train_Y[num])
##                    print('Weights = ',self.weights)
##                    print('Delta Weights = ',delta_weights)
##                    print('x_w = ',self.train_x_w)
                    if (self.train_set[num]==[0,0]).all():
                        assert (delta_weights==[0,0]).all() and np.sum(delta_locations) ==0, 'Error 1'

                    elif (self.train_set[num]==[1,1]).all():
                        assert delta_locations[0] == -delta_locations[1], 'Error 2'
                        
                        
                        if self.weights[0]*self.weights[1]>=0:
                            #assert final_dist>current_dist,'Error 3'
                            
                            assert (np.sign(delta_weights)==-np.sign(self.weights)).all(),'Error 3a'
                        #else:
                            #assert final_dist<current_dist,'Error 4'
                            
                    if (self.train_set[num] == [1,0]).all():
                        assert delta_weights[1]==0, 'Error 5'
                        assert np.sign(self.weights[0])==np.sign(delta_weights[0]),'Error 6'
                    elif (self.train_set[num] == [0,1]).all():
                        assert delta_weights[0]==0, 'Error 7'
                        assert np.sign(self.weights[1])==np.sign(delta_weights[1]),'Error 8'

                        
                         
                        
                    delta_bias += L_minus_Y
                    #print('logistic output = ',predictions[num])
                    if vector_field:
                        vector_field_x_j_example = self.train_x_w[num]#example to be used for w_i_x_i_w_j_x_j for vector field
                    #print('example outputs
            #print('weights = ',self.weights)
            #print('distance = ',abs(self.locations[0][1]-self.locations[0][0]))
            #print('bias = ',self.bias)
            self.bias += bias_learning_rate*delta_bias
            if momentum_locations:
                m_locations = beta1*m_locations + (1-beta1)*delta_locations
                v_locations = beta2*v_locations + (1-beta2)*(delta_locations**2)
                self.locations += np.squeeze(location_learning_rate*m_locations/(np.sqrt(v_locations)+eps))
            else:
                self.locations += np.squeeze(location_learning_rate*delta_locations)
            if momentum_weights:
                m_weights = beta1*m_weights + (1-beta1)*delta_weights
                v_weights = beta2*v_weights + (1-beta2)*(delta_weights**2)
                self.weights += np.squeeze(weight_learning_rate*m_weights/(np.sqrt(v_weights)+eps))
            else:
                self.weights += np.squeeze(weight_learning_rate*delta_weights)
            self.train_x_w = np.multiply((self.train_set),self.weights)
            weights_mat[epoch+1] = self.weights
            #print(weights_mat)
            #if epoch == epochs: activation_matrix,example_outputs,_,accuracy,_ = self.calculate_activation_by_dataset(self.train_set,self.binary_train_Y,datatype = 'train',normalize_outputs = True)
            #else: _,example_outputs,_,accuracy,_ = self.calculate_activation_by_dataset(self.train_set,self.binary_train_Y,datatype = 'train')
            train_accuracies.append(accuracy)
            if break_if_accuracy_goes_under_1:
                if epoch>3:
                    if train_accuracies[-2]==1 and accuracy<1:
                        print('went down in accuracy')
            if stop_early:
                if np.sum(train_accuracies[-10:])==10:
                    self.convergence = epoch-10
                    #print('epoch converged = ',epoch)
                    break   
            bias_vec.append(self.bias)
            location_mat[epoch+1,:] = self.locations
            activations_mat[epoch+1,:] = self.synapse_average
            #vector_field_mat[epoch+1,:] = self.update_locations(vector_field_example,self.distance_matrix,self.delta_location_matrix)
            #print('delta_weights = ',delta_weights)
            #print('delta_locations = ',delta_locations)
            #print('delta_bias = ',delta_bias)
        self.location_mat = location_mat
        self.activations_mat = activations_mat
        self.train_accuracy_vec = train_accuracies
        #print('accuracies = ',train_accuracies)
        if vector_field:
            vector_field_mat[-1,:] = self.create_vector_field(vector_field_x_j_example,num_of_arrows)
            self.vector_field_mat = vector_field_mat
        #print('predictions = ',predictions)
        self.predictions = predictions
        self.weights_mat = weights_mat
        if plot and self.convergence == -1:
            plt.figure('Weights')
            #plt.legend(('Weight 1','Weight 2'))
            plt.plot(weights_mat[:,0])
            plt.plot(weights_mat[:,1])
            plt.figure('Locations')
            plt.plot(location_mat[:,0])
            plt.plot(location_mat[:,1])
            plt.figure('Bias')
            plt.plot(bias_vec)
            plt.figure('f(l_1,l_2)')
            k = -(self.radius**2)/np.log(0.5)
            distance_mat = location_mat[:-1,0]-location_mat[:-1,1]
            plt.plot(np.exp((-np.multiply(distance_mat,distance_mat))/k))
            plt.figure('Accuracies')
            plt.plot(train_accuracies)
            plt.figure('Table of Hits')
            plt.subplot(3,1,1)
            plt.title('Logistic Output')
            plt.imshow(mat_of_hits,aspect = 'auto')
            plt.yticks(np.arange(4),self.train_set)
    ##        xlabels = str(vec_of_exmpls_trained_on)
    ##        string = 
            #plt.xticks(np.arange(epochs),' '.join(str(x) for x in vec_of_exmpls_trained_on),rotation = 90)
            #plt.xticks(np.arange(epochs),vec_of_exmpls_trained_on,rotation = 90)
            plt.colorbar()
            plt.subplot(3,1,2)
            plt.title('Weights')
            plt.imshow((weights_mat[:-1,0],weights_mat[:-1,1]),aspect = 'auto')
            plt.colorbar()
            #plt.xticks(np.arange(epochs),vec_of_exmpls_trained_on,rotation = 90)
            plt.yticks(np.arange(2),['Weight 1','Weight 2'])
            plt.subplot(3,1,3)
            plt.title('Distance Function')
            plt.imshow((np.exp((-np.multiply(distance_mat,distance_mat))/k),
                       np.exp((-np.multiply(distance_mat,distance_mat))/k)),aspect = 'auto')
            plt.colorbar()
            plt.yticks(np.arange(1),'f(l_1,l_2)')
            #plt.xticks(np.arange(epochs),vec_of_exmpls_trained_on,rotation = 90)
            plt.tight_layout()
            plt.show()
            plt.figure('WeightsAndDistance')
            plt.plot(weights_mat[:,0])
            plt.plot(weights_mat[:,1])
            plt.plot(location_mat[:,0]-location_mat[:,1])
            plt.show()
        k = -(self.radius**2)/np.log(0.5)
        self.f_init_dist = np.exp(-((self.initial_locations[0]-self.initial_locations[1])**2)/k)
        self.f_final_dist =np.exp(-((self.locations[0]-self.locations[1])**2)/k)
        return
    
    def create_vector_field(self,x_j_example,num_of_arrows=6):
        location_dist_step = (np.max(self.locations)-np.min(self.locations))/num_of_arrows
        self.vector_field_example_locations = np.linspace(np.min(self.locations)-location_dist_step
                                                     ,np.max(self.locations)+location_dist_step,
                                                     num_of_arrows)
        tile_mat = np.tile(self.locations,(num_of_arrows,1))
        distance_matrix = (tile_mat-np.transpose(np.mat(self.vector_field_example_locations)))
        #G_matrix
        k = -(self.radius**2)/np.log(0.5)
        G_matrix = np.exp((-np.multiply(distance_matrix,distance_matrix))/k)#e^-(l(i)-l(j))^2
        #delta location matrix
        delta_location_matrix = np.multiply(G_matrix,distance_matrix)
        x_j_w_j = np.multiply(x_j_example,self.weights)
        w_x = np.tile(x_j_w_j,(num_of_arrows,1))
        delta_location_matrix_2 = np.multiply(delta_location_matrix,w_x)
        delta_locations = np.squeeze(np.array(np.sum(delta_location_matrix_2,1)))
        return delta_locations

    
