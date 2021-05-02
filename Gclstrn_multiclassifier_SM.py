'''
G-Clusteron SM
'''
import G_Clusteron_Parent as gcl

class G_Clusteron_SM(gcl.G_Clusteron_Parent):
    def __init__(self,train_set,train_Y,test_set,test_Y,posVal,
                 radius, init_distance_scale = 0.01,
                 weights = False,bias_synapse = False,
                 bias_synapse_weight = 10):
        super().__init__(train_set,train_Y,test_set,test_Y,posVal,
                         radius, init_distance_scale = init_distance_scale,
                 weights = weights,bias_synapse = bias_synapse,
                 bias_synapse_weight = bias_synapse_weight)
        self.bias_vec = [0]
        
    def update_bias(self,learning_rate,delta_bias,momentum=True):
        super().update_bias(learning_rate,delta_bias,momentum=momentum)
        self.bias_vec.append(self.bias)
