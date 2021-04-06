'''G-Clusteron one vs rest'''

import G_Clusteron_Parent as gcl
import copy

class G_Clusteron_OVR(gcl.G_Clusteron_Parent):
    def __init__(self,train_set,train_Y,test_set,test_Y,posVal,
                 radius, init_distance_scale = 0.01,weights = False,
                 bias_synapse=False,bias_synapse_weight=False):
        super().__init__(train_set,train_Y,test_set,test_Y,posVal,
                 radius, init_distance_scale = init_distance_scale,
                 weights = weights,bias_synapse=bias_synapse,
                         bias_synapse_weight=bias_synapse_weight)

        self.init_locations = copy.deepcopy(self.locations)
