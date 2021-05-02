'''
G-Clusteron XOR
'''
import random
import numpy as np
import G_Clusteron_Parent as gcl
import copy

class G_Clusteron_XOR(gcl.G_Clusteron_Parent):
    def __init__(self,train_set,train_Y,test_set,test_Y,posVal,
                 radius,init_locations = 'normal_f',
                 weights = False):
        self.initial_locations = init_locations
        super().__init__(train_set,train_Y,test_set,test_Y,posVal,
                         radius, init_distance_scale = init_locations,
                 weights = weights)
        self.convergence = -1
        
    def init_locations(self):
        locations = np.zeros(np.shape(self.train_set)[1])
        random_f = np.random.random(1)
        locations[1] = np.sqrt(-(self.radius)*np.log(random_f))
        if self.initial_locations == 'normal_f_converge':
            locations = np.zeros(np.shape(self.train_set)[1])
            random_f = np.random.random(1)
            locations[1] = np.sqrt(-(self.radius)*np.log(random_f))
            f_init_dist = np.exp(-((locations[0]-locations[1])**2)/self.radius)
            while f_init_dist<=0.5:
                random_f = np.random.random(1)
                locations[1] = np.sqrt(-(self.radius)*np.log(random_f))
                f_init_dist = np.exp(-((locations[0]-locations[1])**2)/self.radius)
        self.initial_locations = copy.deepcopy(locations)
        return locations

    def init_weights(self,init_weights = 'random'):
        if init_weights == 'random':
            weights = np.random.uniform(-1,1,np.shape(self.train_set)[1])
        self.initial_weights = copy.deepcopy(weights)
        return weights

    def train(self,epochs,learning_protocol, batch_size, location_lr, weight_lr, bias_lr,
              W_momentum=False, B_momentum = False, L_momentum = False,test_epoch = 1):
        accuracy_vec = []
        for epoch in range(epochs):
            self.train_epoch(epoch,learning_protocol, batch_size, location_lr,
                        weight_lr, bias_lr,W_momentum, B_momentum,L_momentum)
            accuracy = self.test(self.test_set,
                                 self.binary_test_Y)
            accuracy_vec.append(accuracy)
            self.accuracy_vec = accuracy_vec
            if np.sum(accuracy_vec[-10:])==10:
                self.convergence = int(np.max((0,epoch-10)))
                break
        self.f_init_dist = np.exp(-((self.initial_locations[0]-self.initial_locations[1])**2)/self.radius)
        self.f_final_dist =np.exp(-((self.locations[0]-self.locations[1])**2)/self.radius)

        
