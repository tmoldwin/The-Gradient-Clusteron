"""
G-clusteron (OVR) multiclassifier
"""
from Multi_classifier_OVR import MultiClassifier as gclstrn_multi
import numpy as np
from matplotlib import pyplot as plt
import DataOrganizer as do

algorithm = 'G-clusteron_AVA'
x_train, y_train, x_test, y_test,_,_ = do.get_data(algorithm)

classes = np.arange(10)
num_of_epochs = 20
'for single classifier'
plot_accuracy = False
batch_size = 100
radius = 0.23083120654223419#(radius_convert(0.4)
'bias synapse'
bs = False
bsw = 2

for learning_protocol in ['L','W','B']:#locations, weights, both
    print('Learning protocol = ',learning_protocol)
    if learning_protocol == 'L':
        location_lr = 0.00004
        wlr = 0
        blr = 0.04
        w_m = False
        b_m = True
        l_m = True
    elif learning_protocol == 'W':
        location_lr = 0
        wlr = 0.0001
        blr = 0.04
        w_m = True
        b_m = True
        l_m = False
    elif learning_protocol == 'B':
        location_lr = 0.00004
        wlr = 0.0001
        blr = 0.04
        w_m = True
        b_m = True
        l_m = True
        
    gc_multiclassifier = gclstrn_multi(x_train, y_train, x_test, y_test,
                                       classes,radius,bs,bsw)
    gc_multiclassifier.train(num_of_epochs,batch_size,location_lr,wlr,blr,
                             learning_protocol,w_m,b_m,l_m,plot_accuracy)

