'''
file I used for logistic regression in the paper
Options available for one-vs-all and all-vs-all (OVR and SM)
'''
from sklearn.linear_model import LogisticRegression
import DataOrganizer as do

protocol = 'multi'#'ova','multi' (one vs all or multiclass)
method = 'SM'#'OVR','SM' (one vs rest or softmax)

if protocol == 'ova':
    algorithm = 'LR_OVA'
    for posVal in range(10):
        print('Positive class = ',posVal)
        '''
        in order to use a binary classifier, I built a 50/50 pos/neg dataset, and turned the Y vec into a binary vec
        '''
        train_x, train_y, test_x, test_y,_,_ = do.get_data(algorithm,posVal,
                                                           binary=True)
        logisticRegr = LogisticRegression(solver = 'lbfgs',
                                          multi_class = 'ovr', max_iter=100)
        logisticRegr.fit(train_x, train_y)

        score = logisticRegr.score(test_x, test_y)
        print('Accuracy = ',score)

elif protocol == 'multi':
    if method == 'OVR':
        logisticRegr = LogisticRegression(solver = 'lbfgs',
                                          multi_class = 'ovr',
                                      max_iter=100,)
        algorithm = 'LR_multi_OVR'
    elif method == 'SM':
        solver = 'lbfgs'
        logisticRegr = LogisticRegression(solver = solver,
                                          multi_class = 'multinomial',
                                              max_iter=100, penalty = 'none')
        algorithm = 'LR_multi_SM'
    print(algorithm)
    x_train, y_train, x_test, y_test,_,_ = do.get_data(algorithm)
    logisticRegr.fit(x_train, y_train)
    score = logisticRegr.score(x_test, y_test)
    print('Multiclassifier accuracy = ',score)
      
