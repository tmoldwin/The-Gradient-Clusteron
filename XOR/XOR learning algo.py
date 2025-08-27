# #XOR Learning Algorithm
import os
import sys
path_parent = os.path.dirname(os.getcwd())
# os.chdir(path_parent)
sys.path.insert(0,path_parent)

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
# import XORScatter
import DataOrganizer as do
import XOR_clusteron as gc
from matplotlib import pyplot as plt
import pprint
import pickle as pkl
import json
import winsound
import time

t = time.time()
print(t)
#dataset
num_of_exmpls = 4
init_data = np.array([[0,0,0],[1,0,1],[0,1,1],[1,1,0]])
mid_data = np.repeat(init_data,num_of_exmpls//4,0)
#np.random.shuffle(mid_data)
x_data = mid_data[:,:2]
y_data = mid_data[:,2]

epochs = 10000
batch_size = 1
condition = 'just_location'  
radius = 2.1
wlr = 0.08 #weight learning rate
llr = 0.12 #location learning rate 
blr = 0.1

if condition == 'just_location':
    wlr = 0
    llr = 0.05
    blr = 0.0025

elif condition == 'just_weights':
    llr = 0
    wlr = 0.09
    blr = 0.0025

init_bias = 0

num_of_tests = 1000
results = []
for i in range(num_of_tests):
    print(i)
    learn = gc.Clustering_algo(x_data,y_data,posVal=1,bias = init_bias,
                               radius = radius,XOR=True,init_locations = 'normal_f',
                               )

    learn.learn(epochs,location_learning_rate = llr,weight_learning_rate = wlr,
            bias_learning_rate=blr,batch_size=batch_size,momentum_weights=0,
            momentum_locations = 0,location_update_sign = 1,plot=0,
                stop_early=True,break_if_accuracy_goes_under_1=False)
    
    convergence = learn.convergence
    results.append({'init locations':list(learn.initial_locations),
                   'initial weights':list(learn.initial_weights),
                   'initial f':learn.f_init_dist,
                   'convergence':convergence,
                   'final f':learn.f_final_dist,
                   'final locations':list(learn.locations),
                   'final weights':list(learn.weights),
                    'final bias':learn.bias,
                    #'accuracy vec':learn.train_accuracy_vec
                    })
##    if convergence == -1:
##        print(results[i])
    
#print(results)
#with open('XORData\\' + condition + '_2.json', 'w') as f:
    #json.dump(results, f, ensure_ascii=False, indent=4)

elapsed = time.time() - t
print('elapsed', elapsed)

'Beep when learning finishes'
frequency = 800
duration = 750
winsound.Beep(frequency, duration)

parameters = {'epochs':epochs,
              'batch_size':batch_size,
              'condition':condition,
              'radius':radius,
              'wlr':wlr,
              'llr':llr,
              'blr':blr,
              'num_of_tests':num_of_tests,
              'time elepsed':elapsed,
              'initial bias':init_bias,
              }
              
#with open('XORData\\parameters_' + condition + '_2.json', 'w') as f:
    #json.dump(parameters, f, ensure_ascii=False, indent=4)
    

#getting mean of convergence
conv_count = 0
neg_conv_count = 0#number of times no convergence
for result in results:
    #print(result)
    if result['convergence'] == -1:
        neg_conv_count += 1
    else:
        conv_count += result['convergence']
#assert (num_of_tests-neg_conv_count)>0, 'No convergences'
print('wlr = ',wlr)
print('llr = ',llr)
print('Mean epochs till convergence = ',conv_count/(num_of_tests-neg_conv_count))
print('number of convergences = '+str(num_of_tests-neg_conv_count)+' out of '+str(num_of_tests))

initfs = [result['initial f'] for result in results]
convergences = [epochs if result['convergence'] == -1 else result['convergence'] for result in results]
w1final = [result['final weights'][0] for result in results]
w2final = [result['final weights'][1] for result in results]
f_final = [result['final f'] for result in results]

##plt.figure()
##plt.scatter(initfs, convergences, s = 2)
##plt.ylabel('Epochs until convergence')
##plt.xlabel('f_init')
##plt.yscale('log')
##plt.title('number of convergences = '+str(num_of_tests-neg_conv_count)+' out of '+str(num_of_tests))
##plt.show()
##
##fig = plt.figure(1)
##ax = fig.gca(projection='3d')
##ax.scatter(w1final, w2final, f_final,marker = 'o',s = 1 ,alpha = 1, zorder = 1)
##ax.set_zlim(-0.1,1)
##eps = 10**-5
##ax.set_xticks(np.arange(-1,1+eps,0.5))
##ax.set_yticks(np.arange(-1,1+eps,0.5))
##ax.set_zticks(np.arange(0,1+eps,0.25))
##fig.show()
##plt.show()
##
###pprint.pprint(results)
