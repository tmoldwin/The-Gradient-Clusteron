'''
general g_clusteron functions
'''
import numpy as np
import scipy.special as sp

def calculate_S_matrix(dataset, weights):
    """
    Matrix of x_i_w_i
    P = number of examples, N = number of synapses/locations
    Takes a dataset of PxN matrix of inputs, and 1xN vector of weights, and
    multiplies it by the weights, giving x_i*w_i for all i.
    Returns the PxN S_matrix.
    """
    S_matrix = np.multiply(dataset,weights)#element wise multiplication
    return S_matrix

def calculate_D_matrix(locations):
    """
    Distance matrix [l_j - l_i]
    N = number of synapses/locations
    Takes a 1xN vector of locations, and returns a NxN matrix of location i
    minus location j
    """
    D_matrix = locations - np.transpose(np.matrix(locations))
    return D_matrix

def calculate_F_matrix(D_matrix,radius):
    """
    Matrix of F_12
    Takes in NxN distance matrix, returns symmetrical NxN F_12 matrix, for F value
    of synapse I-J go to row I, column J
    """
    F_matrix = np.exp((-np.multiply(D_matrix,D_matrix))/radius)#e^-(l(i)-l(j))^2
    return F_matrix

def calculate_Q_matrix(example,weights):
    """
    Q Matrix - matrix of x_i_w_i*x_j_w_j
    Calculates Q matrix for a pattern
    Takes in 1xN example and 1xN weights, return NxN Q matrix for that example
    """
    x_i_w_i = np.multiply(example,weights)#element wise multiplication
    Q_matrix = np.multiply(np.transpose(np.matrix(x_i_w_i)),x_i_w_i)
    return Q_matrix

def calculate_activations(dataset, weights, F_matrix):
    """
    Calculates activations for dataset
    Receives PxN S matrix and NxN F matrix
    Returns PxN matrix of activations for each synapse per example in the dataset
    """
    S_matrix = calculate_S_matrix(dataset, weights)
    F_P_matrix = np.dot(S_matrix,F_matrix)#dot product of matrices
    activations = np.multiply(S_matrix,F_P_matrix)
    return activations 

def test_accuracy(test_set,binary_test_y,weights,F_matrix,bias):
    """
    Receives
    """
    P,_ = np.shape(test_set)
    activations = calculate_activations(test_set,weights,F_matrix)
    outputs = calculate_outputs_from_activations(activations,bias)
    predictions = calculate_predictions_from_outputs(outputs,predictions='binary')
    accuracy = 1-(np.sum(np.abs(binary_test_y-predictions))/P)
    return accuracy

def calculate_Q_error_weighted_avg_matrix(dataset, weights, L_minus_y):
    """
    Receives PxN dataset (could be a batch or single example), 1xN row of weights, L_minus_Y
    vector of P errors
    Calculates Q matrix for every pattern, multiplies it by its error, then sums all the Q
    matrices, and divides by P
    Returns NxN matrix of average Q matrices multiplied by that pattern's error
    """
    P,N = np.shape(dataset)
    Q_ewam = np.zeros((N,N))
    for example in range(P):
        Q_ewam += np.multiply(calculate_Q_matrix(dataset[example],weights),np.squeeze(L_minus_y[example]))
    Q_ewam = (1/P)*Q_ewam
    return Q_ewam

def calculate_delta_locations(F_matrix,D_matrix, dataset, weights, L_minus_y):
    """
    Receives following NxN matrices: F_matrix,D_matrix,Q_error_weighted_avg_matrix
    Returns row of N delta locations
    """
    Q_error_weighted_avg_matrix = calculate_Q_error_weighted_avg_matrix(dataset, weights, L_minus_y)
    F_D_matrix = np.multiply(F_matrix,D_matrix)
    F_D_P_matrix = np.multiply(F_D_matrix,Q_error_weighted_avg_matrix)
    delta_locations = np.sum(F_D_P_matrix,1)
    delta_locations = np.squeeze(np.array(np.transpose(delta_locations)))#necessary to get dimensions right 1xN array
    return -delta_locations

def calculate_delta_weights(activations, weights, L_minus_Y):
    """
    Receives PxN matrix (row or dataset) of activations/average activations, 1xN row of
    weights, and vector of errors (L minus Y) with P values - try not to feed in a matrix
    of errors
    Returns 1xN array of delta weights
    """
    if isinstance(L_minus_Y,np.matrix):#this mess is in case of matrix, still isn't perfect
        L_minus_Y = np.squeeze(np.array(L_minus_Y))
    elif isinstance(L_minus_Y,int):
        L_minus_Y = np.array([L_minus_Y])
    if len(L_minus_Y)>1:
        L_minus_Y.shape = (len(L_minus_Y),1)
    act_divided_by_weights = np.multiply((1/weights),activations)
    delta_weights = np.squeeze(np.mean(np.array(np.multiply(act_divided_by_weights,L_minus_Y)),0))
    return -delta_weights

def calculate_delta_bias(L_minus_Y):
    """
    For the G-clusteron, the delta bias is just +=learning_rate*error value (L minus Y)
    """
    return np.mean(L_minus_Y)

def calculate_outputs_from_activations(activations_mat, bias):
    """
    Receives PxN matrix of activations
    Returns Px1 column of outputs per example (before logistic function)
    """
    return np.squeeze(np.asarray(np.sum(activations_mat,1)))-bias

def calculate_predictions_from_outputs(outputs,function='logistic',predictions='binary'):
    """
    """
    if function == 'logistic':
        logistic_function = sp.expit(outputs)#didn't subtract bias b/c already done in output calculation
        if predictions=='binary':
            prediction_vec = np.where(logistic_function>=0.5,1,0)
        elif predictions=='probability':
            prediction_vec = logistic_function
    return prediction_vec

def calculate_momentum_update(raw_delta_vec, m,v,beta1 = 0.9,beta2 = 0.999, eps = 1e-8):
    """
    Momentum calculation - Receives 1xN row of deltas, and instance variables m and v
    Returns same, make sure to multiply by learning rate outside
    """
    m = beta1*m + (1-beta1)*raw_delta_vec
    v = beta2*v + (1-beta2)*(raw_delta_vec**2)
    momentum_delta_vec = np.squeeze(m/(np.sqrt(v)+eps))#deleted a lr, and a minus for locations, + for bias, - for weights
    return momentum_delta_vec, m, v

def sanity_check_delta_locations(dataset, weights,locations,radius,error):#add for activations seperate function
    """
    Like it sounds. Confirms delta locations in matrix form working same as straightforward
    calculation
    """
    P,N = np.shape(dataset)
    delta_locations = np.zeros(N)
    for pattern in range(P):
        if type(dataset)==np.matrix:
            dataset[pattern] = np.array(dataset[pattern])[0]
        for i in range(N):
            summ = 0
            for j in range(N):
                dist = locations[j]-locations[i]
                F = np.exp(-(dist**2)/radius)
                summ +=dist*F*dataset[pattern][j]*weights[j]
            delta_locations[i] += dataset[pattern][i]*weights[i]*summ*error[pattern]
    delta_locations = (-1/P)*delta_locations
    return delta_locations

def sanity_check_activations(dataset, weights, locations,radius):
    """
    Like it sounds. Confirms activations in matrix form working same as straightforward
    calculation
    """
    P,N = np.shape(dataset)
    activations = np.zeros((P,N))
    for pattern in range(P):
        for syn_i in range(N):
            summ = 0
            for syn_j in range(N):
                dist = locations[syn_j]-locations[syn_i]
                F = np.exp(-(dist**2)/radius)
                summ += F*dataset[pattern][syn_j]*weights[syn_j]
            activations[pattern,syn_i] = summ*dataset[pattern][syn_i]*weights[syn_i]
    return

def add_bias_synapse(dataset):
    '''
    add a bias synapse (x_0 = 1) to a dataset, receives a PxN matrix, returns a
    px(1+N) matrix
    '''
    r,c = np.shape(dataset)
    dataset = np.hstack((np.ones((r,1)),dataset))
    return dataset

