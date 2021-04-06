'''
single classifier G clusteron
'''
import numpy as np
import DataOrganizer as do
from G_Clusteron_OVR import G_Clusteron_OVR
from matplotlib import pyplot as plt

radius = 0.23083120654223419
num_of_epochs = 10
learning_protocol = 'L'
algorithm = 'G-clusteron_OVA'
batch_size = 50
init_distance_scale = 0.01
location_lr = 0.00005
wlr = 0
blr = 0.04
epoch_to_test = 5#how often should learning algorithm test accuracy during training
plot_activations = False
plot_accuracy = False
'to add a bias synapse (x_0 = 1)'
bs = False
bsw = 2
posVal = 0

x_train, y_train, x_test, y_test,_,_ = do.get_data(algorithm,posVal)

clusteron = G_Clusteron_OVR(x_train,y_train,
                            x_test,y_test,posVal,
                            radius=radius,init_distance_scale=init_distance_scale,
                            weights=False,bias_synapse = bs,bias_synapse_weight=bsw)

clusteron.train(num_of_epochs,learning_protocol,batch_size,location_lr,wlr,blr,
                W_momentum=False,B_momentum=True,L_momentum=True,
                test_epoch=epoch_to_test,plot_accuracy=plot_accuracy)
