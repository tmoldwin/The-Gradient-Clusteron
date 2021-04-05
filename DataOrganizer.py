import pickle as pkl
import numpy as np
import tensorflow as tf

def get_data(algorithm = None, posVal=None, dataset_size=None, train_set_plit = '1/10',
             test_set_split = '1/10', binary=False, normalize = True):
        '''
        Use this as a general function to get the full MNIST dataset.
        
        param algorithm: clusteron,G-clusteron,Logistic Regression
        param posVal: positive class
        param dataset_size: number of positive examples in your dataset. Note:
        full dataset will include negative examples as well
        param train_set_plit: '1/10', '50/50', how the train_set should be split,
        postive/negative examples
        param test_set_plit: as above, for test_set
        param binary: should the returned y vectors be binary or have real labels
        param normalize: if to normalize input values

        return: if not specified, will return 1/10 train and test sets 

        '''
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
        data = fix_dataset_dimensions(x_train,y_train,x_test,y_test)
        x_train, y_train, x_test, y_test = data[0],data[1],data[2],data[3]
        x_train,x_test =  normalize_data(x_train), normalize_data(x_test)
        x_train_balanced,y_train_balanced = None,None

        if algorithm == 'clusteron':
                '''
                trains on all positive dataset, but gives a 50/50 test set
                '''
                pos_trainX,neg_trainX,pos_trainY,neg_trainY = split_data_by_posVal(x_train,y_train,posVal)
                
                x_train_balanced,y_train_balanced = build_mixed_dataset(pos_trainX,neg_trainX[:len(pos_trainX)],
                                                                        pos_trainY,neg_trainY[:len(pos_trainY)])
                x_train,y_train = pos_trainX,pos_trainY
                
                pos_testX,neg_testX,pos_testY,neg_testY = split_data_by_posVal(x_test,y_test,posVal)
                x_test, y_test = build_mixed_dataset(pos_testX,neg_testX[:len(pos_testX)],pos_testY,neg_testY[:len(pos_testY)])

        elif algorithm == 'G-clusteron_OVA' or algorithm == 'LR_OVA':
                '''
                trains on 50/50, tests on 50/50
                '''
                pos_trainX,neg_trainX,pos_trainY,neg_trainY = split_data_by_posVal(x_train,y_train,posVal)
                x_train,y_train = build_mixed_dataset(pos_trainX,neg_trainX[:len(pos_trainX)],
                                                                        pos_trainY,neg_trainY[:len(pos_trainY)])
                pos_testX,neg_testX,pos_testY,neg_testY = split_data_by_posVal(x_test,y_test,posVal)
                x_test, y_test = build_mixed_dataset(pos_testX,neg_testX[:len(pos_testX)],pos_testY,neg_testY[:len(pos_testY)])

        if binary:
                y_train = np.where(y_train == posVal,1,0)
                y_test = np.where(y_test == posVal,1,0)
                
        return x_train, y_train, x_test, y_test,x_train_balanced,y_train_balanced
        
def normalize_data(dataset):
        dataset = np.array(dataset)
        dataset = np.array([dataset[i] - np.mean(dataset[i]) for i in range(len(dataset))])
        dataset = np.array([dataset[i]/np.std(dataset[i]) for i in range(len(dataset))])
        #dataset = add_minimum(dataset)
        return dataset

def add_minimum(dataset):
        dataset = np.array([dataset[i] + abs(min(dataset[i])) for i in range(len(dataset))])
        return dataset

def normalize_data_min_max(dataset):
        dataset = np.array(dataset)
        dataset = np.array([(dataset[i]-min(dataset[i]))/(max(dataset[i])-min(dataset[i])) for i in range(len(dataset))])
        return dataset

def split_data_by_posVal(dataset,Y,posVal):
        '''
        returns: pos/neg input values, and a pos_y vec with just the posVal,
        and a neg_y vec with real labels of all neg classes
        '''
        pos_data_inds = np.squeeze(np.where(np.array(Y) == posVal))
        neg_data_inds = np.squeeze(np.where(np.array(Y) != posVal))
        pos_data = np.array(dataset)[pos_data_inds]
        neg_data = np.array(dataset)[neg_data_inds]
        pos_Y_vec = Y[pos_data_inds]
        neg_Y_vec = Y[neg_data_inds]
        return pos_data,neg_data,pos_Y_vec,neg_Y_vec

def build_mixed_dataset(pos_data,neg_data,pos_Y,neg_Y,all_positive=False):
        '''
        returns a balanced dataset with an appropriate balanced Y
        '''
        dataset = np.vstack((pos_data,neg_data))
        P = len(dataset)
        rand = np.random.choice(range(P),P,replace=False)
        dataset = dataset[[rand],:]
        if all_positive: y = np.vstack((np.vstack(np.ones(np.shape(pos_data)[0])),np.vstack(np.ones(np.shape(neg_data)[0]))))
        else: Y = np.hstack((pos_Y,neg_Y))
        Y = Y[rand]
        return dataset[0],Y

def two_value_dataset(dataset,Y,val_1,val_2):
        val_1_data_inds = np.squeeze(np.where(np.array(Y) == val_1))
        val_2_data_inds = np.squeeze(np.where(np.array(Y) == val_2))
        val_1_data = np.array(dataset)[val_1_data_inds]
        val_2_data = np.array(dataset)[val_2_data_inds]
        return val_1_data, val_2_data

def build_mixed_dataset_for_logistic_regression(pos_data,neg_data):# returns a balanced dataset with an appropriate balanced binary Y
        dataset = np.vstack((pos_data,neg_data))
        P = len(dataset)
        rand = np.random.choice(range(P),P,replace=False)
        dataset = dataset[[rand],:]
        y = np.vstack((np.vstack(np.ones(len(pos_data))),np.vstack(np.zeros(len(neg_data)))))
        y = y[rand]
        return dataset[0],y

def split_dataset_into_classes(dataset,Y,num_of_classes=10):
        indices_vec = [None]*num_of_classes
        dataset_vec = [None]*num_of_classes
        for i in range(num_of_classes):
                indices_vec[i] = np.squeeze(np.where(np.array(Y) == i))
        for i in range(num_of_classes):
                dataset_vec[i] = np.array(dataset)[indices_vec[i]]
        return dataset_vec

def fix_dataset_dimensions(x_train,y_train,x_test,y_test):
        '''
        Returns data in dimensions appropriate for our algorithms
        '''
        num_of_train_exmpls,r,c = np.shape(x_train)
        num_of_pxls = r*c
        x_train = np.reshape(x_train,(num_of_train_exmpls,num_of_pxls))
        num_of_test_exmpls,_,_ = np.shape(x_test)
        x_test = np.reshape(x_test,(num_of_test_exmpls,num_of_pxls))
        data = [x_train,y_train,x_test,y_test]
        return data

def get_y_indeces(Y,posVal):
        pos_data_inds = np.squeeze(np.where(np.array(Y) == posVal))
#        neg_data_inds = np.squeeze(np.where(np.array(Y) != posVal))
#        pos_data = np.array(dataset)[pos_data_inds]
#        neg_data = np.array(dataset)[neg_data_inds]
        #pos_Y_vec = Y[pos_data_inds]
#        neg_Y_vec = Y[neg_data_inds]
        return pos_data_inds

def multiple_value_dataset(dataset,Y,classes):
        num_of_values = len(classes)
        ind_list = [None]*num_of_values
        for value in range(num_of_values):
                ind_list[value] = get_y_indeces(Y,classes[value])
        final_ind_list = []
        for i in range(len(ind_list)):
                final_ind_list = np.hstack((final_ind_list,ind_list[i]))
        final_ind_list = np.int0(final_ind_list)
        np.random.shuffle(final_ind_list)       
        shuffled_dataset = dataset[final_ind_list]
        shuffled_Y = Y[final_ind_list]
        return shuffled_dataset,shuffled_Y

def balanced_dataset(dataset,y):
        unique, counts = np.unique(y, return_counts=True)
        num_of_exmpls = np.min(counts)
        unique_values = np.unique(y)
        P = len(unique_values)
        index_mat = [None]*P*num_of_exmpls
        index_mat = np.reshape(index_mat,(num_of_exmpls,P))
        for i in range(P):
                index_mat[:,i]=np.where(y==unique_values[i])[0][:num_of_exmpls]
        index_vec = np.reshape(index_mat,(num_of_exmpls*P,1))
        balanced_data = dataset[np.int0(np.squeeze(index_vec))]
        balanced_y = y[np.int0(np.squeeze(index_vec))]
        return balanced_data,balanced_y
