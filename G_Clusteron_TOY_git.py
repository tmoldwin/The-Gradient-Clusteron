'''
G-Clusteron TOY model
'''
import numpy as np
import G_Clusteron_Parent as gcl
import general_Gclusteron_functions as genFunc

class G_Clusteron_TOY(gcl.G_Clusteron_Parent):
    def __init__(self,train_set,train_Y,radius,label,experiment,clstr_sz=None,
                 test_set=None,test_Y=None,posVal=None,save_folder=None,hist_folder=None,
                 weights = False):
        self.label = label
        self.experiment = experiment
        self.clstr_sz = clstr_sz
        self.clusterness_vec = []
        super().__init__(train_set,train_Y,test_set,test_Y,posVal,
                         radius,weights = weights)
        if label == 'pos': self.error_sign = -1
        elif label == 'neg': self.error_sign = 1
            
    def init_locations(self):
        if self.label == 'pos':
            locations = abs(np.linspace(0,1,self.num_of_syn))
            np.random.shuffle(locations)
        elif self.label == 'neg':
            if self.experiment == 'mv_gaussian':
                init_loc_values = np.arange(self.num_of_syn//self.clstr_sz)
                locations = np.float64(np.repeat(init_loc_values,self.clstr_sz))
            else:
                locations = 0.5*np.sign(self.train_set)+np.random.rand(100)*0.05#random noise added to make sure distance between synapses isn't 0
        return locations
        
    def train(self,epochs,learning_protocol,batch_size,location_lr,blr):
        location_mat = np.zeros((epochs, self.num_of_syn))
        activations_mat = np.zeros((epochs, self.num_of_syn))
        self.calculate_D_matrix(),self.calculate_F_matrix()
        activations = self.calculate_activations_by_dataset(self.train_set)

        for epoch in range(epochs):
            location_mat[epoch,:] = self.locations

            self.train_epoch(epoch,learning_protocol, batch_size, location_lr,
                        bias_lr = blr,weight_lr=0,W_momentum=False,B_momentum=False,
                        L_momentum=True)
            activations_mat[epoch,:] = np.mean(self.activations,0)

            self.location_mat = location_mat
            self.activations_mat = activations_mat

    def calculate_error_term(self,prediction_vec,correct_y):
        if self.experiment == 'uniform': error_term = np.array([self.error_sign])
        elif self.experiment == 'mv_gaussian': error_term = self.error_sign*np.ones(self.num_of_examples)
        return error_term
