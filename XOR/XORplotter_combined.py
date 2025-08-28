'''
XOR plotter for data in json files - Combined version
Shows both initial and final weights in a single figure with two rows
'''
import os
import sys
path_parent = os.path.dirname(os.getcwd())
# os.chdir(path_parent)
sys.path.insert(0,path_parent)
#print(path_parent)
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from matplotlib import cm
import pprint 
import json
from pylab import rcParams


fig_folder = path_parent 
fignum = 6

def create_combined_scatter_plots(json_files,epochs=10000,fig_size = (7.5,6.)):
    rcParams['figure.figsize'] = fig_size
    fig = plt.figure('Combined XOR Visualization')

    for i in range(len(json_files)):
        file_name = 'XORData/'+json_files[i]+'.json'
        with open(file_name, "r") as read_file:#extract data from file
            results = json.load(read_file)

        num_of_tests = len(results)

        #getting mean of convergence
        conv_count = 0
        neg_conv_count = 0#number of times no convergence
        for result in results:
            if result['convergence'] == -1:
                neg_conv_count += 1
            else:
                conv_count += result['convergence']

        initfs = [result['initial f'] for result in results]
        convergences = [epochs if result['convergence'] == -1 else result['convergence'] for result in results]
        w1_init = np.array([result['initial weights'][0] for result in results])
        w1_final = np.array([result['final weights'][0] for result in results])
        w2_init = np.array([result['initial weights'][1] for result in results])
        w2_final = np.array([result['final weights'][1] for result in results])
        f_init = np.array([result['initial f'] for result in results])
        f_final = np.array([result['final f'] for result in results])

        if file_name[file_name.find('/')+1:file_name.find('.')] == files[0]:
            title = 'Weight and Location Rule'
        elif file_name[file_name.find('/')+1:file_name.find('.')] == files[2]:
            title = 'Weight Rule'
        elif file_name[file_name.find('/')+1:file_name.find('.')] == files[1]:
            title = 'Location Rule'
        else:
            title = 'title'
           
        eps = 1
        
        colors = np.array([epochs if (result['convergence'] == -1) else result['convergence'] for result in results]) + eps
        list_of_convergences = [0 if result['convergence'] == -1 else 1 for result in results]
        list_of_expectations = [result['expected to converge'] for result in results]
        conv_indices = np.where(list_of_convergences)
        non_conv_indices_unexp = np.where([1 if list_of_convergences[ind] == 0 and list_of_expectations[ind] == 1 else 0 for ind in range(len(list_of_convergences))])[0]
        non_conv_but_expctd_indices = np.where([1 if list_of_convergences[ind] == 0 and list_of_expectations[ind] == 0 else 0 for ind in range(len(list_of_convergences))])[0]

        norm = matplotlib.colors.LogNorm(vmin=colors.min(),vmax=colors.max())
        cmap = plt.get_cmap("viridis_r")

        'these three lines were for color scheme of green,pink, black'
        conv_colors = 'g'
        non_conv_colors = 'fuchsia'
        non_conv_but_expctd_colors = 'k'

        # INITIAL WEIGHTS - TOP ROW
        ax_init = fig.add_subplot(2, 3, i+1, projection='3d')

        if len(conv_indices) > 0:
            ax_init.scatter(w1_init[conv_indices], w2_init[conv_indices],
                       f_init[conv_indices], c = conv_colors, marker = 'o',
                       s = 10, alpha = 1, cmap = cmap)
        if len(non_conv_indices_unexp) > 0:
            ax_init.scatter(w1_init[non_conv_indices_unexp], w2_init[non_conv_indices_unexp],
                       f_init[non_conv_indices_unexp], edgecolor = non_conv_but_expctd_colors,
                       facecolor=(0,0,0,0), marker ='v',s = 40, cmap = cmap)
        if len(non_conv_but_expctd_indices) > 0:   
            ax_init.scatter(w1_init[non_conv_but_expctd_indices], w2_init[non_conv_but_expctd_indices],
                       f_init[non_conv_but_expctd_indices],edgecolor = non_conv_colors,
                       facecolor=(0,0,0,0), marker ='o',s = 10, cmap = cmap)
        
        ax_init.set_zlim(0,1)
        eps = 10**-5
        ax_init.set_title('Initial Weights')
        ax_init.set_xticks(np.arange(-1,1+eps,1))
        ax_init.set_yticks(np.arange(-1,1+eps,1))
        ax_init.set_zticks(np.arange(0,1+eps,0.25))
        ax_init.set_xlabel(r'$\ w_1$',size=10)
        ax_init.set_ylabel(r'$\ w_2$',size=10)
        azimuths = [-141,-134,-143]
        elevations = [14,24,11]
        ax_init.view_init(elev=elevations[i], azim=azimuths[i])

        # FINAL WEIGHTS - BOTTOM ROW
        ax_final = fig.add_subplot(2, 3, i+4, projection='3d')
        
        if len(conv_indices) > 0:
            ax_final.scatter(w1_final[conv_indices], w2_final[conv_indices],
                       f_final[conv_indices], c = conv_colors, marker = 'o',
                       s = 10, alpha = 1, cmap = cmap)
        if len(non_conv_indices_unexp) > 0:
            ax_final.scatter(w1_final[non_conv_indices_unexp], w2_final[non_conv_indices_unexp],
                       f_final[non_conv_indices_unexp], edgecolor = non_conv_but_expctd_colors,
                       facecolor=(0,0,0,0), marker ='v',s = 40, cmap = cmap)
        if len(non_conv_but_expctd_indices) > 0:   
            ax_final.scatter(w1_final[non_conv_but_expctd_indices], w2_final[non_conv_but_expctd_indices],
                       f_final[non_conv_but_expctd_indices],edgecolor = non_conv_colors,
                       facecolor=(0,0,0,0), marker ='o',s = 10, cmap = cmap)
        

        ax_final.set_zlim(0,1)
        ax_final.set_xlim(np.min([np.floor(np.min(w1_final)),-1]),np.max([np.ceil(np.max(w1_final)),1]))
        ax_final.set_ylim(0,1)
        eps = 10**-5
        ax_final.set_title('Final Weights')
        ax_final.set_xticks([np.min([np.floor(np.min(w1_final)),-1]),0,np.max([np.ceil(np.max(w1_final)),1])])
        ax_final.set_yticks([np.min([np.floor(np.min(w2_final)),-1]),0,np.max([np.ceil(np.max(w2_final)),1])])
        ax_final.set_zticks(np.arange(0,1+eps,0.25))
        ax_final.set_xlabel(r'$\ w_1$',size=10)
        ax_final.set_ylabel(r'$\ w_2$',size=10)
        azimuths = [-147,-143,-143]
        elevations = [17,19,11]
        ax_final.view_init(elev=elevations[i], azim=azimuths[i])
    
    fig.text(0.03, 0.5, r'$\ F_{12}$', va='center', rotation='vertical')
    plt.subplots_adjust(left = 0.08,right = 1,wspace = 0.1, hspace = 0.3)

    plt.show()
    return 


files = ['W_test_161','just_location1','both']
#files = ['just_locationonly_expected_convs','just_locationonly_expected_convs','just_locationonly_expected_convs']
#files = ['both','just_location_2','just_weights']

create_combined_scatter_plots(files, fig_size = (7.5,6.))


def create_bar_charts(files):
    
    percent_converged = []
    mean_epochs_till_conv = []
    expected_convergences_bar_chart = []
    
    
    for file in files:
        with open('XORData/'+file+'.json', 'r') as read_file:#extract data from file
            results = json.load(read_file)

        num_of_tests = len(results)
        convs = [1 for result in results if result['convergence'] != -1]
        epochs_till_conv = [result['convergence'] for result in results if result['convergence'] != -1]
        
        mean_epochs = sum(epochs_till_conv)/sum(convs)
        percent = (sum(convs)/num_of_tests)*100

        mean_epochs_till_conv.append(mean_epochs)
        percent_converged.append(percent)

        expected_conv_trials = []
        if file == files[0]:
            expected_conv_trials = [1 if result['initial f']>0.5 else 0 for result in results]
        
        elif file == files[1]:
            for result in results:
                w_1,w_2 = result['initial weights'][0],result['initial weights'][1]
                if (np.sign(w_1)!=np.sign(w_2)) and (abs(w_1)<2*abs(w_2)) and (abs(w_2)<2*abs(w_1)):
                    expected_conv_trials.append(1)
                else:
                    expected_conv_trials.append(0)
        elif file == files[2]:
            expected_conv_trials = [1 for result in results]
        expected_conv_percent = (sum(expected_conv_trials)/num_of_tests)*100
        expected_convergences_bar_chart.append((np.sum(expected_conv_percent)))
        print('ecp',np.sum(expected_conv_trials))
        print('ac',np.sum(convs))
        
    titles = ['Weight \nRule','Location \nRule','Weight and \nLocation Rule']
    rcParams['figure.figsize'] = 4.25,3.5


####    plt.figure('Mean Epochs Until Convergence')
####    plt.bar(titles,mean_epochs_till_conv)

    x = np.arange(len(titles))
    width = 0.35#width of bar
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, percent_converged, width, label='Converged')
    rects2 = ax.bar(x + width/2, expected_convergences_bar_chart, width,
                    label='Possible Convergences')
    ax.set_xticks(x)
    ax.set_ylabel('Trials Converged %',fontsize = 'large')
    ax.set_xticklabels(titles,fontsize = 'medium')
    ax.legend(fontsize = 'medium')
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(fig_folder + '/bar_chart_1.png')#, bbox_inches = 'tight')
    plt.show()


files = ['W_test_161','L_test_161','both']
results = create_bar_charts(files)

##something else

##expected_conv_init_weights = []
##for result in results:
##    w_1,w_2 = result['initial weights'][0],result['initial weights'][1]
##    if (np.sign(w_1)!=np.sign(w_2)) and (abs(w_1)<2*abs(w_2)) and (abs(w_2)<2*abs(w_1)) and result['convergence']==-1:
##        expected_conv_init_weights.append(result['initial weights'])

##print(np.max(np.min(np.absolute(expected_conv_init_weights),1)))

        
    
