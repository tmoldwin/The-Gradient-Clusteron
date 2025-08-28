'''
XOR plotter for data in json files
Use script on bottom of page to add 'convergence expectation' to JSON file
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

def create_scatter_plots(json_files,epochs=10000,plot_what = 'f_vs_conv',
                         fig_size = (7,3.3),plot_2_d = False):#f vs convergences, f vs weights in 3D
    rcParams['figure.figsize'] = fig_size
    fig = plt.figure(plot_what)

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

        #print('Mean epochs till convergence = ',conv_count/(num_of_tests-neg_conv_count))
        #print('number of convergences = '+str(num_of_tests-neg_conv_count)+' out of '+str(num_of_tests))

        #colors = ['b' if result['convergence'] == -1 else 'k' for result in results]


        if file_name[file_name.find('\\')+1:file_name.find('.')] == files[0]:
            title = 'Weight and Location Rule'
        elif file_name[file_name.find('\\')+1:file_name.find('.')] == files[2]:
            title = 'Weight Rule'
        elif file_name[file_name.find('\\')+1:file_name.find('.')] == files[1]:
            title = 'Location Rule'
        else:
            title = 'title'

#         if plot_what == 'f_vs_conv':
#             #if json_files[i] == 'both':
#             plt.subplot(1,3,i+1)
#             plt.scatter(initfs, convergences, c =colors, s = 2)
#             plt.xlabel(r'$\ f(l_1^{initial}-l_2^{initial})$',size = 12)
#             plt.yscale('log')
#             plt.ylim([1,10**4+5000])
#             plt.title(title,size=9)
#             ax = plt.gca()
#             ax.spines["top"].set_visible(False)
#             ax.spines["right"].set_visible(False)
           
        eps = 1
        
        colors = np.array([epochs if (result['convergence'] == -1) else result['convergence'] for result in results]) + eps
        list_of_convergences = [0 if result['convergence'] == -1 else 1 for result in results]
        list_of_expectations = [result['expected to converge'] for result in results]
        #print(list_of_convergences)
        conv_indices = np.where(list_of_convergences)
        #print('loc', conv_indices)
        non_conv_indices_unexp = np.where([1 if list_of_convergences[ind] == 0 and list_of_expectations[ind] == 1 else 0 for ind in range(len(list_of_convergences))])[0]
        #print(non_conv_indices_unexp)
        non_conv_but_expctd_indices = np.where([1 if list_of_convergences[ind] == 0 and list_of_expectations[ind] == 0 else 0 for ind in range(len(list_of_convergences))])[0]
        #print(non_conv_but_expctd_indices)

        norm = matplotlib.colors.LogNorm(vmin=colors.min(),vmax=colors.max())
        cmap = plt.get_cmap("viridis_r")

        'first three lines were colors based on epochs to coverged'
##        conv_colors = norm(colors[conv_indices])
##        non_conv_colors = cmap(norm(colors[non_conv_indices_unexp])[0])
##        non_conv_but_expctd_colors = cmap(norm(colors[non_conv_but_expctd_indices]))
        'these three lines were for color scheme of green,pink, black'
        conv_colors = 'g'
        non_conv_colors = 'fuchsia'
        non_conv_but_expctd_colors = 'k'


        
        #colors = np.log([epochs if result['convergence'] == -1 else result['convergence'] for result in results])

        if plot_what == 'f_init_vs_w1_w2':
            ylabel = r'$\ F_{12}$'
            ax = fig.add_subplot(1, 3, i+1, projection='3d')

            if len(conv_indices) > 0:
                ax.scatter(w1_init[conv_indices], w2_init[conv_indices],
                           f_init[conv_indices], c = conv_colors, marker = 'o',
                           s = 10, alpha = 1, cmap = cmap)
            if len(non_conv_indices_unexp) > 0:
                ax.scatter(w1_init[non_conv_indices_unexp], w2_init[non_conv_indices_unexp],
                           f_init[non_conv_indices_unexp], edgecolor = non_conv_but_expctd_colors,
                           facecolor=(0,0,0,0), marker ='v',s = 40, cmap = cmap)
            if len(non_conv_but_expctd_indices) > 0:   
                ax.scatter(w1_init[non_conv_but_expctd_indices], w2_init[non_conv_but_expctd_indices],
                           f_init[non_conv_but_expctd_indices],edgecolor = non_conv_colors,
                           facecolor=(0,0,0,0), marker ='o',s = 10, cmap = cmap)
            
            ax.set_zlim(0,1)
            eps = 10**-5
            ax.set_title('')
            ax.set_xticks(np.arange(-1,1+eps,1))
            ax.set_yticks(np.arange(-1,1+eps,1))
            ax.set_zticks(np.arange(0,1+eps,0.25))
            ax.set_xlabel(r'$\ w_1$',size=10)
            ax.set_ylabel(r'$\ w_2$',size=10)
            #ax.set_zlabel(r'$\ f_{init}$',size=15)
            #plt.title(title)
            #x.spines['left'].set_bounds(-1, 1) 
            azimuths = [-141,-134,-143]
            elevations = [14,24,11]
            ax.view_init(elev=elevations[i], azim=azimuths[i])
            
        if plot_what == 'f_final_vs_w1_w2':
            ylabel = r'$\ F_{12}$'
            ax = fig.add_subplot(1, 3, i+1, projection='3d')
            #print(w1_final[conv_indices])
            #print(conv_indices)
            
            if len(conv_indices) > 0:
                ax.scatter(w1_final[conv_indices], w2_final[conv_indices],
                           f_final[conv_indices], c = conv_colors, marker = 'o',
                           s = 10, alpha = 1, cmap = cmap)
            if len(non_conv_indices_unexp) > 0:
                ax.scatter(w1_final[non_conv_indices_unexp], w2_final[non_conv_indices_unexp],
                           f_final[non_conv_indices_unexp], edgecolor = non_conv_but_expctd_colors,
                           facecolor=(0,0,0,0), marker ='v',s = 40, cmap = cmap)
            if len(non_conv_but_expctd_indices) > 0:   
                ax.scatter(w1_final[non_conv_but_expctd_indices], w2_final[non_conv_but_expctd_indices],
                           f_final[non_conv_but_expctd_indices],edgecolor = non_conv_colors,
                           facecolor=(0,0,0,0), marker ='o',s = 10, cmap = cmap)
            

            ax.set_zlim(0,1)
            ax.set_xlim(np.min([np.floor(np.min(w1_final)),-1]),np.max([np.ceil(np.max(w1_final)),1]))
            ax.set_ylim(0,1)
            eps = 10**-5
            ax.set_title('')
            ax.set_xticks([np.min([np.floor(np.min(w1_final)),-1]),0,np.max([np.ceil(np.max(w1_final)),1])])
            ax.set_yticks([np.min([np.floor(np.min(w2_final)),-1]),0,np.max([np.ceil(np.max(w2_final)),1])])
            ax.set_zticks(np.arange(0,1+eps,0.25))
            ax.set_xlabel(r'$\ w_1$',size=10)
            ax.set_ylabel(r'$\ w_2$',size=10)
            #plt.title(title)
            azimuths = [-147,-143,-143]
            elevations = [17,19,11]
            ax.view_init(elev=elevations[i], azim=azimuths[i])
    
    fig.text(0.03, 0.5,ylabel , va='center', rotation='vertical')
    plt.subplots_adjust(left = 0.08,right = 1,wspace = 0.1)

    #plt.tight_layout()
##    if plot_what == 'f_vs_conv':        
##        fig.text(0.015,0.5, 'Epochs Until Convergence',
##                 ha="center", va="center", rotation=90)
    #plt.savefig(fig_folder + '/' + plot_what + '1.png')#, bbox_inches = 'tight')
##    _,ax = plt.subplots()
##    cax, _ = matplotlib.colorbar.make_axes(ax)
##    cbar = matplotlib.colorbar.ColorbarBase((cax), cmap = cmap, norm=norm)
##    plt.savefig(fig_folder + '/Figure' + str(fignum) + '/' + plot_what + 'colorbar.png')#, bbox_inches = 'tight')
##    cbar.set_label('Epochs Until Convergence',rotation = 90,labelpad = -45)
##    plt.savefig(fig_folder + '/Figure' + str(fignum) + '/' + plot_what + 'colorbar.png')#, bbox_inches = 'tight')
    plt.show()
    if plot_2_d:
        n = 0.01

        x_neg = np.arange(-10,-n,n) 
        x_pos = np.arange(n,10,n)
        x_range = np.concatenate((x_neg,x_pos))

        x_sqr = np.float16(np.square(x_range))
        x = x_range
        rcParams['figure.figsize'] = 5, 5
        fig, ax = plt.subplots(1,1)

        f_12 = 1
        y = (x_sqr/x)*(-2)*f_12
        y1 = (x_sqr/x)*(1/((-2)*f_12))
        y_neg = y[:len(y)//2]
        y1_neg = y1[:len(y1)//2]
        
        
        line = (y,x_range)
        ax.plot(x_range,y)
        ax.plot(x_range,y1)
        ax.scatter(w1_init[conv_indices], w2_init[conv_indices],
                    c = norm(conv_colors), marker = 'o',
                   s = 10, alpha = 1, cmap = cmap)
        ax.scatter(w1_init[non_conv_indices_unexp], w2_init[non_conv_indices_unexp],
                   edgecolor = cmap(norm(non_conv_colors)[0]),
                   facecolor=(0,0,0,0), marker ='v',s = 40, cmap = cmap)

        #ax.grid()
        lim = 1.2
        ax.set_xlim(-lim,lim)
        ax.set_ylim(-lim,lim)
        ax.set_xlabel(r'$\ w_1$')
        ax.set_ylabel(r'$\ w_2$')

        ax.fill_between(x_neg,y_neg,color = 'b',alpha=0.1,label='_nolegend_')
        ax.fill_between(x_neg,y1_neg,10,color = 'orange',alpha=0.1,label='_nolegend_')
        ax.fill_between(-x_neg,-y_neg,color = 'b',alpha=0.1,label='_nolegend_')
        ax.fill_between(-x_neg,-y1_neg,-10,color = 'orange',alpha=0.1,label='_nolegend_')
        ax.set_title(r'$\ f(l_1-l_2) = %g$' %f_12)

        plt.tight_layout()
        plt.show()
    return 


files = ['W_test_161','just_location1','both']
#files = ['just_locationonly_expected_convs','just_locationonly_expected_convs','just_locationonly_expected_convs']
#files = ['both','just_location_2','just_weights']

create_scatter_plots(files, plot_what = 'f_init_vs_w1_w2',fig_size = (7.5,3.),plot_2_d=False)
create_scatter_plots(files, plot_what = 'f_final_vs_w1_w2',fig_size = (7.5,3))
#create_scatter_plots(files, plot_what = 'f_vs_conv',fig_size = (6,2.5))


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

        
    
