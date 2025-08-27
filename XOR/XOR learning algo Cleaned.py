'''
XOR Learning Algorithm
'''
import os
import sys
path_parent = os.path.dirname(os.getcwd())
# os.chdir(path_parent)
sys.path.insert(0,path_parent)

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
# import XORScatter
#import DataOrganizer as do
import G_clusteron_XOR as gcl
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

condition = 'L'

init_bias = 0
##radius_convert = lambda x: -(x**2)/np.log(0.5)
radius = 6.36
radius = 1
epochs = 10000#10000
batch_size = 1
num_of_tests = 1000#1000
if condition == 'B':
    wlr = 0.08 #weight learning rate
    llr = 0.12 #location learning rate 
    blr = 0.1   
#     llr = 0.14
#     blr = 0.05
#     wlr = 0.08
#     blr = 0.
#     wlr = 2*blr
#     llr = (4/radius)*blr
#     wlr = 0.0001
#     llr = 0.0001
#     blr = 0.0001
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
    print(i)
    clusteron = gcl.G_Clusteron_XOR(x_data,y_data,x_data,y_data,posVal=1,#x_data,y_data twice because same as test set
                                    radius = radius,#deleted bias = init_bias,
                                    init_locations = 'normal_f')

    clusteron.train(epochs,condition,batch_size,llr,wlr,blr,W_momentum=W_momentum,
            B_momentum = B_momentum,L_momentum=L_momentum,test_epoch=1)#stop_early=True,
                    #break_if_accuracy_goes_under_1=False)
    
    convergence = clusteron.convergence
    results.append({'init locations':list(clusteron.initial_locations),
                   'initial weights':list(clusteron.initial_weights),
                   'initial f':clusteron.f_init_dist,
                   'convergence':convergence,
                   'final f':clusteron.f_final_dist,
                   'final locations':list(clusteron.locations),
                   'final weights':list(clusteron.weights),
                    'final bias':clusteron.bias,
                    #'accuracy vec':clusteron.accuracy_vec
                    })
##    if convergence == -1:
##        print(results[i])
    
#print(results)
with open(path_parent+'\\XOR\\XORData\\' + condition + '_test_'+str(t)[:3]+'.json', 'w') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

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
              
with open(path_parent+'\\XOR\\XORData\\parameters_' + condition +str(t)[:3]+'.json', 'w') as f:
    json.dump(parameters, f, ensure_ascii=False, indent=4)
    

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
#print('wlr = ',wlr)
#print('llr = ',llr)
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
#pprint.pprint(results)

'''updating json files to include expected convergences, might need to fix for B and L'''
files = [condition + '_test_'+str(t)[:3]]
for file in files:
    file_name = os.getcwd()+'\\PaperFigures_5_31_2020\\Figure6\\XOR\\XORData\\'
    with open(file_name+file+'.json',
              'r') as read_file:#extract data from file
        results = json.load(read_file)

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
    elif condition == 'both':
        for result in results:
            result['expected to converge'] = 1

    with open(file_name + file + '.json', 'w') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
