'''
multiclassifier for G-clusteron with softmax
(name used to be Multi_classifier_Tovia_cleaned)
'''
from G_Clusteron_SM import G_Clusteron_SM
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import DataOrganizer as do
    
class MultiClassifier():

    def __init__(self,train_set,train_Y,test_set,test_Y,classes, radius,bias_synapse,
                 bias_synapse_weight,):
        self.num_of_exmpls = len(train_set)
        self.train_set = train_set
        self.train_Y = train_Y
        self.test_set = test_set
        
        self.test_Y = test_Y
        self.classes = classes
        self.bs = bias_synapse
        self.bsw = bias_synapse_weight
        self.num_of_classes = len(classes)
        self.clusteron_vec = [None]*self.num_of_classes
        self.num_of_syn = len(self.train_set[0])
        for i in range(self.num_of_classes):
            print('clusteron ',classes[i])
            clusteron = G_Clusteron_SM(self.train_set,self.train_Y,self.test_set,
                                       self.test_Y,classes[i],radius = radius,
                                       bias_synapse = self.bs,
                                       bias_synapse_weight = self.bsw)
            self.clusteron_vec[i] = clusteron
        if bias_synapse:
            self.train_set = np.hstack((np.ones((self.num_of_exmpls,1)),self.train_set))
            self.test_set = np.hstack((np.ones((len(self.test_set),1)),self.test_set))
            self.num_of_syn = len(self.train_set[0])
            
    def make_one_hot(self, correct_y):
            one_hot_matrix = np.zeros((len(correct_y),10))
            one_hot_matrix[np.arange(len(correct_y)),correct_y]=1
            one_hot_matrix = np.squeeze(one_hot_matrix[:,[self.classes]])
            one_hot_matrix = np.transpose(one_hot_matrix)
            if np.ndim(one_hot_matrix)==1:
                one_hot_matrix = np.reshape(one_hot_matrix,(self.num_of_classes,1))
            return one_hot_matrix
        
    def softmax_prediction_matrix(self,outputs_matrix):
        self.rr = outputs_matrix
        pre_predict_matrix = np.exp(outputs_matrix.astype('float'))
        prediction_matrix = pre_predict_matrix/np.sum(pre_predict_matrix,0)
        return prediction_matrix                 
            
    def train(self,epochs,learning_protocol, batch_size, location_lr, weight_lr,
              bias_lr,W_momentum=True, B_momentum = True, L_momentum = True,
              plot_confusion_M = False,test_epoch=5,
              plot_activations_curve = False):
        count = 0
        accuracy_vec = []

        for epoch in range(epochs):
            print('epoch = ',epoch)
            for clusteron in range(self.num_of_classes):
                    self.clusteron_vec[clusteron].calculate_D_matrix()#distance,G,and delta locations matrices
                    self.clusteron_vec[clusteron].calculate_F_matrix()
            ##Generate dataset for batch
            rand_vec = np.random.choice(range(self.num_of_exmpls),batch_size,replace=False)
            outputs_matrix = np.matrix(np.reshape([None]*self.num_of_classes*batch_size,(self.num_of_classes,batch_size)))#creates an empty matrix for the outputs
            activations_matrix = [None]*self.num_of_classes
            for clusteron in range(self.num_of_classes):
                activations_matrix[clusteron] = self.clusteron_vec[clusteron].calculate_activations_by_dataset(self.train_set[rand_vec])
                outputs_matrix[clusteron] = self.clusteron_vec[clusteron].calculate_outputs_from_activations(activations_matrix[clusteron])         
            prediction_matrix = self.softmax_prediction_matrix(outputs_matrix)
            correct_y = self.train_Y[rand_vec]            
            one_hot_matrix = self.make_one_hot(correct_y)
            predict_minus_y_mat = prediction_matrix - one_hot_matrix
            for clusteron in range(self.num_of_classes):
                predict_minus_y_vec = np.array(np.transpose(predict_minus_y_mat[clusteron]))
                if learning_protocol in ['B','L']:
                    delta_locations = self.clusteron_vec[clusteron].calculate_delta_locations_per_dataset(self.train_set[rand_vec],predict_minus_y_vec)
                if learning_protocol in ['B','W']:
                    delta_weights = self.clusteron_vec[clusteron].calculate_delta_weights(activations_matrix[clusteron],predict_minus_y_vec)
                delta_bias = self.clusteron_vec[clusteron].calculate_delta_bias(predict_minus_y_vec)
                
                if learning_protocol in ['B','L']:
                    self.clusteron_vec[clusteron].update_locations(location_lr, delta_locations, L_momentum)    
                if learning_protocol in ['B','W']:
                    self.clusteron_vec[clusteron].update_weights(weight_lr, delta_weights, W_momentum)  
                self.clusteron_vec[clusteron].update_bias(bias_lr, delta_bias, B_momentum)    
            
            if count%test_epoch==0:
                accuracy = self.test(self.test_set,
                                     self.test_Y,confusion_matrix=plot_confusion_M,
                                     activations_plot=plot_activations_curve)
                print('Multiclassifier accuracy = ',accuracy)
                accuracy_vec.append(accuracy)
            count += 1
        accuracy = self.test(self.test_set,
                                     self.test_Y,confusion_matrix=plot_confusion_M,
                                     activations_plot=plot_activations_curve)
        print(accuracy)
        accuracy_vec.append(accuracy)
        self.accuracy_vec = accuracy_vec
        return
    
    def test(self,dataset,Y,confusion_matrix=None,activations_plot=None):
        P = len(Y)
        outputs_matrix = np.matrix(np.reshape([None]*self.num_of_classes*P,(self.num_of_classes,P)))#creates an empty matrix for the activations
        for clusteron in range(self.num_of_classes):
            activations_clusteron = self.clusteron_vec[clusteron].calculate_activations_by_dataset(dataset)
            outputs_matrix[clusteron] = self.clusteron_vec[clusteron].calculate_outputs_from_activations(activations_clusteron)
        prediction_matrix = np.exp(np.float16(outputs_matrix))/np.sum(np.exp(np.float16(outputs_matrix)),0)
        clusteron_predictions = np.argmax(prediction_matrix,0)#gives predictions based on clusteron location in vector, not class
        accuracy = np.sum(np.where(self.classes[[clusteron_predictions]]==Y,1,0))/P
        if confusion_matrix:
            self.predictions = np.argmax(prediction_matrix,0)
            self.predictions = np.squeeze(np.reshape(np.array(self.predictions),(P,1)))
            confusionMat = plot_confusion_matrix(Y,self.classes[[clusteron_predictions]][0],self.classes) 
        if activations_plot:
            plt.figure()
            for i in range(self.num_of_classes):
                sns.distplot(outputs_matrix[i],label=i,hist=False)
                plt.axvline(self.clusteron_vec[i].bias)
            plt.show()
        return accuracy

hist_folder = 'Histograms/'
if __name__ == '__main__':
    num_epochs = 2000
    plot_accuracies = False
    'bias synapse'
    bs = False
    bsw = 2
    for learning_protocol in ['L','W','B']:#locations, weights, both
        rule = learning_protocol
        print('Learning protocol = ',rule)
        if rule == 'B':
            #Parameters for Both
             batch_size = 5
             location_lr = 0.00001
             weight_lr = 0.00001
             bias_lr=location_lr
             num_of_test_exmpls = 1000
             location_rule = True
             weight_rule = True
        if rule == 'L':
            #Parameters for Locations
            batch_size = 3
            location_lr = 0.000005
            weight_lr = 0
            bias_lr=location_lr
            num_of_test_exmpls = 1000
            location_rule = True
            weight_rule = False
        if rule == 'W':
            #Parameters for Weights
            batch_size = 30
            location_lr = 0
            weight_lr = 0.00001
            bias_lr=weight_lr
            num_of_test_exmpls = 1000
            location_rule = False
            weight_rule = True

        algorithm = 'G-clusteron_SM'
        x_train, y_train, x_test, y_test,_,_ = do.get_data(algorithm)
        radius_convert = lambda x: -(x**2)/np.log(0.5)
        radius = radius_convert(0.4)
        multiclassifier = MultiClassifier(x_train, y_train, x_test, y_test,
                                          classes, radius = radius,bias_synapse = bs,
                                          bias_synapse_weight = bsw)
        multiclassifier.train(num_epochs,
                              learning_protocol = rule, batch_size = batch_size,
                              location_lr = location_lr, weight_lr = weight_lr, bias_lr = bias_lr,
                              W_momentum=True, B_momentum = True, L_momentum = True,
                              plot_confusion_M = False,
                              plot_activations_curve = False,test_epoch=100)
        if plot_accuracies:
            plt.plot(multiclassifier.accuracy_vec)
            plt.show()
            
