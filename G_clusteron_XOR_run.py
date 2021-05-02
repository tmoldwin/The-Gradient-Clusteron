'''
Run XOR Learning Algorithm for the G-clusteron
'''
import numpy as np
import G_clusteron_XOR as gcl

num_of_exmpls = 4
init_data = np.array([[0,0,0],[1,0,1],[0,1,1],[1,1,0]])
mid_data = np.repeat(init_data,num_of_exmpls//4,0)
x_data = mid_data[:,:2]
y_data = mid_data[:,2]

init_bias = 0
radius = 1
epochs = 10000
batch_size = 1
num_of_tests = 1000

'''
condition should be 'L' for location update rule only, 'W' for weight update rule,
'B' for both update rules
'''
condition = 'B'

if condition == 'B':
    wlr = 0.08 #weight learning rate
    llr = 0.12 #location learning rate 
    blr = 0.1 #bias learning rate 
elif condition == 'L':
    wlr = 0
    llr = 0.05
    blr = 0.0025
elif condition == 'W':
    llr = 0
    wlr = 0.09
    blr = 0.0025

W_momentum = 0
L_momentum = 0
B_momentum = 0

results = []

for i in range(num_of_tests):
    print('Trial number = ',i)
    clusteron = gcl.G_Clusteron_XOR(x_data,y_data,x_data,y_data,posVal=1,#x_data,y_data twice because same as test set
                                    radius = radius,init_locations = 'normal_f')

    clusteron.train(epochs,condition,batch_size,llr,wlr,blr,W_momentum=W_momentum,
            B_momentum = B_momentum,L_momentum=L_momentum,test_epoch=1)
    
    convergence = clusteron.convergence
    results.append({'init locations':list(clusteron.initial_locations),
                   'initial weights':list(clusteron.initial_weights),
                   'initial f':clusteron.f_init_dist,
                   'convergence':convergence,
                   'final f':clusteron.f_final_dist,
                   'final locations':list(clusteron.locations),
                   'final weights':list(clusteron.weights),
                    'final bias':clusteron.bias,
                    })

'''updating results to include expected convergences'''
if condition == 'W':
    for result in results:
        if result['initial f']>0.5:
            result['expected to converge'] = 1
        else:
            result['expected to converge'] = 0
elif condition == 'L':
    for result in results:
        w_1,w_2 = result['initial weights'][0],result['initial weights'][1]
        if (np.sign(w_1)!=np.sign(w_2)) and (abs(w_1)<2*abs(w_2)) and (abs(w_2)<2*abs(w_1)):
            result['expected to converge'] = 1
        else:
            result['expected to converge'] = 0
elif condition == 'B':
    for result in results:
        result['expected to converge'] = 1
print(results)
