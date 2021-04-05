'''
clusteron algorithm
'''
from random import shuffle
from matplotlib import pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve
import scipy.special as sp
import DataOrganizer as DO

class Clusteron():
    
    def __init__(self,pos_trainX,neg_trainX,trainXall,trainYall,pos_testX,neg_testX,testXall,
                 testYall,posVal,syn_at_halfVal=10,radius=8,pix_to_syn = None):
        self.posVal = posVal
        self.trainXall = trainXall
        self.trainYall = trainYall
        self.testXall = testXall
        self.testYall = testYall
        self.trainXPos,self.trainXNeg = pos_trainX,neg_trainX
        self.testXPos,self.testXNeg = pos_testX,neg_testX
        self.Y_binary_vector = np.where(trainYall == posVal,1,0)
        self.Y_binary_vector_test = np.where(testYall == posVal,1,0)
        self.N = len(self.trainXPos[0]) #N = number of columns (pixels in 1 picture)
        self.P = len(self.trainXPos)+len(self.trainXNeg) #number of rows (pictures)
        self.radius = radius
        self.weights = np.ones(self.N)
        self.bias = 1 #random starting threshold for activations
        self.initial_activations = None
        self.thresholds = np.empty(0)
        self.gaussian_matrix = np.zeros([self.N,self.N])
        for i in range(self.N):
                start = max(0,i-radius)
                end = min(self.N,i+radius)
                self.gaussian_matrix[start:end,i] = 1
        self.neighbor_map = {}
        if pix_to_syn == None:
            self.pix_to_syn = np.array(list(range(self.N)))
            np.random.shuffle(self.pix_to_syn)
        else:
            self.pix_to_syn = np.array(pix_to_syn)           
        self.syn_to_pix = np.array(list(range(self.N)))
        self.update_syn_to_pix()
        self.accuracy_vec = []
        
    def update_syn_to_pix(self):
        self.syn_to_pix = np.array([self.pix_to_syn.tolist().index(i) for i in range(self.N)])

    def update_pix_to_syn(self):
        self.pix_to_syn = np.array([self.syn_to_pix.tolist().index(i) for i in range(self.N)])

    def calculate_activation_by_dataset_new(self,dataset,normalized=True):
        if len(np.shape(dataset)) == 1:
                dataset = np.array([dataset,])
        self.neuron_data = dataset[:,self.syn_to_pix]
        x_w = self.neuron_data*self.weights
        fi_mins_j_matrix = np.dot(x_w,self.gaussian_matrix)
        self.activations_matrix = x_w*fi_mins_j_matrix
        self.example_outputs = np.sum(self.activations_matrix,1)
        return self.activations_matrix,self.example_outputs

    def find_neighbors(self,synapse): #call once per epoch
        start = max(0,synapse-self.radius)
        end = min(self.N-1,synapse + self.radius)
        return np.array(self.syn_to_pix)[range(start,end+1)]

    def calculate_output(self,dataset): #vector of activations for a dataset 
        self.calculate_activation_by_dataset_new(dataset)
        self.example_outputs = self.activations_matrix.sum(1) #vector of sum of synapse activations for each example
        self.synapse_average = sum(self.activations_matrix)/self.P #vector of synapse average activations
        self.first_example_activations = self.activations_matrix[0]
        return self.example_outputs

    def perform_swaps(self,value):
        if value: synapses_to_swap = [synapse for synapse in range(self.N) if self.synapse_average[synapse] < self.threshold]
        elif not value: synapses_to_swap = [synapse for synapse in range(self.N) if self.synapse_average[synapse] > self.threshold]
        shuffle(synapses_to_swap)
        plc_holder = self.syn_to_pix[synapses_to_swap[0]]
        for i in range(len(synapses_to_swap)-1):
            self.syn_to_pix[synapses_to_swap[i]] = self.syn_to_pix[synapses_to_swap[i+1]]
        self.syn_to_pix[synapses_to_swap[len(synapses_to_swap)-1]] = plc_holder
        self.syn_to_pix = np.array(self.syn_to_pix)
        self.update_pix_to_syn()
        
    def average_activation(self,dataset,value,i):
        self.calculate_output(dataset)
        individ_activations_matrix = self.activations_matrix
        synapse_average_activation = self.synapse_average #vector of average activation per synapse over data set
        self.activation_mat[i] = individ_activations_matrix[0]
        if value:
            self.threshold = np.mean(synapse_average_activation)
            self.thresholds = np.append(self.thresholds,self.threshold)
        return individ_activations_matrix

    def learning_algo(self,number_of_epochs,pos_neg='positive',plot=False):
        self.initial_pos_exmpl_activations = self.calculate_activation_by_dataset_new(self.testXPos[0])
        self.initial_neg_exmpl_activations = self.calculate_activation_by_dataset_new(self.testXNeg[0])
        self.calculate_output(self.trainXall)
        self.ROC_curve(self.Y_binary_vector,self.example_outputs)
        self.activation_mat = np.empty((number_of_epochs,self.N))
        self.test_accuracies_vec = []
        for i in range(number_of_epochs):
            print(i)
            self.calculate_sigmoid_accuracy(self.testXall,self.prediction_threshold,self.Y_binary_vector_test)
            self.test_accuracies_vec.append(self.epoch_accuracy)
            self.calculate_output(self.trainXall)
            self.ROC_curve(self.Y_binary_vector,self.example_outputs)
            self.neighbor_map = {synapse:self.find_neighbors(synapse) for synapse in range(self.N)}
            if pos_neg == 'positive':             
                if i == 0:
                    self.average_activation(self.trainXPos,1,i)
                    self.initial_activations = self.synapse_average
                    self.perform_swaps(True)
                else:
                    self.average_activation(self.trainXPos,1,i)
                    self.perform_swaps(True)
            elif pos_neg == 'negative':
                if i == 0:
                    self.average_activation(self.trainXNeg,1,i)
                    self.initial_activations = self.synapse_average
                    self.perform_swaps(False)
                else:
                    self.average_activation(self.trainXNeg,1,i)
                    self.perform_swaps(False)
        self.calculate_output(self.trainXall)
        self.ROC_curve(self.Y_binary_vector,self.example_outputs)
        self.calculate_sigmoid_accuracy(self.testXall,self.prediction_threshold,self.Y_binary_vector_test)
        plt.plot(self.accuracy_vec)
        if plot:plt.show()
        self.max_accuracy = max(self.accuracy_vec)
        print('max acc = ',self.max_accuracy)

    def ROC_curve(self,binary_Y,outputs):#takes dataset outputs with it's binary vector and finds the optimal prediction threshold based on minimum error
        fpr = dict()
        tpr = dict()
        fpr, tpr, thresholds = roc_curve(binary_Y,outputs)
        accuracy = (tpr-fpr+1)/2
        self.accuracy_vec.append(max(accuracy))
        self.accuracy = max(accuracy)
        self.prediction_threshold = thresholds[np.argmax(accuracy)]
        return self.prediction_threshold,self.accuracy

    def calculate_sigmoid_accuracy(self,dataset,bias,y):
        _,example_outputs = self.calculate_activation_by_dataset_new(dataset)
        output_vector = sp.expit(example_outputs-bias)
        binary_output_vector = np.where(output_vector>=0.5,1,0)
        errors = binary_output_vector-np.squeeze(y)
        error_sum = sum(abs(errors))
        self.epoch_accuracy = 1-(error_sum/len(dataset))
        return 
    
if __name__ == '__main__':
    algorithm = 'clusteron' 
    posVal = 5
    x_train, y_train, x_test, y_test, x_train_balanced, y_train_balanced = DO.get_data(algorithm, posVal)

    _,neg_data,_,_ = DO.split_data_by_posVal(x_train_balanced,
                                             y_train_balanced,posVal)

    test_pos,test_neg,_,_ = DO.split_data_by_posVal(x_test,y_test,posVal)

    num_of_epochs = 3

    clstr = Clusteron(x_train,neg_data,x_train_balanced,
                      y_train_balanced,test_pos,test_neg,x_test,y_test,posVal=posVal,
                      syn_at_halfVal=10)
    clstr.learning_algo(num_of_epochs,'positive',plot=False)

